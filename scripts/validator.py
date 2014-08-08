
import json
from functools import partial
from bottle import Bottle, route, run, request, response, abort, error

import uuid
import datetime

import cgitb
import urllib, urllib2, urlparse

import StringIO
import os, sys
import re
import random
import uuid
import math

try:
    from PIL import Image, ImageDraw
except:
    import Image, ImageDraw

from uritemplate import expand

class ValidatorError(Exception):
    def __init__(self, type, got, expected, validator=None):
        self.type = type
        self.got = got
        self.expected = expected
        if validator != None:
            self.url = validator.last_url
            self.headers = validator.last_headers
            self.status = validator.last_status
        else:
            self.url = None
            self.headers = None
            self.status = None
                
    def __str__(self):
        return "Expected %r for %s; Got: %r" % (self.expected, self.type, self.got)


class ValidationInfo(object):
    def __init__(self):

        self.qualities = ['native','color','grey','bitonal']
        self.formats= ['jpg','png','pdf','tif','gif','jp2']
        self.mimetypes = {'bmp' : 'image/bmp',  
                   'gif' : 'image/gif', 
                   'jpg': 'image/jpeg', 
                   'pcx' : 'image/pcx', 
                   'pdf' :  'application/pdf', 
                   'png' : 'image/png', 
                   'tif' : 'image/tiff'}

        self.pil_formats = {'BMP' : 'image/bmp',  
                   'GIF' : 'image/gif', 
                   'JPEG': 'image/jpeg', 
                   'PCX' : 'image/pcx', 
                   'PDF' :  'application/pdf', 
                   'PNG' : 'image/png', 
                   'TIFF' : 'image/tiff'}
        
        self.colorInfo = [[(61, 170, 126), (61, 107, 178), (82, 85, 234), (164, 122, 110), (129, 226, 88), (91, 37, 121), (138, 128, 42), (6, 85, 234), (121, 109, 204), (65, 246, 84)], 
            [(195, 133, 120), (171, 43, 102), (118, 45, 130), (242, 105, 171), (5, 85, 105), (113, 58, 41), (223, 69, 3), (45, 79, 140), (35, 117, 248), (121, 156, 184)], 
            [(168, 92, 163), (28, 91, 143), (86, 41, 173), (111, 230, 29), (174, 189, 7), (18, 139, 88), (93, 168, 128), (35, 2, 14), (204, 105, 137), (18, 86, 128)], 
            [(107, 55, 178), (251, 40, 184), (47, 36, 139), (2, 127, 170), (224, 12, 114), (133, 67, 108), (239, 174, 209), (85, 29, 156), (8, 55, 188), (240, 125, 7)], 
            [(112, 167, 30), (166, 63, 161), (232, 227, 23), (74, 80, 135), (79, 97, 47), (145, 160, 80), (45, 160, 79), (12, 54, 215), (203, 83, 70), (78, 28, 46)], 
            [(102, 193, 63), (225, 55, 91), (107, 194, 147), (167, 24, 95), (249, 214, 96), (167, 34, 136), (53, 254, 209), (172, 222, 21), (153, 77, 51), (137, 39, 183)], 
            [(159, 182, 192), (128, 252, 173), (148, 162, 90), (192, 165, 115), (154, 102, 2), (107, 237, 62), (111, 236, 219), (129, 113, 172), (239, 204, 166), (60, 96, 37)], 
            [(72, 172, 227), (119, 51, 100), (209, 85, 165), (87, 172, 159), (188, 42, 162), (99, 3, 54), (7, 42, 37), (105, 155, 100), (38, 220, 240), (98, 46, 2)], 
            [(18, 223, 145), (189, 121, 17), (88, 3, 210), (181, 16, 43), (189, 39, 244), (123, 147, 116), (246, 148, 214), (223, 177, 199), (77, 18, 136), (235, 36, 21)], 
            [(146, 137, 176), (84, 248, 55), (61, 144, 79), (110, 251, 49), (43, 105, 132), (165, 131, 55), (60, 23, 225), (147, 197, 226), (80, 67, 104), (161, 119, 182)]]
  
    def do_test_square(self, img, x,y, result):
        truth = self.colorInfo[x][y]
        # Similarity, not necessarily perceived
        cols = img.getcolors()
        cols.sort(reverse=True)
        col = cols[0][1]
        ok = abs(col[0]-truth[0]) < 6 and abs(col[1]-truth[1]) < 6 and abs(col[2]-truth[2]) < 6
        result.tests.append("%s,%s:%s" % (x,y,ok))
        return ok           

    def make_randomstring(self, length):
        stuff = []
        for x in range(length):
            stuff.append(chr(random.randint(48, 122)))
        return ''.join(stuff)

    def check(self, typ, got, expected, result=None):
        if type(expected) == list:
            if not got in expected:
                raise ValidatorError(typ, got, expected, result)
        elif got != expected:
            raise ValidatorError(typ, got, expected, result)
        if result:
            result.tests.append(typ)
        return 1

        
