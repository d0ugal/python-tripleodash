# coding: utf-8

import urwid

from tripleodash.sections.base import DashboardSection

LOGO = '''
  ,   .   ,
  )-_"""_-(
 ./ o\ /o \.
. \__/ \__/ .
...   V   ...
... - - - ...
 .   - -   .
  `-.....-´
'''


class About(DashboardSection):

    def __init__(self, clients):
        super(About, self).__init__(clients, "About")

    def widgets(self):
        widgets = [urwid.Text(l) for l in LOGO.splitlines()]
        return super(About, self).widgets() + widgets
