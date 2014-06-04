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


 
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("noy_user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

