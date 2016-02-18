import datetime

import urwid

import tripleodash
from tripleodash import palette
from tripleodash.sections import nodes
from tripleodash.sections import overview
from tripleodash.sections import stacks
from tripleodash import util


class Dashboard(urwid.WidgetWrap):

    def __init__(self, clients, update_interval):

        self._clients = clients

        self._list_box = None
        self._content_walker = None
        self._interval = update_interval
        self._sections = {}
        self._time = None

        self.overview_window()
        self.update_time()

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

        vline = urwid.AttrMap(urwid.SolidFill(u'\u2502'), 'line')
        menu = self.menu()
        w = urwid.Columns([
            menu,
            ('fixed', 1, vline),
            ('weight', 5, content_wrap),
        ], dividechars=1, focus_column=0)

        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
        w = urwid.AttrMap(w, 'body')
        w = urwid.LineBox(w)
        w = urwid.AttrMap(w, 'line')
        return w

    def update_content(self):

        self._active_section.update()
        widgets = self._active_section.widgets()

        if self._content_walker is None:
            self._content_walker = urwid.SimpleListWalker(widgets)
        else:
            self._content_walker[:] = widgets

        if self._list_box is None:
            self._list_box = urwid.ListBox(self._content_walker)

        return self._list_box

    def nodes_window(self, loop=None, user_data=None):
        if 'nodes' not in self._sections:
            self._sections['nodes'] = nodes.NodesWidget(self._clients)
        self._active_section = self._sections['nodes']

    def stacks_window(self, loop=None, user_data=None):
        if 'stacks' not in self._sections:
            self._sections['stacks'] = stacks.StacksWidget(self._clients)
        self._active_section = self._sections['stacks']

    def overview_window(self, loop=None, user_data=None):
        if 'overview' not in self._sections:
            self._sections['overview'] = overview.OverviewWidget(
                self._clients)
        self._active_section = self._sections['overview']

    def _now(self):
        return datetime.datetime.now()

    def update_time(self):
        time_string = self._now().strftime("%H:%M:%S")
        if self._time is None:
            self._time = util.subtle(time_string, align="center")
        else:
            self._time.set_text(("subtle", time_string))

    def menu(self):

        l = [
            util.main_header("TripleO Dashboard", align="center"),
            util.subtle("v{0}".format(tripleodash.RELEASE_STRING),
                        align="center"),
            self._time,
            urwid.Divider(),
            urwid.Divider(),
            util.button("Overview", self.overview_window),
            util.button("Nodes", self.nodes_window),
            util.button("Stacks", self.stacks_window),
            urwid.Divider(),
            urwid.Divider(),
            util.exit_button("Quit")
        ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        w.set_focus(3)
        return w

    def tick(self, loop=None, user_data=None):

        self.update_time()
        self.update_content()

        self.animate_alarm = self._loop.set_alarm_in(self._interval, self.tick)
