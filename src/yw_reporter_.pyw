#!/usr/bin/env python3
"""Configurable reports from yWriter. 

Version @release
Requires Python 3.6+
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
from ywreporterlib.rp_converter import RpConverter
from ywreporterlib.yw_reporter_tk import YwReporterTk

SUFFIX = '_report'
APPNAME = 'yw-reporter'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='',
    key_restore_status='<Escape>',
    key_open_project='<Control-o>',
    key_quit_program='<Control-q>',
    output_selection=0,
)
OPTIONS = dict(
    show_chapters=True,
    show_scenes=True,
    show_normal_type=True,
    show_unused_type=False,
    show_notes_type=False,
    show_todo_type=False,
    show_unexported=False,
    show_number=False,
    show_title=True,
    show_description=True,
    show_viewpoint=False,
    show_tags=False,
    show_notes=False,
    show_date=False,
    show_time=False,
    show_duration=False,
    show_action_pattern=False,
    show_ratings=False,
    show_words_total=False,
    show_wordcount=False,
    show_lettercount=False,
    show_status=False,
    show_characters=False,
    show_locations=False,
    show_items=False,
)


def run(sourcePath, silentMode=True, installDir='.'):

    #--- Load configuration
    iniFile = f'{installDir}/{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = dict(
        suffix=SUFFIX,
        scene_filter=Filter()
    )
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter = RpConverter()
    if silentMode:
        converter.ui = Ui('')
        converter.run(sourcePath, **kwargs)
    else:
        converter.ui = YwReporterTk('yWriter report generator @release', **kwargs)
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
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config'
    except:
        installDir = '.'
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
