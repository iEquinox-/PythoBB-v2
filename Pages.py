import os,re,types,Render

class Pages():
	def __init__(self):
		self._Render = self.OpenPage
		self._CSS    = self.RenderCSS
		self.pageKeys = {
			"index": "index",
			"userblock_guest": "userblock_guest",
			"userblock_user": "userblock_user"
			}
		
	def OpenPage(self, name=None):
		return str(open(os.path.dirname(os.path.abspath(__file__))+"/templates/%s.ptmp"%(name)).read())

	def RenderCSS(self, request, fname):
		return Render.Render()._Page(content=str(open(os.path.dirname(os.path.abspath(__file__))+"/templates/styles/%s.css"%(fname)).read()), setCookies=None, setContentType="text/css")

	def _FullRender(self, content=None, condit=None):
		userblock,sid = "",None
		if not isinstance(content, types.NoneType):
			if not isinstance(condit, types.NoneType):
				if condit["user"] == False:
					userblock = "userblock_guest"
				else:
					userblock,sid = "userblock_user",condit["sid_"]
			tags = {
				"forumname": "test forum",
				"userblock": self._Render(name=userblock),
				"forums": "test"
			}
			c = re.findall("\{\[(.*?)\]\}", str(content))
			for x in c:
				try:
					content = content.replace("{[%s]}"%(x), tags[str(x)])
				except:
					pass
			return content
