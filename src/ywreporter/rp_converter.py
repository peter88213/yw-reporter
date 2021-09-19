"""Provide a HTML report generator class for yWriter projects. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.converter.yw_cnv_ui import YwCnvUi

from pywriter.yw.yw7_file import Yw7File
from ywreporter.html_report import HtmlReport
from ywreporter.csv_report import CsvReport


class RpConverter(YwCnvUi):
    """A converter class for yWriter reports."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.
        Override the superclass method.
        """
        self.newFile = None

        if not os.path.isfile(sourcePath):
            self.ui.set_info_how('ERROR: File "' + os.path.normpath(sourcePath) + '" not found.')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath, **kwargs)

            if kwargs['outputSelection'] == '1':
                targetFile = CsvReport(fileName + kwargs['suffix'] + CsvReport.EXTENSION, **kwargs)

            else:
                targetFile = HtmlReport(fileName + kwargs['suffix'] + HtmlReport.EXTENSION, **kwargs)

            self.export_from_yw(sourceFile, targetFile)

        else:
            self.ui.set_info_how('ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.')
