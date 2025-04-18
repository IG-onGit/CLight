from clight.system.importer import *


class cli:
    mode = "text"
    speed = 150
    voice = 1
    dev = False

    ####################################################################################// Load
    def __init__(self):
        pass

    ####################################################################################// Main
    def hint(message="", update=False):
        end = "\n"
        if update and not cli.dev:
            end = "\r"
            message += " " * 100
        print(fg("yellow") + message + attr("reset"), end=end)

    def done(message="", update=False):
        end = "\n"
        if update and not cli.dev:
            end = "\r"
            message += " " * 100
        print(fg("green") + message + attr("reset"), end=end)

    def info(message="", update=False):
        end = "\n"
        if update and not cli.dev:
            end = "\r"
            message += " " * 100
        print(fg("cyan") + message + attr("reset"), end=end)

    def error(message="", update=False):
        end = "\n"
        if update and not cli.dev:
            end = "\r"
            message += " " * 100
        print(fg("red") + message + "!" + attr("reset"), end=end)

    def trace(message=""):
        if cli.dev:
            print("● " + message)

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

        cli.sound("ask")
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

        if cli.mode == "voice":
            cli.speak(hint)
        cli.sound("ask")

        options = "y" if must else "y/n"
        value = input(f"{hint} ({options}): ")
        while must and (not value or value not in ["Y", "y"]):
            value = input(f"{hint} ({options}): ")

        return True if value in ["Y", "y"] else False

    def value(key="", data=None, default=""):
        if key is not None and isinstance(key, int) and 0 <= key < len(data):
            return data[key]
        elif key in data:
            return data[key]
        else:
            return default

    def sound(name=""):
        dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(dir, "sources", str(name) + ".wav")
        if not os.path.exists(path):
            return False

        pygame.init()
        pygame.mixer.init()

        try:
            sound = pygame.mixer.Sound(path)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
        except Exception as e:
            print(e)
            sys.exit()
        finally:
            pygame.quit()

    def speak(text="", speed=None, voice=None):
        speed = cli.speed if speed == None else speed
        voice = cli.voice if voice == None else voice

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[voice].id)
        engine.setProperty("rate", speed)
        engine.say(str(text))
        engine.runAndWait()
        return "Reading Done"

    def listen():
        rec = speech.Recognizer()
        with speech.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
            cli.sound("start")
            audio = rec.listen(source)
            try:
                text = rec.recognize_google(audio)
                cli.sound("done")
                return text
            except Exception as error:
                cli.sound("error")
                if len(str(error)) == 0:
                    return False
                else:
                    time.sleep(2)
                    return False

    def read(file=""):
        if not os.path.exists(file) or not os.path.isfile(file):
            return ""

        return open(file, "r", encoding="utf-8", errors="replace").read()

    def write(file="", content=""):
        if not file:
            return False
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        return file

    def yaml(file=""):
        if not os.path.exists(file):
            return {}

        yml = {}
        with open(file, "r") as yaml_file:
            yml = yaml.safe_load(yaml_file)

        if not yml:
            return {}

        return yml

    def template(content="", replacers={}):
        if not content or not replacers:
            return ""

        for replacer in replacers:
            content = content.replace("{{" + replacer + "}}", str(replacers[replacer]))

        return content

    def chars(length=50):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def isValue(value):
        if value:
            return True
        return False

    def isPath(path=""):
        if path and os.path.exists(path):
            return True
        return False

    def isFile(path=""):
        if path and os.path.exists(path) and os.path.isfile(path):
            return True
        return False

    def isFolder(path=""):
        if path and os.path.exists(path) and os.path.isdir(path):
            return True
        return False

    def execute(line="", message="", background=False):
        if not line:
            cli.error("Invalid CMD line")
            return False

        try:
            if background:
                subprocess.Popen(line, shell=True)
            else:
                subprocess.run(line, check=True)
            cli.done(message)
            return True
        except subprocess.CalledProcessError:
            cli.error(f"CMD Failed: {message}")
            return False

        return False

    ####################################################################################// Helpers
