import Security,Render,Pages,Database,Settings
from django.middleware.csrf import rotate_token as RotateCSRFToken

class Base:
	def Home(self, request):
		RotateCSRFToken(request)
		if request.COOKIES.has_key("sid"):
			if(request.COOKIES["sid"] != ""):
				user_status,sid = True,request.COOKIES["sid"]
			else:
				user_status,sid = False,None
		else:
			user_status,sid = False,None
		return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["index"]),
				condit = {
					"user": user_status,
					"sid_": sid
					}
			), setCookies=None)

	def Login(self, request):
		if request.COOKIES.has_key("sid"):
			if request.COOKIES["sid"] != "":
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
