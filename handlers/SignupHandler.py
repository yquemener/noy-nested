from handlers.BaseHandler import BaseHandler

class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html")

