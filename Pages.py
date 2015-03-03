import os,Render

class Pages():
	def __init__(self):
		self._Render = self.OpenPage
		self._CSS    = self.RenderCSS
		self.pageKeys = {
			"index": "index",
			"userblock_guest": "",
			"userblock_user": ""
			}
		
	def OpenPage(self, name=None):
		return str(open(os.path.dirname(os.path.abspath(__file__))+"/templates/%s.ptmp"%(name)).read())

	def RenderCSS(self, request, fname):
		return Render.Render()._Page(content=str(open(os.path.dirname(os.path.abspath(__file__))+"/templates/styles/%s.css"%(fname)).read()), setCookies=None, setContentType="text/css")
