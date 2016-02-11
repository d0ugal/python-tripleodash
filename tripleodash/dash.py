import urwid

import tripleodash
from tripleodash import palette
from tripleodash.sections import nodes
from tripleodash.sections import overview
from tripleodash.sections import stacks
from tripleodash import util


class Dashboard(urwid.WidgetWrap):

    def __init__(self, update_interval):

        self._list_box = None
        self._content_walker = None
        self._interval = update_interval
        self._widgets = {}

        self.overview_window()

        super(Dashboard, self).__init__(self.main_window())

    def handle_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):

        screen = urwid.raw_display.Screen()
        screen.register_palette(palette.palette)
        screen.set_terminal_properties(256)

        self._loop = urwid.MainLoop(self, screen=screen,
                                    unhandled_input=self.handle_q)
        self._loop.set_alarm_in(self._interval, self.tick)
        self._loop.run()

    def main_window(self):

        content_wrap = self.update_content()

        vline = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'line')
        menu = self.menu()
        w = urwid.Columns([
            menu,
            ('fixed', 1, vline),
            ('weight', 5, content_wrap),
        ], dividechars=1, focus_column=0)

        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
        w = urwid.AttrWrap(w, 'body')
        w = urwid.LineBox(w)
        w = urwid.AttrWrap(w, 'line')
        return w

    def update_content(self):

        self._active_widget.update()
        widgets = self._active_widget.widgets()

        if self._content_walker is None:
            self._content_walker = urwid.SimpleListWalker(widgets)
        else:
            self._content_walker[:] = widgets

        if self._list_box is None:
            self._list_box = urwid.ListBox(self._content_walker)

        return self._list_box

    def nodes_window(self, loop=None, user_data=None):
        if 'nodes' not in self._widgets:
            self._widgets['nodes'] = nodes.NodesWidget()
        self._active_widget = self._widgets['nodes']

    def stack_window(self, loop=None, user_data=None):
        if 'stack' not in self._widgets:
            self._widgets['stack'] = stacks.StackWidget()
        self._active_widget = self._widgets['stack']

    def overview_window(self, loop=None, user_data=None):
        if 'overview' not in self._widgets:
            self._widgets['overview'] = overview.OverviewWidget()
        self._active_widget = self._widgets['overview']

    def menu(self):

        l = [
            util.main_header("TripleO Dashboard", align="center"),
            util.subtle("v{0}".format(tripleodash.RELEASE_STRING),
                        align="center"),
            urwid.Divider(),
            urwid.Divider(),
            util.button("Overview", self.overview_window),
            util.button("Nodes", self.nodes_window),
            util.button("Stack", self.stack_window),
            urwid.Divider(),
            urwid.Divider(),
            util.exit_button("Quit")
        ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        w.set_focus(3)
        return w

    def tick(self, loop=None, user_data=None):

        self.update_content()

        self.animate_alarm = self._loop.set_alarm_in(self._interval, self.tick)
