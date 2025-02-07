from imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", args=[]):
        self.app, self.args = app, args
        # ...
        pass

    ####################################################################################// Main
    def demo(self, param=""):  # (param) - Test demo method with param
        if not param:
            return "Invalid param!"

        cli.hint(param)
        # cli.info(param)
        # cli.done(param)
        # cli.error(param)

        return self.__helper()

    ####################################################################################// Helpers
    def __helper(self):
        return jobs.test()
