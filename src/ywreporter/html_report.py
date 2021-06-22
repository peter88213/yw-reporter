"""HTML report from yWriter. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2html
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

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
h1 {text-align: center}
td, th {padding: 10}
table {border-spacing: 0}
table, th, td {border: lightgrey solid 1px; vertical-align: top}
</style>

<title>$Title</title>
</head>

<body>
<p class=title><strong>$Title</strong></p>
<p class=author>by $AuthorName</p>
<br />
<table>
'''

    chapterTemplate = '''<tr>
<td><b>$Title</b></td>
<td>$Desc</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
'''

    partTemplate = chapterTemplate

    sceneTemplate = '''<tr>
<td>$Title</td>
<td>$Desc</td>
<td>$Viewpoint</td>
<td>$WordCount</td>
<td>$Status</td>
<td>$Locations</td>
</tr>
'''
    notesSceneTemplate = '''<tr>
<td>($Title)</td>
<td>$Desc</td>
<td>$Viewpoint</td>
<td>$WordCount</td>
<td>$Status</td>
<td>$Locations</td>
</tr>
'''

    todoSceneTemplate = '''<tr>
<td>($Title)</td>
<td>$Desc</td>
<td>$Viewpoint</td>
<td>$WordCount</td>
<td>$Status</td>
<td>$Locations</td>
</tr>
'''

    unusedSceneTemplate = '''<tr>
<td>($Title)</td>
<td>$Desc</td>
<td>$Viewpoint</td>
<td>$WordCount</td>
<td>$Status</td>
<td>$Locations</td>
</tr>
'''

    notExportedSceneTemplate = '''<tr>
<td>($Title)</td>
<td>$Desc</td>
<td>$Viewpoint</td>
<td>$WordCount</td>
<td>$Status</td>
<td>$Locations</td>
</tr>
'''

    fileFooter = '''</table>
</body>
</html>
'''
