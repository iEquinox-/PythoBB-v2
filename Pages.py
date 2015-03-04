import os,re,types,Render,Settings,Database

class Pages():
	def __init__(self):
		self._Render  = self.OpenPage
		self._CSS     = self.RenderCSS
		self._JS      = self.RenderJS
		self.pageKeys = {
			"index":             "index",
			"userblock_guest":   "userblock_guest",
			"userblock_user":    "userblock_user",
			"cat_display":       "cat_display",
			"cat_display_forum": "cat_display_forum"
			}
		
	def OpenPage(self, name=None):
		return str(open(Settings.BASEDIR+"/templates/%s.ptmp"%(self.pageKeys[name])).read())

	def RenderCSS(self, request, fname):
		return Render.Render()._Page(content=str(open(Settings.BASEDIR+"/templates/styles/%s.css"%(fname)).read()), setCookies=None, setContentType="text/css")
		
	def RenderJS(self, request, fname):
		return Render.Render()._Page(content=str(open(Settings.BASEDIR+"/templates/js/%s.js"%(fname)).read()), setCookies=None, setContentType="text/javascript")

	def _FullRender(self, content=None, condit=None):
		userblock,sid = "",None
		if not isinstance(content, types.NoneType):
			if not isinstance(condit, types.NoneType):
				if condit["user"] == False:
					userblock = "userblock_guest"
				else:
					userblock,sid = "userblock_user",condit["sid_"]
			tags = {
				"forumname": Settings.FORUMNAME,
				"userblock": self._Render(name=userblock),
				"forums": self._RenderForums(),
				"forumurl": Settings.FORUMURL
			}
			c = re.findall("\{\[(.*?)\]\}", str(content))
			for x in c:
				try:
					content = content.replace("{[%s]}"%(x), tags[str(x)])
				except:
					pass
			return content
			
	def _RenderForums(self):
		render = ""
		que  = Database.Database().Execute(query="SELECT * FROM pythobb_categories", variables=(), commit=False, doReturn=True)
		template = self.OpenPage(name="cat_display")
		for x in que:
			render += (template.replace(
				"{[catname]}", x[1]
				).replace(
				"{[catdesc]}", x[2]
				).replace(
				"{[catforums]}", self._RenderCategory(cid=x[0])
				).replace(
				"{[catid]}", str(x[0])
				))
			if len(que) > 1:
				render += "<br/>"
		return render
		
	def _RenderCategory(self, cid=None):
		if(isinstance(cid, types.IntType))and(cid > 0):
			render = ""
			forums = Database.Database().Execute(query="SELECT * FROM pythobb_forums WHERE parent=?", variables=(1,), commit=False, doReturn=True)
			template = self.OpenPage(name="cat_display_forum")
			for x in forums:
				render += (template.replace(
				"{[forumname]}",x[2]
				).replace(
				"{[forumdesc]}",x[3]
				))
			return render
