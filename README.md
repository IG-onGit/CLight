# CLight v1.2

**Project**: CLight
<br>**Version**: 1.2
<br>**OS**: Microsoft / Windows
<br>**Author**: Irakli Gzirishvili
<br>**Mail**: gziraklirex@gmail.com

**CLight** is a Python command-line interface application. A lightweight Framework that simplifies CLI app development and the package distribution process, with automatic deployment strategies from Local, GitHub and GitLab environments.

## Installation

To use **CLight**, follow these steps:

- Open CMD as administrator and run the following command to install `pip install clight` then restart your CMD
- To check if **CLight** is installed correctly, run the following command `clight`

> Runn CMD as administrator

## Commands

These are the available commands you can use:

- `clight` - To list available commands
- `clight new` - Create new project
- `clight module (name)` - Create new module
- `clight reform (-t)` - Edit project params, (-t) to skip templates
- `clight all` - List existing projects
- `clight publish (-t)` - Publish project on PyPI, (-t) to test locally
- `clight remove (project)` - Remove project
- `clight pypidel` - Delete PyPI credentials
- `clight install` - Test the installation process locally
- `clight update` - Update local installation test
- `clight uninstall` - Test the uninstallation process locally

## Rules

Don't remove these items from the project's `.system` folder:

- **modules** - Folder for your custom modules
- **sources** - Folder for system resources
- **imports.py** - File to import pip and your custom packages
- **index.py** - Index file, defining the main CLI commands that users will interact with

The index and module files are constructed with 3 sections of code:

1. **Load** - Section for initializing your project and running some scripts before executing required command
2. **Main** - CLI command methods with name, arguments and description
3. **Helpers** - Private methods used to support the Main methods

> You don't need anything else, this is the simplest CLI application framework interface to save your time

## Shared `cli` Methods

These are basic methods from the `clight` package class called `cli` that you can use in your index and module files:

- `cli.error("message")` - Print an error message in red
- `cli.info("message")` - Print an info message in blue
- `cli.hint("message")` - Print a hint in yellow
- `cli.done("message")` - Print a completion message in green
- `cli.input("hint")` - Define CLI input field
- `cli.selection("hint", ["A", "B"])` - Define selection input field
- `cli.confirmation("hint")` - Define confirmation input field
- `cli.value("key", {...}, "default")` - Get value from data
- `cli.sound("done")` - Set system sound - start, ready, done, error, ask, set or unset
- `cli.speak("text")` - Read text with voice
- `cli.listen()` - Listen and convert speech to text
- `cli.read("Folder/file.txt")` - Read file and get content
- `cli.write("Folder/file.txt", "content")` - Write file with content
- `cli.yaml("Folder/file.yaml")` - Read and convert YAML file as dict
- `cli.template("content", {...})` - Parse template content with given key-value pairs
- `cli.chars(10)` - Get random characters with given length
- `cli.isValue(value)` - Check if value exists
- `cli.isPath(path)` - Check if path exists
- `cli.isFile(file)` - Check if file exists
- `cli.isFolder(folder)` - Check if folder exists
- `cli.execute("cmd", "message")` - Execute CMD command

## Specifying Parameters

When creating your new project, you will be asked to fill a simple form just once, to specify your project's configuration parameters:

1. **Name** - Name of your project `required`
2. **Version** - Version of your project `required`
3. **Description** - Description of your project `required`
4. **Link** - Link to your project
5. **CMD** - CMD name alias for your project `required`
6. **Author** - Author of the project `required`
7. **Mail** - Mail of the project author `required`
8. **Project Type** - Type of the project `required`
9. **Repository Type** - Project repository type `required`
10. **License** - License for your project
11. **Operating System** - Required operating system for your project `required`

> **Project Type**: Select `App` to develop a new CLI application, or select `Module` to develop a single pip module

## Specifying Repository Type

At this stage, **CLight** works with 3 types of project repository environments:

- **Local** - Publishing projects from your local development Windows environment to PyPI
- **GitHub** - Automated deployment process to PyPI once you push changes to the main branch
- **GitLab** - Automated deployment process to PyPI once you push changes to the main branch

> **PyPI** is the official third-party package repository for the Python programming language. It hosts and distributes software packages for developers to use. Developers can upload Python packages to PyPI, where they can be easily accessed by others. Anyone can then download them using the `pip install <package>` command

## Specifying License

When creating a project with **CLight**, you can include one of the 8 OSI-Approved license types:

1. MIT License
2. BSD License
3. ISC License (ISCL)
4. Apache Software License
5. Mozilla Public License 2.0 (MPL 2.0)
6. GNU Affero General Public License v3
7. GNU General Public License v3 (GPLv3)
8. GNU Lesser General Public License v3 (LGPLv3)

## Specifying Operating System

When creating a project with **CLight**, you should specify the OS environment for your project:

1. OS Independent
1. Microsoft / Windows
1. POSIX / Linux
1. MacOS

## Deployment

**Before publishing your updated project, according to PyPI rules, you must increase your project's version number:**

1. Navigate to your project's root directory using CMD and run `clight reform`
1. Skip everything else, and only edit the **Version** parameter's value

**Based on your selected Repository Type, the project will be deployed to PyPI in the following ways:**

- **Local** - Publishing projects from your local development Windows environment to PyPI

    - Navigate to your project's root directory using CMD and run `clight publish`
    - If this is your first time, provide your PyPI `PYPI_USERNAME` and `PYPI_API_TOKEN`
    - Then choose whether to save your credentials or not
    - If you choose to save your credentials, provide a `Password Key` to encrypt them
    - That's it. The next time, you will just be asked for the Password Key

- **GitHub** - Automated deployment process to PyPI once you push changes to the main branch

    - Nothing to do, just push the changes

- **GitLab** - Automated deployment process to PyPI once you push changes to the main branch

    - Nothing to do, just push the changes

> **Note:** You must add PyPI credentials as repository secure variables in GitHub and GitLab with these names: `PYPI_USERNAME` and `PYPI_API_TOKEN`
