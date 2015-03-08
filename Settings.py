import os

FORUMURL    = "http://127.0.0.1:8000"
FORUMNAME   = "PythoBB v2"
TABLEPREFIX = "pythobb_"
APIENABLED  = True

# DON'T EDIT THE FOLLOWING SETTINGS

BASEDIR     = os.path.dirname(os.path.abspath(__file__))
TABLESCHEMA = """
			CREATE TABLE pythobb_categories (cid int, name text, desc text)
			CREATE TABLE pythobb_forums (fid int, parent int, name text, desc text)
			CREATE TABLE pythobb_threads (tid int, parent int, name text, tags text)
			CREATE TABLE pythobb_posts (pid int, parent int, content text, uid int)
			CREATE TABLE pythobb_users (uid int, username text, salt text, password text)
			CREATE TABLE pythobb_user_data (uid int, sessionid text, ipaddr text)
			CREATE TABLE pythobb_user_data2 (uid int, email text, avatar text, usertitle text, gid int)
			"""
