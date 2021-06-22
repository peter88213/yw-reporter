#!/usr/bin/env python3
"""Configurable reports from yWriter. 

GUI version using tkinter

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2md
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from configparser import ConfigParser
import webbrowser

from ywreporter.html_report import HtmlReport
from ywreporter.rp_converter import RpConverter
from pywriter.ui.ui_tk import UiTk

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

tShowChapters = 'Include chapters'
tShowScenes = 'Include scenes'
levelsTotal = 2
tShowNormalType = 'Include "normal" type'
tShowUnusedType = 'Include "unused" type'
tShowNotesType = 'Include "notes" type'
tShowTodoType = 'Include "to do" type'
tShowUnexported = 'Include "do not export" type'
typesTotal = 5
tShowTitle = 'Title'
tShowDescription = 'Description'
tShowTags = 'Tags'
tShowNotes = 'Notes'
tShowActionPattern = 'A/R-Goal-Conflict-Outcome'
tShowRatings = 'Scene ratings'
tShowWordcount = 'Word count'
tShowLettercount = 'Letter count'
tShowStatus = 'Status'
tShowViewpoint = 'Viewpoint'
tShowCharacters = 'Characters'
tShowLocations = 'Locations'
tShowItems = 'Items'
columnsTotal = 13


class MyGui(UiTk):
    """Extend the Tkinter GUI, 
    and link it to the application.
    """

    def __init__(self, title, description=None):
        """Make the converter object visible to the user interface 
        in order to make method calls possible.
        Add the widgets needed to invoke the converter manually.
        """
        self.converter = None
        self.infoWhatText = ''
        self.infoHowText = ''
        # UiTk.__init__(self, title)

        self.root = Tk()
        self.root.title(title)

        self.hdLevels = Label(self.root, text='Levels')
        self.hdTypes = Label(self.root, text='Types')
        self.hdColumns = Label(self.root, text='Columns')
        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=80)

        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=80)

        self.processInfo = Label(self.root, text='')

        self.ShowChapters = BooleanVar()
        self.ShowScenes = BooleanVar()
        self.ShowNormalType = BooleanVar()
        self.ShowUnusedType = BooleanVar()
        self.ShowNotesType = BooleanVar()
        self.ShowTodoType = BooleanVar()
        self.ShowUnexported = BooleanVar()
        self.ShowTitle = BooleanVar()
        self.ShowDescription = BooleanVar()
        self.ShowViewpoint = BooleanVar()
        self.ShowTags = BooleanVar()
        self.ShowNotes = BooleanVar()
        self.ShowActionPattern = BooleanVar()
        self.ShowRatings = BooleanVar()
        self.ShowWordcount = BooleanVar()
        self.ShowLettercount = BooleanVar()
        self.ShowStatus = BooleanVar()
        self.ShowCharacters = BooleanVar()
        self.ShowLocations = BooleanVar()
        self.ShowItems = BooleanVar()

        self.root.ShowChaptersCheckbox = ttk.Checkbutton(
            text=tShowChapters, variable=self.ShowChapters, onvalue=True, offvalue=False)
        self.root.ShowScenesCheckbox = ttk.Checkbutton(
            text=tShowScenes, variable=self.ShowScenes, onvalue=True, offvalue=False)
        self.root.ShowNormalTypeCheckbox = ttk.Checkbutton(
            text=tShowNormalType, variable=self.ShowNormalType, onvalue=True, offvalue=False)
        self.root.ShowUnusedTypeCheckbox = ttk.Checkbutton(
            text=tShowUnusedType, variable=self.ShowUnusedType, onvalue=True, offvalue=False)
        self.root.ShowNotesTypeCheckbox = ttk.Checkbutton(
            text=tShowNotesType, variable=self.ShowNotesType, onvalue=True, offvalue=False)
        self.root.ShowTodoTypeCheckbox = ttk.Checkbutton(
            text=tShowTodoType, variable=self.ShowTodoType, onvalue=True, offvalue=False)
        self.root.ShowUnexportedCheckbox = ttk.Checkbutton(
            text=tShowUnexported, variable=self.ShowUnexported, onvalue=True, offvalue=False)
        self.root.ShowTitleCheckbox = ttk.Checkbutton(
            text=tShowTitle, variable=self.ShowTitle, onvalue=True, offvalue=False)
        self.root.ShowDescriptionCheckbox = ttk.Checkbutton(
            text=tShowDescription, variable=self.ShowDescription, onvalue=True, offvalue=False)
        self.root.ShowViewpointCheckbox = ttk.Checkbutton(
            text=tShowViewpoint, variable=self.ShowViewpoint, onvalue=True, offvalue=False)
        self.root.ShowTagsCheckbox = ttk.Checkbutton(
            text=tShowTags, variable=self.ShowTags, onvalue=True, offvalue=False)
        self.root.ShowNotesCheckbox = ttk.Checkbutton(
            text=tShowNotes, variable=self.ShowNotes, onvalue=True, offvalue=False)
        self.root.ShowActionPatternCheckbox = ttk.Checkbutton(
            text=tShowActionPattern, variable=self.ShowActionPattern, onvalue=True, offvalue=False)
        self.root.ShowRatingsCheckbox = ttk.Checkbutton(
            text=tShowRatings, variable=self.ShowRatings, onvalue=True, offvalue=False)
        self.root.ShowWordcountCheckbox = ttk.Checkbutton(
            text=tShowWordcount, variable=self.ShowWordcount, onvalue=True, offvalue=False)
        self.root.ShowLettercountCheckbox = ttk.Checkbutton(
            text=tShowLettercount, variable=self.ShowLettercount, onvalue=True, offvalue=False)
        self.root.ShowStatusCheckbox = ttk.Checkbutton(
            text=tShowStatus, variable=self.ShowStatus, onvalue=True, offvalue=False)
        self.root.ShowCharactersCheckbox = ttk.Checkbutton(
            text=tShowCharacters, variable=self.ShowCharacters, onvalue=True, offvalue=False)
        self.root.ShowLocationsCheckbox = ttk.Checkbutton(
            text=tShowLocations, variable=self.ShowLocations, onvalue=True, offvalue=False)
        self.root.ShowItemsCheckbox = ttk.Checkbutton(
            text=tShowItems, variable=self.ShowItems, onvalue=True, offvalue=False)

        self.root.selectButton = Button(
            text="Select file", command=self.select_file)
        self.root.selectButton.config(height=1, width=10)

        self.root.runButton = Button(text='Convert', command=self.convert_file)
        self.root.runButton.config(height=1, width=10)
        self.root.runButton.config(state='disabled')

        self.root.quitButton = Button(text='Quit', command=self.stop)
        self.root.quitButton.config(height=1, width=10)

        rowCnt = 1
        self.hdLevels.grid(row=rowCnt, column=1, sticky=W,
                           padx=20)
        rowCnt += 1
        self.root.ShowChaptersCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowScenesCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)

        rowCnt = 1
        self.hdTypes.grid(row=rowCnt, column=2, sticky=W,
                          padx=20)
        rowCnt += 1
        self.root.ShowNormalTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowUnusedTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowNotesTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowTodoTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowUnexportedCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)

        rowCnt = 1
        self.hdColumns.grid(row=rowCnt, column=3, sticky=W,
                            padx=20)
        rowCnt += 1
        self.root.ShowTitleCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowDescriptionCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowViewpointCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowTagsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowNotesCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowActionPatternCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowRatingsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowWordcountCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowLettercountCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowStatusCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowCharactersCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowLocationsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowItemsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)

        rowCnt += 1
        self.appInfo.grid(row=rowCnt, column=1,
                          columnspan=3, pady=10)

        rowCnt += 1
        self.root.selectButton.grid(row=rowCnt, column=1, pady=10)
        self.root.runButton.grid(row=rowCnt, column=2, pady=10)
        self.root.quitButton.grid(row=rowCnt, column=3, pady=10)

        rowCnt += 1
        self.successInfo.grid(row=rowCnt, column=1, columnspan=3)

        rowCnt += 1
        self.processInfo.grid(row=rowCnt, column=1,
                              columnspan=3, pady=10)

        self.sourcePath = None
        self.set_info_what('No file selected')
        self.startDir = os.getcwd()

    def start(self):
        """Start the user interface.
        Note: This can not be done in the __init__() method.
        """
        self.root.mainloop()

    def stop(self):
        """Stop the user interface.
        """
        self.root.destroy()

    def select_file(self):
        """Open a file dialog in order to set the sourcePath property.
        """
        self.processInfo.config(text='')
        self.successInfo.config(
            bg=self.root.cget("background"))

        if self.sourcePath is not None:
            self.startDir = os.path.dirname(self.sourcePath)

        file = filedialog.askopenfile(initialdir=self.startDir)

        if file:
            self.sourcePath = file.name

        if self.sourcePath:
            self.set_info_what(
                'File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self.set_info_what('No file selected')
            self.root.runButton.config(state='disabled')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self.processInfo.config(text='')
        self.successInfo.config(
            bg=self.root.cget("background"))

        options = [False, True]

        if self.sourcePath:
            kwargs = {'suffix': HtmlReport.SUFFIX,
                      'showChapters': self.ShowChapters.get(),
                      'showScenes': self.ShowScenes.get(),
                      'showNormalType': self.ShowNormalType.get(),
                      'showUnusedType': self.ShowUnusedType.get(),
                      'showNotesType': self.ShowNotesType.get(),
                      'showTodoType': self.ShowTodoType.get(),
                      'showUnexported': self.ShowUnexported.get(),
                      'showTitle': self.ShowTitle.get(),
                      'showDescription': self.ShowDescription.get(),
                      'showViewpoint': self.ShowViewpoint.get(),
                      'showTags': self.ShowTags.get(),
                      'showNotes': self.ShowNotes.get(),
                      'showActionPattern': self.ShowActionPattern.get(),
                      'showRatings': self.ShowRatings.get(),
                      'showWordcount': self.ShowWordcount.get(),
                      'showLettercount': self.ShowLettercount.get(),
                      'showStatus': self.ShowStatus.get(),
                      'showCharacters': self.ShowCharacters.get(),
                      'showLocations': self.ShowLocations.get(),
                      'showItems': self.ShowItems.get(),
                      }
            self.converter.run(self.sourcePath, **kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)


def run(sourcePath):

    #--- Try to get persistent configuration data

    iniPath = os.getenv('APPDATA').replace('\\', '/') + '/yw-reporter'

    if not os.path.isdir(iniPath):
        os.makedirs(iniPath)

    iniFile = iniPath + '/yw-reporter.ini'
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

        for i in range(levelsTotal):
            levels.append(config.get('LEVELS', str(i)))

        for i in range(typesTotal):
            types.append(config.get('TYPES', str(i)))

        for i in range(columnsTotal):
            columns.append(config.get('COLUMNS', str(i)))

    except:

        for i in range(levelsTotal):
            levels.append(True)

        for i in range(typesTotal):
            types.append(False)

        for i in range(columnsTotal):
            columns.append(False)

        types[0] = True
        columns[0] = True
        columns[1] = True

    #--- Instantiate a user interface object

    ui = MyGui('yWriter report')

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
    ui.ShowActionPattern.set(columns[optionCnt])
    optionCnt += 1
    ui.ShowRatings.set(columns[optionCnt])
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
    config.set('COLUMNS', str(optionCnt), str(ui.ShowActionPattern.get()))
    optionCnt += 1
    config.set('COLUMNS', str(optionCnt), str(ui.ShowRatings.get()))
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

    try:
        sourcePath = sys.argv[1].replace('\\', '/')

    except:
        sourcePath = None

    run(sourcePath)
