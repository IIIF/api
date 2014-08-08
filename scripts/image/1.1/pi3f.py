
import cgitb
from wsgiref import headers
import urllib, urlparse

import StringIO
import os, sys
import glob
import re
import math

try:
    from PIL import Image
except:
    import Image
try:
    import json
except:
    import simplejson as json


HOMEDIR = "/home/iiif/Web"
# BASEDIR is unused if CACHEDIR is set
BASEDIR = HOMEDIR + "/Dropbox/Rob/Web/iiif-dev/"

FILEDIRS = [
 HOMEDIR+"/image_data/"
]
IMAGEFMTS = ['png', 'jpg', 'tif']

CACHEDIR = HOMEDIR+"/image_cache/1.1/"

BASEURL = "http://iiif.io/"
PREFIX = "api/image/1.1/example/reference"

TILE_SIZE = 512

def parse_qs(data):
    # 2.4 doesn't have list comprehensions :(
    d = {}
    try:
        bits = data.split('&')
        for b in bits:
            (n,v) = b.split('=')
            d[n]=urllib.unquote_plus(v)
    except:
        pass
    return d

class WsgiApp:

    def __init__(self):
        self.codes = {
            200 : 'OK',
            201 : 'Created',
            202 : 'Accepted',
            300 : 'Multiple Choies',
            301 : 'Moved Permanently',
            302 : 'Found',
            303 : 'See Other',
            304 : 'Not Modified',
            400 : 'Bad Request',
            401 : 'Unauthorized',
            403 : 'Forbidden',
            404 : 'Not Found',
            405 : 'Method Not Allowed',
            406 : 'Not Acceptable',
            415 : 'Invalid Media',
            500 : 'Internal Server Error',
            501 : 'Not Implemented',
            503 : 'Service Unavailable'
        }

    def __call__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

        try:
            self.full_uri = environ['SCRIPT_URI']
            self.path = environ['SCRIPT_URL'][len(environ['SCRIPT_NAME']):]
            self.host = environ['wsgi.url_scheme'] + "://" + environ['SERVER_NAME']
        except:
            self.full_uri = environ['REQUEST_URI']
            self.path = environ['PATH_INFO']
            self.host = environ['HTTP_HOST']

        if environ['QUERY_STRING']:
            #self.query = urlparse.parse_qs(environ['QUERY_STRING'])
            self.query = parse_qs(environ['QUERY_STRING'])
        else:
            self.query = {}

        try:
            self.body = environ['wsgi.input'].read()
        except:
            self.body = ''

        h = {}
        for (k,v) in environ.items():
            if k.startswith('HTTP_'):
                name = k[5:].lower().replace('_', '-')
                h[name] = v
        self.in_headers = h

        self.status = 200
        self.out_headers = headers.Headers([])

        try:
            data = self.handle()
        except:
            sio = StringIO.StringIO()
            cgitb.Hook(file=sio).handle()
            sio.seek(0)
            data = sio.read()
            self.out_headers['Content-type'] = 'text/html'
            self.status = 500
            
        self.out_headers['Content-length'] = str(len(data))    
        status = "%s %s" % (self.status, self.codes[self.status])
        start_response(status, self.out_headers.items())

        if type(data) == str:
            return [data]
        elif type(data) == unicode:
            return [data.encode('utf-8')]
        else:
            # see if response is iterable
            try:
                iter(data)
                return data
            except TypeError:
                return [data]

    def send(self, data, status=200, ct = 'text/html'):
        self.status = status
        self.out_headers['Content-type'] = ct
        return data


