import Security,Render,Pages

class Base:
	def Home(self, request):
		if request.COOKIES.has_key("SESSION_ID"):
			user_status = True
			sid = request.COOKIES["sid"]
		else:
			user_status = False
			sid = None
			
		return Render.Render()._Page(content=Pages.Pages()._FullRender(
				content=Pages.Pages()._Render(name=Pages.Pages().pageKeys["index"]),
				condit = {
					"user": user_status,
					"sid_": sid
					}
			), setCookies=None)
