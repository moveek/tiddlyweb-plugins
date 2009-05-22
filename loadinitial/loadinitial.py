"""
This plugin facilitates loading of only a selected collection 
of tiddlers when an user first opens a TiddlyWiki (instead of 
loading an entire recipe). It requires the presence of the
mselect plugin, and optionally the tiddlylinkfilter which provides
the select attribute 'in'.

The list of tiddlers to load can be specified as a dictionary
in the configuration file tiddlywebconfig.py.

the dictionary is read by the plugin and expanded into an
mselect query string.
"""

from tiddlyweb.web.query import Query

class LoadInitial():
    """
    WSGI environment manipulator that tacks an
    mselect query onto an incoming request to return 
    a subset of the tiddlers in the requested wiki.
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        # Only add filter if the request is for a tiddlywiki
        # that doesn't already contain a select query by the user.
        if environ['PATH_INFO'].find("tiddlers.wiki") != -1 and len(environ['QUERY_STRING']) == 0:
            self._add_filter_to_query(environ)

        return self.application(environ, start_response)
        
    def _add_filter_to_query(self, environ):
        initial_tiddlers = environ['tiddlyweb.config']['initial_tiddlers']

        # Expand the tiddlers from the config dictionary into an mselect query
        expanded_queries = []
        for sel_attribute, sel_list in initial_tiddlers.items():
            expanded_queries.append(",".join([sel_attribute+":"+sel_value for sel_value in sel_list]))
            
        environ['QUERY_STRING'] = "mselect=" + ",".join(expanded_queries) 


def init(config):
    config['server_request_filters'].insert(
        config['server_request_filters'].index(Query), LoadInitial)
