

class ActionTracesMiddleware(object):

    def __init__(self, app, conf):
        self.app = app