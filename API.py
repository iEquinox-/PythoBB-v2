
import Render,Database,types,Settings

class API():
	def __init__(self):
		self.types  = ["*","category","forum","thread","user"]
		self.dbkeys = {
			"category": "categories",
			"forum":    "forums",
			"thread":   "threads",
			"user":     "users",
			"query": {
				"*": "SELECT * FROM pythobb_%s",
				"users": "SELECT * FROM pythobb_users WHERE uid=?",
				"categories": "SELECT * FROM pythobb_categories WHERE cid=?",
				"forums": "SELECT * FROM pythobb_forums WHERE fid=?",
				"threads": "SELECT * FROM pythobb_threads WHERE tid=?"
			}
		}
		
	def RenderJSON(self, request, type, requested):
		if Settings.APIENABLED == True:
			if(type == "user")and(requested == "*"):
				JSON = Render.Render()._JSON(variable="Error", boolean=None, data="Type 'User' cannot use the * request.", complete=True)
			elif(type == "thread")and(requested == "*"):
				JSON = Render.Render()._JSON(variable="Error", boolean=None, data="Type 'Thread' cannot use the * request.", complete=True)
			else:
				if type in self.types:
					doData = self.dbkeys["query"][self.dbkeys[type]] if requested != "*" else (self.dbkeys["query"]["*"] % (self.dbkeys[type]) )
					print doData
					# NEVER COMMIT
					vars = (requested,) if requested != "*" else ()
					doData = self.SortData(data=Database.Database().Execute(query=doData, variables=vars, commit=False, doReturn=True), query=self.dbkeys[type] if requested != "*" else self.dbkeys[type]+"(*)")
					JSON = Render.Render()._JSON(variable=type.capitalize() if requested != "*" else type.capitalize()+"(*)", boolean=None, data=doData, complete=True)
				else:
					JSON = Render.Render()._JSON(variable="Error", boolean=None, data="Invalid type '%s'." % (type), complete=True)
			return Render.Render()._Page(content=JSON, setCookies=None, setContentType="application/JSON")
		else:
			return Render.Render()._Page(content=Render.Render()._JSON(
				variable="Error",
				boolean=None,
				data="The bulletin board administrator has disabled the usage of an API.",
				complete=True)
			,setCookies=None, setContentType="application/JSON")

	def SortData(self, data=None, query=None):
		newdata = None
		if(not isinstance(data, types.NoneType))and(not isinstance(query, types.NoneType)):
			if query == "categories":
				for c in data:
					newdata = {"Name": c[1], "Description": c[2], "cid": c[0]}
			if query == "categories(*)":
				newdata = []
				for c in data:
					newdata.append(
						{c[0]:{"Name":c[1], "Description": c[2], "cid": c[0]}}
					)
			if query == "forums":
				for c in data:
					newdata = {"Name": c[2], "Description": c[3], "fid":c[0]}
			if query == "forums(*)":
				newdata = []
				for c in data:
					newdata.append(
						{"Name": c[2], "Description": c[3], "fid":c[0]}
					)
			if query == "users":
				x = Database.Database().Execute(query="SELECT * FROM pythobb_user_data2 WHERE uid=?", variables=(data[0][0],), commit=False, doReturn=True)
				for c in data:
					newdata = {"Username": c[1], "UID": c[0],"Avatar": x[0][2],"Usertitle": x[0][3],"GID": x[0][4]}
			if query == "threads":
				for c in data:
					newdata = {"Name": c[2], "Tags": c[3], "tid": c[0]}
		return newdata
