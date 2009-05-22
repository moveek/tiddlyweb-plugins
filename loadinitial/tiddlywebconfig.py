# Here is a workable start config for an experimental load-on-demand setup.
# It is intended to make a logical list of tiddlers available at start up

config = {
    'system_plugins': ['mselect', 'loadinitial', 'tiddlylinkfilter'],

    'initial_tiddlers': {
	    'in': ['DefaultTiddlers', 'MainMenu', 'StyleSheet', 'PageTemplate'],
	    'tag': ['systemConfig'],
	    'title': ['SiteTitle', 'SiteSubtitle']
    },

}


