import Security,Render,Pages,Database,Settings,IDs
from django.middleware.csrf import rotate_token as RotateCSRFToken

class Base:
	def Home(self, request):
		RotateCSRFToken(request)
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				user_status,sid = False,None
		else:
			user_status,sid = False,None
		return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name="index"),
				condit = {
					"user": user_status,
					"sid_": sid
					}
			), setCookies=None)

	def Login(self, request):
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
			else:
				return Render.Render()._Page(content=Pages.Pages()._FullRender(
					content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["user_login_page"]),
					condit = {
						"user": False,
						"sid_": None
						}
				), setCookies=None)
		else:
			return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["user_login_page"]),
				condit = {
					"user": False,
					"sid_": None
					}
			), setCookies=None)
			
	def Register(self, request):
		if request.COOKIES.has_key("sid"):
			if(request.COOKIES["sid"] != "")and(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
			else:
				return Render.Render()._Page(content=Pages.Pages()._FullRender(
					content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["user_register_page"]),
					condit = {"user":False, "sid_":None}), setCookies=None)
		else:
			return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["user_register_page"]),
				condit = {"user":False, "sid_":None}), setCookies=None)

	def ProcessLogin(self, request):
		_RequestedUser = {
			"Username": request.POST["Username"],
			"Password": request.POST["Password"]
		}
		_return   = Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE username=?", variables=(_RequestedUser["Username"],), commit=False, doReturn=True)
		uid,salt,password = _return[0][0],_return[0][2],_return[0][3]
		_UserData = Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE uid=?", variables=(uid,),commit=False,doReturn=True)
		if(Security.Security()._Hash(verify=True, string=(_RequestedUser["Password"]+salt), hash=password) == True):
			JSON = Render.Render()._Page(content=str(Render.Render()._JSON(variable="LoginAttempt", boolean=None, data=_UserData[0][1], complete=True)),
			setCookies=None, setContentType="application/json")
		else:
			JSON = Render.Render()._Page(content=str(Render.Render()._JSON(variable="LoginAttempt", boolean=False, data=None, complete=True)),
			setCookies=None, setContentType="application/json")
		return JSON
		
	def ProcessRegister(self, request):
		# http://stackoverflow.com/a/4581997
		def getIP():
			meta_xfor = request.META.get('HTTP_X_FORWARDED_FOR')
			if meta_xfor: ip = meta_xfor.split(',')[0]
			else: ip = request.META.get('REMOTE_ADDR')
			return ip
		IPADDR = getIP()
		_RequestedData = {
			"Username": Security.Security()._Parse(content=request.POST["Username"]),
			"Password": request.POST["Password"],
			"Email": request.POST["Email"]
		}
		_returnUserdata  = Database.Database().Execute(query="SELECT * FROM pythobb_users WHERE username=?", variables=(_RequestedData["Username"],) , commit=False, doReturn=True)
		_returnEmaildata = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE email=?", variables=(_RequestedData["Email"],) , commit=False, doReturn=True)
		if( len(_returnUserdata) > 0 ):
			returnVars = None
			returnString = "Username is already taken."
			return Render.Render()._Page(content=str(Render.Render()._JSON(variable="RegisterAttempt", boolean=None, data={"message":returnString, "register":False, "sid":None}, complete=True)),
			setCookies=None, setContentType="application/json")
		elif( len(_returnEmaildata) > 0 ):
			returnVars = None
			returnString = "Email is already in use."
			return Render.Render()._Page(content=str(Render.Render()._JSON(variable="RegisterAttempt", boolean=None, data={"message":returnString, "register":False, "sid":None}, complete=True)),
			setCookies=None, setContentType="application/json")
		else:
			uid,saltGen,Token = IDs.Values()._UID,Security.Security()._Salt,Security.Security()._TID
			try:
				Database.Database().Execute(query="INSERT INTO pythobb_users VALUES (?,?,?,?)", variables=( uid, _RequestedData["Username"], saltGen, Security.Security()._Hash(verify=False, string=str(saltGen + _RequestedData["Password"]) , hash=None )), commit=True, doReturn=False)
				Database.Database().Execute(query="INSERT INTO pythobb_user_data VALUES (?,?,?)", variables=(uid, Token, IPADDR,), commit=True, doReturn=False)
				Database.Database().Execute(query="INSERT INTO pythobb_user_data2 VALUES (?,?,?,?,?)", variables=(uid, _RequestedData["Email"], "", "Default user", 2), commit=True, doReturn=False)
				returnVars = {"message": "Registration successful. Redirecting.", "register":True, "sid":Token}
			except Exception as e:
				returnVars = None
				returnString = str(e)
			if( returnVars != None ):
				JSON = Render.Render()._Page(content=str(Render.Render()._JSON(variable="RegisterAttempt", boolean=None, data=returnVars, complete=True)),
				setCookies=None, setContentType="application/json")
			else:
				JSON = Render.Render()._Page(content=str(Render.Render()._JSON(variable="RegisterAttempt", boolean=None, data={"message":returnString, "register":False, "sid":None}, complete=True)),
				setCookies=None, setContentType="application/json")
			return JSON
	
	def MakeProfile(self, request, uid):
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				user_status,sid = False,None
		else:
			user_status,sid = False,None
		return Render.Render()._Page(content=Pages.Pages()._FullRender(content=Pages.Pages()._Render("user_profile"),
			condit={"user": user_status,"sid_": sid}, extra={"GET":"userprofile", "requesteduser":uid}), setCookies=None)

	def ControlPanel(self, request):
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
		else:
			return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
		return Render.Render()._Page(content=Pages.Pages()._RenderUserCP(
				content=Pages.Pages()._Render(name="user_controlpanel"),
				condit = {
					"user": user_status,
					"sid_": sid
					}
			), setCookies=None)
			
	def ProcessUserCP(self, request):
		reqData = {
			"Usertitle": request.POST["Usertitle"],
			"Avatar": request.POST["AvatarURL"]
		}
		print request.COOKIES
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
		else:
			return Render.Render()._Page(content="<script>location.href='%s';</script>"%(Settings.FORUMURL), setCookies=None)
		try:
			uid = Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE sessionid=?", variables=(sid,), commit=False, doReturn=True)[0][0]
			for c in reqData:
				if(c == "Usertitle")and(reqData[c]!=""):
					Database.Database().Execute(query="UPDATE pythobb_user_data2 SET usertitle=? WHERE uid=?", variables=(str(reqData["Usertitle"]),uid,), commit=True)
				if(c == "Avatar")and(reqData[c]!=""):
					Database.Database().Execute(query="UPDATE pythobb_user_data2 SET avatar=? WHERE uid=?", variables=(str(reqData["Avatar"]),uid,), commit=True)
			JSON = Render.Render()._Page(content=Render.Render()._JSON(variable="Updated", boolean=True, data=None, complete=True), setCookies=None, setContentType="application/json")
		except Exception as e:
			print str(e)
			JSON = Render.Render()._Page(content=Render.Render()._JSON(variable="Updated", boolean=None, data=[False, "An error occured."], complete=True), setCookies=None, setContentType="application/json")
		return JSON

	def Forum(self, request, fid):
		if request.COOKIES.has_key("sid"):
			if(IDs.VerifySID(sid=request.COOKIES["sid"])==True):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				user_status,sid = False,None
		else:
			user_status,sid = False,None
		return Render.Render()._Page(
			content=Pages.Pages()._RenderForum(
				content=Pages.Pages()._Render(name="forum_display"),
				condit={"user":user_status,"sid_":sid},
				fid = fid
			), setCookies=None)
