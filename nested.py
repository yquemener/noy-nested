from datetime import datetime
from pymongo.connection import Connection
from bson.objectid import ObjectId
 
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
 
from tornado.options import define, options
 
define("port", default=8888, type=int)
 
 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
 
        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
 
        self.con = Connection('localhost', 27017)
        self.database = self.con["nested"]
 
 
class MainHandler(tornado.web.RequestHandler):
	def recurseComment(self, comment, margin):
		if comment == None:
			return
		self.write(margin + comment["content"])
		self.write("\n<br/>\n")
		for c in comment.get("children", []):
			self.recurseComment(c, margin + "___")

	def get(self):
		db=self.application.database

		comments = db["comments"].find()

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
			if not v.has_key("parent"):
				self.recurseComment(v, "")
		

	def post(self):
		db=self.application.database
		content = self.request.arguments.get("content", None)[0]
		parent = self.request.arguments.get("parent", None)[0]
		superparent = self.request.arguments.get("superparent", None)[0]

		new_comment = {
			"content" : content,
			"time" : datetime.utcnow(),
		}

		if parent != None:
			new_comment["parent"] = parent

		if superparent != None:
			new_comment["superparent"] = superparent

		db.comments.insert(new_comment)

 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
 
if __name__ == "__main__":
    main()
