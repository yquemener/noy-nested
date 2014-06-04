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
	def recurseComment(self, comment, margin, blockid):
		if comment == None:
			return
		#self.write('<div class="comment" style="margin-left:'+str(margin*20)+'px;margin-bottom:10px"><span class="comment">' + comment["content"] + '</span>')
		self.write('<div class="comment">')
		self.write('<div class="comment_head"><span class="comment_author">' + str(comment['author']))
		self.write('</span> - <span class="comment_date">' + str(comment['time']).split(".")[0] + '</span></div>')
		self.write('<span class="comment_body">' + comment["content"] + '</span>')
		self.write(self.render_string("post.html", blockid=blockid, default_display="none", parent_id=comment["_id"]))
		i=0
		for c in comment.get("children", []):
			i+=1
			self.recurseComment(c, margin + 1, blockid+"."+str(i))
		self.write('</div>')

	@tornado.web.asynchronous
	def get(self):
		self.write(self.render_string("header.html"))
		db=self.application.database
		comments = db["comments"].find()
		self.write("<div class='header'>\n")
		if self.get_current_user() == None:
			self.write("Not Logged in.<br/>\n")
			self.write("<a href='/signup'>Sign up</a> &nbsp; <a href='/login/classic'>Log in</a>  &nbsp; <a href='/login/facebook'>Log in with facebook</a> ")
		else:
			self.write("<span>Logged in as "+str(self.get_current_user())+"</span> - \n")
			self.write("<span><a href='/logout'>Log out</a></span>")
		self.write("</div><hr/>\n")
		d = dict()
		for c in comments:
			d[str(c["_id"])] = c
		# TODO: check if some smartass makes a cyclic reference
		for (k,v) in d.items():
			par = v.get("parent",None)
			if par!=None:
				if d[par].has_key("children"):
					d[par]["children"].append(v)
				else:
					d[par]["children"] = [v]
		for (k,v) in d.items():
			if v.has_key("children"):
				v["children"].sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		a=d.values()
		a.sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		i=0
		for v in a:
			if not v.has_key("parent"):
				i+=1
				self.recurseComment(v, 0, str(i))
		self.write("<hr>Commenter")
		self.render("post.html", blockid="0", default_display="block", parent_id="")
