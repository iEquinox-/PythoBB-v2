
import random,string,cgi,types,re,time,uuid
from passlib.apps import custom_app_context as passlib_context

class Utils():
	def __init__(self):
		self.charset = {"default":[c for c in list(string.ascii_letters + "+_)(*&^%$#@!=-\\[]';/.,<>?\":")], "special":list("+_)(*&^%$#@!=-\\[]';/.,<>?\":")}

class Security():
	def __init__(self):
		self._Salt  = self.Rotate_Salt(length=5, charset=Utils().charset["default"])
		self._Parse = self.Parse_Msg
		self._Hash  = self.Hash_Text
		self._TID   = self.Rotate_Token()
		
	def Rotate_Salt(self, length=None, charset=[]):
		_string = ""
		for x in range(0,length):
			_string += random.choice(charset)
		return _string

	def Parse_Msg(self, message=None):
		_Str = {1:[],0:[]}
		if not isinstance(message, types.NoneType):
			queue = re.findall("&lt;script&gt;(.*?)&lt;/script&gt;", cgi.escape(message))
			if not len(queue) == 0:
				for q in queue:
					_Str[1].append(
						"%s " % (time.time()) + q
						)
				message = cgi.escape(message)
		return {"MSG":message, "STR":_Str}

	def Hash_Text(self, verify=False, string=None, hash=None):
		if(verify == True)and(not isinstance(string,types.NoneType))and(not isinstance(hash,types.NoneType)):
			return passlib_context.verify(string, hash)
		else:
			if not isinstance(string,types.NoneType):
				return passlib_context.encrypt(string)
				
	def Rotate_Token(self):
		Salt = self.Rotate_Salt(length=10, charset=Utils().charset["default"])
		Hash = self.Hash_Text(verify=False, string="%s%s" % (str(uuid.uuid4()), Salt), hash=None).split("$")[-1].split(".")[0]
		while len(Hash) < 20:
			Hash = self.Hash_Text(verify=False, string="%s%s" % (str(uuid.uuid4()), Salt), hash=None).split("$")[-1].split(".")[0]
		return Hash
