import os
import sys
import subprocess


class main:
    def __init__(self):
        file = os.path.join(os.path.dirname(__file__), ".system/index.py")
        args = " ".join(sys.argv[1:])
        if not os.path.exists(file):
            print("Failed to launch package!")
            sys.exit()

        index = file.replace("\\", "/")
        command = f'clight execute "{index}" {args}'
        subprocess.run(command, shell=True)
        pass


if __name__ == "__main__":
    app = main()
