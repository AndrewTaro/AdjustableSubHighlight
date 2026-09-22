API_VERSION = 'API_v1.0'
MOD_NAME = 'AdjustableSubHighlight'

from Math import Vector4

try:
    import battle, events, dataHub, ui, constants, utils
except:
    pass

import Hub

CC = constants.UiComponents

def logInfo(*args):
    data = [str(i) for i in args]
    utils.logInfo( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )

def logError(*args):
    data = [str(i) for i in args]
    utils.logError( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )


# shortName -> full dotted key, from ttaro-subs-highlight.schema.json.  The short name IS the engine's
# own state name, the string ui.setSubmarineUnderwaterColor takes, so nothing is composed anywhere.
#
# The legacy store spent FOUR keys on each of these colours -- <base>Red/Green/Blue/Opacity, each a
# 0-20 step index divided by 20 at read time, so 32 keys and 5% quantisation for 8 colours.  The CMS
# packs all four channels into one `color` key (the packChannels migration).
PREF_KEYS = {
    'SurfaceHitLockColor':        'ttaro.subHighlight.psHitLock',
    'SurfaceHitNoLockColor':      'ttaro.subHighlight.psHitNoLock',
    'SurfaceNoHitLockColor':      'ttaro.subHighlight.psNoHitLock',
    'SurfaceNoHitNoLockColor':    'ttaro.subHighlight.psNoHitNoLock',
    'UnderwaterHitLockColor':     'ttaro.subHighlight.uwHitLock',
    'UnderwaterHitNoLockColor':   'ttaro.subHighlight.uwHitNoLock',
    'UnderwaterNoHitLockColor':   'ttaro.subHighlight.uwNoHitLock',
    'UnderwaterNoHitNoLockColor': 'ttaro.subHighlight.uwNoHitNoLock',
}


def _toVector4(data):
    """A `color` component -> Vector4(r, g, b, a) with each channel 0..1.

    Read the component's own unpacked floats, never `value`: a packed 0xAARRGGBB is >= 2**31 and
    the stored/migrated form is a float, so `value & 0xFF0000` would raise in py2.  `vec4` is
    already [r, g, b, a] -- the order the engine wants.  It is absent only on the framework's
    derive() exception fallback (VIEW_CONTRACT), hence the int()-guarded unpack below it.
    """
    vec = data.get('vec4')
    if vec is not None and len(vec) == 4:
        return Vector4(vec[0], vec[1], vec[2], vec[3])

    packed = int(data['value']) & 0xFFFFFFFF
    a = ((packed >> 24) & 0xFF) / 255.0
    r = ((packed >> 16) & 0xFF) / 255.0
    g = ((packed >> 8) & 0xFF) / 255.0
    b = (packed & 0xFF) / 255.0
    return Vector4(r, g, b, a)


def applyColor(stateName):
    ui.setSubmarineUnderwaterColor(stateName, _toVector4(gPrefs.data(stateName)))


def applyColors():
    """Push all eight colours into the engine.

    Unlike a read-in-the-draw-path consumer, this mod WRITES its values out, so a subscription is
    load-bearing here rather than an optimisation: without one a config-panel edit would not reach
    setSubmarineUnderwaterColor until the next launch.
    """
    for stateName in PREF_KEYS:
        applyColor(stateName)


def _colorPusher(stateName):
    # A factory, not a default argument: evDataChanged passes the component as the first
    # positional arg, which would land in a `_state=stateName` default and be pushed as the
    # state name.  Closing over the factory's parameter cannot be overwritten that way.
    def push(*args):
        applyColor(stateName)
    return push


def onPrefsReady():
    applyColors()
    # Per key, not subscribeAll: editing one colour would otherwise re-push all eight, seven of
    # them unchanged, on every write the config panel makes while a slider is dragged.
    for stateName in PREF_KEYS:
        gPrefs.subscribe(stateName, _colorPusher(stateName))


gPrefs = Hub.Prefs(MOD_NAME, PREF_KEYS, onReady=onPrefsReady)
