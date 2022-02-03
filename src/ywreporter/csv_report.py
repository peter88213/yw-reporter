"""Provide a class for CSV report file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class CsvReport(FileExport):
    """Class for CSV export file representation.
    """
    DESCRIPTION = 'CSV report'
    EXTENSION = '.csv'
    SUFFIX = '_report'

    def convert_from_yw(self, text):

        if text is None:
            text = ''

        else:
            text = text.replace('"', '""')

        return text

    def __init__(self, filePath, **kwargs):
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

        self.fileHeader = f'{self.fileHeader}{hdRow.rstrip(",")}'

        if kwargs['show_chapters']:

            if kwargs['show_normal_type']:
                self.chapterTemplate = chRow
                self.partTemplate = chRow

            if kwargs['show_unused_type']:
                self.unusedChapterTemplate = chRow

            if kwargs['show_notes_type']:
                self.notesChapterTemplate = chRow

            if kwargs['show_todo_type']:
                self.todoChapterTemplate = chRow

        if kwargs['show_scenes']:

            if kwargs['show_normal_type']:
                self.sceneTemplate = scRow

            if kwargs['show_unused_type']:
                self.unusedSceneTemplate = scRow

            if kwargs['show_notes_type']:
                self.notesSceneTemplate = scRow

            if kwargs['show_todo_type']:
                self.todoSceneTemplate = scRow

            if kwargs['show_unexported']:
                self.notExportedSceneTemplate = scRow
