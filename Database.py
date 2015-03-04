import sqlite3,types,Security,Settings

class Database():
	def __init__(self):
		self._DB = self.Parse_DB(db_dir=Settings.BASEDIR + "/pythobb.db")
		self.exe = self.Execute
		
	def Parse_DB(self, db_dir=None):
		if not db_dir:
			db_dir = Settings.BASEDIR + "pythobb.db"
		connection = sqlite3.connect(db_dir)
		cursor     = connection.cursor()
		execute    = cursor.execute
		return {"connection":connection, "cursor":cursor, "execute":execute}
		
	def Execute(self, query=None, variables=None, commit=False, doReturn=False, string=True):
		if string:
			if( not isinstance(query, types.NoneType) )and( isinstance(variables, types.TupleType) ):
				try:
					c = self._DB["execute"](query, variables)
					if commit == True:
						self._DB["connection"].commit()
					if doReturn == True:
						return [x for x in c]
				except Exception as e:
					return [None, "Error parsed " + str(e)]
			else:
				return [None, "Error, missing or obstructed data. [QUERY] " + query + " [VARIABLES] " + str(variables)]
		else:
			return

