import re,types,Render,Settings,Database,Groups

class Pages():
	def __init__(self):
		self._Render  = self.OpenPage
		self._CSS     = self.RenderCSS
		self._JS      = self.RenderJS
		self.pageKeys = {
			"index":                "index",
			"userblock_guest":      "userblock_guest",
			"userblock_user":       "userblock_user",
			"cat_display":          "cat_display",
			"cat_display_forum":    "cat_display_forum",
			"user_login_page":      "user_login_page",
			"user_register_page":   "user_register_page",
			"user_profile":         "user_profile",
			"user_profile_content": "user_profile_content",
			}
		
	def OpenPage(self, name=None):
		return str(open(Settings.BASEDIR+"/templates/%s.html"%( self.pageKeys[ name ] )).read())

	def RenderCSS(self, request, fname):
		return Render.Render()._Page(content=str(open(Settings.BASEDIR+"/templates/styles/%s.css"%(fname)).read()), setCookies=None, setContentType="text/css")
		
	def RenderJS(self, request, fname):
		return Render.Render()._Page(content=str(open(Settings.BASEDIR+"/templates/js/%s.js"%(fname)).read()), setCookies=None, setContentType="text/javascript")

	def _FullRender(self, content=None, condit=None, extra=None):
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
				"forumurl": Settings.FORUMURL,
				"userprofile": None
			}
			
			if(userblock == "userblock_user")and(sid != None):
				tags["userblock"] = self._RenderUserblock(sid=sid)
			if(not isinstance(extra, types.NoneType)):
				if extra["GET"] == "userprofile":
					tags["userprofile"] = self._RenderProfile(uid=extra["requesteduser"], content=self._Render(name="user_profile_content"))
			
			c = re.findall("\{\[(.*?)\]\}", str(content))
			for x in c:
				try:
					content = content.replace("{[%s]}"%(x), tags[str(x)])
				except:
					pass
			return content
			
	def _RenderUserblock(self, sid=None):
		if sid != "":
			if not isinstance(sid, types.NoneType):
				ub = self._Render(name="userblock_user")
				us = Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE uid=?", variables=(Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE sessionid=?", variables=(sid,), commit=False, doReturn=True)[0][0],), commit=False, doReturn=True)[0]
				return ub.replace("{[uid]}", str(us[0])).replace("{[username]}", us[1])
		else:
			return self._Render(name="userblock_guest")
			
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
				)).replace(
				"{[forumid]}", str(x[0])
				)
			return render

	def _RenderProfile(self, uid=None, content=None):
		if(not isinstance(content, types.NoneType)) and not isinstance(uid, types.NoneType):
			c = Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE uid=?", variables=(uid,), commit=False, doReturn=True)
			u = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE uid=?", variables=(uid,), commit=False, doReturn=True)
			if len(c) > 0:
				content = content.replace("{[username]}", c[0][1]).replace("{[uid]}", str(c[0][0])).replace("{[avatarimg]}", "<img src=\"%s\">"%(u[0][2])).replace("{[usertitle]}", u[0][3]).replace("{[usergroup]}", Groups.Groups[u[0][4]]["Name"])
			else:
				content = "<div id=\"error\">Invalid user.</div>"
		return content
