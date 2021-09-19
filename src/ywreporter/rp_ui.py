"""Provide a user interface for the reporter: Tkinter facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from pywriter.ui.ui_tk import UiTk
from ywreporter.html_report import HtmlReport
from pywriter.file.filter import Filter
from pywriter.file.sc_tg_filter import ScTgFilter
from pywriter.file.sc_vp_filter import ScVpFilter
from pywriter.file.sc_cr_filter import ScCrFilter
from pywriter.file.sc_lc_filter import ScLcFilter
from pywriter.file.sc_it_filter import ScItFilter

from pywriter.yw.yw7_file import Yw7File


class RpUi(UiTk):
    """Extend the Tkinter GUI, 
    and link it to the application.
    """

    tShowChapters = 'Include chapters'
    tShowScenes = 'Include scenes'
    levelsTotal = 2
    tShowNormalType = 'Include "normal" type'
    tShowUnusedType = 'Include "unused" type'
    tShowNotesType = 'Include "notes" type'
    tShowTodoType = 'Include "to do" type'
    tShowUnexported = 'Include "do not export" type'
    typesTotal = 5
    tShowNumber = 'Number'
    tShowTitle = 'Title'
    tShowDescription = 'Description'
    tShowTags = 'Tags'
    tShowNotes = 'Notes'
    tShowDate = 'Date'
    tShowTime = 'Time'
    tShowDuration = 'Duration'
    tShowActionPattern = 'A/R-Goal-Conflict-Outcome'
    tShowRatings = 'Scene ratings'
    tShowWordsTotal = 'Words total'
    tShowWordcount = 'Word count'
    tShowLettercount = 'Letter count'
    tShowStatus = 'Status'
    tShowViewpoint = 'Viewpoint'
    tShowCharacters = 'Characters'
    tShowLocations = 'Locations'
    tShowItems = 'Items'
    columnsTotal = 18
    tNone = 'None'
    tTags = 'Tag'
    tViewpoints = 'Viewpoint'
    tCharacters = 'Character'
    tLocations = 'Location'
    tItems = 'Item'
    filtersTotal = 6
    tHtml = 'HTML'
    tCsv = 'CSV'

    def __init__(self, title, description=None, sourcePath=None, **kwargs):
        """Make the converter object visible to the user interface 
        in order to make method calls possible.
        Add the widgets needed to invoke the converter manually.
        """
        self.kwargs = kwargs
        self.tags = []
        self.viewpoints = []
        self.vpIds = []
        self.characters = []
        self.crIds = []
        self.locations = []
        self.lcIds = []
        self.items = []
        self.itIds = []
        self.filterCat = []

        self.converter = None
        self.infoWhatText = ''
        self.infoHowText = ''
        # UiTk.__init__(self, title)

        self.root = Tk()
        self.root.title(title)

        self.hdLevels = Label(self.root, text='Levels')
        self.hdTypes = Label(self.root, text='Types')
        self.hdFilters = Label(self.root, text='Filter')
        self.hdColumns = Label(self.root, text='Columns')
        self.hdOutput = Label(self.root, text='Output')
        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=80)

        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=80)

        self.processInfo = Label(self.root, text='')

        self.showChapters = BooleanVar(value=kwargs['showChapters'])
        self.showScenes = BooleanVar(value=kwargs['showScenes'])
        self.showNormalType = BooleanVar(value=kwargs['showNormalType'])
        self.showUnusedType = BooleanVar(value=kwargs['showUnusedType'])
        self.showNotesType = BooleanVar(value=kwargs['showNotesType'])
        self.showTodoType = BooleanVar(value=kwargs['showTodoType'])
        self.showUnexported = BooleanVar(value=kwargs['showUnexported'])

        self.showNumber = BooleanVar(value=kwargs['showNumber'])
        self.showTitle = BooleanVar(value=kwargs['showTitle'])
        self.showDescription = BooleanVar(value=kwargs['showDescription'])
        self.showViewpoint = BooleanVar(value=kwargs['showViewpoint'])
        self.showTags = BooleanVar(value=kwargs['showTags'])
        self.showNotes = BooleanVar(value=kwargs['showNotes'])
        self.showDate = BooleanVar(value=kwargs['showDate'])
        self.showTime = BooleanVar(value=kwargs['showTime'])
        self.showDuration = BooleanVar(value=kwargs['showDuration'])
        self.showActionPattern = BooleanVar(value=kwargs['showActionPattern'])
        self.showRatings = BooleanVar(value=kwargs['showRatings'])
        self.showWordsTotal = BooleanVar(value=kwargs['showWordsTotal'])
        self.showWordcount = BooleanVar(value=kwargs['showWordcount'])
        self.showLettercount = BooleanVar(value=kwargs['showLettercount'])
        self.showStatus = BooleanVar(value=kwargs['showStatus'])
        self.showCharacters = BooleanVar(value=kwargs['showCharacters'])
        self.showLocations = BooleanVar(value=kwargs['showLocations'])
        self.showItems = BooleanVar(value=kwargs['showItems'])
        self.filterCatSelection = IntVar()
        self.outputSelection = IntVar(value=kwargs['outputSelection'])

        self.root.ShowChaptersCheckbox = ttk.Checkbutton(
            text=self.tShowChapters, variable=self.showChapters, onvalue=True, offvalue=False)
        self.root.ShowScenesCheckbox = ttk.Checkbutton(
            text=self.tShowScenes, variable=self.showScenes, onvalue=True, offvalue=False)
        self.root.ShowNormalTypeCheckbox = ttk.Checkbutton(
            text=self.tShowNormalType, variable=self.showNormalType, onvalue=True, offvalue=False)
        self.root.ShowUnusedTypeCheckbox = ttk.Checkbutton(
            text=self.tShowUnusedType, variable=self.showUnusedType, onvalue=True, offvalue=False)
        self.root.ShowNotesTypeCheckbox = ttk.Checkbutton(
            text=self.tShowNotesType, variable=self.showNotesType, onvalue=True, offvalue=False)
        self.root.ShowTodoTypeCheckbox = ttk.Checkbutton(
            text=self.tShowTodoType, variable=self.showTodoType, onvalue=True, offvalue=False)
        self.root.ShowUnexportedCheckbox = ttk.Checkbutton(
            text=self.tShowUnexported, variable=self.showUnexported, onvalue=True, offvalue=False)

        self.root.ShowNumberCheckbox = ttk.Checkbutton(
            text=self.tShowNumber, variable=self.showNumber, onvalue=True, offvalue=False)
        self.root.ShowTitleCheckbox = ttk.Checkbutton(
            text=self.tShowTitle, variable=self.showTitle, onvalue=True, offvalue=False)
        self.root.ShowDescriptionCheckbox = ttk.Checkbutton(
            text=self.tShowDescription, variable=self.showDescription, onvalue=True, offvalue=False)
        self.root.ShowViewpointCheckbox = ttk.Checkbutton(
            text=self.tShowViewpoint, variable=self.showViewpoint, onvalue=True, offvalue=False)
        self.root.ShowTagsCheckbox = ttk.Checkbutton(
            text=self.tShowTags, variable=self.showTags, onvalue=True, offvalue=False)
        self.root.ShowNotesCheckbox = ttk.Checkbutton(
            text=self.tShowNotes, variable=self.showNotes, onvalue=True, offvalue=False)
        self.root.ShowDateCheckbox = ttk.Checkbutton(
            text=self.tShowDate, variable=self.showDate, onvalue=True, offvalue=False)
        self.root.ShowTimeCheckbox = ttk.Checkbutton(
            text=self.tShowTime, variable=self.showTime, onvalue=True, offvalue=False)
        self.root.ShowDurationCheckbox = ttk.Checkbutton(
            text=self.tShowDuration, variable=self.showDuration, onvalue=True, offvalue=False)
        self.root.ShowActionPatternCheckbox = ttk.Checkbutton(
            text=self.tShowActionPattern, variable=self.showActionPattern, onvalue=True, offvalue=False)
        self.root.ShowRatingsCheckbox = ttk.Checkbutton(
            text=self.tShowRatings, variable=self.showRatings, onvalue=True, offvalue=False)
        self.root.ShowWordsTotalCheckbox = ttk.Checkbutton(
            text=self.tShowWordsTotal, variable=self.showWordsTotal, onvalue=True, offvalue=False)
        self.root.ShowWordcountCheckbox = ttk.Checkbutton(
            text=self.tShowWordcount, variable=self.showWordcount, onvalue=True, offvalue=False)
        self.root.ShowLettercountCheckbox = ttk.Checkbutton(
            text=self.tShowLettercount, variable=self.showLettercount, onvalue=True, offvalue=False)
        self.root.ShowStatusCheckbox = ttk.Checkbutton(
            text=self.tShowStatus, variable=self.showStatus, onvalue=True, offvalue=False)
        self.root.ShowCharactersCheckbox = ttk.Checkbutton(
            text=self.tShowCharacters, variable=self.showCharacters, onvalue=True, offvalue=False)
        self.root.ShowLocationsCheckbox = ttk.Checkbutton(
            text=self.tShowLocations, variable=self.showLocations, onvalue=True, offvalue=False)
        self.root.ShowItemsCheckbox = ttk.Checkbutton(
            text=self.tShowItems, variable=self.showItems, onvalue=True, offvalue=False)

        self.root.NoneCheckbox = ttk.Radiobutton(
            text=self.tNone, variable=self.filterCatSelection, value=0, command=lambda: self.set_filter_category(0))
        self.root.TagsCheckbox = ttk.Radiobutton(
            text=self.tTags, variable=self.filterCatSelection, value=1, command=lambda: self.set_filter_category(1))
        self.root.ViewpointsCheckbox = ttk.Radiobutton(
            text=self.tViewpoints, variable=self.filterCatSelection, value=2, command=lambda: self.set_filter_category(2))
        self.root.CharactersCheckbox = ttk.Radiobutton(
            text=self.tCharacters, variable=self.filterCatSelection, value=3, command=lambda: self.set_filter_category(3))
        self.root.LocationsCheckbox = ttk.Radiobutton(
            text=self.tLocations, variable=self.filterCatSelection, value=4, command=lambda: self.set_filter_category(4))
        self.root.ItemsCheckbox = ttk.Radiobutton(
            text=self.tItems, variable=self.filterCatSelection, value=5, command=lambda: self.set_filter_category(5))

        self.root.filterCombobox = ttk.Combobox(values=[])

        self.root.htmlCheckbox = ttk.Radiobutton(
            text=self.tHtml, variable=self.outputSelection, value=0)

        self.root.csvCheckbox = ttk.Radiobutton(
            text=self.tCsv, variable=self.outputSelection, value=1)

        self.root.selectButton = Button(text="Select file", command=self.select_file)
        self.root.selectButton.config(height=1, width=20)

        self.root.runButton = Button(text='Create report', command=self.convert_file)
        self.root.runButton.config(height=1, width=20)
        self.root.runButton.config(state='disabled')

        self.root.quitButton = Button(text='Quit', command=self.stop)
        self.root.quitButton.config(height=1, width=20)

        row1Cnt = 1
        self.hdLevels.grid(row=row1Cnt, column=1, sticky=W, padx=20)

        row1Cnt += 1
        self.root.ShowChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)
        row1Cnt += 1
        self.root.ShowScenesCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)

        row2Cnt = 1
        self.hdTypes.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row2Cnt += 1
        self.root.ShowNormalTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ShowUnusedTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ShowNotesTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ShowTodoTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ShowUnexportedCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row2Cnt += 2
        self.hdFilters.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.NoneCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.TagsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ViewpointsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.CharactersCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.LocationsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.ItemsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.filterCombobox.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row2Cnt += 2
        self.hdOutput.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.htmlCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.csvCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row3Cnt = 1
        self.hdColumns.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowNumberCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowTitleCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowDescriptionCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowViewpointCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowTagsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowNotesCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowDateCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowTimeCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowDurationCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowActionPatternCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowRatingsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowWordsTotalCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowWordcountCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowLettercountCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowStatusCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowCharactersCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowLocationsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.ShowItemsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)

        if row3Cnt > row2Cnt:
            rowCnt = row3Cnt

        else:
            rowCnt = row2Cnt

        if row1Cnt > rowCnt:
            rowCnt = row1Cnt

        rowCnt += 1
        self.appInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        rowCnt += 1
        self.root.selectButton.grid(row=rowCnt, column=1, padx=10, pady=10, sticky=W)
        self.root.runButton.grid(row=rowCnt, column=2, padx=10, pady=10, sticky=E)
        self.root.quitButton.grid(row=rowCnt, column=3, padx=10, pady=10, sticky=E)

        rowCnt += 1
        self.successInfo.grid(row=rowCnt, column=1, columnspan=3)

        rowCnt += 1
        self.processInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        self.sourcePath = None

        if kwargs['yw_last_open']:

            if os.path.isfile(kwargs['yw_last_open']):
                self.sourcePath = kwargs['yw_last_open']

        if sourcePath:

            if os.path.isfile(sourcePath):
                self.sourcePath = sourcePath

        if self.sourcePath is not None:
            self.set_info_what('File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self._sourcePath = None
            self.set_info_what('No file selected')
            self.startDir = os.getcwd()

    @property
    def sourcePath(self):
        return self._sourcePath

    @sourcePath.setter
    def sourcePath(self, path):
        """Set sourcePath updating the filter selector lists."""

        self.locations = []
        self.items = []

        # Build filter selector lists.

        if path is not None:
            novel = Yw7File(path)

            if novel.file_exists():
                novel.read()

                # Build tag and viewpoint list.

                self.tags = []
                self.vpIds = []
                self.viewpoints = []
                self.crIds = []
                self.characters = []
                self.lcIds = []
                self.locations = []
                self.itIds = []
                self.items = []

                for chId in novel.srtChapters:

                    for scId in novel.chapters[chId].srtScenes:

                        if novel.scenes[scId].tags:

                            for tag in novel.scenes[scId].tags:

                                if not tag in self.tags:
                                    self.tags.append(tag)

                        if novel.scenes[scId].characters:
                            vpId = novel.scenes[scId].characters[0]

                            if not vpId in self.vpIds:
                                self.vpIds.append(vpId)
                                self.viewpoints.append(
                                    novel.characters[vpId].title)

                            for crId in novel.scenes[scId].characters:

                                if not crId in self.crIds:
                                    self.crIds.append(crId)
                                    self.characters.append(
                                        novel.characters[crId].title)

                        if novel.scenes[scId].locations:

                            for lcId in novel.scenes[scId].locations:

                                if not lcId in self.lcIds:
                                    self.lcIds.append(lcId)
                                    self.locations.append(
                                        novel.locations[lcId].title)

                        if novel.scenes[scId].items:

                            for itId in novel.scenes[scId].items:

                                if not itId in self.itIds:
                                    self.itIds.append(itId)
                                    self.items.append(
                                        novel.items[itId].title)

            del novel

        # Initialize the filter category selection widgets.

        self.filterCat = [[], self.tags, self.viewpoints,
                          self.characters, self.locations, self.items]
        self.set_filter_category(0)
        self.filterCatSelection.set(0)

        self._sourcePath = path

    def start(self):
        """Start the user interface.
        Note: This can not be done in the __init__() method.
        """
        self.root.mainloop()

    def stop(self):
        """Stop the user interface.
        """
        self.root.destroy()

    def set_filter_category(self, selection):
        options = self.filterCat[selection]
        self.root.filterCombobox['values'] = options

        if options:
            self.root.filterCombobox.set(options[0])

        else:
            self.root.filterCombobox.set('')

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

        # Filter options.

        filterCat = self.filterCatSelection.get()
        option = self.root.filterCombobox.current()

        if filterCat == 0:
            sceneFilter = Filter()

        elif filterCat == 1:
            sceneFilter = ScTgFilter(self.tags[option])

        elif filterCat == 2:
            sceneFilter = ScVpFilter(self.vpIds[option])

        elif filterCat == 3:
            sceneFilter = ScCrFilter(self.crIds[option])

        elif filterCat == 4:
            sceneFilter = ScLcFilter(self.lcIds[option])

        elif filterCat == 5:
            sceneFilter = ScItFilter(self.itIds[option])

        if self.sourcePath:
            self.kwargs = dict(
                yw_last_open=self.sourcePath,
                outputSelection=str(self.outputSelection.get()),
                suffix=HtmlReport.SUFFIX,
                sceneFilter=sceneFilter,
                showChapters=self.showChapters.get(),
                showScenes=self.showScenes.get(),
                showNormalType=self.showNormalType.get(),
                showUnusedType=self.showUnusedType.get(),
                showNotesType=self.showNotesType.get(),
                showTodoType=self.showTodoType.get(),
                showUnexported=self.showUnexported.get(),
                showNumber=self.showNumber.get(),
                showTitle=self.showTitle.get(),
                showDescription=self.showDescription.get(),
                showViewpoint=self.showViewpoint.get(),
                showTags=self.showTags.get(),
                showNotes=self.showNotes.get(),
                showDate=self.showDate.get(),
                showTime=self.showTime.get(),
                showDuration=self.showDuration.get(),
                showActionPattern=self.showActionPattern.get(),
                showRatings=self.showRatings.get(),
                showWordsTotal=self.showWordsTotal.get(),
                showWordcount=self.showWordcount.get(),
                showLettercount=self.showLettercount.get(),
                showStatus=self.showStatus.get(),
                showCharacters=self.showCharacters.get(),
                showLocations=self.showLocations.get(),
                showItems=self.showItems.get(),
            )
            self.converter.run(self.sourcePath, **self.kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)
