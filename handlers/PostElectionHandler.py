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

class PostElectionHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", [""])[0]
        # TODO check it is a real username
		togo = self.request.arguments.get("togo", [""])[0]
        # TODO check it is a real username
		toenter = self.request.arguments.get("toenter", [""])[0]

		content = clean(content)
		togo = clean(togo)
		toenter = clean(toenter)
		new_document = {
			"content" : content,
			"type" : "election",
			"author" : self.get_current_user(),
			"togo" : togo,
			"toenter" : toenter,
			"time": tuple(datetime.now().utctimetuple()),
			"plusvote": list(),
			"minusvote": list()
		}

		db.documents.insert(new_document)
		self.redirect("/")

