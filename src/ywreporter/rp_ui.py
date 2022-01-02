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
    """Tkinter based GUI.
    Extend the superclass.
    """

    def __init__(self, title, sourcePath=None, **kwargs):
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

        self.root = Tk()
        self.root.title(title)

        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=80)
        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=80)
        self.processInfo = Label(self.root, text='')

        self.hdLevels = Label(self.root, text='Levels')
        self.showChapters = BooleanVar(value=kwargs['showChapters'])
        self.showScenes = BooleanVar(value=kwargs['showScenes'])

        self.hdTypes = Label(self.root, text='Types')
        self.showNormalType = BooleanVar(value=kwargs['showNormalType'])
        self.showUnusedType = BooleanVar(value=kwargs['showUnusedType'])
        self.showNotesType = BooleanVar(value=kwargs['showNotesType'])
        self.showTodoType = BooleanVar(value=kwargs['showTodoType'])
        self.showUnexported = BooleanVar(value=kwargs['showUnexported'])

        self.hdColumns = Label(self.root, text='Columns')
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

        self.hdFilters = Label(self.root, text='Filter')
        self.filterCatSelection = IntVar()

        self.hdOutput = Label(self.root, text='Output')
        self.outputSelection = IntVar(value=kwargs['outputSelection'])

        self.root.showChaptersCheckbox = ttk.Checkbutton(
            text='Include chapters', variable=self.showChapters, onvalue=True, offvalue=False)
        self.root.showScenesCheckbox = ttk.Checkbutton(
            text='Include scenes', variable=self.showScenes, onvalue=True, offvalue=False)
        self.root.showNormalTypeCheckbox = ttk.Checkbutton(
            text='Include "normal" type', variable=self.showNormalType, onvalue=True, offvalue=False)
        self.root.showUnusedTypeCheckbox = ttk.Checkbutton(
            text='Include "unused" type', variable=self.showUnusedType, onvalue=True, offvalue=False)
        self.root.showNotesTypeCheckbox = ttk.Checkbutton(
            text='Include "notes" type', variable=self.showNotesType, onvalue=True, offvalue=False)
        self.root.showTodoTypeCheckbox = ttk.Checkbutton(
            text='Include "to do" type', variable=self.showTodoType, onvalue=True, offvalue=False)
        self.root.showUnexportedCheckbox = ttk.Checkbutton(
            text='Include "do not export" type', variable=self.showUnexported, onvalue=True, offvalue=False)

        self.root.showNumberCheckbox = ttk.Checkbutton(
            text='Number', variable=self.showNumber, onvalue=True, offvalue=False)
        self.root.showTitleCheckbox = ttk.Checkbutton(
            text='Title', variable=self.showTitle, onvalue=True, offvalue=False)
        self.root.showDescriptionCheckbox = ttk.Checkbutton(
            text='Description', variable=self.showDescription, onvalue=True, offvalue=False)
        self.root.showViewpointCheckbox = ttk.Checkbutton(
            text='Viewpoint', variable=self.showViewpoint, onvalue=True, offvalue=False)
        self.root.showTagsCheckbox = ttk.Checkbutton(
            text='Tags', variable=self.showTags, onvalue=True, offvalue=False)
        self.root.showNotesCheckbox = ttk.Checkbutton(
            text='Notes', variable=self.showNotes, onvalue=True, offvalue=False)
        self.root.showDateCheckbox = ttk.Checkbutton(
            text='Date', variable=self.showDate, onvalue=True, offvalue=False)
        self.root.showTimeCheckbox = ttk.Checkbutton(
            text='Time', variable=self.showTime, onvalue=True, offvalue=False)
        self.root.showDurationCheckbox = ttk.Checkbutton(
            text='Duration', variable=self.showDuration, onvalue=True, offvalue=False)
        self.root.showActionPatternCheckbox = ttk.Checkbutton(
            text='A/R-Goal-Conflict-Outcome', variable=self.showActionPattern, onvalue=True, offvalue=False)
        self.root.showRatingsCheckbox = ttk.Checkbutton(
            text='Scene ratings', variable=self.showRatings, onvalue=True, offvalue=False)
        self.root.showWordsTotalCheckbox = ttk.Checkbutton(
            text='Words total', variable=self.showWordsTotal, onvalue=True, offvalue=False)
        self.root.showWordcountCheckbox = ttk.Checkbutton(
            text='Word count', variable=self.showWordcount, onvalue=True, offvalue=False)
        self.root.showLettercountCheckbox = ttk.Checkbutton(
            text='Letter count', variable=self.showLettercount, onvalue=True, offvalue=False)
        self.root.showStatusCheckbox = ttk.Checkbutton(
            text='Status', variable=self.showStatus, onvalue=True, offvalue=False)
        self.root.showCharactersCheckbox = ttk.Checkbutton(
            text='Characters', variable=self.showCharacters, onvalue=True, offvalue=False)
        self.root.showLocationsCheckbox = ttk.Checkbutton(
            text='Locations', variable=self.showLocations, onvalue=True, offvalue=False)
        self.root.showItemsCheckbox = ttk.Checkbutton(
            text='Items', variable=self.showItems, onvalue=True, offvalue=False)

        self.root.noneCheckbox = ttk.Radiobutton(
            text='None', variable=self.filterCatSelection, value=0, command=lambda: self.set_filter_category(0))
        self.root.tagsCheckbox = ttk.Radiobutton(
            text='Tag', variable=self.filterCatSelection, value=1, command=lambda: self.set_filter_category(1))
        self.root.viewpointsCheckbox = ttk.Radiobutton(
            text='Viewpoint', variable=self.filterCatSelection, value=2, command=lambda: self.set_filter_category(2))
        self.root.charactersCheckbox = ttk.Radiobutton(
            text='Character', variable=self.filterCatSelection, value=3, command=lambda: self.set_filter_category(3))
        self.root.locationsCheckbox = ttk.Radiobutton(
            text='Location', variable=self.filterCatSelection, value=4, command=lambda: self.set_filter_category(4))
        self.root.itemsCheckbox = ttk.Radiobutton(
            text='Item', variable=self.filterCatSelection, value=5, command=lambda: self.set_filter_category(5))

        self.root.filterCombobox = ttk.Combobox(values=[])

        self.root.htmlCheckbox = ttk.Radiobutton(
            text='HTML', variable=self.outputSelection, value=0)

        self.root.csvCheckbox = ttk.Radiobutton(
            text='CSV', variable=self.outputSelection, value=1)

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
        self.root.showChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)
        row1Cnt += 1
        self.root.showScenesCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)

        row2Cnt = 1
        self.hdTypes.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row2Cnt += 1
        self.root.showNormalTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.showUnusedTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.showNotesTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.showTodoTypeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.showUnexportedCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row2Cnt += 2
        self.hdFilters.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.noneCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.tagsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.viewpointsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.charactersCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.locationsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.itemsCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
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
        self.root.showNumberCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showTitleCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showDescriptionCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showViewpointCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showTagsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showNotesCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showDateCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showTimeCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showDurationCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showActionPatternCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showRatingsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showWordsTotalCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showWordcountCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showLettercountCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showStatusCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showCharactersCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showLocationsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.showItemsCheckbox.grid(row=row3Cnt, column=3, sticky=W, padx=20)

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

            if os.path.isfile(path):
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
