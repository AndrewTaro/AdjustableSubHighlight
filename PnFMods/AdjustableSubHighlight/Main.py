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

class ColorNames(object):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    ALPHA = 'Opacity'

STATE_NAME_TO_PREF_BASE_KEY = {
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

    def __init__(self, stateName, defaultValue):
        if stateName in STATE_NAME_TO_PREF_BASE_KEY:
            self.stateName = stateName
            self._prefBaseKey = STATE_NAME_TO_PREF_BASE_KEY[stateName]
            self._defaults = self.__createDefaults(defaultValue)
        else:
            logError('state name is invalid: {}'.format(stateName))

    def getValue(self, userPrefSection):
        a = self.__readValue(userPrefSection, ColorNames.ALPHA)
        r = self.__readValue(userPrefSection, ColorNames.RED)
        g = self.__readValue(userPrefSection, ColorNames.GREEN)
        b = self.__readValue(userPrefSection, ColorNames.BLUE)
        return Vector4(r,g,b,a)
    
    def __readValue(self, userPrefSection, colorName):
        default = self._defaults[colorName]
        return userPrefSection.get(self._prefBaseKey + colorName, default) / ColorPref.VALUE_STEPS
    
    def __createDefaults(self, defaults):
        defaults = defaults * ColorPref.VALUE_STEPS
        return {
            ColorNames.RED:   defaults[0],
            ColorNames.GREEN: defaults[1],
            ColorNames.BLUE:  defaults[2],
            ColorNames.ALPHA: defaults[3],
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
            stateName = colorPref.stateName
            color = colorPref.getValue(section)
            ui.setSubmarineUnderwaterColor(stateName, color)


adjSubHighlight = AdjustableSubHighlight()