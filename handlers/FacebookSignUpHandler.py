# -*- coding: utf-8

import tornado.auth
import tornado.template
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from handlers.BaseHandler import BaseHandler
from utils import checkClean

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

		if(not checkClean(requested_username)):
			self.write("Merci de ne pas utiliser de HTML ni de markdown dans votre login")
			self.finish()
			return

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

