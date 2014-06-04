# -*- coding: utf-8

import tornado.auth

class AuthLogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_cookie("noy_user")
		self.redirect("/")

