"""
This plugin adds a new select attribute to the filter syntax.

The attribute can be passed in a select command using the name 'in'. 
It takes one "parent tiddler" name as a value and 
selects all tiddlers the parent links to as well as the parent itself.

An example usage would be:

    select=in:MainMenu

This will select MainMenu (the parent) and all the tiddlers 
MainMenu links to.

In order to find the tiddlylinks, the parent tiddler is 
retrieved from the store and its contents are parsed for 
tiddlylinks and saved in a list.

Each call to the filter checks if the current tiddler is 
in the list of tiddlylinks. In this way the filter selects 
only tiddlers referenced by the parent.

The filter was written as a class so that the list of 
tiddlylinks could be preserved across calls, and so avoid
having to retrieve the parent from the store for every tiddler 
being checked.

Note: The regular expressions are rough. They 
are almost definitely missing some special cases
right now (like slice syntax). The safest thing
would be to copy the TiddlyWiki core's regexps.

"""

from tiddlyweb.filters.select import ATTRIBUTE_SELECTOR
from tiddlyweb.store import NoTiddlerError
from tiddlyweb.model.tiddler import Tiddler

import re

class TiddlyLinkFilter():
    """
    Provides a select attribute that takes the name of a 
    parent tiddler and returns true for all tiddlers the 
    parent links to.
    """

    def __init__(self):
        self.parent = Tiddler("uninitialized")
        self.bags_checked = []
        self.tiddlylinks = []

    def __call__(self, tiddler, attribute, value):
        # The value parameter holds the name of the parent. Its links
        # are retrieved only on the first call or if the tiddler being checked 
        # comes from a bag not already encountered. Subsequent calls go straight to 
        # the boolean _parent_has_link function.
        if self.parent.title != value or tiddler.bag not in self.bags_checked:
            self._get_links_in_parent(tiddler, value)
            self.bags_checked.append(tiddler.bag)

        return self._parent_has_link(tiddler)

    def _parent_has_link(self, tiddler):
        return tiddler.title in self.tiddlylinks

    def _get_links_in_parent(self, tiddler, value):
        """
        Try to get parent from store, and make a list of the tiddlylinks it contains. 
        """
        temp_tiddler = Tiddler("temp")
        temp_tiddler.title = value
        temp_tiddler.bag = tiddler.bag
        
        try:
            self.parent = tiddler.store.get(temp_tiddler)
            self._parse_tiddlylinks()
        except NoTiddlerError:
            pass

    def _parse_tiddlylinks(self):
        parent = self.parent
        CamelCase = "[A-Z][^\s]*?[A-Z][^\s]*?\s"
        bracketed = "\[\[(.*?)\]\]"
        results = re.findall(CamelCase, parent.text)
        results.extend(re.findall(bracketed, parent.text))

        tiddlylinks = [parent.title]
        for r in results[:]:
            parts = r.split("|")
            tiddlylinks.append(parts[len(parts) - 1].strip())

        self.tiddlylinks = tiddlylinks
            
def init(config):
    tlf = TiddlyLinkFilter()
    ATTRIBUTE_SELECTOR['in'] = tlf
