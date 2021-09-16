""" Build a python script for the yw-reporter distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

The PyWriter project (see see https://github.com/peter88213/PyWriter)
must be located on the same directory level as the yw-reporter project. 

For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE_GUI = 'yw_reporter_.pyw'
TARGET_FILE_GUI = BUILD + 'yw_reporter.pyw'


def main():
    os.chdir(SRC)

    try:
        os.remove(TARGET_FILE_GUI)

    except:
        pass

    inliner.run(SOURCE_FILE_GUI,
                TARGET_FILE_GUI, 'ywreporter', '../src/')
    inliner.run(TARGET_FILE_GUI,
                TARGET_FILE_GUI, 'pywriter', '../../PyWriter/src/')
    print('Done.')


if __name__ == '__main__':
    main()