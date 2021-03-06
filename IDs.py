import Database,types

class Values():
	def __init__(self):
		self._UID = self.getNewID(type="UID")
		self._CID = self.getNewID(type="CID")
		self._FID = self.getNewID(type="FID")
		
	def getNewID(self, type=None):
		if not isinstance(type, types.NoneType):
			typeTables = {
				"UID": "users",
				"CID": "categories",
				"FID": "forums"
			}
			value = len(Database.Database().Execute(query="SELECT * FROM pythobb_%s"%(typeTables[type]), variables=(), commit=False, doReturn=True))
			return int(value+1)

def VerifySID(sid=None):
	if not isinstance(sid, types.NoneType):
		if len(Database.Database().Execute(query="SELECT * FROM pythobb_user_data WHERE sessionid=?", variables=(sid,), commit=False, doReturn=True)) == 0:
			return False
		else:
			return True
