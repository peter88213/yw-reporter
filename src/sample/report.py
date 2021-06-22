"""Generate HTML report.

This is a sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_report'

import sys

from pywriter.ui.ui_tk import UiTk
from ywreporter.rp_converter import RpConverter


def run(sourcePath, suffix=''):
    ui = UiTk('yWriter report')
    converter = RpConverter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
