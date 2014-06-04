# -*- coding: utf-8

import tornado.auth


class AuthHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect("/login/facebook")


