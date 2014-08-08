
import cgitb
from wsgiref import headers
import urllib, urlparse

import StringIO
import os, sys
import glob
import re

from PIL import Image

try:
    import json
except:
    import simplejson as json


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

    def __init__(self, d):
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

    def __init__(self, d):
        WsgiApp.__init__(self, d)
        self.identifiers = {}
        filedir = '/home/iiif/Web/image_data/'
        fns = glob.glob(filedir+'*jpg')
        fns.extend(glob.glob(filedir+'*png'))
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

        # encoding param for PIL        
        self.jpegQuality = 90

        os.chdir('/home/iiif/Web/image_cache/1.0')
        
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
                
    def xmlerror(self, param, msg, status):

        xml = """<?xml version="1.0" encoding="UTF-8" ?>
<error xmlns="http://library.stanford.edu/iiif/image-api/ns/">
  <parameter>%s</parameter>
  <text>%s</text>
</error>""" % (param, msg)

        self.status = status
        self.out_headers['Content-type'] = 'text/xml'
        return xml

    def get_image_file(self, identifier):
        if self.identifiers.has_key(identifier):
            return self.identifiers[identifier]
        else:
            return ""

    def make_info(self, infoId, image):
        (imageW, imageH) = image.size
        
        if image.mode == 'RGB':
            qualities = ['native','color','grey','bitonal']
        elif image.mode == 'L':
            qualities = ['native','grey','bitonal']
        elif image.mode == '':
            qualities = ['native','bitonal']                
        
        formats = ['jpg','png','pdf','tif','gif','bmp','eps']
        info = {"identifier": infoId,
                "width":imageW,
                "height":imageH,
                "formats": formats,
                "qualities": qualities}
        data = json.dumps(info)
        xmlformats = " ".join(["<format>%s</format>" % x for x in formats])
        xmlqualities = " ".join(["<quality>%s</quality>" % x for x in qualities])
        
        xmldata = """<?xml version="1.0" encoding="UTF-8"?>
        <info xmlns="http://library.stanford.edu/iiif/image-api/ns/">
        <identifier>%s</identifier>
        <width>%s</width>
        <height>%s</height>
        <formats>%s</formats>
        <qualities>%s</qualities>
        </info>""" % (infoId, imageW, imageH, xmlformats, xmlqualities)
        
        try:
            os.mkdir(infoId)
        except:
            pass
        fh = file(infoId+'/info.json', 'w')
        fh.write(data)
        fh.close()
        fh = file(infoId+'/info.xml', 'w')
        fh.write(xmldata)
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
        if bits:
            identifier = bits.pop(0)
            if self.idRe.match(identifier) == None:
                return self.xmlerror("identifier", "Identifier invalid: %r" % identifier, status=400)
            else:
                identifier = urllib.unquote(identifier)
                infoId = urllib.quote(identifier, '')
                filename = self.get_image_file(identifier)
                if not filename:
                    return self.xmlerror('identifier', 'Not found: %s' % identifier, status=404)          
        else:
            return self.xmlerror("identifier", "Identifier unspecified", status=400)

        self.out_headers['Link'] = '<http://library.stanford.edu/iiif/image/conformance/0>;rel="profile"'
                    
        if bits:
            region = bits.pop(0)
            if self.regionRe.match(region) == None:
                # test for info.xml info.json
                mt = "text/xml" if region == "info.xml" else "application/json"
                if region == "info.xml" or region == "info.json":
                    # build and return info
                    if not os.path.exists(infoId +'/'+region):
                        image = Image.open(filename)
                        self.make_info(infoId, image)
                        # image.close()
                    return self.send_file(infoId +'/' + region, mt)
                else:                
                    return self.xmlerror("region", "Region invalid: %r" % region, status = 400)
        else:
            return self.xmlerror("region", "Region unspecified", status=400)

        if bits:
            size = bits.pop(0)
            if self.sizeRe.match(size) == None:
                return self.xmlerror("size", "Size invalid: %r" % size, status = 400)
        else:
            return self.xmlerror("size", "Size unspecified", status=400)

        if bits:
            rotation = bits.pop(0)
            if self.rotationRe.match(rotation) == None:
                return self.xmlerror("rotation", "Rotation invalid: %r" % rotation, status = 400)
        else:
            return self.xmlerror("rotation", "Rotation unspecified", status=400)

        if bits:
            quality = bits.pop(0)
            dotidx = quality.rfind('.')
            if dotidx > -1:
                format = quality[dotidx+1:]
                quality = quality[:dotidx]
            else:
                format = "jpg"                
            if self.qualityRe.match(quality) == None:
                return self.xmlerror("quality", "Quality invalid: %r" % quality, status = 400)
            elif self.formatRe.match(format) == None:
                return self.xmlerror("format", "Format invalid: %r" % format, status = 400)
        else:
            return self.xmlerror("quality", "Quality unspecified", status=400)                

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
                return self.xmlerror('region', 'unable to parse region: %r' % region, status=400)
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
                    return self.xmlerror('region', 'unable to parse region: %r' % region, status=400)                     
            else:
                try:
                    x = int(x) ; y = int(y) ; w = int(w) ; h = int(h)
                except:
                    return self.xmlerror('region', 'unable to parse region: %r' % region, status=400) 
                            
            if (x > imageW):
                return self.xmlerror("region", "X coordinate is outside image", status=400)
            elif (y > imageH):
                return self.xmlerror("region", "Y coordinate is outside image", status=400)
            elif w < 1:
                return self.xmlerror("region", "Region width is zero", status=400)
            elif h < 1:
                return self.xmlerror("region", "Region height is zero", status=400) 
            
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
                else:    # w,h    or invalid
                    (sw,sh) = size.split(',')
                    # exactly w and h, deforming aspect
                    sizeW = int(sw)
                    sizeH = int(sh)                
            except:
                return self.xmlerror('size', 'Size unparseable: %r' % size, status=400)      
        
        # Process rotation
        try:
            rotation = float(rotation)
        except:
            return self.xmlerror('rotation', 'Rotation unparseable: %r' % rotation, status=400)
        if rotation < 0 or rotation > 360:
            return self.xmlerror('rotation', 'Rotation must be 0-359.99: %r' % rotation, status=400)            
        rotation = rotation % 360

        if not quality in info['qualities']:
            return self.xmlerror('quality', 'Quality not supported for this image: %r' % quality, status=501)            
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
            return self.xmlerror('format', 'Unsupported format', status=415)

        # Check disk cache
        paths = [infoId, "%s,%s,%s,%s" % (x,y,w,h), "%s,%s" % (sizeW, sizeH), str(rotation), "%s.%s" % (quality, format.lower())]
        fn = os.path.join(*paths)
        if os.path.exists(fn):
            return self.send_file(fn, mimetype)

        # And finally, process the image!
        if image == None:
            image = Image.open(filename)
        if (w != info['width'] or h != info['height']):
            box = (x,y,x+w,y+h)
            image = image.crop(box)
        if sizeW != w or sizeH != h:
            image = image.resize((sizeW, sizeH))        
        if rotation != 0:
            # NB Rotation in PIL can introduce extra pixels on edges, even for square
            image = image.rotate(rotation, expand=1)
        if quality != 'native':
            nquality = {'color':'RGB','grey':'L','bitonal':'1'}[quality]
            image = image.convert(nquality)

        output = StringIO.StringIO()
        image.save(output,format=nformat, quality=self.jpegQuality)
        contents = output.getvalue()
        output.close()

        # Write to disk cache
        for p in range(1,len(paths)):
            pth = os.path.join(*paths[:p])
            if not os.path.exists(pth):
                os.mkdir(pth)         
        fh = file(fn, 'w')
        fh.write(contents)
        fh.close()
 
        return self.send(contents, ct=mimetype)


application = ServiceHandler('x')