class ServiceHandler(WsgiApp):

    def __init__(self):
        WsgiApp.__init__(self)
        self.identifiers = {}

        fns = []
        for fd in FILEDIRS:
            for fmt in IMAGEFMTS:
                fns.extend(glob.glob(fd + "*" + fmt)) 

        for fn in fns:
            (d, f) = os.path.split(fn)
            f = f.replace('image-', '')
            f = f[:-4]
            self.identifiers[f] = fn
        
        self.formats = {'BMP' : 'image/bmp',  
                   'GIF' : 'image/gif', 
                   'JPEG': 'image/jpeg', 
                   'PCX' : 'image/pcx', 
                   'PDF' :  'application/pdf', 
                   'PNG' : 'image/png', 
                   'TIFF' : 'image/tiff'}

        self.extensions = {'bmp' : 'image/bmp',  
                   'gif' : 'image/gif', 
                   'jpg': 'image/jpeg', 
                   'pcx' : 'image/pcx', 
                   'pdf' :  'application/pdf', 
                   'png' : 'image/png', 
                   'tif' : 'image/tiff'}

        self.compliance = "http://library.stanford.edu/iiif/image-api/1.1/compliance.html#level2"

        self.compliance = "http://library.stanford.edu/iiif/image-api/compliance.html#level2"


        # encoding param for PIL        
        self.jpegQuality = 90

        if CACHEDIR:
            os.chdir(CACHEDIR)
        else:
            os.chdir(os.path.join(BASEDIR, PREFIX))
        
        id = "([^/#?@]+)"
        region = "(full|(pct:)?([\d.]+,){3}([\d.]+))"
        size = "(full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,[\d.]+|![\d.]+,[\d.]+)"
        rot = "([0-9.+])"
        quality = "(native|color|grey|bitonal)"
        format = "(jpg|tif|png|gif|jp2|pdf|eps|bmp)"        
        #ire = '/' + '/'.join([id,region,size,rot,quality]) + "(." + format + ")?"
        self.idRe = re.compile(id)
        self.regionRe = re.compile(region)
        self.sizeRe = re.compile(size)
        self.rotationRe = re.compile(rot)
        self.qualityRe = re.compile(quality)
        self.formatRe = re.compile(format)        
        self.infoRe = re.compile("/" + id + '/info.(xml|json)')
        self.badcharRe= re.compile('[\[\]?@#/]')
                        
    def error_msg(self, param, msg, status):
        text = "An error occured when processing the '%s' parameter:  %s" % (param, msg)
        self.status = status
        self.out_headers['Content-type'] = 'text/plain'
        return text

    def get_image_file(self, identifier):
        if self.identifiers.has_key(identifier):
            return self.identifiers[identifier]
        else:
            return ""

    def make_info(self, infoId, image):
        (imageW, imageH) = image.size
        
        if image.mode == 'L':
            qualities = ['native','grey','bitonal']
        elif image.mode == '':
            qualities = ['native','bitonal']                
        else:
            qualities = ['native','color','grey','bitonal']            
        
        formats = self.extensions.keys()

        info = {"@id": "%s/%s/%s" % (BASEURL, PREFIX, infoId),
                "@context" : "http://library.stanford.edu/iiif/image-api/1.1/context.json",
                "width":imageW,
                "height":imageH,
                "tile_width": TILE_SIZE,
                "tile_height": TILE_SIZE,
                "scale_factors": [1,2,3,4,5,8,10,16],
                "formats": formats,
                "qualities": qualities,
                "profile": self.compliance}

        data = json.dumps(info, sort_keys=True)

        os.mkdir(infoId)
        fh = file(infoId+'/info.json', 'w')
        fh.write(data)
        fh.close()       
        return info
        
    def send_file(self, filename, mt):
        fh = file(filename)
        data = fh.read()
        fh.close()
        return self.send(data, status=200, ct=mt)

    def handle(self):

        # http://{server}{/prefix}   /{identifier}/{region}/{size}/{rotation}/{quality}{.format}
        bits = self.path.split('/')[1:]

        if bits and bits[0] == "list":
            return self.send(repr(self.identifiers), status=200, ct="text/plain");

        if bits:
            identifier = bits.pop(0)
            if self.idRe.match(identifier) == None:
                return self.error_msg("identifier", "Identifier invalid: %r" % identifier, status=400)
            else:
                # Check []?#@ (will never find / )
                if self.badcharRe.match(identifier):
                    return self.error_msg('identifier', 'Unescaped Characters', status=400)                
                identifier = urllib.unquote(identifier)
                infoId = urllib.quote(identifier, '')
                filename = self.get_image_file(identifier)
                if not filename:
                    return self.error_msg('identifier', 'Not found: %s' % identifier, status=404)          
        else:
            return self.error_msg("identifier", "Identifier unspecified", status=400)

        self.out_headers['Link'] = '<http://library.stanford.edu/iiif/image-api/compliance.html#level2>;rel="profile"'

        # Early cache check here
        fp = self.path[1:]
        if len(fp) > 9 and fp[-9:] == "info.json":
            mimetype = "application/json"
        elif len(fp) > 4 and fp[-4] == '.':
            try:
                mimetype = self.extensions[fp[-3:]]
            except:
                # no such format, early break
                return self.error_msg('format', 'Unsupported format', status=415)
        else:
            # allow default extension to be checked and cached separately for conneg
            mimetype = "image/jpeg"
            fp = fp + '.jpg'
        if os.path.exists(fp):
            return self.send_file(fp, mimetype)                    
                    
        if bits:
            region = bits.pop(0)
            if self.regionRe.match(region) == None:
                # test for info.json
                if region == "info.json":
                    # build and return info
                    mt = "application/json"
                    if not os.path.exists(infoId +'/'+region):
                        image = Image.open(filename)
                        self.make_info(infoId, image)
                        try:
                            image.close()
                        except:
                            pass
                    return self.send_file(infoId +'/' + region, mt)
                else:                
                    return self.error_msg("region", "Region invalid: %r" % region, status = 400)
        else:
            return self.error_msg("region", "Region unspecified", status=400)

        if bits:
            size = bits.pop(0)
            if self.sizeRe.match(size) == None:
                return self.error_msg("size", "Size invalid: %r" % size, status = 400)
        else:
            return self.error_msg("size", "Size unspecified", status=400)

        if bits:
            rotation = bits.pop(0)
            if self.rotationRe.match(rotation) == None:
                return self.error_msg("rotation", "Rotation invalid: %r" % rotation, status = 400)
        else:
            return self.error_msg("rotation", "Rotation unspecified", status=400)

        if bits:
            quality = bits.pop(0)
            dotidx = quality.rfind('.')
            if dotidx > -1:
                format = quality[dotidx+1:]
                quality = quality[:dotidx]
            else:
                format = "jpg"                
            if self.qualityRe.match(quality) == None:
                return self.error_msg("quality", "Quality invalid: %r" % quality, status = 400)
            elif self.formatRe.match(format) == None:
                return self.error_msg("format", "Format invalid: %r" % format, status = 400)
        else:
            return self.error_msg("quality", "Quality unspecified", status=400)                

        # Do we already exist?            
        if os.path.exists('./'+infoId):
            # load JSON info file or image?
            fh = file(infoId +'/info.json')
            info = json.load(fh)
            fh.close()
            image = None
        else:
            # Need to load it up for the first time!     
            image = Image.open(filename)
            info = self.make_info(infoId, image)
        imageW = info['width']
        imageH = info['height']
                    
        # Check region
        if region == 'full':
            # full size of image
            x=0;y=0;w=imageW;h=imageH
        else:
            try:
                (x,y,w,h)=region.split(',')
            except:
                return self.error_msg('region', 'unable to parse region: %r' % region, status=400)
            if x.startswith('pct:'):
                x = x[4:]
                # convert pct into px
                try:
                    x = float(x) ; y = float(y) ; w = float(w) ; h = float(h)
                    x = int(x / 100.0 * imageW)
                    y = int(y / 100.0 * imageH)
                    w = int(w / 100.0 * imageW)
                    h = int(h / 100.0 * imageH)
                except:
                    return self.error_msg('region', 'unable to parse region: %r' % region, status=400)                     
            else:
                try:
                    x = int(x) ; y = int(y) ; w = int(w) ; h = int(h)
                except:
                    return self.error_msg('region', 'unable to parse region: %r' % region, status=400) 
                            
            if (x > imageW):
                return self.error_msg("region", "X coordinate is outside image", status=400)
            elif (y > imageH):
                return self.error_msg("region", "Y coordinate is outside image", status=400)
            elif w < 1:
                return self.error_msg("region", "Region width is zero", status=400)
            elif h < 1:
                return self.error_msg("region", "Region height is zero", status=400) 
            
            # PIL will create whitespace outside, so constrain
            # Need this info for next step anyway
            if x+w > imageW:
                w = imageW-x            
            if y+h > imageH:
                h = imageH-y            

        # Output Size
        if size == 'full':
            sizeW = w ; sizeH = h
        else:
            try:
                if size[-1] == ',':    # w,
                    # constrain width to w, and calculate appropriate h
                    sizeW = int(size[:-1])
                    ratio = sizeW/float(w)
                    sizeH = int(h * ratio)      
                elif size[0] == ',':     # ,h
                    # constrain height to h, and calculate appropriate w
                    sizeH = int(size[1:])
                    ratio = sizeH/float(h)
                    sizeW = int(w * ratio)
                elif size[0] == '!':     # !w,h
                    # Must fit inside w and h
                    (maxSizeW, maxSizeH) = size[1:].split(',')
                    # calculate both ratios and pick smaller
                    ratioW = float(maxSizeW) / w
                    ratioH = float(maxSizeH) / h
                    ratio = min(ratioW, ratioH)
                    sizeW = int(w * ratio)
                    sizeH = int(h * ratio)        
                elif size.startswith('pct:'):     #pct: n
                    # n percent of size
                    ratio = float(size[4:])/100
                    sizeW = int(w * ratio)
                    sizeH = int(h * ratio)                         
                    if sizeW < 1:
                        sizeW = 1
                    if sizeH < 1:
                        sizeH = 1
                else:    # w,h    or invalid
                    (sw,sh) = size.split(',')
                    # exactly w and h, deforming aspect
                    sizeW = int(sw)
                    sizeH = int(sh)                
            except:
                return self.error_msg('size', 'Size unparseable: %r' % size, status=400)      
        
        # Process rotation
        try:
            rotation = float(rotation)
        except:
            return self.error_msg('rotation', 'Rotation unparseable: %r' % rotation, status=400)
        if rotation < 0 or rotation > 360:
            return self.error_msg('rotation', 'Rotation must be 0-359.99: %r' % rotation, status=400)            
        rotation = rotation % 360

        if not quality in info['qualities']:
            return self.error_msg('quality', 'Quality not supported for this image: %r' % quality, status=501)            
        elif quality == info['qualities'][1]:
            quality = 'native'
        
        nformat = format.upper()
        if nformat == 'JPG':
            nformat = 'JPEG'
        elif nformat == "TIF":
            nformat = "TIFF"
        try:
            mimetype = self.formats[nformat]
        except:
            return self.error_msg('format', 'Unsupported format', status=415)

        # Check if URI is not canonical, if so redirect to canonical URI
        # Check disk cache and maybe redirect
        paths = [infoId, "%s,%s,%s,%s" % (x,y,w,h), "%s,%s" % (sizeW, sizeH), str(rotation), "%s.%s" % (quality, format.lower())]
        fn = os.path.join(*paths)
        if os.path.exists(fn):
            # Not canonical or would have been caught by early cache check
            self.out_headers['Location'] = BASEURL + '/'+ PREFIX + '/' + fn
            return self.send("", status=301)

        # And finally, process the image!
        if image == None:
            try:
                image = Image.open(filename)
            except IOError:
                return self.error_msg('identifier', 'Unsupported format for base image', status=501)
                
        if (w != info['width'] or h != info['height']):
            box = (x,y,x+w,y+h)
            image = image.crop(box)
        if sizeW != w or sizeH != h:
            image = image.resize((sizeW, sizeH))        
        if rotation != 0:
            # NB Rotation in PIL can introduce extra pixels on edges, even for square
            # PIL is counter-clockwise, so need to reverse
            rotation = 360 - rotation
            try:
                image = image.rotate(rotation, expand=1)
            except:
                # old version of PIL without expand

                # x2 = x0+(x-x0)*cos(theta)+(y-y0)*sin(theta)
                # y2 = y0-(x-x0)*sin(theta)+(y-y0)*cos(theta)

                maxx = image.size[0]
                maxy = image.size[1]
                cx = int(image.size[0]/2)  # x0 above
                cy = int(image.size[1]/2)  # y0 above
                theta = math.radians(rotation)
                
                toplx = cx + (0-cx)*math.cos(theta) + (0-cy)*math.sin(theta)
                toply = cy - (0-cx)*math.sin(theta) + (0-cy)*math.cos(theta)                
                toprx = cx + (0-cx)*math.cos(theta) + (maxy-cy)*math.sin(theta)
                topry = cy - (0-cx)*math.sin(theta) + (maxy-cy)*math.cos(theta)
                botlx = cx + (maxx-cx)*math.cos(theta) + (0-cy)*math.sin(theta)
                botly = cy - (maxx-cx)*math.sin(theta) + (0-cy)*math.cos(theta)    
                botrx = cx + (maxx-cx)*math.cos(theta) + (maxy-cy)*math.sin(theta)
                botry = cy - (maxx-cx)*math.sin(theta) + (maxy-cy)*math.cos(theta)                
                
                nminx = min(toplx, toprx, botlx, botrx)
                nmaxx = max(toplx, toprx, botlx, botrx)
                nminy = min(toply, topry, botly, botry)
                nmaxy = max(toply, topry, botly, botry)
                
                rx = nmaxx - nminx
                ry = nmaxy - nminy
                
                bg = Image.new("RGB", (rx,ry), (0,0,0))
                tx = int((rx-image.size[0])/2)
                ty = int((ry-image.size[1])/2)
                bg.paste(image, (tx,ty,tx+image.size[0],ty+image.size[1]))
                image = bg.rotate(rotation)

        if quality != 'native':
            nquality = {'color':'RGB','grey':'L','bitonal':'1'}[quality]
            image = image.convert(nquality)

        output = StringIO.StringIO()
        try:
            image.save(output,format=nformat, quality=self.jpegQuality)
        except SystemError:
            return self.error_msg('size', 'Unsupported size... tile cannot extend outside image', status=501)
        except IOError:
            return self.error_msg('format', 'Unsupported format for format', status=501)
        contents = output.getvalue()
        output.close()
        
        # Write to disk cache
        for p in range(1,len(paths)):
            pth = os.path.join(*paths[:p])
            if not os.path.exists(pth):
                os.mkdir(pth, 0775)         
        fh = file(fn, 'w')
        fh.write(contents)
        fh.close()
 
        return self.send(contents, ct=mimetype)


application = ServiceHandler()

