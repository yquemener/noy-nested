# -*- coding: utf-8

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

from markdown import markdown
 
from tornado.options import define, options

from handlers.BaseHandler import BaseHandler
import tools.Renderer as Renderer

class MainHandler(BaseHandler):
	def get(self):
		self.write(self.render_string("header.html"))
		db=self.application.database
		documents = list(db["documents"].find())
		self.write("<div class='header'>\n")
		if self.get_current_user() == None:
			self.write("Not Logged in.<br/>\n")
			self.write("<a href='/signup'>Sign up</a> &nbsp; <a href='/login/classic'>Log in</a>  &nbsp; <a href='/login/facebook'>Log in with facebook</a> ")
		else:
			self.write("<span>Logged in as "+str(self.get_current_user())+"</span> - \n")
			self.write("<span><a href='/logout'>Log out</a></span>")
		self.write("</div><hr/>\n")
		self.write("<div class='documentslist'>")
		documents.sort(cmp=lambda x,y:-cmp( len(x['plusvote'])-len(x['minusvote']),  len(y['plusvote'])-len(y['minusvote'])))
		for d in documents:
			self.write("<div class='documentsummary'>")
			self.write(Renderer.DocumentHeader(d))
			self.write("</div>\n")
		self.write("<br><br><div><a href='/post'>Poster un nouveau document</a></div>")
		self.write("</div>")
		self.write(self.returnCurrentBudget(db, 118))

	def returnCurrentBudget(self, db, revenue):
		return Renderer.CurrentBudget(db, revenue)
		