class TestSuite(object):

    def __init__(self, info):
        self.validationInfo = info

    def has_test(self, test):
        return hasattr(self, 'test_%s' % test)
          
    def list_tests(self, version=""):
        all = dir(self)
        tests = {}
        for t in all:
            if t.startswith('test_'):
                # Introspection for the win
                fn = getattr(self, t)
                doc = fn.__doc__
                try:
                    data = json.loads(doc)
                except:
                    data = "{}"
                name = t[5:]
                if version and data.has_key('versions') and not version in data['versions']:
                    continue
                tests[name] = data
        return tests

    def run_test(self, test, result):   

        fn = getattr(self, 'test_%s' % test)        
        try:
            return fn(result)
        except ValidatorError, e:
            result.exception = e
            return result


    #--------------------------------------------------------------------------
                
    def test_info_json(self, result):
        """{"label":"Check Image Information","level":0,"category":1,"versions":["1.0","1.1","2.0"]}"""

        # Does server have info.json
        try:
            info = result.get_info()
            self.validationInfo.check('required-field: @id', info.has_key('@id'), True, result)
            self.validationInfo.check('type-is-uri: @id', info['@id'].startswith('http'), True, result)
            self.validationInfo.check('required-field: width', info.has_key('width'), True, result)
            self.validationInfo.check('required-field: height', info.has_key('height'), True, result)
            self.validationInfo.check('type-is-int: height', type(info['height']) == int, True, result)
            self.validationInfo.check('type-is-int: width', type(info['width']) == int, True, result)
            return result
        except:
            raise
            self.validationInfo.check('status', result.last_status, 200, result)
            ct = result.last_headers['content-type']
            scidx = ct.find(';')
            if scidx > -1:
                ct = ct[:scidx]
            self.validationInfo.check('content-type', result.last_headers['content-type'], ['application/json', 'application/ld+json'], result)
            raise
            
    def test_id_error_random(self, result):
        """{"label":"Random identifier gives 404","level":1,"category":1,"versions":["1.0","1.1","2.0"]}"""
        try:
            url = result.make_url({'identifier': str(uuid.uuid1())})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 404, result)
            return result
        except:
            raise
        
    
    def test_id_error_unescaped(self, result):
        """{"label":"Unescaped identifier gives 400","level":1,"category":1,"versions":["1.0","1.1","2.0"]}"""
        try:
            url = result.make_url({'identifier': '[frob]'})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, [400, 404], result)
            return result   
        except:
            raise
    
    def test_id_error_escapedslash(self, result):
        """{"label":"Forward slash gives 404","level":1,"category":1,"versions":["1.0","1.1","2.0"]}"""        
        try:
            url = result.make_url({'identifier': 'a/b'})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 404, result)
            return result            
        except:
            raise
    
     
    def test_id_basic(self, result):
        """{"label":"Image is returned","level":0,"category":1,"versions":["1.0","1.1","2.0"]}"""
        try:
            url = result.make_url()
            data = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 200, result)
            img = result.make_image(data)
            return result
        except:
            raise
            
    def test_id_escaped(self, result):
        """{"label":"Escaped characters processed","level":1,"category":1,"versions":["1.0","1.1","2.0"]}"""
        try:
            idf = result.identifier.replace('-', '%2D')
            url = result.make_url({'identifier':idf})
            data = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 200, result)
            img = result.make_image(data)
            return result
        except:
            raise  

    def test_id_squares(self, result):
        """{"label":"Correct image returned","level":0,"category":1,"versions":["1.0","1.1","2.0"]}"""        
        try:
            url = result.make_url({'format':'jpg'})
            data = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 200, result)            
            img = result.make_image(data) 
            # Now test some squares for correct color

            match = 0
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * 100 + 13;
                yi = y * 100 + 13;
                box = (xi,yi,xi+74,yi+74)
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)
            if match >= 4:
                return result
            else:
                raise ValidatorError('color', 1,0,self)
        except:
            raise        
        
    def test_region_error_random(self, result):
        """{"label":"Random region gives 400","level":1,"category":2,"versions":["1.0","1.1","2.0"]}"""

        try:
            url = result.make_url({'region': self.validationInfo.make_randomstring(6)})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 400, result)
            return result          
        except:
            # self.validationInfo.check('status', result.last_status, 200)
            raise
    
    def test_region_pixels(self, result):
        """{"label":"Region specified by pixels","level":1,"category":2,"versions":["1.0","1.1","2.0"]}"""
        try:
            match = 0
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)           

                ix = x*100+13
                iy = y*100+13
                hw = 74
                params = {'region' :'%s,%s,%s,%s' % (ix,iy, hw, hw)}
                img = result.get_image(params)
                ok = self.validationInfo.do_test_square(img,x,y, result)
                if ok:
                    match += 1
            if match >= 4:         
                return result
            else:
                raise ValidatorError('color', 1,0,self)
        except:
            # self.validationInfo.check('status', result.last_status, 200, result)
            raise
            
    def test_region_percent(self, result):
        """{"label":"Region specified by percent","level":1,"category":2,"versions":["1.0","1.1","2.0"]}"""        
        try:
            match = 0
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                params = {'region' : 'pct:%s,%s,9,9' % (x*10+1, y*10+1)}
                img = result.get_image(params)                           
                ok = self.validationInfo.do_test_square(img,x,y, result)
                if ok:
                    match += 1
            if match >= 4:         
                return result
            else:
                raise ValidatorError('color', 1,0,self)
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise

    def test_size_error_random(self, result):
        """{"label":"Random size gives 400","level":1,"category":3,"versions":["1.0","1.1","2.0"]}"""        
        try:
            url = result.make_url({'size': self.validationInfo.make_randomstring(6)})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 400, result)
            return result             
        except:
            raise
    
    def test_size_wc(self, result):
        """{"label":"Size specified by w,","level":1,"category":3,"versions":["1.0","1.1","2.0"]}"""           
        try:
            s = random.randint(450,750)
            params = {'size': '%s,' % s}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (s,s), result)

            # Find square size
            sqs = int(s/1000.0 * 100)
            match = 0
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqs + 13;
                yi = y * sqs + 13;
                box = (xi,yi,xi+(sqs-13),yi+(sqs-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)
            if match >= 4:           
                return result
            else:
                raise ValidatorError('color', 1,0,self)          
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise
           
    def test_size_ch(self, result):
        """{"label":"Size specified by ,h","level":1,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            s = random.randint(450,750)
            params = {'size': ',%s' % s}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (s,s), result)

            # Find square size
            sqs = int(s/1000.0 * 100)
            match = 0            

            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqs + 13;
                yi = y * sqs + 13;
                box = (xi,yi,xi+(sqs-13),yi+(sqs-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)      
            if match >= 4:           
                return result
            else:
                raise ValidatorError('color', 1,0,self)           
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise        

    def test_size_percent(self, result):
        """{"label":"Size specified by percent","level":1,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            s = random.randint(45,75)
            params = {'size': 'pct:%s' % s}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (s*10,s*10), result)

            match = 0
            # Find square size
            sqs = s
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqs + 13;
                yi = y * sqs + 13;
                box = (xi,yi,xi+(sqs-13),yi+(sqs-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)      
            if match >= 4:           
                return result
            else:
                raise ValidatorError('color', 1,0,self) 
           
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise   

    def test_size_wh(self, result):
        """{"label":"Size specified by w,h","level":2,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            w = random.randint(350,750)
            h = random.randint(350,750)
            params = {'size': '%s,%s' % (w,h)}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (w,h), result)

            match = 0
            sqsw = int(w/1000.0 * 100)
            sqsh = int(h/1000.0 * 100)
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqsw + 13;
                yi = y * sqsh + 13;
                box = (xi,yi,xi+(sqsw-13),yi+(sqsh-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)      
            if match >= 4:           
                return result
            else:
                raise ValidatorError('color', 1,0,self) 
   
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 
    
    def test_size_bwh(self, result):
        """{"label":"Size specified by !w,h","level":2,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            w = random.randint(350,750)
            h = random.randint(350,750)
            s = min(w,h)
            params = {'size': '!%s,%s' % (w,h)}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (s,s), result)

            match = 0
            sqs = int(s/1000.0 * 100)
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqs + 13;
                yi = y * sqs + 13;
                box = (xi,yi,xi+(sqs-13),yi+(sqs-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)      
            if match >= 3:           
                return result
            else:
                raise ValidatorError('color', 1,0,self) 
               
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 

    def test_size_up(self, result):
        """{"label":"Size greater than 100%","level":3,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            s = random.randint(1100,2000)
            params = {'size': ',%s' % s}
            img = result.get_image(params)
            self.validationInfo.check('size', img.size, (s,s), result)

            match = 0
            sqs = int(s/1000.0 * 100)
            for i in range(5):
                x = random.randint(0,9)
                y = random.randint(0,9)
                xi = x * sqs + 13;
                yi = y * sqs + 13;
                box = (xi,yi,xi+(sqs-13),yi+(sqs-13))
                sqr = img.crop(box)
                ok = self.validationInfo.do_test_square(sqr, x, y, result)
                if ok:
                    match += 1
                else:
                    error = (x,y)      
            if match >= 3:           
                return result
            else:
                raise ValidatorError('color', 1,0,self) 
        except:
            self.validationInfo.check('status', result.last_status, 200)
            raise

    def test_size_region(self, result):
        """{"label":"Region at specified size","level":1,"category":3,"versions":["1.0","1.1","2.0"]}"""          
        try:
            # ask for a random region, at a random size < 100
            for i in range(5):
                s = random.randint(35,90)
                x = random.randint(0,9)
                y = random.randint(0,9)
                params = {'size': '%s,%s' % (s,s)}
                params['region'] = '%s,%s,100,100' % (x*100, y*100)
                img = result.get_image(params)
                if img.size != (s,s):
                    raise ValidatorError('size', img.size, (s,s))        
                ok = self.validationInfo.do_test_square(img,x,y, result)
                if not ok:
                    raise ValidatorError('color', 1, self.validationInfo.colorInfo[0][0], self)            
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise
    
    def test_rot_error_random(self, result):
        """{"label":"Random rotation gives 400","level":1,"category":4,"versions":["1.0","1.1","2.0"]}"""          
        try:
            url = result.make_url({'rotation': self.validationInfo.make_randomstring(4)})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 400, result)
            return result
        except:
            raise
    
    def test_rot_full_basic(self, result):
        """{"label":"Rotation by 90 degree values","level":1,"category":4,"versions":["1.0","1.1","2.0"]}"""          
        try:
            params = {'rotation': '180'}
            img = result.get_image(params)
            s = 1000
            if not img.size[0] in [s-1, s, s+1]:
                raise ValidatorError('size', img.size, (s,s))  
            # Test 0,0 vs 9,9
            box = (12,12,76,76)
            sqr = img.crop(box)
            ok = self.validationInfo.do_test_square(sqr, 9, 9, result)
            if not ok:
                raise ValidatorError('color', 1, self.validationInfo.colorInfo[9][9], self)
            box = (912,912,976,976)
            sqr = img.crop(box)
            ok = self.validationInfo.do_test_square(sqr, 0, 0, result)
            if not ok:
                raise ValidatorError('color', 1, self.validationInfo.colorInfo[0][0], self)             
            return result             
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise  

    def test_rot_full_non90(self, result):
        """{"label":"Rotation by non 90 degree values","level":1,"category":4,"versions":["1.0","1.1","2.0"]}"""          
        try:
            r = random.randint(1,359)
            params = {'rotation': '%s' % r}
            img = result.get_image(params)
            # not sure how to test, other than we got an image       
            return result            
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 

    
    def test_rot_region_basic(self, result):
        """{"label":"Rotation of region by 90 degree values","level":1,"category":4,"versions":["1.0","1.1","2.0"]}"""          
        try:
            s = 76
            # ask for a random region, at a random size < 100
            for i in range(4):
                x = random.randint(0,9)
                y = random.randint(0,9)
                # XXX should do non 180
                params = {'rotation': '180'}
                params['region'] = '%s,%s,%s,%s' % (x*100+13, y*100+13,s,s)
                img = result.get_image(params)
                if not img.size[0] in [s-1, s, s+1]:   # allow some leeway for rotation
                    raise ValidatorError('size', img.size, (s,s))        
                ok = self.validationInfo.do_test_square(img,x,y, result)
                if not ok:
                    raise ValidatorError('color', 1, self.validationInfo.colorInfo[0][0], self)            
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise
    
    def test_rot_region_non90(self, result):
        """{"label":"Rotation by non 90 degree values","level":1,"category":4,"versions":["1.0","1.1","2.0"]}"""          
        try:
            # ask for a random region, at a random size < 100
            for i in range(4):
                r = random.randint(1,359)
                x = random.randint(0,9)
                y = random.randint(0,9)
                params = {'rotation': '%s'%r}
                params['region'] = '%s,%s,100,100' % (x*100, y*100)
                img = result.get_image(params)
                # not sure how to test
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise

    
    def test_quality_error_random(self, result):
        """{"label":"Random quality gives 400","level":1,"category":5,"versions":["1.0","1.1","2.0"]}"""          
        try:
            url = result.make_url({'quality': self.validationInfo.make_randomstring(6)})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, 400, result)
            return result 
        except:
            raise
    
    def test_quality_color(self, result):
        """{"label":"Color quality","level":1,"category":5,"versions":["1.0","1.1","2.0"]}"""           
        try:
            params = {'quality': 'color'}
            img = result.get_image(params)
            self.validationInfo.check('quality', img.mode, 'RGB', result)
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise

    def test_quality_grey(self, result):
        """{"label":"Gray/Grey quality","level":1,"category":5,"versions":["1.0","1.1","2.0"]}"""          
        try:
            params = {'quality': 'grey'}
            img = result.get_image(params)
            # self.validationInfo.check('quality', img.mode, 'L', result)

            cols = img.getcolors()
            if img.mode == 1:
                return self.validationInfo.check('quality', 1,0, result)
            elif img.mode == 'L':
                return self.validationInfo.check('quality', 1, 1, result)
            else:
                # check vast majority of px are triples with v similar r,g,b
                ttl = 0
                for c in cols:
                    if (abs(c[1][0] - c[1][1]) < 5 and abs(c[1][1] - c[1][2]) < 5):
                        ttl += c[0]
                if ttl > 650000:
                    return self.validationInfo.check('quality', 1,1, result)
                else:
                    return self.validationInfo.check('quality', 1,0, result)

            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise    

    def test_quality_bitonal(self, result):
        """{"label":"Bitonal quality","level":1,"category":5,"versions":["1.0","1.1","2.0"]}"""          
        try:
            params = {'quality': 'bitonal', 'format':'png'}
            img = result.get_image(params)

            cols = img.getcolors()
            # cols should be [(x, 0), (y,255)] or [(x,(0,0,0)), (y,(255,255,255))]
            if img.mode == '1' or img.mode == 'L':
                return self.validationInfo.check('quality', 1, 1, result)
            else:
                # check vast majority of px are 0,0,0 or 255,255,255
                okpx = sum([x[0] for x in cols if sum(x[1]) < 15 or sum(x[1]) > 750])
                if okpx > 650000:
                    return self.validationInfo.check('quality', 1,1, result)
                else:
                    return self.validationInfo.check('quality', 1,0, result)
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 
            
    def test_format_error_random(self, result):
        """{"label":"Random format gives 400","level":1,"category":6,"versions":["1.0","1.1","2.0"]}"""          
        try:
            url = result.make_url({'format': self.validationInfo.make_randomstring(3)})
            error = result.fetch(url)
            self.validationInfo.check('status', result.last_status, [400, 415, 503], result)
            return result
        except:
            raise

        
    def test_format_jpg(self, result):
        """{"label":"JPG format","level":1,"category":6,"versions":["1.0","1.1","2.0"]}"""            
        try:
            params = {'format': 'jpg'}
            img = result.get_image(params)
            self.validationInfo.check('quality', img.format, 'JPEG', result)
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 

    def test_format_png(self, result):
        """{"label":"PNG format","level":1,"category":6,"versions":["1.0","1.1","2.0"]}"""          
        try:
            params = {'format': 'png'}
            img = result.get_image(params)
            self.validationInfo.check('quality', img.format, 'PNG', result)
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 
    
    def test_format_gif(self, result):
        """{"label":"GIF format","level":1,"category":6,"versions":["1.0","1.1","2.0"]}"""          
        try:
            params = {'format': 'gif'}
            img = result.get_image(params)
            self.validationInfo.check('quality', img.format, 'GIF', result)
            return result
        except:
            self.validationInfo.check('status', result.last_status, 200, result)
            raise 

    def test_format_conneg(self, result):
        """{"label":"Negotiated format","level":1,"category":6,"versions":["1.0","1.1"]}"""          
        url = result.make_url()
        hdrs = {'Accept': 'image/png;q=1.0'}
        try:
            r = urllib2.Request(url, headers=hdrs)
            wh = urllib2.urlopen(r)
            img = wh.read()   
            wh.close()
        except urllib2.HTTPError, e:
            wh = e
        ct = wh.headers['content-type']
        result.last_url = url
        result.last_headers = wh.headers.dict
        result.last_status = wh.code
        result.urls.append(url)
        self.validationInfo.check('format', ct, 'image/png', result)
        return result
        
    def test_linkheader(self, result):
        """{"label":"Profile Link Header","level":1,"category":6,"versions":["1.0","1.1","2.0"]}"""          
        url = result.make_url()
        data = result.fetch(url)
        try:
            lh = result.last_headers['link']
        except KeyError:
            raise ValidatorError('profile', '', 'URI')
        links = result.parse_links(lh)
        profile = result.get_uri_for_rel(links, 'profile')
        if not profile:
            raise ValidatorError('profile', '', 'URI', self)
        elif not profile.startswith('http://library.stanford.edu/iiif/image-api/compliance.html'):
            raise ValidatorError('profile', profile, 'URI', self)
        else:
            result.tests.append('linkheader')
            return result



class ImageAPI(object):
    def __init__(self, identifier, server, prefix=None, scheme="http", auth="", version="2.0"):

        self.template = "{/prefix*}/{identifier}/{region}/{size}/{rotation}/{quality}{.format}"
        self.infoTemplate = "{/prefix*}/{identifier}/info.json"        
        self.iiifNS = "{http://library.stanford.edu/iiif/image-api/ns/}"

        self.scheme = scheme
        self.server = server
        if not prefix:
            self.prefix = ""
        else:
            self.prefix = prefix.split('/')
        self.identifier = identifier
        self.auth = auth

        self.version = version

        self.last_headers = {}
        self.last_status = 0
        self.last_url = ''

        # DOUBLE duty as result object
        self.name = ""
        self.urls = []
        self.tests = []
        self.exception = None

    def parse_links(self, header):

        state = 'start'
        header = header.strip()
        data = [d for d in header]
        links = {}
        while data:
            if state == 'start':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                if d != "<":
                    raise ValueError("Parsing Link Header: Expected < in start, got %s" % d)                    
                state = "uri"
            elif state == "uri":
                uri = []
                d = data.pop(0)                
                while d != ";":
                    uri.append(d)
                    d = data.pop(0)
                uri = ''.join(uri)
                uri = uri[:-1]
                data.insert(0, ';')
                # Not an error to have the same URI multiple times (I think!)
                if not links.has_key(uri):
                    links[uri] = {}
                state = "paramstart"
            elif state == 'paramstart':
                d = data.pop(0)
                while data and d.isspace():
                    d = data.pop(0)
                if d == ";":
                    state = 'linkparam';
                elif d == ',':
                    state = 'start'
                else:
                    raise ValueError("Parsing Link Header: Expected ; in paramstart, got %s" % d)
                    return
            elif state == 'linkparam':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                paramType = []
                while not d.isspace() and d != "=":
                    paramType.append(d)
                    d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                if d != "=":
                    raise ValueError("Parsing Link Header: Expected = in linkparam, got %s" % d)
                    return
                state='linkvalue'
                pt = ''.join(paramType)
                if not links[uri].has_key(pt):
                    links[uri][pt] = []
            elif state == 'linkvalue':
                d = data.pop(0)
                while d.isspace():
                    d = data.pop(0)
                paramValue = []
                if d == '"':
                    pd = d
                    d = data.pop(0)
                    while d != '"' and pd != '\\':
                        paramValue.append(d)
                        pd = d
                        d = data.pop(0)
                else:
                    while not d.isspace() and not d in (',', ';'):
                        paramValue.append(d)
                        if data:
                            d = data.pop(0)
                        else:
                            break
                    if data:
                        data.insert(0, d)
                state = 'paramstart'
                pv = ''.join(paramValue)
                if pt == 'rel':
                    # rel types are case insensitive and space separated
                    links[uri][pt].extend([y.lower() for y in pv.split(' ')])
                else:
                    if not pv in links[uri][pt]:
                        links[uri][pt].append(pv)
        return links


    def get_uri_for_rel(self, links, rel):
        rel = rel.lower()
        for (uri, info) in links.items():
            rels = info.get('rel', [])
            if rel in rels:
                return uri
        return None

    def fetch(self, url):
        # print url
        sys.stderr.write('url: %s\n' % url)
        sys.stderr.flush()
        try:
            wh = urllib2.urlopen(url)
        except urllib2.HTTPError, wh:
            pass                   
        data = wh.read()
        # nasty side effect
        self.last_headers = wh.headers.dict
        self.last_status = wh.code
        self.last_url = url
        wh.close()
        self.urls.append(url)
        return(data)

    def make_url(self, params={}):
        if self.prefix and not params.has_key('prefix'):
            params['prefix'] = self.prefix
        if not params.has_key('identifier'):
            params['identifier'] = self.identifier
        if not params.has_key('region'):
            params['region'] = 'full'
        if not params.has_key('size'):
            params['size'] = 'full'
        if not params.has_key('rotation'):
            params['rotation'] = '0'
        if not params.has_key('quality'):
            if self.version == "2.0":
                params['quality'] = 'default'
            else:
                params['quality'] = 'native'        
        elif params['quality'] == 'grey' and self.version == "2.0":
            # en-us in 2.0+
            params['quality'] = 'gray'
        if not params.has_key('format') and self.version == "2.0":
            # format is required in 2.0+
            params['format'] = 'jpg'

        url = expand(self.template, params)
        scheme = params.get('scheme', self.scheme)
        server = params.get('server', self.server)
        url = "%s://%s%s" % (scheme, server, url)
        return url

    def make_image(self, data):
        imgio = StringIO.StringIO(data)
        img = Image.open(imgio)
        return img

    def get_image(self, params):
        url = self.make_url(params)
        imgdata = self.fetch(url)
        img = self.make_image(imgdata)
        return img

    def get_info(self):
        params = {'server':self.server, 'identifier':self.identifier, 'scheme':self.scheme}
        if self.prefix:
            params['prefix'] = self.prefix
        url = expand(self.infoTemplate, params)
        scheme = params.get('scheme', self.scheme)
        server = params.get('server', self.server)
        url = "%s://%s%s" % (scheme, server, url)
        self.urls.append(url)

        try:
            idata = self.fetch(url) 
        except:
            # uhoh
            return {}
        try:
            info = json.loads(idata)
        except:
            return {}
        return info


class Validator(object):

    def handle_test(self, testname):

        version = request.query.get('version', '2.0')

        info = ValidationInfo()
        testSuite = TestSuite(info)

        if testname == "list_tests":
            tests = testSuite.list_tests(version)
            return json.dumps(tests)
        if not testSuite.has_test(testname):
            return "No such test: %s" % testname

        server = request.query.get('server', '')
        server = server.strip();
        if server.startswith('https://'):
            scheme = 'https'
            server = server.replace('https://', '')
        else:
            scheme="http"
            server = server.replace('http://', '')  
        atidx = server.find('@') 
        if atidx > -1:
            auth = server[:atidx]
            server = server[atidx+1:]
        else:
            auth = ""
        if not server:
            return "Missing mandatory parameter: server"

        if server[-1] == '/':
            server = server[:-1]

        prefix = request.query.get('prefix', '')
        prefix = prefix.strip()
        if prefix:
            prefix = prefix.replace('%2F', '/')
            if prefix[-1] == '/':
                prefix = prefix[:-1]
            if prefix[0] == '/':
                prefix = prefix[1:]

        identifier = request.query.get('identifier', '')
        identifier = identifier.strip()
        if not identifier:
            return "Missing mandatory parameter: identifier"

        try:
            result = ImageAPI(identifier, server, prefix, scheme, auth, version)

            testSuite.run_test(testname, result)
            if result.exception:
                e = result.exception
                info = {'test' : testname, 'status': 'error', 'url':result.urls, 'got':e.got, 'expected': e.expected, 'type': e.type}
            else:
                info = {'test' : testname, 'status': 'success', 'url':result.urls, 'tests':result.tests}
        except Exception, e:
            raise
            info = {'test' : testname, 'status': 'internal-error', 'url':e.url, 'msg':str(e)}
        infojson = json.dumps(info)
        return infojson
  
    def dispatch_views(self):
        pfx = ""
        self.app.route("/%s<testname>" % pfx, "GET", self.handle_test)

    def after_request(self):
        """A bottle hook for json responses."""
        response["content_type"] = "application/json"
        methods = 'GET'
        headers = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        # Already added by apache config
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = methods
        response.headers['Access-Control-Allow-Headers'] = headers
        response.headers['Allow'] = methods


    def not_implemented(self, *args, **kwargs):
        """Returns not implemented status."""
        abort(501)

    def empty_response(self, *args, **kwargs):
        """Empty response"""

    options_list = empty_response
    options_detail = empty_response


    def error(self, error, message=None):
        """Returns the error response."""
        return self._jsonify({"error": error.status_code,
                        "message": error.body or message}, "")

    def get_error_handler(self):
        """Customized errors"""
        return {
            500: partial(self.error, message="Internal Server Error."),
            404: partial(self.error, message="Document Not Found."),
            501: partial(self.error, message="Not Implemented."),
            405: partial(self.error, message="Method Not Allowed."),
            403: partial(self.error, message="Forbidden."),
            400: self.error
        }

    def get_bottle_app(self):
        """Returns bottle instance"""
        self.app = Bottle()
        self.dispatch_views()
        self.app.hook('after_request')(self.after_request)
        self.app.error_handler = self.get_error_handler()
        return self.app


def apache():
    v = Validator();
    return v.get_bottle_app()

def main():
    mr = Validator()
    run(host='localhost', port=8080, app=mr.get_bottle_app())


if __name__ == "__main__":
    main()
else:
    application = apache()
