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


class DefaultColors(object):
    RED = 0.8
    GREEN = 0.05
    BLUE = 0

# def createPrefs():
#     PREFIX = 'subHighlight'
#     DEPTHS = ['Periscope', 'Underwater']
#     TYPES = ['HitLock', 'HitNoLock', 'NoHitLock', 'NoHitNoLock']
#     COLORS = ['Opacity', 'Red', 'Green', 'Blue']
#     DEFAULTS = [
#         0.8, DefaultColors.RED, DefaultColors.GREEN, DefaultColors.BLUE,
#         0.4, DefaultColors.RED, DefaultColors.GREEN, DefaultColors.BLUE,
#         1,   0, 0, 0,
#         0.5, 0, 0, 0,
#         0.2, DefaultColors.RED, DefaultColors.GREEN, DefaultColors.BLUE,
#         0.1, DefaultColors.RED, DefaultColors.GREEN, DefaultColors.BLUE,
#         1,   0, 0, 0,
#         0.5, 0, 0, 0,
#     ]
#     keys = [PREFIX + depth + type + color for depth in DEPTHS for type in TYPES for color in COLORS]
#     return [{'prefKey': k, 'default': d} for k, d in zip(keys, DEFAULTS)]

# PREFS = createPrefs()

PS_HIT_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightPeriscopeHitLockOpacity', 'default': 0.8},
    'RED':   {'prefKey': 'subHighlightPeriscopeHitLockRed', 'default': DefaultColors.RED},
    'GREEN': {'prefKey': 'subHighlightPeriscopeHitLockGreen', 'default': DefaultColors.GREEN},
    'BLUE':  {'prefKey': 'subHighlightPeriscopeHitLockBlue', 'default': DefaultColors.BLUE},
}
PS_HIT_NO_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightPeriscopeHitNoLockOpacity', 'default': 0.4},
    'RED':   {'prefKey': 'subHighlightPeriscopeHitNoLockRed', 'default': DefaultColors.RED},
    'GREEN': {'prefKey': 'subHighlightPeriscopeHitNoLockGreen', 'default': DefaultColors.GREEN},
    'BLUE':  {'prefKey': 'subHighlightPeriscopeHitNoLockBlue', 'default': DefaultColors.BLUE},
}
PS_NO_HIT_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightPeriscopeNoHitLockOpacity', 'default': 1},
    'RED':   {'prefKey': 'subHighlightPeriscopeNoHitLockRed', 'default': 0},
    'GREEN': {'prefKey': 'subHighlightPeriscopeNoHitLockGreen', 'default': 0},
    'BLUE':  {'prefKey': 'subHighlightPeriscopeNoHitLockBlue', 'default': 0},
}
PS_NO_HIT_NO_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightPeriscopeNoHitNoLockOpacity', 'default': 0.5},
    'RED':   {'prefKey': 'subHighlightPeriscopeNoHitNoLockRed', 'default': 0},
    'GREEN': {'prefKey': 'subHighlightPeriscopeNoHitNoLockGreen', 'default': 0},
    'BLUE':  {'prefKey': 'subHighlightPeriscopeNoHitNoLockBlue', 'default': 0},
}
UW_HIT_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightUnderwaterHitLockOpacity', 'default': 0.2},
    'RED':   {'prefKey': 'subHighlightUnderwaterHitLockRed', 'default': DefaultColors.RED},
    'GREEN': {'prefKey': 'subHighlightUnderwaterHitLockGreen', 'default': DefaultColors.GREEN},
    'BLUE':  {'prefKey': 'subHighlightUnderwaterHitLockBlue', 'default': DefaultColors.BLUE},
}
UW_HIT_NO_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightUnderwaterHitNoLockOpacity', 'default': 0.1},
    'RED':   {'prefKey': 'subHighlightUnderwaterHitNoLockRed', 'default': DefaultColors.RED},
    'GREEN': {'prefKey': 'subHighlightUnderwaterHitNoLockGreen', 'default': DefaultColors.GREEN},
    'BLUE':  {'prefKey': 'subHighlightUnderwaterHitNoLockBlue', 'default': DefaultColors.BLUE},
}
UW_NO_HIT_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightUnderwaterNoHitLockOpacity', 'default': 1},
    'RED':   {'prefKey': 'subHighlightUnderwaterNoHitLockRed', 'default': 0},
    'GREEN': {'prefKey': 'subHighlightUnderwaterNoHitLockGreen', 'default': 0},
    'BLUE':  {'prefKey': 'subHighlightUnderwaterNoHitLockBlue', 'default': 0},
}
UW_NO_HIT_NO_LOCK_PREFS = {
    'ALPHA': {'prefKey': 'subHighlightUnderwaterNoHitNoLockOpacity', 'default': 0.5},
    'RED':   {'prefKey': 'subHighlightUnderwaterNoHitNoLockRed', 'default': 0},
    'GREEN': {'prefKey': 'subHighlightUnderwaterNoHitNoLockGreen', 'default': 0},
    'BLUE':  {'prefKey': 'subHighlightUnderwaterNoHitNoLockBlue', 'default': 0}
}

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

