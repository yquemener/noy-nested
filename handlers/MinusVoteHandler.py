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


class MinusVoteHandler(BaseHandler):
	@tornado.web.authenticated
	# because fuck RESTful standard (actually it should be a POST request but I dont want to fiddle with javascript yet)
	def get(self, path):
		db=self.application.database
		doc = db["documents"].find({'_id':ObjectId(path)})
		db.documents.update({'_id':ObjectId(path)}, {"$addToSet": {"minusvote":self.get_current_user()}})
		self.write(self.render_string("header.html"))
		self.write("Votre vote a été pris en compte.");

