# -*- coding: utf-8

import tornado.auth


class ClassicAuthHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
	def post(self):
		# TODO: hash password
		username = self.request.arguments.get("username", [""])[0]
		password = self.request.arguments.get("password", [None])[0]
		db=self.application.database
		self.write(username+" "+password)
		userobj = db.users.find_one({"name": username, "password": password })
		if userobj==None:
			raise tornado.web.HTTPError(500, "Unknown user/bad password.")
		else:
			self.set_secure_cookie("noy_user", tornado.escape.json_encode(username))
			self.redirect("/")

	
	def get(self):
		self.render("classiclogin.html")
    
