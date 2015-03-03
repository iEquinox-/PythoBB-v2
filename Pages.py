
class Pages():
	def __init__(self):
		self._Render = self.OpenPage
		self.pageKeys = {
			"index": "index",
			"userblock_guest": "",
			"userblock_user": ""
			}
		
	def OpenPage(self, name=None):
		return str(open("templates/%s.ptmp"%(name)).read())
