"""Provide a converter class for yWriter reports. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.pywriter_globals import ERROR
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.yw.yw7_file import Yw7File
from ywreporterlib.html_report import HtmlReport
from ywreporterlib.csv_report import CsvReport


class RpConverter(YwCnvUi):
    """A converter class for yWriter reports."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.
        Override the superclass method.
        """
        self.newFile = None

        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(f'{ERROR}File "{os.path.normpath(sourcePath)}" not found.')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath, **kwargs)

            if kwargs['output_selection'] == '1':
                targetFile = CsvReport(f'{fileName}{kwargs["suffix"]}{CsvReport.EXTENSION}', **kwargs)

            else:
                targetFile = HtmlReport(f'{fileName}{kwargs["suffix"]}{HtmlReport.EXTENSION}', **kwargs)

            self.export_from_yw(sourceFile, targetFile)

        else:
            self.ui.set_info_how(f'{ERROR}File type of "{os.path.normpath(sourcePath)}" not supported.')
