""""Provide a tkinter GUI class for the yWriter report generator.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import webbrowser
import tkinter as tk
from tkinter import ttk
from pywriter.file.filter import Filter
from pywriter.ui.main_tk import MainTk
from ywreporterlib.sc_tg_filter import ScTgFilter
from ywreporterlib.sc_vp_filter import ScVpFilter
from ywreporterlib.sc_cr_filter import ScCrFilter
from ywreporterlib.sc_lc_filter import ScLcFilter
from ywreporterlib.sc_it_filter import ScItFilter
from ywreporterlib.html_report import HtmlReport


class YwReporterTk(MainTk):
    """A tkinter GUI class for yWriter report generation.    

    Public methods:
        open_project(fileName) -- create a yWriter project instance and read the file. 
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
    
        Positional argument:
            title -- application title to be displayed at the window frame.

        Required keyword arguments:
            yw_last_open -- str: initial file.
            output_selection -- str: if '1' export csv, otherwise export html.
            suffix -- str: report filename suffix.
            show_chapters -- bool: if True, include chapters.
            show_scenes -- bool: if True, include scenes.
            show_normal_type -- bool: if True, include "normal" type.
            show_unused_type -- bool: if True, include "notes" type.
            show_notes_type -- bool: if True, include "normal" type.
            show_todo_type -- bool: if True, include "to do" type.
            show_unexported -- bool: if True, include "do not export" type.
            show_uid -- bool: if True, include "ID" column.
            show_number -- bool: if True, include "Number" column.
            show_title -- bool: if True, include "Title" column.
            show_description -- bool: if True, include "Description" column.
            show_viewpoint -- bool: if True, include "Viewpoint" column.
            show_tags -- bool: if True, include "Tags" column.
            show_notes -- bool: if True, include "Notes" column.
            show_date -- bool: if True, include "Date" column.
            show_time -- bool: if True, include "Time" column.
            show_duration -- bool: if True, include "Duration" column.
            show_action_pattern -- bool: if True, include "A/R-Goals-Conflict-Outcome" column.
            show_ratings -- bool: if True, include "Scene ratings" column.
            show_words_total -- bool: if True, include "Words total" column.
            show_wordcount -- bool: if True, include "Word count" column.
            show_lettercount -- bool: if True, include "Letter count" column.
            show_status -- bool: if True, include "Status" column.
            show_characters -- bool: if True, include "Charcter" column.
            show_locations -- bool: if True, include "Locations" column.
            show_items -- bool: if True, include "Items" column.

        Extends the superclass constructor.
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
        hdLevels = tk.Label(self.mainWindow, text='Levels')
        hdLevels.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._showChapters = tk.BooleanVar(value=kwargs['show_chapters'])
        showChaptersCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include chapters', variable=self._showChapters, onvalue=True, offvalue=False)
        showChaptersCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._showScenes = tk.BooleanVar(value=kwargs['show_scenes'])
        showScenesCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include scenes', variable=self._showScenes, onvalue=True, offvalue=False)
        showScenesCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: "Types" checkboxes (normal, unused, ...)
        row2Cnt = 1
        hdTypes = tk.Label(self.mainWindow, text='Types')
        hdTypes.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._showNormalType = tk.BooleanVar(value=kwargs['show_normal_type'])
        showNormalTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "normal" type', variable=self._showNormalType, onvalue=True, offvalue=False)
        showNormalTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._showUnusedType = tk.BooleanVar(value=kwargs['show_unused_type'])
        showUnusedTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "unused" type', variable=self._showUnusedType, onvalue=True, offvalue=False)
        showUnusedTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._showNotesType = tk.BooleanVar(value=kwargs['show_notes_type'])
        showNotesTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "notes" type', variable=self._showNotesType, onvalue=True, offvalue=False)
        showNotesTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._showTodoType = tk.BooleanVar(value=kwargs['show_todo_type'])
        showTodoTypeCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "to do" type', variable=self._showTodoType, onvalue=True, offvalue=False)
        showTodoTypeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._showUnexported = tk.BooleanVar(value=kwargs['show_unexported'])
        showUnexportedCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Include "do not export" type', variable=self._showUnexported, onvalue=True, offvalue=False)
        showUnexportedCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Filter" combo boxes (None/Tag/Viewpoint/...)
        row2Cnt += 2
        hdFilters = tk.Label(self.mainWindow, text='Filter')
        hdFilters.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        self._filterCatSelection = tk.IntVar()
        row2Cnt += 1
        noneCheckbox = ttk.Radiobutton(
            self.mainWindow, text='None', variable=self._filterCatSelection, value=0, command=lambda: self._set_filter_category(0))
        noneCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        tagsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Tag', variable=self._filterCatSelection, value=1, command=lambda: self._set_filter_category(1))
        tagsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        viewpointsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Viewpoint', variable=self._filterCatSelection, value=2, command=lambda: self._set_filter_category(2))
        viewpointsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        charactersCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Character', variable=self._filterCatSelection, value=3, command=lambda: self._set_filter_category(3))
        charactersCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        locationsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Location', variable=self._filterCatSelection, value=4, command=lambda: self._set_filter_category(4))
        locationsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        itemsCheckbox = ttk.Radiobutton(
            self.mainWindow, text='Item', variable=self._filterCatSelection, value=5, command=lambda: self._set_filter_category(5))
        itemsCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._filterCombobox = ttk.Combobox(self.mainWindow, values=[])
        self._filterCombobox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 2: "Output" comboboxes (HTML/CSV)
        row2Cnt += 2
        hdOutput = tk.Label(self.mainWindow, text='Output')
        hdOutput.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        self._outputSelection = tk.IntVar(value=kwargs['output_selection'])
        row2Cnt += 1
        htmlCheckbox = ttk.Radiobutton(self.mainWindow, text='HTML', variable=self._outputSelection, value=0)
        htmlCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        csvCheckbox = ttk.Radiobutton(self.mainWindow, text='CSV', variable=self._outputSelection, value=1)
        csvCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Columns" checkboxes (Number, title, Description ...)
        row3Cnt = 1
        hdColumns = tk.Label(self.mainWindow, text='Columns')
        hdColumns.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showUid = tk.BooleanVar(value=kwargs['show_uid'])
        showUidCheckbox = ttk.Checkbutton(
            self.mainWindow, text='ID', variable=self._showUid, onvalue=True, offvalue=False)
        showUidCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showNumber = tk.BooleanVar(value=kwargs['show_number'])
        showNumberCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Number', variable=self._showNumber, onvalue=True, offvalue=False)
        showNumberCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showTitle = tk.BooleanVar(value=kwargs['show_title'])
        showTitleCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Title', variable=self._showTitle, onvalue=True, offvalue=False)
        showTitleCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showDescription = tk.BooleanVar(value=kwargs['show_description'])
        showDescriptionCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Description', variable=self._showDescription, onvalue=True, offvalue=False)
        showDescriptionCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showViewpoint = tk.BooleanVar(value=kwargs['show_viewpoint'])
        showViewpointCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Viewpoint', variable=self._showViewpoint, onvalue=True, offvalue=False)
        showViewpointCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showTags = tk.BooleanVar(value=kwargs['show_tags'])
        showTagsCheckbox = ttk.Checkbutton(self.mainWindow, text='Tags',
                                           variable=self._showTags, onvalue=True, offvalue=False)
        showTagsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showNotes = tk.BooleanVar(value=kwargs['show_notes'])
        showNotesCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Notes', variable=self._showNotes, onvalue=True, offvalue=False)
        showNotesCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showDate = tk.BooleanVar(value=kwargs['show_date'])
        showDateCheckbox = ttk.Checkbutton(self.mainWindow, text='Date',
                                           variable=self._showDate, onvalue=True, offvalue=False)
        showDateCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showTime = tk.BooleanVar(value=kwargs['show_time'])
        showTimeCheckbox = ttk.Checkbutton(self.mainWindow, text='Time',
                                           variable=self._showTime, onvalue=True, offvalue=False)
        showTimeCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showDuration = tk.BooleanVar(value=kwargs['show_duration'])
        showDurationCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Duration', variable=self._showDuration, onvalue=True, offvalue=False)
        showDurationCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showActionPattern = tk.BooleanVar(value=kwargs['show_action_pattern'])
        showActionPatternCheckbox = ttk.Checkbutton(
            self.mainWindow, text='A/R-Goal-Conflict-Outcome', variable=self._showActionPattern, onvalue=True, offvalue=False)
        showActionPatternCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showRatings = tk.BooleanVar(value=kwargs['show_ratings'])
        showRatingsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Scene ratings', variable=self._showRatings, onvalue=True, offvalue=False)
        showRatingsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showWordsTotal = tk.BooleanVar(value=kwargs['show_words_total'])
        showWordsTotalCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Words total', variable=self._showWordsTotal, onvalue=True, offvalue=False)
        showWordsTotalCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showWordcount = tk.BooleanVar(value=kwargs['show_wordcount'])
        showWordcountCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Word count', variable=self._showWordcount, onvalue=True, offvalue=False)
        showWordcountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showLettercount = tk.BooleanVar(value=kwargs['show_lettercount'])
        showLettercountCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Letter count', variable=self._showLettercount, onvalue=True, offvalue=False)
        showLettercountCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showStatus = tk.BooleanVar(value=kwargs['show_status'])
        showStatusCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Status', variable=self._showStatus, onvalue=True, offvalue=False)
        showStatusCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showCharacters = tk.BooleanVar(value=kwargs['show_characters'])
        showCharactersCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Characters', variable=self._showCharacters, onvalue=True, offvalue=False)
        showCharactersCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showLocations = tk.BooleanVar(value=kwargs['show_locations'])
        showLocationsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Locations', variable=self._showLocations, onvalue=True, offvalue=False)
        showLocationsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._showItems = tk.BooleanVar(value=kwargs['show_items'])
        showItemsCheckbox = ttk.Checkbutton(
            self.mainWindow, text='Items', variable=self._showItems, onvalue=True, offvalue=False)
        showItemsCheckbox.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self.mainMenu.add_command(label='Create report', command=self.convert_file)
        self.mainMenu.entryconfig('Create report', state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Create report', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Create report', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        
        Display project title, description and status.
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if not super().open_project(fileName):
            return False

        # -- Build filter selector lists.
        self._tagList = []
        self._viewpointList = []
        self._viewpointTitles = []
        self._characterList = []
        self._characterTitles = []
        self._locationList = []
        self._locationTitles = []
        self._itemList = []
        self._itemTitles = []
        for chId in self.ywPrj.srtChapters:
            for scId in self.ywPrj.chapters[chId].srtScenes:
                if self.ywPrj.scenes[scId].tags:
                    for tag in self.ywPrj.scenes[scId].tags:
                        if not tag in self._tagList:
                            self._tagList.append(tag)
                if self.ywPrj.scenes[scId].characters:
                    vpId = self.ywPrj.scenes[scId].characters[0]
                    if not vpId in self._viewpointList:
                        self._viewpointList.append(vpId)
                        self._viewpointTitles.append(self.ywPrj.characters[vpId].title)
                    for crId in self.ywPrj.scenes[scId].characters:
                        if not crId in self._characterList:
                            self._characterList.append(crId)
                            self._characterTitles.append(self.ywPrj.characters[crId].title)
                if self.ywPrj.scenes[scId].locations:
                    for lcId in self.ywPrj.scenes[scId].locations:
                        if not lcId in self._locationList:
                            self._locationList.append(lcId)
                            self._locationTitles.append(self.ywPrj.locations[lcId].title)
                if self.ywPrj.scenes[scId].items:
                    for itId in self.ywPrj.scenes[scId].items:
                        if not itId in self._itemList:
                            self._itemList.append(itId)
                            self._itemTitles.append(self.ywPrj.items[itId].title)

        # Initialize the filter category selection widgets.
        self._filterCat = [[], self._tagList, self._viewpointTitles, self._characterTitles, self._locationTitles, self._itemTitles]
        self._set_filter_category(0)
        self._filterCatSelection.set(0)
        return True

    def close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        super().close_project()
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

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected."""
        self.show_status('')

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
        self.kwargs['yw_last_open'] = self.ywPrj.filePath
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
        self.kwargs['show_uid'] = self._showUid.get()
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
        self.converter.run(self.ywPrj.filePath, **self.kwargs)
        if self.converter.newFile is not None:
            webbrowser.open(self.converter.newFile)
