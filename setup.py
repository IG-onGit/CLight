from setuptools import setup, find_packages

setup(
    name="clight",
    version="2.4.3",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "pygame",
        "pyttsx3",
        "inquirer",
        "datetime",
        "importlib",
        "colored",
        "cryptography",
        "SpeechRecognition",
    ],
    entry_points={
        "console_scripts": [
            "clight=clight.system.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "clight": [
            "licenses/Apache Software License",
            "licenses/BSD License",
            "licenses/GNU Affero General Public License v3",
            "licenses/GNU General Public License v3 (GPLv3)",
            "licenses/GNU Lesser General Public License v3 (LGPLv3)",
            "licenses/ISC License (ISCL)",
            "licenses/MIT License",
            "licenses/Mozilla Public License 2.0 (MPL 2.0)",
            "package/.placeholder",
            "skeleton/.gitignore",
            "skeleton/.system/imports.py",
            "skeleton/.system/index.py",
            "skeleton/.system/modules/jobs.py",
            "skeleton/.system/sources/logo.ico",
            "system/importer.py",
            "system/main.py",
            "system/modules/cli.py",
            "system/modules/semver.py",
            "system/sources/.gitlab-ci.yml",
            "system/sources/logo.ico",
            "system/sources/main.py",
            "system/sources/README.md",
            "system/sources/setup.py",
            "system/sources/__init__.py",
            "system/sources/init.py",
            "system/sources/{{CMD}}.bat",
            "system/sources/{{module}}.py",
            "system/sources/.github/labels.yml",
            "system/sources/.github/workflows/publish.yml",
            "system/sources/ansi_escape",
            "system/sources/ask.wav",
            "system/sources/done.wav",
            "system/sources/error.wav",
            "system/sources/ready.wav",
            "system/sources/set.wav",
            "system/sources/start.wav",
            "system/sources/unset.wav",
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="CLight is a Python command-line interface application. A lightweight Framework that simplifies CLI app development and the package distribution process, with automatic deployment strategies from Local, GitHub and GitLab environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IG-onGit/CLight",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
