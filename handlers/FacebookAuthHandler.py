# -*- coding: utf-8

import tornado.auth
import tornado.template
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

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
		
		

