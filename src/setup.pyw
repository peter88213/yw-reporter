#!/usr/bin/env python3
"""Install the yw-reporter script. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from shutil import copyfile
from pathlib import Path
from tkinter import messagebox
from string import Template

APPNAME = 'yw-reporter'

APP = APPNAME + '.pyw'
INI_FILE = APPNAME + '.ini'
INI_PATH = '/config/'
SAMPLE_PATH = 'sample/'
MESSAGE = '''The $Appname program is installed here:
$Apppath

Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder clicking "Ok", hold down the Alt key on your keyboard, and then drag and drop $Appname.pyw to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 '$Apppath' %F
'''


def run(pywriterPath):
    """Install the script."""

    # Create a general PyWriter installation directory, if necessary.

    os.makedirs(pywriterPath, exist_ok=True)
    installDir = pywriterPath + APPNAME
    cnfDir = installDir + INI_PATH

    try:
        # Move an existing installation to the new place, if necessary.

        oldInstDir = os.getenv('APPDATA').replace('\\', '/') + '/pyWriter/' + APPNAME
        os.replace(oldInstDir, installDir)

    except:
        pass

    os.makedirs(cnfDir, exist_ok=True)

    # Delete the old version, but retain configuration, if any.

    with os.scandir(installDir) as files:

        for file in files:

            if not 'config' in file.name:
                os.remove(file)

    # Install the new version.

    copyfile(APP, installDir + '/' + APP)

    # Install a configuration file, if needed.

    try:
        if not os.path.isfile(cnfDir + INI_FILE):
            copyfile(SAMPLE_PATH + INI_FILE, cnfDir + INI_FILE)

    except:
        pass

    # Display a message and optionally open the installation folder for shortcut creation.

    mapping = {'Appname': APPNAME, 'Apppath': installDir + '/' + APP}

    if messagebox.askokcancel(APPNAME, Template(MESSAGE).safe_substitute(mapping)):
        os.startfile(os.path.normpath(installDir))


if __name__ == '__main__':
    pywriterPath = str(Path.home()).replace('\\', '/') + '/.pywriter/'
    run(pywriterPath)