VALUE_STEPS = 20
PREFS = [
    {'prefBaseKey': NAME_COLOR_TO_PREF_BASE_KEYS[d.name], 'colorName': d.name, 'default': d.value * VALUE_STEPS}
    for d in ui.getDefaultSubmarineUnderwaterColors()
]

class ColorPref(object):
    def __init__(self, prefs):
        self._alphaPref = prefs['ALPHA']
        self._redPref = prefs['RED']
        self._greenPref = prefs['GREEN']
        self._bluePref = prefs['BLUE']

    def getValue(self, userPrefSection):
        a = ColorPref.readValue(userPrefSection, self._alphaPref)
        r = ColorPref.readValue(userPrefSection, self._redPref)
        g = ColorPref.readValue(userPrefSection, self._greenPref)
        b = ColorPref.readValue(userPrefSection, self._bluePref)
        return Vector4(r,g,b,a)
    
    @staticmethod
    def readValue(userPrefSection, pref):
        key = pref['prefKey']
        if key in userPrefSection:
            return userPrefSection[key] * 0.05
        else:
            return pref['default']


class Colors(object):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    ALPHA = 'Alpha'


class ColorPref(object):
    def __init__(self, colorName, defaultValue):
        if colorName in NAME_COLOR_TO_PREF_BASE_KEYS:
            self._prefBaseKey = NAME_COLOR_TO_PREF_BASE_KEYS[colorName]
            defaultValue = defaultValue * VALUE_STEPS
            self._defaults = {
                Colors.RED:   defaultValue[0],
                Colors.GREEN: defaultValue[1],
                Colors.BLUE:  defaultValue[2],
                Colors.ALPHA: defaultValue[3],
            }
        else:
            logError('color name is invalid: {}'.format(colorName))

    def getValue(self, userPrefSection):
        a = self.readValue(userPrefSection, Colors.ALPHA)
        r = self.readValue(userPrefSection, Colors.RED)
        g = self.readValue(userPrefSection, Colors.GREEN)
        b = self.readValue(userPrefSection, Colors.BLUE)
        return Vector4(r,g,b,a)
    
    def readValue(self, userPrefSection, color):
        default = self._defaults[color]
        return userPrefSection.get(self._prefBaseKey + color, default) / VALUE_STEPS


SECTION_NAME = 'chatBoxWidth'

COLOR_PREFS = {
    # Periscope
    'SurfaceHitLockColor':          ColorPref(PS_HIT_LOCK_PREFS),
    'SurfaceHitNoLockColor':        ColorPref(PS_HIT_NO_LOCK_PREFS),
    'SurfaceNoHitLockColor':        ColorPref(PS_NO_HIT_LOCK_PREFS),
    'SurfaceNoHitNoLockColor':      ColorPref(PS_NO_HIT_NO_LOCK_PREFS),
    # Underwater
    'UnderwaterHitLockColor':       ColorPref(UW_HIT_LOCK_PREFS),
    'UnderwaterHitNoLockColor':     ColorPref(UW_HIT_NO_LOCK_PREFS),
    'UnderwaterNoHitLockColor':     ColorPref(UW_NO_HIT_LOCK_PREFS),
    'UnderwaterNoHitNoLockColor':   ColorPref(UW_NO_HIT_NO_LOCK_PREFS),
}


class UserPrefsManager(object):
    def __init__(self):
        userPrefsEntity = dataHub.getSingleEntity('userPrefs')
        if userPrefsEntity:
            userPrefs =  userPrefsEntity[CC.userPrefs].userPrefs
        else:
            userPrefs = None
            logError('User Prefs Entity does not exist!')

        self.userPrefs = userPrefs
        events.onUserPrefsChanged(self.onUserPrefsChanged)

    def onUserPrefsChanged(self, *args):
        if self.userPrefs is None:
            return
        
        for pref in PREFS:
            baseKey = pref['prefBaseKey']
            colorName = pref['colorName']
            default = pref['default']

            r = self.userPrefs.get(baseKey + 'Red',     default[0]) / VALUE_STEPS
            g = self.userPrefs.get(baseKey + 'Green',   default[1]) / VALUE_STEPS
            b = self.userPrefs.get(baseKey + 'Blue',    default[2]) / VALUE_STEPS
            a = self.userPrefs.get(baseKey + 'Opacity', default[3]) / VALUE_STEPS

            ui.setSubmarineUnderwaterColor(colorName, Vector4(r,g,b,a))
        
        section = self.userPrefs.get(SECTION_NAME, {})
        for colorName, colorPref in COLOR_PREFS.items():
            color = colorPref.getValue(section)
            ui.setSubmarineUnderwaterColor(colorName, color)

prefsManager = UserPrefsManager()