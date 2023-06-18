#!/usr/bin/env python3
# ------------------------------------------------
#
#                 SSH MANAGER
#               (c) Pau Gasull
#                 25/05/2024
#
# ------------------------------------------------

# --INCLUDES-- #
import os
from pathlib import Path


# --CLASSES-- #
class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    italic = '\033[03m'

    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    light_grey = '\033[37m'
    dark_grey = '\033[90m'
    light_red = '\033[91m'
    light_green = '\033[92m'
    yellow = '\033[93m'
    light_blue = '\033[94m'
    pink = '\033[95m'
    light_cyan = '\033[96m'


class LineCursor:
    up = '\u001b[1A'
    down = '\u001b[1B'


# --CONSTANTS-- #
HOME_PATH = os.path.expanduser('~')
FILES_PATH = f'{HOME_PATH}/SSHConn'
EXIT_OPTION = -1

# --VARIABLES-- #
maxOptions = 0


# --FUNCTIONS-- #
def create_connection():
    connection_name = input(f"Enter the{Colors.bold} Connection Name {Colors.reset}: ")
    print(f"{LineCursor.up}Enter the Connection Name {Colors.reset}: "
          f"{Colors.underline}{connection_name}{Colors.reset}")

    connection_host = input(f"Enter the{Colors.bold} Connection Host {Colors.reset}: ")
    print(f"{LineCursor.up}Enter the Connection Host {Colors.reset}: "
          f"{Colors.underline}{connection_host}{Colors.reset}")

    connection_user = input(f"Enter the{Colors.bold} Connection User {Colors.reset}: ")
    print(f"{LineCursor.up}Enter the Connection User {Colors.reset}: "
          f"{Colors.underline}{connection_user}{Colors.reset}")

    connection_pass = input(f"Enter the{Colors.bold} Connection Password {Colors.reset}: ")
    print(f"{LineCursor.up}Enter the Connection Password {Colors.reset}: {Colors.underline}"
          + "*" * len(connection_pass) + f"{Colors.reset}")

    f = open(f"{FILES_PATH}/{connection_name}.py", "a")
    f.write("import os \n")
    f.write(f"hostname = \"{connection_host}\" \nuser = \"{connection_user}\" \npassw = \"{connection_pass}\" \n")
    f.write("os.system(f\"sshpass -p {passw} ssh {user}@{hostname}\")")
    f.close()

    print(f"{Colors.cyan}   ## Connecting to {connection_host} ##")
    print(f"{Colors.dark_grey}{Colors.italic}   You'll need to enter your password to make sure "
          f"you're able to enter the server{Colors.reset}")

    os.system(f"ssh {connection_user}@{connection_host}")


def start_connection(connectionID: int):
    counter = 0
    file_name = None
    for element in os.listdir(FILES_PATH):
        if os.path.isfile(os.path.join(FILES_PATH, element)):
            counter = counter + 1
            if counter == connectionID:
                file_name = Path(element)
                break
    with open(f"{FILES_PATH}/{file_name}") as f:
        exec(f.read())


# --MAIN-- #
# install SSH Pass
if os.system("which sshpass") == "":
    print(f"{Colors.green}Installing SSHPass {Colors.reset}")
    os.system("apt-get install sshpass")

print(f"{LineCursor.up}{Colors.light_grey} /|>~----··MENU··----~<|\\ {Colors.reset}")
print(f"{Colors.yellow}[{maxOptions}]-> Add new SSH Connection {Colors.reset}")

for path in os.listdir(FILES_PATH):
    if os.path.isfile(os.path.join(FILES_PATH, path)):
        maxOptions += 1
        print(f"{Colors.green}[{maxOptions}]-> {Path(path).stem} {Colors.reset}")

maxOptions += 1
print(f"{Colors.blue}[{maxOptions}]-> Open Folder {Colors.reset}")
print(f"{Colors.light_red}[{EXIT_OPTION}]-> Exit {Colors.reset}")

print("")
option = None

while option is None:
    try:
        option = int(input("Enter Option ["))

        if option < EXIT_OPTION or option > maxOptions:
            option = None
            raise ValueError()
    except ValueError:
        print(f"{LineCursor.up}{Colors.red}ERROR: NOT A VALID OPTION! {Colors.reset}")

print(f"{LineCursor.up}{Colors.dark_grey}Enter Option [{option}] {Colors.reset}")

if option == maxOptions:  # open folder
    os.system('xdg-open "%s"' % FILES_PATH)
elif option == 0:  # create a new SSH Connection
    create_connection()
elif option > -1:  # connect
    start_connection(option)
