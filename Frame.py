import Security,Render,Pages,Database

class Base:
	def Home(self, request):
		if request.COOKIES.has_key("sid"):
			user_status,sid = True,request.COOKIES["sid"]
		else:
			user_status,sid = False,None
		return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["index"]),
				condit = {
					"user": user_status,
					"sid_": sid
					}
			), setCookies=None)
