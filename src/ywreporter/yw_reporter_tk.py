#!/usr/bin/env python3
""""Provide a tkinter GUI class for the yWriter report generator.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import webbrowser
import tkinter as tk
from tkinter import ttk

from pywriter.pywriter_globals import ERROR
from pywriter.file.filter import Filter
from pywriter.file.sc_tg_filter import ScTgFilter
from pywriter.file.sc_vp_filter import ScVpFilter
from pywriter.file.sc_cr_filter import ScCrFilter
from pywriter.file.sc_lc_filter import ScLcFilter
from pywriter.file.sc_it_filter import ScItFilter

from ywreporter.html_report import HtmlReport
from pywriter.yw.yw7_file import Yw7File

from pywriter.ui.main_tk import MainTk


class YwReporterTk(MainTk):
    """A tkinter GUI class for yWriter report generation.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.converter = None
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

        #--- Row 1: "Levels" checkboxes (chapters, scenes)

        row1Cnt = 1
        hdLevels = tk.Label(self.mainWindow, text='Levels')
        hdLevels.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.showChapters = tk.BooleanVar(value=kwargs['showChapters'])
        showChaptersCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include chapters', variable=self.showChapters, onvalue=True, offvalue=False)
        showChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.showScenes = tk.BooleanVar(value=kwargs['showScenes'])
        showScenesCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include scenes', variable=self.showScenes, onvalue=True, offvalue=False)
        showScenesCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: "Types" checkboxes (normal, unused, ...)

        row2Cnt = 1
        hdTypes = tk.Label(self.mainWindow, text='Types')
        hdTypes.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.showNormalType = tk.BooleanVar(value=kwargs['showNormalType'])
        showNormalTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "normal" type', variable=self.showNormalType, onvalue=True, offvalue=False)
        showNormalTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.showUnusedType = tk.BooleanVar(value=kwargs['showUnusedType'])
        showUnusedTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "unused" type', variable=self.showUnusedType, onvalue=True, offvalue=False)
        showUnusedTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.showNotesType = tk.BooleanVar(value=kwargs['showNotesType'])
        showNotesTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "notes" type', variable=self.showNotesType, onvalue=True, offvalue=False)
        showNotesTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.showTodoType = tk.BooleanVar(value=kwargs['showTodoType'])
        showTodoTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "to do" type', variable=self.showTodoType, onvalue=True, offvalue=False)
        showTodoTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.showUnexported = tk.BooleanVar(value=kwargs['showUnexported'])
        showUnexportedCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "do not export" type', variable=self.showUnexported, onvalue=True, offvalue=False)
        showUnexportedCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Filter" combo boxes (None/Tag/Viewpoint/...)

        row2Cnt += 2
        hdFilters = tk.Label(self.mainWindow, text='Filter')
        hdFilters.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        self.filterCatSelection = tk.IntVar()

        row2Cnt += 1
        noneCheckbox = ttk.Radiobutton(
            self.mainWindow, text='None', variable=self.filterCatSelection, value=0, command=lambda: self.set_filter_category(0))
        noneCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        tagsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Tag', variable=self.filterCatSelection, value=1, command=lambda: self.set_filter_category(1))
        tagsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        viewpointsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Viewpoint', variable=self.filterCatSelection, value=2, command=lambda: self.set_filter_category(2))
        viewpointsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        charactersCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Character', variable=self.filterCatSelection, value=3, command=lambda: self.set_filter_category(3))
        charactersCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        locationsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Location', variable=self.filterCatSelection, value=4, command=lambda: self.set_filter_category(4))
        locationsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        itemsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Item', variable=self.filterCatSelection, value=5, command=lambda: self.set_filter_category(5))
        itemsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.filterCombobox = ttk.Combobox(self.mainWindow, values=[])
        self.filterCombobox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Output" comboboxes (HTML/CSV)

        row2Cnt += 2
        hdOutput = tk.Label(self.mainWindow, text='Output')
        hdOutput.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        self.outputSelection = tk.IntVar(value=kwargs['outputSelection'])

        row2Cnt += 1
        htmlCheckbox = ttk.Radiobutton(self.mainWindow, text='HTML', variable=self.outputSelection, value=0)
        htmlCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        csvCheckbox = ttk.Radiobutton(self.mainWindow, text='CSV', variable=self.outputSelection, value=1)
        csvCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Columns" checkboxes (Number, title, Description ...)

        row3Cnt = 1
        hdColumns = tk.Label(self.mainWindow, text='Columns')
        hdColumns.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showNumber = tk.BooleanVar(value=kwargs['showNumber'])
        showNumberCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Number', variable=self.showNumber, onvalue=True, offvalue=False)
        showNumberCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showTitle = tk.BooleanVar(value=kwargs['showTitle'])
        showTitleCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Title', variable=self.showTitle, onvalue=True, offvalue=False)
        showTitleCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showDescription = tk.BooleanVar(value=kwargs['showDescription'])
        showDescriptionCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Description', variable=self.showDescription, onvalue=True, offvalue=False)
        showDescriptionCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showViewpoint = tk.BooleanVar(value=kwargs['showViewpoint'])
        showViewpointCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Viewpoint', variable=self.showViewpoint, onvalue=True, offvalue=False)
        showViewpointCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showTags = tk.BooleanVar(value=kwargs['showTags'])
        showTagsCheckbox = ttk.Checkbutton(self.mainWindow, text='Tags',
                                           variable=self.showTags, onvalue=True, offvalue=False)
        showTagsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showNotes = tk.BooleanVar(value=kwargs['showNotes'])
        showNotesCheckbox = ttk.Checkbutton(
            self.mainWindow,  text='Notes', variable=self.showNotes, onvalue=True, offvalue=False)
        showNotesCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showDate = tk.BooleanVar(value=kwargs['showDate'])
        showDateCheckbox = ttk.Checkbutton(self.mainWindow, text='Date',
                                           variable=self.showDate, onvalue=True, offvalue=False)
        showDateCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showTime = tk.BooleanVar(value=kwargs['showTime'])
        showTimeCheckbox = ttk.Checkbutton(self.mainWindow, text='Time',
                                           variable=self.showTime, onvalue=True, offvalue=False)
        showTimeCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showDuration = tk.BooleanVar(value=kwargs['showDuration'])
        showDurationCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Duration', variable=self.showDuration, onvalue=True, offvalue=False)
        showDurationCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showActionPattern = tk.BooleanVar(value=kwargs['showActionPattern'])
        showActionPatternCheckbox = ttk.Checkbutton(
            self.mainWindow, text='A/R-Goal-Conflict-Outcome', variable=self.showActionPattern, onvalue=True, offvalue=False)
        showActionPatternCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showRatings = tk.BooleanVar(value=kwargs['showRatings'])
        showRatingsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Scene ratings', variable=self.showRatings, onvalue=True, offvalue=False)
        showRatingsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showWordsTotal = tk.BooleanVar(value=kwargs['showWordsTotal'])
        showWordsTotalCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Words total', variable=self.showWordsTotal, onvalue=True, offvalue=False)
        showWordsTotalCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showWordcount = tk.BooleanVar(value=kwargs['showWordcount'])
        showWordcountCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Word count', variable=self.showWordcount, onvalue=True, offvalue=False)
        showWordcountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showLettercount = tk.BooleanVar(value=kwargs['showLettercount'])
        showLettercountCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Letter count', variable=self.showLettercount, onvalue=True, offvalue=False)
        showLettercountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showStatus = tk.BooleanVar(value=kwargs['showStatus'])
        showStatusCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Status', variable=self.showStatus, onvalue=True, offvalue=False)
        showStatusCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showCharacters = tk.BooleanVar(value=kwargs['showCharacters'])
        showCharactersCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Characters', variable=self.showCharacters, onvalue=True, offvalue=False)
        showCharactersCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showLocations = tk.BooleanVar(value=kwargs['showLocations'])
        showLocationsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Locations', variable=self.showLocations, onvalue=True, offvalue=False)
        showLocationsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.showItems = tk.BooleanVar(value=kwargs['showItems'])
        showItemsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Items', variable=self.showItems, onvalue=True, offvalue=False)
        showItemsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.mainMenu.add_command(label='Create report', command=self.convert_file)
        self.mainMenu.entryconfig('Create report', state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Create report', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Create report', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7File(fileName)
        message = self.ywPrj.read()

        if message.startswith(ERROR):
            self.close_project()
            self.set_info_how(message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=titleView + ' by ' + authorView)
        self.enable_menu()

        self.locations = []
        self.items = []

        #-- Build filter selector lists.

        self.tags = []
        self.vpIds = []
        self.viewpoints = []
        self.crIds = []
        self.characters = []
        self.lcIds = []
        self.locations = []
        self.itIds = []
        self.items = []

        for chId in self.ywPrj.srtChapters:

            for scId in self.ywPrj.chapters[chId].srtScenes:

                if self.ywPrj.scenes[scId].tags:

                    for tag in self.ywPrj.scenes[scId].tags:

                        if not tag in self.tags:
                            self.tags.append(tag)

                if self.ywPrj.scenes[scId].characters:
                    vpId = self.ywPrj.scenes[scId].characters[0]

                    if not vpId in self.vpIds:
                        self.vpIds.append(vpId)
                        self.viewpoints.append(
                            self.ywPrj.characters[vpId].title)

                    for crId in self.ywPrj.scenes[scId].characters:

                        if not crId in self.crIds:
                            self.crIds.append(crId)
                            self.characters.append(
                                self.ywPrj.characters[crId].title)

                if self.ywPrj.scenes[scId].locations:

                    for lcId in self.ywPrj.scenes[scId].locations:

                        if not lcId in self.lcIds:
                            self.lcIds.append(lcId)
                            self.locations.append(
                                self.ywPrj.locations[lcId].title)

                if self.ywPrj.scenes[scId].items:

                    for itId in self.ywPrj.scenes[scId].items:

                        if not itId in self.itIds:
                            self.itIds.append(itId)
                            self.items.append(
                                self.ywPrj.items[itId].title)

        # Initialize the filter category selection widgets.

        self.filterCat = [[], self.tags, self.viewpoints, self.characters, self.locations, self.items]
        self.set_filter_category(0)
        self.filterCatSelection.set(0)

        return fileName

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super().close_project()
        self.filterCat = [[], [], [], [], [], []]
        self.filterCombobox['values'] = []
        self.set_filter_category(0)
        self.filterCatSelection.set(0)
        self.filterCombobox.set('')

    def set_filter_category(self, selection):
        options = self.filterCat[selection]
        self.filterCombobox['values'] = options

        if options:
            self.filterCombobox.set(options[0])

        else:
            self.filterCombobox.set('')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self.set_status('')

        # Filter options.

        filterCat = self.filterCatSelection.get()
        option = self.filterCombobox.current()

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

        self.kwargs = dict(
            yw_last_open=self.ywPrj.filePath,
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
        self.converter.run(self.ywPrj.filePath, **self.kwargs)

        if self.converter.newFile is not None:
            webbrowser.open(self.converter.newFile)
