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

class PostSpendingHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", [""])[0]
		title = self.request.arguments.get("title", [""])[0]
		amount = int(self.request.arguments.get("amount", [""])[0])
        # TODO check it is a real username
		leader = self.request.arguments.get("leader", [""])[0]

		content = clean(content)
		title = clean(title)
		leader = clean(leader)
		new_document = {
			"content" : content,
			"type" : "spending",
			"author" : self.get_current_user(),
			"title" : title,
			"leader" : leader,
			"amount" : amount,
			"time": tuple(datetime.now().utctimetuple())
		}

		db.documents.insert(new_document)
		self.redirect("/")

