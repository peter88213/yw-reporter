[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 2.2.16

- Refactor for future Python versions.

Based on PyWriter version 7.14.10

### Version 2.2.15

- Provide a workaround to avoid unicode error with "C:\Users\...".
- Handling "invalid" escape sequences in regular expressions.

Based on PyWriter version 7.14.9

### Version 2.2.14

- Providing a meaningful error message on XML parser error.

Based on PyWriter version 7.14.6

### Version 2.2.13

- UTF-16 error handling like with PyWriter v12.19.0.

Based on PyWriter version 7.14.5

### Version 2.2.12

- Provide a detailed error message if the yw7 file cannot be processed.
- Handle UTF-16 encoded files with wrong XML declaration as created with yWriter iOS.

Based on PyWriter version 7.14.4

### Version 2.2.11

- Fix typo.

Based on PyWriter version 7.14.3

### Version 2.2.10

- Make it run with old Windows versions.

Based on PyWriter version 7.14.3

### Version 2.2.9

- Modify "shebang" line to make the script run with Python 3.11 under Windows.

Based on PyWriter version 7.14.2

### Version 2.2.8

- Update the PyWriter library for future Python versions.

Based on PyWriter version 7.14.2

### Version 2.2.7 Optional release

- Code refactoring and library update.

Based on PyWriter version 7.2.1

### Version 2.2.6 Update setup script

- Change the working dir to the script dir on startup in order to avoid "file not found" error.

Based on PyWriter version 5.18.0

### Version 2.2.5 Improved setup

- Catch exceptions in the setup script.

Based on PyWriter version 5.18.0

### Version 2.2.4 Improved word counting

- Fix word counting considering ellipses.

Based on PyWriter version 5.12.4

### Version 2.2.3 Improved word counting

- Fix word counting considering comments, hyphens, and dashes.

Based on PyWriter version 5.12.3

### Version 2.2.2 Optional update

- Add yWriter's internal chapter and scene IDs.

Based on PyWriter version 5.10.2

### Version 2.2.1 Optional update

- Refactor the code.

Based on PyWriter version 5.6.0

### Version 2.2.0

- Add shortcuts:
    - Ctrl-o to open.
    - Ctrl-q to exit.
- Enable menu shortcuts.
- Display document title on the window frame.
- Save and restore window size and position.

Based on PyWriter version 5.2.0

### Version 2.0.1

- Improve code and documentation quality.

Based on PyWriter version 5.0.3

### Version 2.0.0

- Fix a bug where "To do" chapters cause an exception.
- Rework the user interface. 
- Refactor the code.

Based on PyWriter version 5.0.0

### Version 1.6.0 GUI update

Based on PyWriter version  4.0.0

### Version 1.4.3 Support non-Windows OS

- Move installation and configuration to another location (see instructions for use).

Based on PyWriter version 3.28.1

### Version 1.4.2 Optional update

- Refactor for better maintainability.

Based on PyWriter version 3.24.3

### Version 1.4.1 Optional update

- Refactor for better maintainability.

Based on PyWriter version 3.24.3

### Version 1.4.0 Add output selector to the configuration file

- The configuration file has a new format.
- Major refactoring to enable automated testing.

Based on PyWriter version 3.24.3

### Version 1.2.0 Optional CSV report

The report can optionally be output in csv format instead of HTML.

Based on PyWriter version 3.22.0

### Version 1.0.3 Bugfix release

This release is strongly recommended.
Fix a regression from PyWriter v3.12.5. causing a crash if a scene has an 
hour, but no minute set.

Based on PyWriter version 3.16.4

### Version 1.0.2 No automatic shortcut creation

- Due to sporadic security warnings, the automatic shortcut creation during installation is removed. The user is now guided to create the application shortcut manually.  

Based on PyWriter version 3.16.0

### Version 1.0.1 Include installation script

**install.bat** installs the script for the local user and creates a 
shortcut on the desktop.
The Configuration file's path has moved to a subfolder of the installation path.

Based on PyWriter version 3.12.7

### Version 1.0.0 Feature complete

- Abandon yw5 and yw6 support.
- Add chapter/scene numbers.
- Add Words total.
- Add filtering.

Based on PyWriter version  3.12.1

### Version 0.4.0 Add date, time and duration columns

Based on PyWriter version  3.10.0

### Version 0.2.0

Beta test release based on PyWriter v3.8.2.
