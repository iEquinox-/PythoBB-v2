import json,types

class Render():
	def __init__(self):
		self._JSON    = self.RenderJSON
		self.JSONDict = dict()
		
	def RenderJSON(self, variable=None, boolean=None, data=None, complete=False, get=None):
		if(isinstance(get, types.NoneType)):
			self.JSONDict[variable] = ([c for c in data] if isinstance(data, types.ListType) else data) if not isinstance(data, types.NoneType) else boolean
			if(complete == True):
				return self.JSONDict
		else:
			return self.JSONDict[get]
