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
        self._tagList = []
        self._viewpointTitles = []
        self._viewpointList = []
        self._characterTitles = []
        self._characterList = []
        self._locationTitles = []
        self._locationList = []
        self._itemTitles = []
        self._itemList = []
        self._filterCat = []

        #--- Row 1: "Levels" checkboxes (chapters, scenes)

        row1Cnt = 1
        hdLevels = tk.Label(self._mainWindow, text='Levels')
        hdLevels.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self._showChapters = tk.BooleanVar(value=kwargs['show_chapters'])
        showChaptersCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include chapters', variable=self._showChapters, onvalue=True, offvalue=False)
        showChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self._showScenes = tk.BooleanVar(value=kwargs['show_scenes'])
        showScenesCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include scenes', variable=self._showScenes, onvalue=True, offvalue=False)
        showScenesCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: "Types" checkboxes (normal, unused, ...)

        row2Cnt = 1
        hdTypes = tk.Label(self._mainWindow, text='Types')
        hdTypes.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._showNormalType = tk.BooleanVar(value=kwargs['show_normal_type'])
        showNormalTypeCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include "normal" type', variable=self._showNormalType, onvalue=True, offvalue=False)
        showNormalTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._showUnusedType = tk.BooleanVar(value=kwargs['show_unused_type'])
        showUnusedTypeCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include "unused" type', variable=self._showUnusedType, onvalue=True, offvalue=False)
        showUnusedTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._showNotesType = tk.BooleanVar(value=kwargs['show_notes_type'])
        showNotesTypeCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include "notes" type', variable=self._showNotesType, onvalue=True, offvalue=False)
        showNotesTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._showTodoType = tk.BooleanVar(value=kwargs['show_todo_type'])
        showTodoTypeCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include "to do" type', variable=self._showTodoType, onvalue=True, offvalue=False)
        showTodoTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._showUnexported = tk.BooleanVar(value=kwargs['show_unexported'])
        showUnexportedCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Include "do not export" type', variable=self._showUnexported, onvalue=True, offvalue=False)
        showUnexportedCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Filter" combo boxes (None/Tag/Viewpoint/...)

        row2Cnt += 2
        hdFilters = tk.Label(self._mainWindow, text='Filter')
        hdFilters.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        self._filterCatSelection = tk.IntVar()

        row2Cnt += 1
        noneCheckbox = ttk.Radiobutton(
            self._mainWindow, text='None', variable=self._filterCatSelection, value=0, command=lambda: self._set_filter_category(0))
        noneCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        tagsCheckbox = ttk.Radiobutton(
            self._mainWindow, text='Tag', variable=self._filterCatSelection, value=1, command=lambda: self._set_filter_category(1))
        tagsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        viewpointsCheckbox = ttk.Radiobutton(
            self._mainWindow, text='Viewpoint', variable=self._filterCatSelection, value=2, command=lambda: self._set_filter_category(2))
        viewpointsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        charactersCheckbox = ttk.Radiobutton(
            self._mainWindow, text='Character', variable=self._filterCatSelection, value=3, command=lambda: self._set_filter_category(3))
        charactersCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        locationsCheckbox = ttk.Radiobutton(
            self._mainWindow, text='Location', variable=self._filterCatSelection, value=4, command=lambda: self._set_filter_category(4))
        locationsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        itemsCheckbox = ttk.Radiobutton(
            self._mainWindow, text='Item', variable=self._filterCatSelection, value=5, command=lambda: self._set_filter_category(5))
        itemsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self._filterCombobox = ttk.Combobox(self._mainWindow, values=[])
        self._filterCombobox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Output" comboboxes (HTML/CSV)

        row2Cnt += 2
        hdOutput = tk.Label(self._mainWindow, text='Output')
        hdOutput.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        self._outputSelection = tk.IntVar(value=kwargs['output_selection'])

        row2Cnt += 1
        htmlCheckbox = ttk.Radiobutton(self._mainWindow, text='HTML', variable=self._outputSelection, value=0)
        htmlCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        csvCheckbox = ttk.Radiobutton(self._mainWindow, text='CSV', variable=self._outputSelection, value=1)
        csvCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Columns" checkboxes (Number, title, Description ...)

        row3Cnt = 1
        hdColumns = tk.Label(self._mainWindow, text='Columns')
        hdColumns.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showNumber = tk.BooleanVar(value=kwargs['show_number'])
        showNumberCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Number', variable=self._showNumber, onvalue=True, offvalue=False)
        showNumberCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showTitle = tk.BooleanVar(value=kwargs['show_title'])
        showTitleCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Title', variable=self._showTitle, onvalue=True, offvalue=False)
        showTitleCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showDescription = tk.BooleanVar(value=kwargs['show_description'])
        showDescriptionCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Description', variable=self._showDescription, onvalue=True, offvalue=False)
        showDescriptionCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showViewpoint = tk.BooleanVar(value=kwargs['show_viewpoint'])
        showViewpointCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Viewpoint', variable=self._showViewpoint, onvalue=True, offvalue=False)
        showViewpointCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showTags = tk.BooleanVar(value=kwargs['show_tags'])
        showTagsCheckbox = ttk.Checkbutton(self._mainWindow, text='Tags',
                                           variable=self._showTags, onvalue=True, offvalue=False)
        showTagsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showNotes = tk.BooleanVar(value=kwargs['show_notes'])
        showNotesCheckbox = ttk.Checkbutton(
            self._mainWindow,  text='Notes', variable=self._showNotes, onvalue=True, offvalue=False)
        showNotesCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showDate = tk.BooleanVar(value=kwargs['show_date'])
        showDateCheckbox = ttk.Checkbutton(self._mainWindow, text='Date',
                                           variable=self._showDate, onvalue=True, offvalue=False)
        showDateCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showTime = tk.BooleanVar(value=kwargs['show_time'])
        showTimeCheckbox = ttk.Checkbutton(self._mainWindow, text='Time',
                                           variable=self._showTime, onvalue=True, offvalue=False)
        showTimeCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showDuration = tk.BooleanVar(value=kwargs['show_duration'])
        showDurationCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Duration', variable=self._showDuration, onvalue=True, offvalue=False)
        showDurationCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showActionPattern = tk.BooleanVar(value=kwargs['show_action_pattern'])
        showActionPatternCheckbox = ttk.Checkbutton(
            self._mainWindow, text='A/R-Goal-Conflict-Outcome', variable=self._showActionPattern, onvalue=True, offvalue=False)
        showActionPatternCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showRatings = tk.BooleanVar(value=kwargs['show_ratings'])
        showRatingsCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Scene ratings', variable=self._showRatings, onvalue=True, offvalue=False)
        showRatingsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showWordsTotal = tk.BooleanVar(value=kwargs['show_words_total'])
        showWordsTotalCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Words total', variable=self._showWordsTotal, onvalue=True, offvalue=False)
        showWordsTotalCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showWordcount = tk.BooleanVar(value=kwargs['show_wordcount'])
        showWordcountCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Word count', variable=self._showWordcount, onvalue=True, offvalue=False)
        showWordcountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showLettercount = tk.BooleanVar(value=kwargs['show_lettercount'])
        showLettercountCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Letter count', variable=self._showLettercount, onvalue=True, offvalue=False)
        showLettercountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showStatus = tk.BooleanVar(value=kwargs['show_status'])
        showStatusCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Status', variable=self._showStatus, onvalue=True, offvalue=False)
        showStatusCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showCharacters = tk.BooleanVar(value=kwargs['show_characters'])
        showCharactersCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Characters', variable=self._showCharacters, onvalue=True, offvalue=False)
        showCharactersCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showLocations = tk.BooleanVar(value=kwargs['show_locations'])
        showLocationsCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Locations', variable=self._showLocations, onvalue=True, offvalue=False)
        showLocationsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self._showItems = tk.BooleanVar(value=kwargs['show_items'])
        showItemsCheckbox = ttk.Checkbutton(
            self._mainWindow, text='Items', variable=self._showItems, onvalue=True, offvalue=False)
        showItemsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def _extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self._mainMenu.add_command(label='Create report', command=self._convert_file)
        self._mainMenu.entryconfig('Create report', state='disabled')

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Create report', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Create report', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self._ywPrj = Yw7File(fileName)
        message = self._ywPrj.read()

        if message.startswith(ERROR):
            self._close_project()
            self.set_info_how(message)
            return ''

        if self._ywPrj.title:
            titleView = self._ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self._ywPrj.author:
            authorView = self._ywPrj.author

        else:
            authorView = 'Unknown author'

        self._titleBar.config(text=f'{titleView} by {authorView}')
        self._enable_menu()

        #-- Build filter selector lists.

        self._tagList = []
        self._viewpointList = []
        self._viewpointTitles = []
        self._characterList = []
        self._characterTitles = []
        self._locationList = []
        self._locationTitles = []
        self._itemList = []
        self._itemTitles = []

        for chId in self._ywPrj.srtChapters:

            for scId in self._ywPrj.chapters[chId].srtScenes:

                if self._ywPrj.scenes[scId].tags:

                    for tag in self._ywPrj.scenes[scId].tags:

                        if not tag in self._tagList:
                            self._tagList.append(tag)

                if self._ywPrj.scenes[scId].characters:
                    vpId = self._ywPrj.scenes[scId].characters[0]

                    if not vpId in self._viewpointList:
                        self._viewpointList.append(vpId)
                        self._viewpointTitles.append(self._ywPrj.characters[vpId].title)

                    for crId in self._ywPrj.scenes[scId].characters:

                        if not crId in self._characterList:
                            self._characterList.append(crId)
                            self._characterTitles.append(self._ywPrj.characters[crId].title)

                if self._ywPrj.scenes[scId].locations:

                    for lcId in self._ywPrj.scenes[scId].locations:

                        if not lcId in self._locationList:
                            self._locationList.append(lcId)
                            self._locationTitles.append(self._ywPrj.locations[lcId].title)

                if self._ywPrj.scenes[scId].items:

                    for itId in self._ywPrj.scenes[scId].items:

                        if not itId in self._itemList:
                            self._itemList.append(itId)
                            self._itemTitles.append(self._ywPrj.items[itId].title)

        # Initialize the filter category selection widgets.

        self._filterCat = [[], self._tagList, self._viewpointTitles, self._characterTitles, self._locationTitles, self._itemTitles]
        self._set_filter_category(0)
        self._filterCatSelection.set(0)

        return fileName

    def _close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super()._close_project()
        self._filterCat = [[], [], [], [], [], []]
        self._filterCombobox['values'] = []
        self._set_filter_category(0)
        self._filterCatSelection.set(0)
        self._filterCombobox.set('')

    def _set_filter_category(self, selection):
        options = self._filterCat[selection]
        self._filterCombobox['values'] = options

        if options:
            self._filterCombobox.set(options[0])

        else:
            self._filterCombobox.set('')

    def _convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self._set_status('')

        # Filter options.

        filterCat = self._filterCatSelection.get()
        option = self._filterCombobox.current()

        if filterCat == 0:
            sceneFilter = Filter()

        elif filterCat == 1:
            sceneFilter = ScTgFilter(self._tagList[option])

        elif filterCat == 2:
            sceneFilter = ScVpFilter(self._viewpointList[option])

        elif filterCat == 3:
            sceneFilter = ScCrFilter(self._characterList[option])

        elif filterCat == 4:
            sceneFilter = ScLcFilter(self._locationList[option])

        elif filterCat == 5:
            sceneFilter = ScItFilter(self._itemList[option])

        self.kwargs['yw_last_open'] = self._ywPrj.filePath
        self.kwargs['output_selection'] = str(self._outputSelection.get())
        self.kwargs['suffix'] = HtmlReport.SUFFIX
        self.kwargs['scene_filter'] = sceneFilter
        self.kwargs['show_chapters'] = self._showChapters.get()
        self.kwargs['show_scenes'] = self._showScenes.get()
        self.kwargs['show_normal_type'] = self._showNormalType.get()
        self.kwargs['show_unused_type'] = self._showUnusedType.get()
        self.kwargs['show_notes_type'] = self._showNotesType.get()
        self.kwargs['show_todo_type'] = self._showTodoType.get()
        self.kwargs['show_unexported'] = self._showUnexported.get()
        self.kwargs['show_number'] = self._showNumber.get()
        self.kwargs['show_title'] = self._showTitle.get()
        self.kwargs['show_description'] = self._showDescription.get()
        self.kwargs['show_viewpoint'] = self._showViewpoint.get()
        self.kwargs['show_tags'] = self._showTags.get()
        self.kwargs['show_notes'] = self._showNotes.get()
        self.kwargs['show_date'] = self._showDate.get()
        self.kwargs['show_time'] = self._showTime.get()
        self.kwargs['show_duration'] = self._showDuration.get()
        self.kwargs['show_action_pattern'] = self._showActionPattern.get()
        self.kwargs['show_ratings'] = self._showRatings.get()
        self.kwargs['show_words_total'] = self._showWordsTotal.get()
        self.kwargs['show_wordcount'] = self._showWordcount.get()
        self.kwargs['show_lettercount'] = self._showLettercount.get()
        self.kwargs['show_status'] = self._showStatus.get()
        self.kwargs['show_characters'] = self._showCharacters.get()
        self.kwargs['show_locations'] = self._showLocations.get()
        self.kwargs['show_items'] = self._showItems.get()
        
        self.converter.run(self._ywPrj.filePath, **self.kwargs)

        if self.converter.newFile is not None:
            webbrowser.open(self.converter.newFile)
