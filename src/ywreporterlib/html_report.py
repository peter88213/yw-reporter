"""Provide a class for HTML report file representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class HtmlReport(FileExport):
    """Export content or metadata from an yWriter project to a HTML file.
    """

    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    _fileHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

<style type="text/css">
body {font-family: sans-serif}
p.title {font-size: larger; font-weight: bold}
p.author {font-style: italic}
td, th {padding: 10}
th {font-size:smaller}
table {border-spacing: 0}
table, th, td {border: lightgrey solid 1px; vertical-align: top}
td.chtitle {font-weight: bold}
td.chdesc {font-style: italic}
tr.part {font-weight: bold}
tr.unused {color:gray}
tr.notes {color:blue}
tr.todo {color:firebrick}
tr.notexp {font-style: italic}
</style>

<title>$Title</title>
</head>

<body>
<p class=title>$Title</p>
<p class=author>$AuthorName</p>
<br />
<table>
'''

    _fileFooter = '''</table>
</body>
</html>
'''

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)

        self._sceneFilter = kwargs['scene_filter']

        hdColumns = []
        chColumns = []
        scColumns = []

        if kwargs['show_number']:
            hdColumns.append('<th>Number</th>')
            chColumns.append('<td class="chtitle">$ChapterNumber</td>')
            scColumns.append('<td>$SceneNumber</td>')

        if kwargs['show_title']:
            hdColumns.append('<th>Title</th>')
            chColumns.append('<td class="chtitle">$Title</td>')
            scColumns.append('<td>$Title</td>')

        if kwargs['show_description']:
            hdColumns.append('<th>Description</th>')
            chColumns.append('<td class="chdesc">$Desc</td>')
            scColumns.append('<td>$Desc</td>')

        if kwargs['show_viewpoint']:
            hdColumns.append('<th>Viewpoint</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Viewpoint</td>')

        if kwargs['show_tags']:
            hdColumns.append('<th>Tags</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Tags</td>')

        if kwargs['show_notes']:
            hdColumns.append('<th>Notes</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Notes</td>')

        if kwargs['show_date']:
            hdColumns.append('<th>Date</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ScDate</td>')

        if kwargs['show_time']:
            hdColumns.append('<th>Time</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ScTime</td>')

        if kwargs['show_duration']:
            hdColumns.append('<th>Duration</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Duration</td>')

        if kwargs['show_action_pattern']:
            hdColumns.append('<th>A/R</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ReactionScene</td>')
            hdColumns.append('<th>Goal</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Goal</td>')
            hdColumns.append('<th>Conflict</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Conflict</td>')
            hdColumns.append('<th>Outcome</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Outcome</td>')

        if kwargs['show_ratings']:
            hdColumns.append('<th>$FieldTitle1</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field1</td>')
            hdColumns.append('<th>$FieldTitle2</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field2</td>')
            hdColumns.append('<th>$FieldTitle3</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field3</td>')
            hdColumns.append('<th>$FieldTitle4</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field4</td>')

        if kwargs['show_words_total']:
            hdColumns.append('<th>Words total</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$WordsTotal</td>')

        if kwargs['show_wordcount']:
            hdColumns.append('<th>Word count</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$WordCount</td>')

        if kwargs['show_lettercount']:
            hdColumns.append('<th>Letter count</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$LetterCount</td>')

        if kwargs['show_status']:
            hdColumns.append('<th>Status</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Status</td>')

        if kwargs['show_characters']:
            hdColumns.append('<th>Characters</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Characters</td>')

        if kwargs['show_locations']:
            hdColumns.append('<th>Locations</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Locations</td>')

        if kwargs['show_items']:
            hdColumns.append('<th>Items</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Items</td>')

        hdRow = ''.join(hdColumns)
        chRow = ''.join(chColumns)
        scRow = ''.join(scColumns)

        self._fileHeader = f'{self._fileHeader}<thead><tr>{hdRow}</tr></thead>'

        if kwargs['show_chapters']:

            if kwargs['show_normal_type']:
                self._chapterTemplate = f'<tr>{chRow}</tr>'
                self._partTemplate = f'<tr class="part">{chRow}</tr>'

            if kwargs['show_unused_type']:
                self._unusedChapterTemplate = f'<tr class="unused">{chRow}</tr>'

            if kwargs['show_notes_type']:
                self._notesChapterTemplate = f'<tr class="notes">{chRow}</tr>'

            if kwargs['show_todo_type']:
                self._todoChapterTemplate = f'<tr class="todo">{chRow}</tr>'

        if kwargs['show_scenes']:

            if kwargs['show_normal_type']:
                self._sceneTemplate = f'<tr>{scRow}</tr>'

            if kwargs['show_unused_type']:
                self._unusedSceneTemplate = f'<tr class="unused">{scRow}</tr>'

            if kwargs['show_notes_type']:
                self._notesSceneTemplate = f'<tr class="notes">{scRow}</tr>'

            if kwargs['show_todo_type']:
                self._todoSceneTemplate = f'<tr class="todo">{scRow}</tr>'

            if kwargs['show_unexported']:
                self._notExportedSceneTemplate = f'<tr class="notexp">{scRow}</tr>'
