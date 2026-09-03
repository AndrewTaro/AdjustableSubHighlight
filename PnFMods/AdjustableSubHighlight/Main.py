API_VERSION = 'API_v1.0'
MOD_NAME = 'AdjustableSubHighlight'

from Math import Vector4

try:
    import battle, events, dataHub, ui, constants, utils
except:
    pass

import TTaroPrefs

CC = constants.UiComponents

def logInfo(*args):
    data = [str(i) for i in args]
    utils.logInfo( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )

def logError(*args):
    data = [str(i) for i in args]
    utils.logError( '[{}] {}'.format(MOD_NAME, ', '.join(data)) )


# shortName -> full dotted key, from subs-highlight.schema.json.  The short name IS the engine's
# own state name, the string ui.setSubmarineUnderwaterColor takes, so nothing is composed anywhere.
#
# The legacy store spent FOUR keys on each of these colours -- <base>Red/Green/Blue/Opacity, each a
# 0-20 step index divided by 20 at read time, so 32 keys and 5% quantisation for 8 colours.  The CMS
# packs all four channels into one `color` key (the packChannels migration), which is why the
# ColorPref class and its VALUE_STEPS are gone rather than renamed.
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

gPrefs = TTaroPrefs.PrefStore(MOD_NAME, PREF_KEYS)


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


def applyColors(*args):
    """Push all eight colours into the engine.

    Unlike a read-in-the-draw-path consumer, this mod WRITES its values out once, so a
    subscription is load-bearing here rather than an optimisation: without it a config-panel edit
    would not reach setSubmarineUnderwaterColor until the next launch.  The callback takes *args
    because evDataChanged passes the component and that arity is not contractual.
    """
    for stateName in PREF_KEYS:
        ui.setSubmarineUnderwaterColor(stateName, _toVector4(gPrefs.data(stateName)))


def onPrefsReady():
    applyColors()
    gPrefs.subscribeAll(applyColors)


gPrefs.start(onReady=onPrefsReady)
