"""Provide a HTML report generator class for yWriter projects. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2md
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ui import YwCnvUi

from pywriter.yw.yw7_file import Yw7File
from ywreporter.html_report import HtmlReport


class RpConverter(YwCnvUi):
    """A converter class for html report."""
    EXPORT_SOURCE_CLASSES = [Yw7File, ]
    EXPORT_TARGET_CLASSES = [HtmlReport, ]
