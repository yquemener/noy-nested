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
from utils import clean

class PostCommentHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", [""])[0]
		parent = self.request.arguments.get("parent", [None])[0]
		super_parent = self.request.arguments.get("super_parent", [None])[0]

		content = clean(content)
		
		new_comment = {
			"content" : content,
			"time" : datetime.utcnow(),
			"author" : self.get_current_user(),
			"plusvote": list(),
			"minusvote": list()
		}

		if parent != None:
			new_comment["parent"] = parent
		if super_parent != None:
			new_comment["super_parent"] = super_parent
		new_id = db.comments.insert(new_comment)
		print new_id
		print parent
		print db.comments.update({"_id": ObjectId(parent)}, {"$push": {"children": str(new_id)}})
		self.redirect("/")

