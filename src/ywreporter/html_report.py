"""HTML report from yWriter. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2html
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class HtmlReport(FileExport):
    """Export content or metadata from an yWriter project to a HTML file.
    """

    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    fileHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

<style type="text/css">
body {font-family: sans-serif}
p.title {font-size: large; font-weight: bold}
p.author {font-style: italic}
td, th {padding: 10}
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

    fileFooter = '''</table>
</body>
</html>
'''

    def __init__(self, filePath, **kwargs):
        FileExport.__init__(self, filePath)

        hdColumns = []
        chColumns = []
        scColumns = []

        if kwargs['showTitle']:
            hdColumns.append('<td>Title</td>')
            chColumns.append('<td class="chtitle">$Title</td>')
            scColumns.append('<td>$Title</td>')

        if kwargs['showDescription']:
            hdColumns.append('<td>Description</td>')
            chColumns.append('<td class="chdesc">$Desc</td>')
            scColumns.append('<td>$Desc</td>')

        if kwargs['showViewpoint']:
            hdColumns.append('<td>Viewpoint</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Viewpoint</td>')

        if kwargs['showTags']:
            hdColumns.append('<td>Tags</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Tags</td>')

        if kwargs['showNotes']:
            hdColumns.append('<td>Notes</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Notes</td>')

        if kwargs['showActionPattern']:
            hdColumns.append('<td>A/R</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ReactionScene</td>')
            hdColumns.append('<td>Goal</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Goal</td>')
            hdColumns.append('<td>Conflict</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Conflict</td>')
            hdColumns.append('<td>Outcome</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Outcome</td>')

        if kwargs['showRatings']:
            hdColumns.append('<td>$FieldTitle1</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field1</td>')
            hdColumns.append('<td>$FieldTitle2</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field2</td>')
            hdColumns.append('<td>$FieldTitle3</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field3</td>')
            hdColumns.append('<td>$FieldTitle4</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field4</td>')

        if kwargs['showWordcount']:
            hdColumns.append('<td>Word count</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$WordCount</td>')

        if kwargs['showLettercount']:
            hdColumns.append('<td>Letter count</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$LetterCount</td>')

        if kwargs['showStatus']:
            hdColumns.append('<td>Status</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Status</td>')

        if kwargs['showCharacters']:
            hdColumns.append('<td>Characters</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Characters</td>')

        if kwargs['showLocations']:
            hdColumns.append('<td>Locations</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Locations</td>')

        if kwargs['showItems']:
            hdColumns.append('<td>Items</td>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Items</td>')

        hdRow = ''.join(hdColumns)
        chRow = ''.join(chColumns)
        scRow = ''.join(scColumns)

        self.fileHeader += '<tr>' + hdRow + '</tr>'

        if kwargs['showChapters']:

            if kwargs['showNormalType']:
                self.chapterTemplate = '<tr>' + chRow + '</tr>'
                self.partTemplate = '<tr class="part">' + chRow + '</tr>'

            if kwargs['showUnusedType']:
                self.unusedChapterTemplate = '<tr class="unused">' + chRow + '</tr>'

            if kwargs['showNotesType']:
                self.notesChapterTemplate = '<tr class="notes">' + chRow + '</tr>'

            if kwargs['showTodoType']:
                self.todoChapterTemplate = '<tr class="todo">' + chRow + '</tr>'

        if kwargs['showScenes']:

            if kwargs['showNormalType']:
                self.sceneTemplate = '<tr>' + scRow + '</tr>'

            if kwargs['showUnusedType']:
                self.unusedSceneTemplate = '<tr class="unused">' + scRow + '</tr>'

            if kwargs['showNotesType']:
                self.notesSceneTemplate = '<tr class="notes">' + scRow + '</tr>'

            if kwargs['showTodoType']:
                self.todoSceneTemplate = '<tr class="todo">' + scRow + '</tr>'

            if kwargs['showUnexported']:
                self.notExportedSceneTemplate = '<tr class="notexp">' + scRow + '</tr>'
