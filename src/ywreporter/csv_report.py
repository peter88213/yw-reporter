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

        self.sceneFilter = kwargs['sceneFilter']

        hdColumns = []
        chColumns = []
        scColumns = []

        if kwargs['showNumber']:
            hdColumns.append('"Number"')
            chColumns.append('"$ChapterNumber"')
            scColumns.append('"$SceneNumber"')

        if kwargs['showTitle']:
            hdColumns.append('"Title"')
            chColumns.append('"$Title"')
            scColumns.append('"$Title"')

        if kwargs['showDescription']:
            hdColumns.append('"Description"')
            chColumns.append('"$Desc"')
            scColumns.append('"$Desc"')

        if kwargs['showViewpoint']:
            hdColumns.append('"Viewpoint"')
            chColumns.append(',')
            scColumns.append('"$Viewpoint"')

        if kwargs['showTags']:
            hdColumns.append('"Tags"')
            chColumns.append(',')
            scColumns.append('"$Tags"')

        if kwargs['showNotes']:
            hdColumns.append('"Notes"')
            chColumns.append(',')
            scColumns.append('"$Notes"')

        if kwargs['showDate']:
            hdColumns.append('"Date"')
            chColumns.append(',')
            scColumns.append('"$ScDate"')

        if kwargs['showTime']:
            hdColumns.append('"Time"')
            chColumns.append(',')
            scColumns.append('"$ScTime"')

        if kwargs['showDuration']:
            hdColumns.append('"Duration"')
            chColumns.append(',')
            scColumns.append('"$Duration"')

        if kwargs['showActionPattern']:
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

        if kwargs['showRatings']:
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

        if kwargs['showWordsTotal']:
            hdColumns.append('"Words total"')
            chColumns.append(',')
            scColumns.append('"$WordsTotal"')

        if kwargs['showWordcount']:
            hdColumns.append('"Word count"')
            chColumns.append(',')
            scColumns.append('"$WordCount"')

        if kwargs['showLettercount']:
            hdColumns.append('"Letter count"')
            chColumns.append(',')
            scColumns.append('"$LetterCount"')

        if kwargs['showStatus']:
            hdColumns.append('"Status"')
            chColumns.append(',')
            scColumns.append('"$Status"')

        if kwargs['showCharacters']:
            hdColumns.append('"Characters"')
            chColumns.append(',')
            scColumns.append('"$Characters"')

        if kwargs['showLocations']:
            hdColumns.append('"Locations"')
            chColumns.append(',')
            scColumns.append('"$Locations"')

        if kwargs['showItems']:
            hdColumns.append('"Items"')
            chColumns.append(',')
            scColumns.append('"$Items"')

        hdRow = f'{",".join(hdColumns)}\n'
        chRow = f'{",".join(chColumns)}\n'
        scRow = f'{",".join(scColumns)}\n'

        self.fileHeader += hdRow.rstrip(',')

        if kwargs['showChapters']:

            if kwargs['showNormalType']:
                self.chapterTemplate = chRow
                self.partTemplate = chRow

            if kwargs['showUnusedType']:
                self.unusedChapterTemplate = chRow

            if kwargs['showNotesType']:
                self.notesChapterTemplate = chRow

            if kwargs['showTodoType']:
                self.todoChapterTemplate = chRow

        if kwargs['showScenes']:

            if kwargs['showNormalType']:
                self.sceneTemplate = scRow

            if kwargs['showUnusedType']:
                self.unusedSceneTemplate = scRow

            if kwargs['showNotesType']:
                self.notesSceneTemplate = scRow

            if kwargs['showTodoType']:
                self.todoSceneTemplate = scRow

            if kwargs['showUnexported']:
                self.notExportedSceneTemplate = scRow
