# -*- coding: utf-8

import tornado.auth

from handlers.BaseHandler import BaseHandler
from utils import checkClean

class ClassicSignUpHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def post(self):
		requested_username = self.get_argument("username", default=None, strip=False)
		requested_password= self.get_argument("password", default=None, strip=False)
		
		db=self.application.database
		userobj = db.users.find_one({"name": requested_username })

		if(userobj!=None):
			self.write("A user with this name already exists.")
			self.finish()
			return

		if(not checkClean(requested_username)):
			self.write("Merci de ne pas utiliser de HTML ni de markdown dans votre login")
			self.finish()
			return
		
		db.users.insert({'name': requested_username, 'password': requested_password})

		self.redirect("/login/classic")


