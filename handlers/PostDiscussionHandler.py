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

class PostDiscussionHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", [""])[0]
		title = self.request.arguments.get("title", [""])[0]

		title = clean(title)
		content = clean(content)

		new_document = {
			"content" : content,
			"type" : "discussion",
			"author" : self.get_current_user(),
			"title" : title,
			"time": tuple(datetime.now().utctimetuple()),
			"plusvote": list(),
			"minusvote": list()
		}

		db.documents.insert(new_document)
		self.redirect("/")

