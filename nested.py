#!/usr/bin/env python
# -*- coding: utf-8

from datetime import datetime
from pymongo.connection import Connection
from bson.objectid import ObjectId
 
import os.path
import tornado.auth
import tornado.template
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from 	markdown import markdown
 
from tornado.options import define, options
 
define("port", default=8888, type=int)
define("facebook_api_key", help="your Facebook application API key",
                           default="1408863776041585")

define("facebook_secret", help="your Facebook application secret",
                          default="056d1d09366b04aaf82d307124dc852f")

define("home_url", help="The URL the website will be at", 
                   default="http://localhost:8888")  
 
class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            autoescape=None,
            cookie_secret="Hé, tu sais quoi? je vais me le générer à la main, tant pis pour l'entropie156851huguyfcvbnnjqdjsknbhgyuhjb",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            home_url=options.home_url,
            debug=True,
        )

        handlers = [
            (r"/", MainHandler),
            (r"/signup/facebook", FacebookSignUpHandler),
            (r"/login", AuthHandler),
            (r"/login/facebook", FacebookAuthHandler),
            (r"/logout", AuthLogoutHandler),
            (r"/signup", SignupHandler),
            (r"/post", PostHandler),
        ]
 
        tornado.web.Application.__init__(self, handlers, **settings)
 
        self.con = Connection('localhost', 27017)
        self.database = self.con["nested"]
 
 
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("noy_user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
        
class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html")

class FacebookSignUpHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		requested_username = self.get_argument("username", default=None, strip=False)
		
		my_url = self.settings["home_url"]+"/signup/facebook?username="+requested_username
		if self.get_argument("code", False):
			self.get_authenticated_user(
							redirect_uri=my_url,
							client_id=self.settings["facebook_api_key"],
							client_secret=self.settings["facebook_secret"],
							code=self.get_argument("code"),
							callback=self._on_auth)
			return
		self.authorize_redirect(redirect_uri=my_url,
														client_id=self.settings["facebook_api_key"],
														extra_params={"scope": "read_stream"})
		
	def _on_auth(self, user):
		if not user:
			raise tornado.web.HTTPError(500, "Facebook auth failed")
		
		requested_username = self.get_argument("username", default=None, strip=False)
		db=self.application.database
		userobj = db.users.find_one({"facebook_id": user["id"] })
		userobj2 = db.users.find_one({"name": requested_username })
		if(userobj!=None):
			self.write("A user with this facebook ID already exists: " + str(userobj["name"]))
			self.finish()
			return

		if(userobj2!=None):
			self.write("A user with this name already exists.")
			self.finish()
			return
		db.users.insert({'name': requested_username, 'facebook_id': user['id']})

		self.redirect("/login/facebook")
   
class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/login/facebook")

class FacebookAuthHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		my_url = self.settings["home_url"]+"/login/facebook"
		if self.get_argument("code", False):
			self.get_authenticated_user(
							redirect_uri=my_url,
							client_id=self.settings["facebook_api_key"],
							client_secret=self.settings["facebook_secret"],
							code=self.get_argument("code"),
							callback=self._on_auth)
			return
		self.authorize_redirect(redirect_uri=my_url,
														client_id=self.settings["facebook_api_key"],
														extra_params={"scope": "read_stream"})
		
	def _on_auth(self, user):
		if not user:
			raise tornado.web.HTTPError(500, "Facebook auth failed")
		db=self.application.database
		userobj = db.users.find_one({"facebook_id": user["id"] })
		if userobj==None:
			raise tornado.web.HTTPError(500, "Unknown user. Please sign up.")
		self.set_secure_cookie("noy_user", tornado.escape.json_encode(userobj["name"]))
		self.redirect("/")
		
		
class AuthLogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_cookie("noy_user")
		self.redirect("/")

class PostHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", [""])[0]
		parent = self.request.arguments.get("parent", [None])[0]
		superparent = self.request.arguments.get("superparent", [None])[0]

		# TODO: add some bleach
		content = markdown(content.decode("utf-8"), safe_mode="escape")
		if content.startswith("<p>"):
			content = content[3:]
		if content.endswith("</p>"):
			content=content[:-4]
		
		new_comment = {
			"content" : content,
			"time" : datetime.utcnow(),
			"author" : self.get_current_user()
		}

		if parent != None:
			new_comment["parent"] = parent
		if superparent != None:
			new_comment["superparent"] = superparent
		db.comments.insert(new_comment)
		self.redirect("/")

        
class MainHandler(BaseHandler):
	def recurseComment(self, comment, margin, blockid):
		if comment == None:
			return
		self.write('<div style="margin-left:'+str(margin*20)+'px"><span class="comment">' + comment["content"] + '</span>')
		self.write(self.render_string("post.html", blockid=blockid, default_display="none", parent_id=comment["_id"]))
		self.write('</div>')
		#self.write("&nbsp;"*10 + str(comment.get("time",0)))
		#self.write("\n<br/>\n")
		i=0
		for c in comment.get("children", []):
			i+=1
			self.recurseComment(c, margin + 1, blockid+"."+str(i))

	@tornado.web.asynchronous
	def get(self):
		self.write(self.render_string("header.html"))
		db=self.application.database
		comments = db["comments"].find()
		if self.get_current_user() == None:
			self.write("Not Logged in.<br/>\n")
			self.write("<a href='/signup'>Sign up</a> &nbsp; <a href='/login'>Log in</a> ")
		else:
			self.write("Logged in as "+str(self.get_current_user())+"<br/>\n")
			self.write("<a href='/logout'>Log out</a>")
		self.write("<hr>" + str(self.settings) + "<hr>")
		self.write(str(self.get_secure_cookie("noy_auth_facebook"))+"<hr>")
		d = dict()
		for c in comments:
			d[str(c["_id"])] = c
		# TODO: check if some smartass makes a cyclic reference
		for (k,v) in d.items():
			par = v.get("parent",None)
			if par!=None:
				if d[par].has_key("children"):
					d[par]["children"].append(v)
				else:
					d[par]["children"] = [v]
		for (k,v) in d.items():
			if v.has_key("children"):
				v["children"].sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		a=d.values()
		a.sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		i=0
		for v in a:
			if not v.has_key("parent"):
				i+=1
				self.recurseComment(v, 0, str(i))
		self.write("<hr>Commenter")
		self.render("post.html", blockid="0", default_display="block", parent_id="")

 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
 
if __name__ == "__main__":
    main()
