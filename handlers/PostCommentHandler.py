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

import config 

from handlers.BaseHandler import BaseHandler

class PostCommentHandler(BaseHandler):
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

