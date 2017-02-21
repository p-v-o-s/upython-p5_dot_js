import time
try:
    from collections import OrderedDict
except ImportError: 
    from ucollections import OrderedDict #micrpython specific

#-------------------------------------------------------------------------------
# PAWPAW PACKAGE IMPORTS
from pawpaw import WebApp, Router, route, Template


DEBUG = True
################################################################################

html = """
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
  Page {{page_name}}
  </body>
</html>
"""

page_tmp = Template(html)

################################################################################
# TEST  CODE
################################################################################
@Router
class App1(WebApp):
    @route("/11", methods = ['GET', 'PUT'])
    def myhandler11(self,context):
        print("INSIDE App.myhandler")
        page_tmp.format(page_name="11")
        context.render_template(page_tmp)
        
    @route("/12")
    def myhandler12(self,context):
        print("INSIDE App.myhandler2")
        page_tmp.format(page_name="12")
        context.render_template(page_tmp)
        
    @route(regex = r"[/](\d+)")
    def myhandler_regex(self,context):
        print("INSIDE App.myhandler2")
        num = context.request.match.group(1)
        page_tmp.format(page_name=num)
        context.render_template(page_tmp)
        
@Router
class App2(WebApp):
    @route("/21", methods = ['GET', 'PUT'])
    def myhandler21(self,context):
        print("INSIDE App.myhandler")
    @route("/22")
    def myhandler22(self,context):
        print("INSIDE App.myhandler2")
        
        
app1 = App1(server_addr = "0.0.0.0", server_port = 8080)

app2 = App2(server_addr = "0.0.0.0", server_port = 8081)

app1.serve_forever()

