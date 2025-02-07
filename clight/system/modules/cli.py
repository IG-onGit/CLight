from clight.system.importer import *


class cli:
    ####################################################################################// Load
    def __init__(self):
        pass

    ####################################################################################// Main
    def hint(message="", update=False):
        end = "\n"
        if update:
            end = "\r"
            message += " " * 100
        print(fg("yellow") + message + attr("reset"), end=end)

    def done(message="", update=False):
        end = "\n"
        if update:
            end = "\r"
            message += " " * 100
        print(fg("green") + message + attr("reset"), end=end)

    def info(message="", update=False):
        end = "\n"
        if update:
            end = "\r"
            message += " " * 100
        print(fg("blue") + message + attr("reset"), end=end)

    def error(message="", update=False):
        end = "\n"
        if update:
            end = "\r"
            message += " " * 100
        print(fg("red") + message + "!" + attr("reset"), end=end)

    ####################################################################################// Helpers
