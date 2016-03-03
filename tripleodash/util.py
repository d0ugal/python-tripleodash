import urwid


def button(t, *fns):

    def fn(*args, **kwargs):
        for fn_ in fns:
            fn_(*args, **kwargs)

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


def table_header(t):
    return header(t, 'center')
table_header.selectable = False


def row_a(t):
    return urwid.Text(("row_a", t), 'center')
row_a.selectable = True


def row_b(t):
    return urwid.Text(("row_b", t), 'center')
row_b.selectable = True


def heat_event_log_formatter(events):
    """Return the events in log format."""
    event_log = []
    log_format = ("%(event_time)s "
                  "[%(rsrc_name)s]: %(rsrc_status)s %(rsrc_status_reason)s")
    for event in list(events)[:200]:
        event_time = getattr(event, 'event_time', '')
        log = log_format % {
            'event_time': event_time.replace('T', ' '),
            'rsrc_name': getattr(event, 'resource_name', ''),
            'rsrc_status': getattr(event, 'resource_status', ''),
            'rsrc_status_reason': getattr(event, 'resource_status_reason', '')
        }
        event_log.append(log)

    return [urwid.Text(line, wrap="clip") for line in event_log]


class TableRow(urwid.WidgetWrap):

    def __init__(self, row, widths, widget=urwid.Text):

        self._selectable = widget.selectable
        self.row = row
        self.widths = widths

        row = [widget(str(r)) for r in self.row]
        cols = urwid.Columns(zip(self.widths, row))

        wrapped_cols = urwid.AttrMap(cols, None, 'reversed')
        super(TableRow, self).__init__(wrapped_cols)

    def selectable(self):
        return self._selectable

    def keypress(self, size, key):
        return key


class AutoTable(object):
    """urwid AutoTable

    The AutoTable takes a list of rows and and converts them to a list of
    widgets that will represent a table.
    """

    def __init__(self, rows):

        if len(set(len(row) for row in rows)) > 1:
            raise ValueError("All rows must be the same length.")

        self.header = rows[0]

        self.rows = rows[1:]

    def col_widths(self):
        """Calculate the required widths for the cols

        This takes each column, one at a time and finds the length required
        when it is converted to a string. We then take the maximum for each
        column and use that for the width (plus 1 for padding)
        """

        headers = [max(h.split(), key=len) for h in self.header]
        all_rows = [headers, ] + self.rows

        # Transpose the rows, so we have a list of cols
        cols = zip(*all_rows[::-1])

        # For each col, get the length of it's contents as a string and then
        # save the max for that col.
        widths = (max(len(str(cell)) for cell in col) for col in cols)

        # Add two to each width, for padding. Otherwise it can be hard to
        # distinguish the difference.
        return [w+2 for w in widths]

    def wrapped_widgets(self):
        """Create the widgets for the table

        For each col, create a TableRow with the calculated widths. By default
        this will style the Header row and then have an alternating style for
        the following rows.
        """

        widths = self.col_widths()

        yield TableRow(self.header, widths, table_header)
        yield urwid.Divider()

        for i, row in enumerate(self.rows):
            widget = row_a if i % 2 else row_b
            yield TableRow(row, widths, widget)
