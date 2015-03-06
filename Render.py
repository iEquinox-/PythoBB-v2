import json,types
from django.http import HttpResponse

class Render():
	def __init__(self):
		self._JSON    = self.RenderJSON
		self.JSONDict = dict()
		self._Page    = self.RenderPage
		
	def RenderJSON(self, variable=None, boolean=None, data=None, complete=False, get=None):
		if(isinstance(get, types.NoneType)):
			self.JSONDict[variable] = ([c for c in data] if isinstance(data, types.ListType) else data) if not isinstance(data, types.NoneType) else boolean
			if(complete == True):
				return json.dumps(self.JSONDict)
		else:
			return self.JSONDict[get]

	def RenderPage(self, content=None, setCookies=None, setContentType=None):
		_RenderedContent = HttpResponse(content) if not isinstance(content, types.NoneType) else HttpResponse(self.RenderError(Error=1,Additional=content))
		if(isinstance(setCookies, types.DictType))and(len(setCookies)>=1):
			for c in setCookies:
				_RenderedContent.set_cookie(str(c), setCookies[c])
		if(not isinstance(setContentType, types.NoneType)):
			_RenderedContent["content-type"] = setContentType
		return _RenderedContent
		
	def RenderError(self, Error=None, Additional=None):
		keys = {
			1: "Missing or obstructed content: Render()._Page function."
			}
		if isinstance(Error, types.IntType):
			e = keys[Error]
			return (e+Additional) if Additional else e
