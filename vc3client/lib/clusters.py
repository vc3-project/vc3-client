#!/usr/bin/env python   


from plugin import PluginManager

class ClustersMgr(object):

    def __init__(self):
        pass
    
    def add(self):
        pass

    def delete(self):
        pass 

    def list(self):
        pass

    def get(self):
        pass

    def _getplugin(self):
        pluginmgr = PluginManager(self)
        plugin = pluginmgr.getplugin(......)
