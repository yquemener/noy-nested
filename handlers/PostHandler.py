from handlers.BaseHandler import BaseHandler

class PostHandler(BaseHandler):
    def get(self):
        self.render("proposals.html")

