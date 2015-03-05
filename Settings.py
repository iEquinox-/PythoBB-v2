import os

FORUMURL    = "http://127.0.0.1:8000"
FORUMNAME   = "PythoBB"
TABLEPREFIX = "pythobb_"
BASEDIR     = os.path.dirname(os.path.abspath(__file__))

TABLESCHEMA = """
			CREATE TABLE pythobb_categories (cid int, name text, desc text)
			CREATE TABLE pythobb_forums (fid int, parent int, name text, desc text)
			
			CREATE TABLE pythobb_users (uid int, username text, salt text, password text)
			CREATE TABLE pythobb_user_data (uid int, sessionid text, ipaddr text)
			"""
