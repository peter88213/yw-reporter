"""Provide a class for CSV report file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class CsvReport(FileExport):
    """Class for CSV report file representation."""
    DESCRIPTION = 'CSV report'
    EXTENSION = '.csv'
    SUFFIX = '_report'

    def _convert_from_yw(self, text, quick=False):
        if text is None:
            text = ''
        else:
            text = text.replace('"', '""')
        return text

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
    
        Positional arguments:
            filePath -- str: path to the csv file.

        Required keyword arguments:
            scene_filter -- Filter subclass instance.
            show_chapters -- bool: if True, include chapters.
            show_scenes -- bool: if True, include scenes.
            show_normal_type -- bool: if True, include "normal" type.
            show_unused_type -- bool: if True, include "notes" type.
            show_notes_type -- bool: if True, include "normal" type.
            show_todo_type -- bool: if True, include "to do" type.
            show_unexported -- bool: if True, include "do not export" type.
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
        super().__init__(filePath)
        self._sceneFilter = kwargs['scene_filter']
        hdColumns = []
        chColumns = []
        scColumns = []
        if kwargs['show_number']:
            hdColumns.append('"Number"')
            chColumns.append('"$ChapterNumber"')
            scColumns.append('"$SceneNumber"')
        if kwargs['show_title']:
            hdColumns.append('"Title"')
            chColumns.append('"$Title"')
            scColumns.append('"$Title"')
        if kwargs['show_description']:
            hdColumns.append('"Description"')
            chColumns.append('"$Desc"')
            scColumns.append('"$Desc"')
        if kwargs['show_viewpoint']:
            hdColumns.append('"Viewpoint"')
            chColumns.append(',')
            scColumns.append('"$Viewpoint"')
        if kwargs['show_tags']:
            hdColumns.append('"Tags"')
            chColumns.append(',')
            scColumns.append('"$Tags"')
        if kwargs['show_notes']:
            hdColumns.append('"Notes"')
            chColumns.append(',')
            scColumns.append('"$Notes"')
        if kwargs['show_date']:
            hdColumns.append('"Date"')
            chColumns.append(',')
            scColumns.append('"$ScDate"')
        if kwargs['show_time']:
            hdColumns.append('"Time"')
            chColumns.append(',')
            scColumns.append('"$ScTime"')
        if kwargs['show_duration']:
            hdColumns.append('"Duration"')
            chColumns.append(',')
            scColumns.append('"$Duration"')
        if kwargs['show_action_pattern']:
            hdColumns.append('"A/R"')
            chColumns.append(',')
            scColumns.append('"$ReactionScene"')
            hdColumns.append('"Goal"')
            chColumns.append(',')
            scColumns.append('"$Goal"')
            hdColumns.append('"Conflict"')
            chColumns.append(',')
            scColumns.append('"$Conflict"')
            hdColumns.append('"Outcome"')
            chColumns.append(',')
            scColumns.append('"$Outcome"')
        if kwargs['show_ratings']:
            hdColumns.append('"$FieldTitle1"')
            chColumns.append(',')
            scColumns.append('"$Field1"')
            hdColumns.append('"$FieldTitle2"')
            chColumns.append(',')
            scColumns.append('"$Field2"')
            hdColumns.append('"$FieldTitle3"')
            chColumns.append(',')
            scColumns.append('"$Field3"')
            hdColumns.append('"$FieldTitle4"')
            chColumns.append(',')
            scColumns.append('"$Field4"')
        if kwargs['show_words_total']:
            hdColumns.append('"Words total"')
            chColumns.append(',')
            scColumns.append('"$WordsTotal"')
        if kwargs['show_wordcount']:
            hdColumns.append('"Word count"')
            chColumns.append(',')
            scColumns.append('"$WordCount"')
        if kwargs['show_lettercount']:
            hdColumns.append('"Letter count"')
            chColumns.append(',')
            scColumns.append('"$LetterCount"')
        if kwargs['show_status']:
            hdColumns.append('"Status"')
            chColumns.append(',')
            scColumns.append('"$Status"')
        if kwargs['show_characters']:
            hdColumns.append('"Characters"')
            chColumns.append(',')
            scColumns.append('"$Characters"')
        if kwargs['show_locations']:
            hdColumns.append('"Locations"')
            chColumns.append(',')
            scColumns.append('"$Locations"')
        if kwargs['show_items']:
            hdColumns.append('"Items"')
            chColumns.append(',')
            scColumns.append('"$Items"')
        hdRow = f'{",".join(hdColumns)}\n'
        chRow = f'{",".join(chColumns)}\n'
        scRow = f'{",".join(scColumns)}\n'
        self._fileHeader = f'{self._fileHeader}{hdRow.rstrip(",")}'
        if kwargs['show_chapters']:
            if kwargs['show_normal_type']:
                self._chapterTemplate = chRow
                self._partTemplate = chRow
            if kwargs['show_unused_type']:
                self._unusedChapterTemplate = chRow
            if kwargs['show_notes_type']:
                self._notesChapterTemplate = chRow
            if kwargs['show_todo_type']:
                self._todoChapterTemplate = chRow
        if kwargs['show_scenes']:
            if kwargs['show_normal_type']:
                self._sceneTemplate = scRow
            if kwargs['show_unused_type']:
                self._unusedSceneTemplate = scRow
            if kwargs['show_notes_type']:
                self._notesSceneTemplate = scRow
            if kwargs['show_todo_type']:
                self._todoSceneTemplate = scRow
            if kwargs['show_unexported']:
                self._notExportedSceneTemplate = scRow
