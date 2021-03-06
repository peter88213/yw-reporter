"""Provide a scene per tag filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScTgFilter():
    """Filter Scene per tag.

    Public methods:
        accept(source, eId) -- check whether a scene is tagged with the filter tag.
    
    Strategy class, implementing filtering criteria for template-based scene export.
    """

    def __init__(self, tag=None):
        """Set the filter tag.
        
        Positional arguments:
            tag -- str: filter tag.
        """
        self._tag = tag

    def accept(self, source, eId):
        """Check whether a scene is tagged with the filter tag.
        
        Positional arguments:
            source -- Novel instance holding the scene to check.
            eId -- scene ID of the scene to check.       
        
        Return True if a source scene's tag matches the filter tag.
        Return True if no filter tag is set. 
        Oherwise, return False.
        Overrides the superclass method.
        """
        if self._tag is not None:
            try:
                if self._tag in source.scenes[eId].tags:
                    return True
                else:
                    return False
            except:
                return False
        return True
