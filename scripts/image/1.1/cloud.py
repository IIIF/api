
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
    import json
except:
    import simplejson as json

import cloudinary
from cloudinary import api

BASEURL = "http://iiif-dev.localhost/"
PREFIX = "services/cloud"

TILE_SIZE = 512

CLOUD_NAME = "iiif"
CLOUD_KEY = "244538263287441"
CLOUD_SECRET = "4tTjTfcng3lFlN5ZNf6DhQSYa5U"
config = cloudinary.config(cloud_name=CLOUD_NAME, api_key=CLOUD_KEY, api_secret=CLOUD_SECRET)

CLOUD_BASEURL = "http://res.cloudinary.com/" + CLOUD_NAME + "/image/upload"

INFO_CACHE={}


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


    def make_info(self, identifier):

        if INFO_CACHE.has_key(identifier):
            (imageW, imageH) = INFO_CACHE[identifier]
        else:
            external = api.resource(identifier)
            imageW = external['width']
            imageH = external['height']
            INFO_CACHE[identifier] = (imageW, imageH)

        qualities = ['native','color','grey','bitonal']            
        
        formats = self.extensions.keys()

        info = {"@id": "%s%s/%s" % (BASEURL, PREFIX, identifier),
                "@context" : "http://library.stanford.edu/iiif/image-api/1.1/context.json",
                "width":imageW,
                "height":imageH,
                "tile_width": TILE_SIZE,
                "tile_height": TILE_SIZE,
                "scale_factors": [1,2,3,4,5,8,10,16],
                "formats": formats,
                "qualities": qualities,
                "profile": self.compliance}
      
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

        raise NotImplementedError

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
        else:
            return self.error_msg("identifier", "Identifier unspecified", status=400)

        self.out_headers['Link'] = '<http://library.stanford.edu/iiif/image-api/compliance.html#level2>;rel="profile"'
                    
        if bits:
            region = bits.pop(0)
            if self.regionRe.match(region) == None:
                # test for info.json
                if region == "info.json":
                    # build and return info
                    info = self.make_info(identifier)
                    jsoninfo = json.dumps(info, sort_keys=True)
                    return self.send( jsoninfo, status=200, ct="application/json")
                else:                
                    return self.error_msg("region", "Region invalid: %r" % region, status = 400)
        else:
            # As of 1.1, identifier should redirect with 303 to identifier/info.json
            self.status = 303
            self.out_headers['location'] = "%s%s/%s/info.json" % (BASEURL, PREFIX, infoId)
            return ""

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

        # Now we need the info for the image from cloudinary or cache
        info = self.make_info(identifier)
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

        # Build simplest cloudinary URL 
        cloud_url = [CLOUD_BASEURL] 
        if x != 0 or y != 0 or w != imageW or h != imageH:
            cloud_url.append("c_crop,x_%s,y_%s,w_%s,h_%s" % (x,y,w,h))
        if sizeW != w or sizeH != h:
            cloud_url.append("c_scale,w_%s,h_%s" % (sizeW, sizeH))
        if rotation != 0:
            cloud_url.append("a_%s" % rotation)
        if quality == 'bitonal':
            cloud_url.append("e_blackwhite")
        elif quality == 'grey':
            cloud_url.append("e_grayscale")    

        cloud_url.append("%s.%s" % (identifier, format))
        location = "/".join(cloud_url)

        # And redirect to it
        self.out_headers['Location'] = location
        return self.send("", status=301)


application = ServiceHandler()

