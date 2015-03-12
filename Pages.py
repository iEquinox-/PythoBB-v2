import re,types,Render,Settings,Database,Groups,Misc

class Pages():
	def __init__(self):
		self._Render  = self.OpenPage
		self._CSS     = self.RenderCSS
		self._JS      = self.RenderJS
		self.pageKeys = {
			"index":                  "index",
			"userblock_guest":        "userblock_guest",
			"userblock_user":         "userblock_user",
			"cat_display":            "cat_display",
			"cat_display_forum":      "cat_display_forum",
			"user_login_page":        "user_login_page",
			"user_register_page":     "user_register_page",
			"user_profile":           "user_profile",
			"user_profile_content":   "user_profile_content",
			"user_controlpanel":      "user_controlpanel",
			"searchbox":              "searchbox",
			"search_results":         "search_results",
			"forum_display":          "forum_display",
			"forum_display_forum":    "forum_display_forum",
			"thread_display":         "thread_display",
			"post_display":           "thread_display_post",
			"thread_display_newpost": "thread_display_newpost",
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
				"userblock": self._Render(name=userblock).replace("{[searchbox]}", self._Render(name="searchbox")),
				"categories": self._RenderForums(),
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
				uid = Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE sessionid=?", variables=(sid,), commit=False, doReturn=True)[0][0]
				us = Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE uid=?", variables=(uid,), commit=False, doReturn=True)[0]
				return ub.replace("{[uid]}", str(us[0])).replace("{[username]}", us[1]).replace("{[searchbox]}", self._Render(name="searchbox"))
		else:
			return self._Render(name="userblock_guest").replace("{[searchbox]}", self._Render(name="searchbox"))
			
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

	def _RenderUserCP(self, content=None, condit=None):
		uid = Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE sessionid=?", variables=(condit["sid_"],), commit=False, doReturn=True)[0][0]
		udt = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE uid=?", variables=(uid,), commit=False, doReturn=True)
		return self._FullRender(
			content=content.replace(
				"{[usercp_useravatar]}", "<img src=\"%s\" class=\"userimg\" style=\"float:left;margin-top: 10px;margin-right: 5px;margin-left:5px;\">"%(udt[0][2])
				),
			condit=condit)

	def _RenderSearchResults(self, content=None, results=None, condit=None):
		page = self._FullRender(content=content, condit=condit)
		page = page.replace(
			"{[results->threads]}", Misc.Sort().Array(array=results["threads"], type="searchresult", syn="threads")
			).replace(
			"{[results->tags]}", Misc.Sort().Array(array=results["tags"], type="searchresult", syn="tags", extr={"tag":results["query"]})
			).replace(
			"{[results->posts]}", Misc.Sort().Array(array=results["posts"], type="searchresult", syn="posts")
			).replace(
			"{[results->users]}", Misc.Sort().Array(array=results["members"], type="searchresult", syn="users")
			)
		return Render.Render()._Page(content=page, setCookies=None)

	def _RenderForum(self, content=None, condit=None, fid=None):
		page = self._FullRender(content=content, condit=condit)
		_for = Database.Database().Execute(query="SELECT * FROM pythobb_forums WHERE fid=?", variables=(fid,), commit=False, doReturn=True)[0]
		page = page.replace("{[forums]}", self._RenderForumThreads(content=self._Render(name="forum_display_forum"), fid=fid)).replace(
			"{[forumname]}", _for[2]
			).replace(
			"{[forumdesc]}", _for[3]
			).replace("{[fid]}", str(fid)).replace("{[forumurl]}", Settings.FORUMURL)
		return Render.Render()._Page(content=page, setCookies=None)

	def _RenderForumThreads(self, content=None, fid=None):
		repl = ""
		threads = Database.Database().Execute(query="SELECT * FROM pythobb_threads WHERE parent=?", variables=(fid,), commit=False, doReturn=True)
		if len(threads) == 0:
			repl += "<div class=\"forum-body\">There are no threads in this forum.</div>"
		else:
			for c in threads:
				repl += "<div class=\"forum-body\"><a href=\"%s/thread/%s/\">%s</a> <span>%s replies</span></div>" % (Settings.FORUMURL, c[0], c[2], str(len(Database.Database().Execute(query="SELECT * FROM pythobb_posts WHERE parent=?", variables=(c[0],), commit=False, doReturn=True))))
		return content.replace("{[forum_threads]}", repl)

	def _RenderThread(self, content=None, condit=None, tid=None):
		def getThreadName(tid=0):
			return Database.Database().Execute(query="SELECT * FROM pythobb_threads WHERE tid=?", variables=(tid,), commit=False, doReturn=True)[0][2]
		page = self._FullRender(content=content, condit=condit)
		if condit["user"] == True:
			newpost    = """<a href="javascript:;" class="makenewpost">New Post</a>"""
			newpostbox = self._Render(name="thread_display_newpost")
		else:
			newpost    = ""
			newpostbox = ""
		page = page.replace("{[newpost->newpost]}", newpostbox)
		page = page.replace("{[threadname]}", getThreadName(tid=tid)).replace("{[newpost]}", newpost).replace("{[tid]}", str(tid))
		return Render.Render()._Page(content=page.replace("{[posts]}", self._RenderPosts(tid=tid, loggedin=condit["user"])), setCookies=None)
		
	def _RenderPosts(self, tid=0, loggedin=False):
		parent_Post = Database.Database().Execute(query="SELECT * FROM pythobb_threads WHERE tid=?", variables=(tid,), commit=False, doReturn=True)[0]
		pPost = {"post": parent_Post[4], "poster": parent_Post[5].split(":")[0]}
		posts       = Database.Database().Execute(query="SELECT * FROM pythobb_posts WHERE parent=?", variables=(tid,), commit=False, doReturn=True)
		post_String = ""
		pid         = parent_Post[5].split(":")[2]
		getAvatar   = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE uid=?", variables=(Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE username=?", variables=(pPost["poster"],), commit=False, doReturn=True)[0][0],), commit=False, doReturn=True)[0][2]
		if getAvatar != "":
			getAvatar = "<br/><img src=\"" + getAvatar + "\" class=\"userimg\" style=\"height:75px;width:75px;margin-top:10px;\">"
		post_String += self._Render(name="post_display").replace(
			"{[username]}", pPost["poster"]
		).replace(
			"{[content]}", pPost["post"]
		).replace(
			"{[postoptions]}", self._PostOpt(pid=pid, loggedin=loggedin)
		).replace(
			"{[useravatar]}", getAvatar
		)
		def getUser(uid=None):
			return str(Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE uid=?", variables=(uid,), commit=False, doReturn=True)[0][1])
		for c in posts:
			avatar = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE uid=?", variables=(c[3],), commit=False, doReturn=True)[0][2]
			if avatar != "":
				avatar = "<br/><img src=\"" + avatar + "\" class=\"userimg\" style=\"height:75px;width:75px;margin-top:10px;\">"
			post_String += self._Render(name="post_display").replace(
				"{[username]}", getUser(uid=c[3])
			).replace(
				"{[content]}", Misc.PBBCode()._Parse(content=c[2])
			).replace(
				"{[postoptions]}", self._PostOpt(pid=c[0], loggedin=loggedin)
			).replace(
				"{[useravatar]}", avatar
			)
			
		return post_String
		
	def _PostOpt(self, pid, loggedin=False):
		if(loggedin == True):
			links = {"Quote": ["javascript:;"], "Like":["javascript:;","counter-p1","<div class=\"counter-p2\">%s</div>"]}; link  = ""
			def getLikes(pid=0):
				num = Database.Database().Execute(query="SELECT likes FROM pythobb_thread_misc WHERE pid=?", variables=(pid,), commit=False, doReturn=True)[0]
				print num
				return num[0]
			for c in links:
				if c == "Like":
					extra = [links["Like"][1], links["Like"][2]%(str(getLikes(pid=pid)))]
				else:
					extra = ["",""]
				link += "<a href=\"{0}\" id=\"pid-{2}\" class=\"{1} {3}\">{1}</a>{4}".format(links[c][0], c, str(pid), extra[0], extra[1])
			return link
		else:
			return ""
