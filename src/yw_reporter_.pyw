#!/usr/bin/env python3
"""Configurable reports from yWriter. 

Version @release

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path

from pywriter.config.configuration import Configuration
from pywriter.ui.ui import Ui
from pywriter.file.filter import Filter

from ywreporter.rp_converter import RpConverter
from ywreporter.yw_reporter_tk import YwReporterTk

SUFFIX = '_report'
APPNAME = 'yw-reporter'

SETTINGS = dict(
    yw_last_open='',
    outputSelection=0,
)

OPTIONS = dict(
    showChapters=True,
    showScenes=True,
    showNormalType=True,
    showUnusedType=False,
    showNotesType=False,
    showTodoType=False,
    showUnexported=False,
    showNumber=False,
    showTitle=True,
    showDescription=True,
    showViewpoint=False,
    showTags=False,
    showNotes=False,
    showDate=False,
    showTime=False,
    showDuration=False,
    showActionPattern=False,
    showRatings=False,
    showWordsTotal=False,
    showWordcount=False,
    showLettercount=False,
    showStatus=False,
    showCharacters=False,
    showLocations=False,
    showItems=False,
)


def run(sourcePath, silentMode=True, installDir=''):

    #--- Load configuration

    sourceDir = os.path.dirname(sourcePath)

    if sourceDir == '':
        sourceDir = './'

    else:
        sourceDir += '/'

    iniFile = installDir + APPNAME + '.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = dict(
        suffix=SUFFIX,
        sceneFilter=Filter()
    )
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    converter = RpConverter()

    if silentMode:
        converter.ui = Ui('')
        converter.run(sourcePath, **kwargs)

    else:
        converter.ui = YwReporterTk('yWriter report generator @release', sourcePath=sourcePath, **kwargs)
        converter.ui.converter = converter

        #--- Get initial project path.

        if not sourcePath or not os.path.isfile(sourcePath):
            sourcePath = kwargs['yw_last_open']

        #--- Instantiate the viewer object.

        converter.ui.open_project(sourcePath)
        converter.ui.start()

        #--- Save project specific configuration

        for keyword in converter.ui.kwargs:

            if keyword in configuration.options:
                configuration.options[keyword] = converter.ui.kwargs[keyword]

            elif keyword in configuration.settings:
                configuration.settings[keyword] = converter.ui.kwargs[keyword]

            configuration.write(iniFile)


if __name__ == '__main__':

    try:
        installDir = str(Path.home()).replace('\\', '/') + '/.pywriter/' + APPNAME + '/config/'

    except:
        installDir = ''

    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', False, installDir)

    else:
        parser = argparse.ArgumentParser(
            description='yWriter report generator',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        parser.add_argument('--silent',
                            action="store_true",
                            help='operation without grphical user interface; suppress error messages and the request to confirm overwriting')
        args = parser.parse_args()
        run(args.sourcePath, args.silent, installDir)
