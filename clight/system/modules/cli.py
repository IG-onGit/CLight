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

    def input(hint="", must=False):
        if not hint:
            hint = "Enter"

        value = input(f"{hint}: ")
        while must and not value:
            value = input(f"{hint}: ")

        return value

    def selection(hint="", options=[], must=False):
        if not hint:
            hint = "Select"
        if not options:
            return ""

        if not must:
            options = ["Skip"] + options

        questions = [
            inquirer.List(
                "option",
                message=hint,
                choices=options,
            ),
        ]

        answers = inquirer.prompt(questions)["option"]
        if answers == "Skip":
            return ""

        return answers

    def confirmation(hint="", must=False):
        if not hint:
            hint = "Confirm"

        options = "y" if must else "y/n"
        value = input(f"{hint} ({options}): ")
        while must and (not value or value not in ["Y", "y"]):
            value = input(f"{hint} ({options}): ")

        return True if value in ["Y", "y"] else False

    ####################################################################################// Helpers
