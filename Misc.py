import Render,Database,Settings,Pages,IDs

class Search():
	def __init__(self):
		self.postquery = ["SELECT * FROM pythobb_posts WHERE content LIKE ?","posts"]
		self.tagsquery = ["SELECT * FROM pythobb_threads WHERE tags LIKE ?", "tags"]
		self.threquery = ["SELECT * FROM pythobb_threads WHERE name LIKE ?", "threads"]
		self.membquery = ["SELECT * FROM pythobb_users WHERE username LIKE ?", "members"]

	def Execute(self, query=None):
		JSON = dict()
		for c in [self.postquery, self.tagsquery, self.threquery, self.membquery]:
			x = Database.Database().Execute(query=c[0], variables=("%{0}%".format(query),), commit=False, doReturn=True)
			if c[1] == "members":
				JSON[c[1]] = [str("<a href=\"%s/member/profile/%s/\" class=\"prot\">%s</a>"%(Settings.FORUMURL,f[0],f[1])) for f in x]
			else:
				JSON[c[1]] = x
		return JSON

	def doSearch(self, request):
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				user_status,sid = False,None
		else:
			user_status,sid = False,None
		if request.POST["query"] != "":
			searchquery = request.POST["query"]
		else:
			return Render.Render()._Page(content="<script>location.href= \"%s\";</script>"%(Settings.FORUMURL), setCookies=None)
		return Pages.Pages()._RenderSearchResults(content=Pages.Pages()._Render(name="search_results"), results=self.Execute(query=searchquery), condit={"user":user_status, "sid_": sid})
		
class Sort():
	def __init__(self):
		self.string = ""
		
	def Array(self, array=[], type=None):
		for c in array:
			if type == "searchresult":
				self.string += "<div class=\"result\">"+c+"</div>"
		if len(array) == 0:
			if type == "searchresult":
				self.string += "<div class=\"result\">No results.</div>"
		return self.string
			
