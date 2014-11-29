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

from handlers.BaseHandler import BaseHandler

class MainHandler(BaseHandler):
	def createDocumentHeader(self, doc):
		# TODO: make a clean unicde/str conversion
		score = len(doc['plusvote'])-len(doc['minusvote'])
		s = ""
		if doc['type']=="discussion":
			s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
			s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
			s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
			s+="  <span class='documentsummarytype'>[Discussion]</span>\n"
			s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>" +doc['title']+"</a></span>\n"
			s+="   par \n"
			s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
	 		s+="   en date du \n"
			s+="  <span class='documentsummarydate'>"+str(datetime(*doc['time'][:7]))+"</span>\n"
		elif doc['type']=="spending":
			s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
			s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
			s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
			s+="  <span class='documentsummarytype'>[Dépense]</span>\n"
			s+="  <span class='documentsummaryamount'>["+str(doc['amount'])+"&euro;]</span>\n"
			s+="  <span class='documentsummarytitle'><a href='/document/"
                        s+=str(doc['_id'])+"'>" + doc['title'].encode("utf-8")+"</a></span>\n"
			s+="   par \n"
			s+="  <span class='documentsummaryauthor'>"+str(doc['author'])+"</span>\n"
	 		s+="   en date du \n"
			s+="  <span class='documentsummarydate'>"+str(datetime(*doc['time'][:7]))+"</span>\n"
		elif doc['type']=="election":
			s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
			s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
			s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
			s+="  <span class='documentsummarytype'>[Election]</span>\n"
			s+=u"  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])
			s+="'>Remplacer " +str(doc['togo'])+" par "+unicode(doc['toenter'])+"</a></span>\n"
			s+=u"   proposé par \n"
			s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
	 		s+="   en date du \n"
			s+="  <span class='documentsummarydate'>"+str(datetime(*doc['time'][:7]))+"</span>\n"
		elif doc['type']=="status":
			s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
			s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
			s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
			s+="  <span class='documentsummarytype'>[Statuts]</span>\n"
			s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>"+doc['title']+"</a></span>\n"
			s+=u"   proposé par \n"
			s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
	 		s+="   en date du \n"
			s+="  <span class='documentsummarydate'>"+str(datetime(*doc['time'][:7]))+"</span>\n"
		elif doc['type']=="vote":
			s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
			s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
			s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
			s+="  <span class='documentsummarytype'>[Vote]</span>\n"
			s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>"+doc['title']+"</a></span>\n"
			s+=u"   proposé par \n"
			s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
	 		s+="   en date du \n"
			s+="  <span class='documentsummarydate'>"+str(datetime(*doc['time'][:7]))+"</span>\n"
		return s


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
		documents.sort(cmp=lambda x,y:-cmp( len(x['plusvote'])-len(x['minusvote']),  len(y['plusvote'])-len(y['minusvote'])))
		for d in documents:
			self.write("<div class='documentsummary'>")
			self.write(self.createDocumentHeader(d))
			self.write("</div>\n")
		self.write("<br><br><div><a href='/post'>Poster un nouveau document</a></div>")

