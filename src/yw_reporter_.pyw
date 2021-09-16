#!/usr/bin/env python3
"""Configurable reports from yWriter. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import argparse
from configparser import ConfigParser

from ywreporter.rp_converter import RpConverter
from ywreporter.rp_ui import RpUi

APPNAME = 'yw-reporter'


def run(sourcePath, silentMode=True, installDir='./'):

    if not os.path.isdir(installDir):
        os.makedirs(installDir)

    iniFile = installDir + APPNAME + '.ini'
    config = ConfigParser()

    levels = []
    types = []
    columns = []

    try:
        config.read(iniFile)

        if sourcePath is None:
            sourcePath = config.get('FILES', 'yw_last_open')

            if sourcePath == 'None':
                sourcePath = None

        for i in range(RpUi.levelsTotal):
            levels.append(config.get('LEVELS', str(i)))

        for i in range(RpUi.typesTotal):
            types.append(config.get('TYPES', str(i)))

        for i in range(RpUi.columnsTotal):
            columns.append(config.get('COLUMNS', str(i)))

    except:

        for i in range(RpUi.levelsTotal):
            levels.append(True)

        for i in range(RpUi.typesTotal):
            types.append(False)

        for i in range(RpUi.columnsTotal):
            columns.append(False)

        # Extra Preset: Show "normal"/"Title"/"Description".

        types[0] = True
        columns[1] = True
        columns[2] = True

    #--- Instantiate a user interface object

    ui = RpUi('yWriter report generator @release')

    optionCnt = 0
    ui.ShowChapters.set(levels[optionCnt])
    optionCnt += 1
    ui.ShowScenes.set(levels[optionCnt])

    optionCnt = 0
    ui.ShowNormalType.set(types[optionCnt])
    optionCnt += 1
    ui.ShowUnusedType.set(types[optionCnt])
    optionCnt += 1
    ui.ShowNotesType.set(types[optionCnt])
    optionCnt += 1
    ui.ShowTodoType.set(types[optionCnt])
    optionCnt += 1
    ui.ShowUnexported.set(types[optionCnt])

    optionCnt = 0
    ui.ShowNumber.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowTitle.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowDescription.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowViewpoint.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowTags.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowNotes.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowDate.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowTime.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowDuration.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowActionPattern.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowRatings.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowWordsTotal.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowWordcount.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowLettercount.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowStatus.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowCharacters.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowLocations.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowItems.set(columns[optionCnt])

    if sourcePath is not None:

        if os.path.isfile(sourcePath):
            ui.sourcePath = sourcePath
            ui.set_info_what(
                'File: ' + os.path.normpath(sourcePath))
            ui.root.runButton.config(state='normal')

        else:
            sourcePath = None

    converter = RpConverter()
    # instantiate a converter object

    # Create a bidirectional association between the
    # user interface object and the converter object.

    converter.ui = ui
    # make the user interface's methods visible to the converter

    ui.converter = converter
    # make the converter's methods visible to the user interface

    ui.start()

    #--- Save configuration

    if ui.sourcePath is not None:
        sourcePath = ui.sourcePath

    else:
        sourcePath = 'None'

    if not config.has_section('FILES'):
        config.add_section('FILES')

    config.set('FILES', 'yw_last_open', sourcePath)

    if not config.has_section('LEVELS'):
        config.add_section('LEVELS')

    optionCnt = 0
    config.set('LEVELS', str(optionCnt), str(ui.ShowChapters.get()))
    optionCnt += 1
    config.set('LEVELS', str(optionCnt), str(ui.ShowScenes.get()))

    if not config.has_section('TYPES'):
        config.add_section('TYPES')

    optionCnt = 0
    config.set('TYPES', str(optionCnt), str(ui.ShowNormalType.get()))
    optionCnt += 1
    config.set('TYPES', str(optionCnt), str(ui.ShowUnusedType.get()))
    optionCnt += 1
    config.set('TYPES', str(optionCnt), str(ui.ShowNotesType.get()))
    optionCnt += 1
    config.set('TYPES', str(optionCnt), str(ui.ShowTodoType.get()))
    optionCnt += 1
    config.set('TYPES', str(optionCnt), str(ui.ShowUnexported.get()))

    if not config.has_section('COLUMNS'):
        config.add_section('COLUMNS')

    optionCnt = 0
    config.set('COLUMNS', str(optionCnt), str(ui.ShowNumber.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowTitle.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowDescription.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowViewpoint.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowTags.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowNotes.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowDate.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowTime.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowDuration.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowActionPattern.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowRatings.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowWordsTotal.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowWordcount.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowLettercount.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowStatus.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowCharacters.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowLocations.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowItems.get()))

    with open(iniFile, 'w') as f:
        config.write(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='yWriter report generator',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the yWriter project file.')

    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()
    installDir = os.getenv('APPDATA').replace('\\', '/') + '/pyWriter/' + APPNAME + '/config/'
    run(args.sourcePath, args.silent, installDir)