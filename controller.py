from base import BaseController

class MainController(BaseController):

    @classmethod
    def get_instance(cls):
        return cls()

    def pre_switch(self):
        pass

    def start(self):
        raise Exception()
