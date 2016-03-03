import datetime
import math
import time

import urwid

import tripleodash
from tripleodash import palette
from tripleodash.sections import about
from tripleodash.sections import images
from tripleodash.sections import nodes
from tripleodash.sections import overview
from tripleodash.sections import servers
from tripleodash.sections import stacks
from tripleodash import util


class Dashboard(urwid.WidgetWrap):

    def __init__(self, clients, update_interval):

        self._clients = clients

        self._content_walker = None
        self._interval = update_interval
        self._last_update = time.time()
        self._list_box = None
        self._sections = {}
        self._time = None
        self._time_until_update = None
        self._update_duration = 0

        self.update_time(update_interval)
        self.overview_window()

        super(Dashboard, self).__init__(self.main_window())

    def handle_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key in ('a', 'A'):
            self.about_window()
            self._trigger_update()

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

    def images_window(self, loop=None, user_data=None):
        if 'images' not in self._sections:
            self._sections['images'] = images.ImagesWidget(self._clients)
        self._active_section = self._sections['images']

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

    def about_window(self, loop=None, user_data=None):
        if 'about' not in self._sections:
            self._sections['about'] = about.About(
                self._clients)
        self._active_section = self._sections['about']

    def servers_window(self, loop=None, user_data=None):
        if 'servers' not in self._sections:
            self._sections['servers'] = servers.ServersWidget(
                self._clients)
        self._active_section = self._sections['servers']

    def _now(self):
        return datetime.datetime.now()

    def update_time(self, seconds_until_update):
        time_string = self._now().strftime("%H:%M:%S")
        update = "Updating in {0:.0f}s".format(seconds_until_update)
        if self._time is None:
            self._time = util.subtle(time_string, align="center")
            self._time_until_update = util.subtle(update, align="center")
        else:
            self._time.set_text(("subtle", time_string))
            self._time_until_update.set_text(("subtle", update))

    def menu(self):

        l = [
            util.main_header("TripleO Dashboard", align="center"),
            util.subtle("v{0}".format(tripleodash.RELEASE_STRING),
                        align="center"),
            self._time,
            self._time_until_update,
            urwid.Divider(),
            util.button("Overview", self.overview_window,
                        self._trigger_update),
            util.button("Glance Images", self.images_window,
                        self._trigger_update),
            util.button("Ironic Nodes", self.nodes_window,
                        self._trigger_update),
            util.button("Heat Stacks", self.stacks_window,
                        self._trigger_update),
            util.button("Nova Servers", self.servers_window,
                        self._trigger_update),
            urwid.Divider(),
            urwid.Divider(),
            util.exit_button("Quit")
        ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        w.set_focus(3)
        return w

    def _update(self, loop=None, user_data=None):
        now = time.time()
        self.update_content()
        self._last_update = time.time()
        self._update_duration = self._last_update - now

    def _trigger_update(self, loop=None, user_data=None):
        self._time_until_update.set_text(("subtle", "Updating..."))
        self.animate_alarm = self._loop.set_alarm_in(0.1, self._update)

    def tick(self, loop=None, user_data=None):

        # Find out how long the last update took and use that as the interval
        # this time. Otherwise the UI will be frozen more than 50% of the time.
        # This still isn't ideal, it would be much better if the update was
        # non-blocking but until we can do this it will be a bit nicer to use.
        now = time.time()
        interval = max(self._interval, self._update_duration)

        seconds_until_update = math.ceil(interval - (now - self._last_update))
        self.update_time(seconds_until_update)

        if seconds_until_update <= 0:
            self._trigger_update()

        self.animate_alarm = self._loop.set_alarm_in(1, self.tick)
