from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa


info = PluginInfo(
    title='Mail',
    icon='mail',
    dependencies=[
        PluginDependency('main'),
    ],
)


def init():
    import main

