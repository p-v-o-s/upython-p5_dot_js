################################################################################
# STANDARD LIB IMPORTS
import sys, os, time, gc

try:
    import sys
    from sys import print_exception #micropython specific
except ImportError:
    import traceback
    print_exception = lambda exc, file_: traceback.print_exc(file=file_)

try:
    from time import monotonic as time_monotonic
except ImportError:
    time_monotonic = lambda: time.ticks_us()/1e6

try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict #micropython specific
    
try:
    import json
except ImportError:
    import ujson as json #micropython specific

#-------------------------------------------------------------------------------
# PAWPAW PACKAGE IMPORTS
from pawpaw import WebApp, Router, route, Template, LazyTemplate, AutoTreeFormat
from pawpaw import auto_tree_format
#-------------------------------------------------------------------------------
# LOCAL IMPORTS


################################################################################
# PLATFORM SPECIFIC SETUP
#-------------------------------------------------------------------------------

import platform_setup
SERVER_ADDR = platform_setup.SERVER_ADDR
SERVER_PORT = platform_setup.SERVER_PORT
DEBUG       = platform_setup.DEBUG
DEFAULT_LOOP_PY_TIMEOUT_MS = 5000

if DEBUG:
    print("INSIDE MODULE name='%s' " % ('p5js_app',))
    try:
        from micropython import mem_info #micropython specific
        mem_info()
    except ImportError:
        pass
################################################################################
# HARDWARE INTERFACES
#-------------------------------------------------------------------------------
PINS = OrderedDict()
try:
    import machine #micropython specific
except ImportError:
    import mock_machine as machine #a substitute for PC testing
        
pin_numbers = (0, 2, 4, 5, 12, 13, 14, 15)
PINS = OrderedDict((i,machine.Pin(i, machine.Pin.IN)) for i in pin_numbers)
    
#configure humidity/temperature sensor interface
try:
    from am2315 import AM2315
except ImportError:
    from mock_am2315 import AM2315
    
try:
    from micropython import mem_info
except ImportError:
    mem_info = lambda: None
    
ht_sensor = AM2315()
ht_sensor.init()


################################################################################
# APPLICATION CODE
#-------------------------------------------------------------------------------
@Router
class P5jsServer(WebApp):
    @route("/", methods=['GET'])
    def index(self, context):
        context.send_file("html/index.html")
        
    @route("/p5.min.js", methods=['GET'])
    def p5minjs(self, context):
        context.send_file("html/p5.min.js")
        
    @route("/example", methods=['GET'])
    def example(self, context):
        context.send_file("html/example/index.html")
        
    @route("/example/sketch.js", methods=['GET'])
    def example_sketch(self, context):
        if DEBUG:
            print("INSIDE ROUTE HANDLER 'example_sketch'")
        context.send_file("html/example/sketch.js")
        
#    @route("/test", methods=['GET'])
#    def test(self, context):
#        context.send_file("html/test.html")
        
    @route("/logs/P5jsServer.yaml", methods=['GET','DELETE'])
    def logs(self, context):
        if context.request.method == 'GET':
            context.send_file("logs/PolyServer.yaml")
        elif context.request.method == 'DELETE':
            os.remove("logs/P5jsServer.yaml")
            open("logs/P5js.yaml",'w').close()
            context.send_json({})
        
    @route("/am2315", methods=['GET'])
    def am2315(self, context):
        d = {}
        #acquire a humidity and temperature sample
        ht_sensor.get_data(d)  #adds fields 'humid', 'temp'
        context.send_json(d)
    
#    def __init__(self, *args,**kwargs):
#        super().__init__(*args, **kwargs)  #IMPORTANT call parent constructor
#        self._loop_timer = machine.Timer(0)
        
        
################################################################################
# MAIN
#-------------------------------------------------------------------------------
#if __name__ == "__main__":
#---------------------------------------------------------------------------
# Create application instance binding to localhost on port 9999
time.sleep(2.0)
gc.collect()

app = P5jsServer(server_addr = SERVER_ADDR,
                 server_port = SERVER_PORT,
                 socket_timeout = 1.0,
               )
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
app.serve_forever()
