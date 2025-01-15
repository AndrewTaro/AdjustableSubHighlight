API_VERSION = 'API_v1.0'
MOD_NAME = 'AdjustableSubHighlight'

from Math import Vector4

try:
    import battle, events, dataHub, ui, constants, utils
except:
    pass

CC = constants.UiComponents

def logInfo(*args):
    data = [str(i) for i in args]
    utils.logInfo( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )

def logError(*args):
    data = [str(i) for i in args]
    utils.logError( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )

class Colors(object):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    ALPHA = 'Alpha'

NAME_COLOR_TO_PREF_BASE_KEYS = {
    # Periscope
    'SurfaceHitLockColor':          'subHighlightPeriscopeHitLock',
    'SurfaceHitNoLockColor':        'subHighlightPeriscopeHitNoLock',
    'SurfaceNoHitLockColor':        'subHighlightPeriscopeNoHitLock',
    'SurfaceNoHitNoLockColor':      'subHighlightPeriscopeNoHitNoLock',
    # Underwater
    'UnderwaterHitLockColor':       'subHighlightUnderwaterHitLock',
    'UnderwaterHitNoLockColor':     'subHighlightUnderwaterHitNoLock',
    'UnderwaterNoHitLockColor':     'subHighlightUnderwaterNoHitLock',
    'UnderwaterNoHitNoLockColor':   'subHighlightUnderwaterNoHitNoLock',
}

class ColorPref(object):
    VALUE_STEPS = 20
    # User can set a value from 0.0, 0.05, 0.10, ..., 0.95, 1.0 => 20 steps in total

    def __init__(self, colorName, defaultValue):
        if colorName in NAME_COLOR_TO_PREF_BASE_KEYS:
            self.colorName = colorName
            self._prefBaseKey = NAME_COLOR_TO_PREF_BASE_KEYS[colorName]
            self._defaults = self.__createDefaults(defaultValue * ColorPref.VALUE_STEPS)
        else:
            logError('color name is invalid: {}'.format(colorName))

    def getValue(self, userPrefSection):
        a = self.__readValue(userPrefSection, Colors.ALPHA)
        r = self.__readValue(userPrefSection, Colors.RED)
        g = self.__readValue(userPrefSection, Colors.GREEN)
        b = self.__readValue(userPrefSection, Colors.BLUE)
        return Vector4(r,g,b,a)
    
    def __readValue(self, userPrefSection, color):
        default = self._defaults[color]
        return userPrefSection.get(self._prefBaseKey + color, default) / ColorPref.VALUE_STEPS
    
    def __createDefaults(self, defaults):
        return {
            Colors.RED:   defaults[0],
            Colors.GREEN: defaults[1],
            Colors.BLUE:  defaults[2],
            Colors.ALPHA: defaults[3],
        }


SECTION_NAME = 'chatBoxWidth'
COLOR_PREFS = [
    ColorPref(d.name, d.value)
    for d in ui.getDefaultSubmarineUnderwaterColors()
]

class AdjustableSubHighlight(object):
    def __init__(self):
        self.__initUserPrefs()
        # Init
        self.__onUserPrefsChanged()
        events.onUserPrefsChanged(self.__onUserPrefsChanged)

    def __initUserPrefs(self):
        userPrefsEntity = dataHub.getSingleEntity('userPrefs')
        if userPrefsEntity:
            userPrefs =  userPrefsEntity[CC.userPrefs].userPrefs
        else:
            userPrefs = None
            logError('User Prefs Entity does not exist!')
        self.userPrefs = userPrefs

    def __onUserPrefsChanged(self, *args):
        if self.userPrefs is None:
            # Just to be sure.
            # Must Never fail when this event is triggered
            self.__initUserPrefs()

        # Update colors
        section = self.userPrefs.get(SECTION_NAME, {})
        for colorPref in COLOR_PREFS:
            colorName = colorPref.colorName
            color = colorPref.getValue(section)
            ui.setSubmarineUnderwaterColor(colorName, color)


adjSubHighlight = AdjustableSubHighlight()