import urwid


def button(t, fn):
    w = urwid.Button(t, fn)
    w = urwid.AttrWrap(w, 'button normal', 'button select')
    return w


def exit_button(t):

    def fn(*args, **kwargs):
        raise urwid.ExitMainLoop()

    return button(t, fn)


def main_header(t, **kwargs):
    return urwid.Text(("main header", "{0} ".format(t)), **kwargs)


def header(t, *args, **kwargs):
    return urwid.Text(("header", t), *args, **kwargs)


def subtle(t, **kwargs):
    return urwid.Text(("subtle", t), **kwargs)


def row_a(t):
    return urwid.Text(("row_a", t))


def row_b(t):
    return urwid.Text(("row_b", t))


def heat_event_log_formatter(events):
    """Return the events in log format."""
    event_log = []
    log_format = ("%(event_time)s "
                  "[%(rsrc_name)s]: %(rsrc_status)s  %(rsrc_status_reason)s")
    for event in events:
        event_time = getattr(event, 'event_time', '')
        log = log_format % {
            'event_time': event_time.replace('T', ' '),
            'rsrc_name': getattr(event, 'resource_name', ''),
            'rsrc_status': getattr(event, 'resource_status', ''),
            'rsrc_status_reason': getattr(event, 'resource_status_reason', '')
        }
        event_log.append(log)

    body = [urwid.Text(line) for line in event_log]

    return urwid.BoxAdapter(urwid.ListBox(urwid.SimpleListWalker(body)), 10)
