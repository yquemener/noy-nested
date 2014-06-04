#!/usr/bin/env python
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
from handlers.MainHandler import MainHandler
from handlers.BaseHandler import BaseHandler
from handlers.ClassicSignUpHandler import ClassicSignUpHandler
from handlers.FacebookSignUpHandler import FacebookSignUpHandler
from handlers.ClassicAuthHandler import ClassicAuthHandler
from handlers.FacebookAuthHandler import FacebookAuthHandler
from handlers.AuthLogoutHandler import AuthLogoutHandler
from handlers.SignupHandler import SignupHandler
from handlers.PostCommentHandler import PostCommentHandler
from handlers.PostDocumentHandler import PostDocumentHandler


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            autoescape=None,
            cookie_secret=options.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            home_url=options.home_url,
            debug=True,
        )

        handlers = [
            (r"/", MainHandler),
            (r"/signup/facebook", FacebookSignUpHandler),
            (r"/signup/classic", ClassicSignUpHandler),
            (r"/login/facebook", FacebookAuthHandler),
            (r"/login/classic", ClassicAuthHandler),
            (r"/logout", AuthLogoutHandler),
            (r"/signup", SignupHandler),
            (r"/post_comment", PostCommentHandler),
            (r"/post_document", PostDocumentHandler),
        ]
 
        tornado.web.Application.__init__(self, handlers, **settings)
 
        self.con = Connection('localhost', 27017)
        self.database = self.con["nested"]
 
        

   


		
 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
 
if __name__ == "__main__":
    main()
