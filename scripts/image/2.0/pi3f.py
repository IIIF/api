
import cgi, cgitb
from wsgiref import headers
import urllib, urlparse

import StringIO
import os, sys
import glob
import re
import math
import uuid

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
UPLOADDIR = HOMEDIR+"/image_uploads/"
UPLOADS = False

FILEDIRS = [
 HOMEDIR+"/image_data/"
]
IMAGEFMTS = ['png', 'jpg', 'tif']

CACHEDIR = HOMEDIR+"/image_cache/2.0/"

BASEURL = "http://iiif.io/"
PREFIX = "api/image/2.0/example/reference"


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

        self.compliance = "http://iiif.io/api/image/2/level2.json"
        self.context = "http://iiif.io/api/image/2/context.json"
        self.protocol = "http://iiif.io/api/image"

        # encoding param for PIL        
        self.jpegQuality = 90

        if CACHEDIR:
            os.chdir(CACHEDIR)
        else:
            os.chdir(os.path.join(BASEDIR, PREFIX))
        
        id = "([^/#?@]+)"
        region = "(full|(pct:)?([\d.]+,){3}([\d.]+))"
        size = "(full|[\d.]+,|,[\d.]+|pct:[\d.]+|[\d.]+,[\d.]+|![\d.]+,[\d.]+)"
        rot = "(!)?([0-9.]+)$"
        quality = "(default|color|gray|bitonal)"
        format = "(jpg|tif|png|gif|jp2|pdf|eps|bmp)"        

        self.idRe = re.compile(id)
        self.regionRe = re.compile(region)
        self.sizeRe = re.compile(size)
        self.rotationRe = re.compile(rot)
        self.qualityRe = re.compile(quality)
        self.formatRe = re.compile(format)        
        self.infoRe = re.compile("/" + id + '/info.json')
        self.badcharRe= re.compile('[\[\]?@#/]')

    def error(self, status, message=""):
        self.status = status
        self.out_headers['Content-type'] = 'text/plain'
        if message:
            return message
        else:    
            return self.codes[status]
                        
    def error_msg(self, param, msg, status):
        text = "An error occured when processing the '%s' parameter:  %s" % (param, msg)
        self.status = status
        self.out_headers['Content-type'] = 'text/plain'
        return text

    def get_image_file(self, identifier):
        if self.identifiers.has_key(identifier):
            return self.identifiers[identifier]
        else:
            # recheck uploaded...
            fns = glob.glob(UPLOADDIR + identifier + '.*')
            if fns:
                self.identifiers[identifier] = fns[0]
                return fns[0]
            else:
                return ""

    def make_info(self, infoId, image):
        (imageW, imageH) = image.size
        
        if image.mode == 'L':
            qualities = ['gray']
        elif image.mode == '':
            qualities = []                
        else:
            qualities = ['color','gray']            

        all_scales = [1,2,4,8,16]

        sizes = []
        for scale in all_scales:
            sizes.append({'width': imageW / scale, 'height': imageH / scale })
        sizes.reverse()
        info = {
                "@id": "%s%s/%s" % (BASEURL, PREFIX, infoId),
                "@context" : self.context,
                "protocol" : self.protocol,
                "width":imageW,
                "height":imageH,
                "tiles" : [{'width':1024, 'scale_factors': [1,2]}, {'width':512, 'scale_factors':[4,8,16]}],
                "sizes" : sizes,
                "profile": [self.compliance,
                    {
                        "formats":["gif","tif","pdf"],
                        "supports":["canonical_link_header", "mirroring", "rotation_arbitrary", "size_above_full"],
                        "qualities":qualities
                    }
                ]
        }
        if qualities:
            info["profile"][1]["qualities"] = qualities

        data = json.dumps(info, sort_keys=True)

        try:
            os.mkdir(infoId)
        except OSError:
            # directory already exists
            pass
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
        # dispatch for different methods.

        method = self.environ['REQUEST_METHOD']

        if method == "GET":
            return self.handle_GET();
        elif not UPLOADS:
            return self.error(405)
        elif method == "POST":
            return self.handle_POST();
        elif method == "PUT":
            return self.handle_PUT();
        elif method == "DELETE":
            return self.handle_DELETE();
        else:
            return self.error(405);

    def handle_PUT(self):
        # PUT to /prefix/id create/replace image WITH id and return info.json
        if not self.path:
            self.error(400, message="Need identifier for PUT")
        else:
            bits = self.path[1:].split('/')
            if len(bits) > 1:
                return self.error(400, message="Cannot give parameters for PUT, just identifier: %r" % bits)
            # Read in body of request
            data = self.body
            ct = self.environ['CONTENT_TYPE'].lower()
            return self.create_image(data, ct, bits[0])            

    def handle_POST(self):
        # POST to /prefix create new image and return info.json
        if self.path != "":
            # Can't POST to an id
            self.error(400, message="Can only upload to base prefix")

        # Read in body of request
        data = self.body
        ct = self.environ['CONTENT_TYPE'].lower()
        return self.create_image(data, ct)

    def handle_DELETE(self):
        # DELETE to /prefix/id delete image with id and return ... ???
        if not self.path:
            self.error(400, message="Need identifier for DELETE")
        else:
            bits = self.path[1:].split('/')
            if len(bits) > 1:
                return self.error(400, message="Cannot give parameters for DELETE, just identifier: %r" % bits)
            # Read in body of request
            ident = bits[0]
            fns = glob.glob(UPLOADDIR + ident + ".*")
            if not fns:
                return self.error(404, message="No such resource to delete")
            else:
                fn = fns[0]
                try:
                    os.remove(fn)
                    self.status = 200
                    return "Deleted"
                except:
                    return self.error(500, message="Cannot delete that resource")
 


    def create_image(self, data, ct, ident=""):

        if ct.startswith("multipart/form-data"):
            # extract form data for file upload
            pstr = ct[19:].strip()
            if pstr[0] == ";":
                pstr = pstr[1:]
            prms = pstr.split('=')
            fpd = {prms[0] : prms[1]}
            return self.error(500, message=repr(fpd))
            fs = cgi.parse_multipart(StringIO.StringIO(data), fpd)
            return self.error(500, message=repr(fs))

        if ct.startswith('image/'):

            if not ident:
                newid = str(uuid.uuid4())
            else:
                # Check id to make sure it's sane
                if len(ident) > 50 or urllib.unquote(ident) != ident:
                    return self.error(400, "Unacceptable identifier")
                else:
                    newid = ident 

            if ct == "image/png":
                fn = newid + ".png"
            elif ct in ["image/jpeg", "image/jpg"]:
                fn = newid + ".jpg"
            elif ct in ["image/tif", 'image/tiff']:
                fn = newid + '.tif'

            try:
                fullfn = os.path.join(UPLOADDIR, fn)
                fh = file(fullfn, 'w')
                fh.write(data)
                fh.close()
                self.identifiers[str(newid)] = fullfn
            except:
                raise
                return self.error(500, "Couldn't write to disk, sorry")

            mt = "application/json"
    
            image = Image.open(fullfn)
            self.make_info(newid, image)
            try:
                image.close()
            except:
                pass
            return self.send_file(newid + '/info.json', mt)

        else:
            return self.error(400, "Need image content-type request header, got %s" % ct)


    def handle_GET(self):

        # http://{server}{/prefix}   /{identifier}/{region}/{size}/{rotation}/{quality}{.format}
        bits = self.path.split('/')[1:]

        # Nasty but useful debugging hack
        if len(bits) == 1 and bits[0] == "list":
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

        self.out_headers['Link'] = '<%s>;rel="profile"' % self.compliance

        # Early cache check here
        fp = self.path[1:]
        if fp == identifier or fp == "%s/" % identifier:
            self.status = 303
            self.out_headers['location'] = "%s%s/%s/info.json" % (BASEURL, PREFIX, infoId)
            return ""            
        elif len(fp) > 9 and fp[-9:] == "info.json":
            mimetype = "application/json"
        elif len(fp) > 4 and fp[-4] == '.':
            try:
                mimetype = self.extensions[fp[-3:]]
            except:
                # no such format, early break
                return self.error_msg('format', 'Unsupported format', status=400)
        if os.path.exists(fp):
            self.out_headers['X-cache-hit'] = "1"
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
        # else is caught by checking identifier in early cache check

        if bits:
            size = bits.pop(0)
            if self.sizeRe.match(size) == None:
                return self.error_msg("size", "Size invalid: %r" % size, status = 400)
        else:
            return self.error_msg("size", "Size unspecified", status=400)

        if bits:
            rotation = bits.pop(0)
            m = self.rotationRe.match(rotation) 
            if m == None:
                return self.error_msg("rotation", "Rotation invalid: %r" % rotation, status = 400)
            else:
                mirror, rotation = m.groups()
        else:
            return self.error_msg("rotation", "Rotation unspecified", status=400)

        if bits:
            quality = bits.pop(0)
            dotidx = quality.rfind('.')
            if dotidx > -1:
                format = quality[dotidx+1:]
                quality = quality[:dotidx]
            else:
                return self.error_msg("format", "Format not specified but mandatory", status=400)               
            if self.qualityRe.match(quality) == None:
                return self.error_msg("quality", "Quality invalid: %r" % quality, status = 400)
            elif self.formatRe.match(format) == None:
                return self.error_msg("format", "Format invalid: %r" % format, status = 400)
        else:
            return self.error_msg("quality", "Quality unspecified", status=400)                

        # MUCH quicker to load JSON than the image to find h/w
        # Does json already exist?            
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
            if '.' in rotation:
                rot = float(rotation)
                if rot == int(rot):
                    rot = int(rot)
            else:
                rot = int(rotation)
        except:
            return self.error_msg('rotation', 'Rotation unparseable: %r' % rotation, status=400)
        if rot < 0 or rot > 360:
            return self.error_msg('rotation', 'Rotation must be 0-359.99: %r' % rotation, status=400)            
        # 360 --> 0
        rot = rot % 360

        quals = info['profile'][1]['qualities']
        quals.extend(["default","bitonal"])
        if not quality in quals:
            return self.error_msg('quality', 'Quality not supported for this image: %r not in %r' % (quality, quals), status=501)
        if quality == quals[0]:
            raise ValueError("%s vs %r" % (quality, quals))
            quality = "default"
        
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
        if x == 0 and y == 0 and w == imageW and h == imageH:
            c_region = "full"
        else:
            c_region = "%s,%s,%s,%s" % (x,y,w,h)
        if sizeW == imageW and sizeH == imageH:
            c_size = "full"
        else:
            c_size = "%s,%s" % (sizeW, sizeH)

        c_rot = "!%s" % rot if mirror else str(rot) 
        c_qual = "%s.%s" % (quality, format.lower())

        paths = [infoId, c_region, c_size, c_rot, c_qual]
        fn = os.path.join(*paths)
        if fn != self.path[1:]:
            new_url = BASEURL + PREFIX + '/' + fn
            self.out_headers['Link'] += ', <%s>;rel="canonical"' % new_url
            self.out_headers['Location'] = new_url
            return self.send("", status=301)

        # Won't regenerate needlessly as earlier cache check would have found it
        # if we're canonical already

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
        if mirror:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        if rot != 0:
            # NB Rotation in PIL can introduce extra pixels on edges, even for square
            # PIL is counter-clockwise, so need to reverse
            rot = 360 - rot
            try:
                image = image.rotate(rot, expand=1)
            except:
                # old version of PIL without expand
                segx = image.size[0]
                segy = image.size[1]
                angle = radians(rot)
                rx = abs(segx*cos(angle)) + abs(segy*sin(angle))
                ry = abs(segy*cos(angle)) + abs(segx*sin(angle))
                
                bg = Image.new("RGB", (rx,ry), (0,0,0))
                tx = int((rx-segx)/2)
                ty = int((ry-segy)/2)
                bg.paste(image, (tx,ty,tx+segx,ty+segy))
                image = bg.rotate(rot)

        if quality != 'default':
            nquality = {'color':'RGB','gray':'L','bitonal':'1'}[quality]
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
