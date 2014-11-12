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

class ShowDiscussHandler(BaseHandler):
	def recurseComment(self, comment, margin, blockid, path):
		if comment == None:
			return
		#self.write('<div class="comment" style="margin-left:'+str(margin*20)+'px;margin-bottom:10px"><span class="comment">' + comment["content"] + '</span>')
		self.write('<div class="comment">')
		self.write('<div class="comment_head"><span class="comment_author">' + str(comment['author']))
		self.write('</span> - <span class="comment_date">' + str(comment['time']).split(".")[0] + '</span></div>')
		self.write('<span class="comment_body">' + comment["content"] + '</span>')
		self.write(self.render_string("post.html", blockid=blockid, default_display="none", parent_id=comment["_id"], super_parent_id=ObjectId(path)))
		i=0
		for c in comment.get("children", []):
			i+=1
			self.recurseComment(c, margin + 1, blockid+"."+str(i), path)
		self.write('</div>')

	def get(self, path):
		self.write(self.render_string("header.html"))
		db=self.application.database
		doc = db["documents"].find({'_id':ObjectId(path)})
		self.write("<div class='documentheader'>\n")
		if(doc[0]['type']!="election"):
			self.write("  <div class='documenttitle'>"+doc[0]['title']+"</div>\n")
		else:
			self.write("  <div class='documenttitle'>")
			self.write("Remplacer " +str(doc[0]['togo'])+" par "+unicode(doc[0]['toenter']))
			self.write("</div>\n")
		self.write("   par <span class='documentauthor'>"+doc[0]['author']+"</span>\n")
		self.write("   en date du <span class='documentdate'>"+str(datetime(*doc[0]['time'][:7]))+"</span>\n")
		self.write("</div>")
		self.write("<div class='documentcontent'>\n")
		self.write(doc[0]['content'])
		self.write("</div>")
		self.write(self.render_string("post.html", blockid="0", default_display="block", parent_id="", super_parent_id=path))
		
		comments = db["comments"].find({'super_parent':path})
		d = dict()
		for c in comments:
			d[str(c["_id"])] = c
		for (k,v) in d.items():
			ch = v.get("children", list())
			newch = list()
			print ch
			for c in ch:
				newch.append(d[str(c)])
			d[k]["children"]=newch
		# TODO: check if some smartass makes a cyclic reference
		"""for (k,v) in d.items():
			par = v.get("parent",None)
			if par!=None:
				if d[par].has_key("children"):
					d[par]["children"].append(v)
				else:
					d[par]["children"] = [v]"""
		for (k,v) in d.items():
			if v.has_key("children"):
				v["children"].sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		a=d.values()
		a.sort(cmp=lambda x,y:cmp(str(x.get("time",0)), str(y.get("time",0))))
		i=0
		for v in a:
			if not v.has_key("parent"):
				i+=1
				self.recurseComment(v, 0, str(i), path)
		
