"""
GUI module.
"""

from __future__ import absolute_import
import os
try:
    # python 2.x
    from Tkinter import *
    from ttk import *
    from tkFileDialog import askopenfilenames, asksaveasfilename
    from tkMessageBox import showerror, showinfo
    from tkSimpleDialog import Dialog
except ImportError:
    # python 3.x
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.filedialog import askopenfilenames, asksaveasfilename
    from tkinter.messagebox import showerror, showinfo
    from tkinter.simpledialog import Dialog

try:
    import matplotlib.pyplot as plt
except ImportError:
    HAS_PLOTLIB = False
else:
    HAS_PLOTLIB = True

    def show_plots(x, ys, xlb, ylbs):
        """Plot multiple 2D line/point figures, which share a x-axis."""
        plt.close('all')
        n = len(ylbs)
        if n == 1:  # single plot
            _, ax = plt.subplots()
            ax.plot(x, ys[0], 'k-')
            ax.set_ylabel(ylbs[0])
        else:       # multiple plots
            _, axs = plt.subplots(n, sharex=True)
            for ax, y, ylb in zip(axs, ys, ylbs):
                ax.plot(x, y, 'k-')
                ax.set_ylabel(ylb)
        ax.set_xlabel(xlb)
        plt.show()

from . import __doc__ as DOC, __program__ as NAME, __version__ as VER
from .analysis import LogAnalyzer
from .datfile import DatFile
from .csvfile import CsvFile

INPTYPES = {'Amber': ('Amber MDOUT File', '.mdout .out'),
            'NAMD': ('NAMD Log File', '.log')}
OUTTYPES = {'Simple': ('Simple Data File', '.dat'),
            'CSV': ('Comma-Separated Values File', '.csv')}


class PyMDLogGUI(object):
    """PyMDLog GUI."""

    def __init__(self, parent=None):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # title
        # ----------
        title = Label(self.parent,
                      text=DOC,
                      anchor='center',
                      justify='center',
                      borderwidth=2,
                      background='dark slate blue',
                      foreground='white',
                      font='Arial 9 bold')
        title.pack(fill='both', expand=1, ipady=4, padx=4, pady=4)

        # main frame
        # ----------
        page = Frame()
        page.pack(fill='both', expand=1, padx=10, pady=10)

        # IO
        # ==========
        ioframe = LabelFrame(page, text='I/O')
        ioframe.pack(fill='both', expand=1)

        Label(ioframe, text='Input type:').grid(row=0, column=0, sticky='w')

        self.inptype = StringVar()

        types = sorted(INPTYPES.keys())
        OptionMenu(ioframe,
                   self.inptype,
                   'Amber',
                   *types).grid(row=0, column=1, sticky='w')

        Label(ioframe, text='Output type:').grid(row=0, column=2, sticky='w')

        self.outtype = StringVar()

        types = sorted(OUTTYPES.keys())
        OptionMenu(ioframe,
                   self.outtype,
                   'Simple',
                   *types).grid(row=0, column=3, sticky='w')

        Label(ioframe, text='Input files:').grid(row=1, column=0, sticky='w')

        self.inploc = StringVar()

        inpent = Entry(ioframe, textvariable=self.inploc)
        inpent.bind('<Escape>', func=lambda x: self.inploc.set(''))
        inpent.grid(row=1, column=1)

        Button(ioframe, command=self.on_browse_clicked,
               text='Browse').grid(row=1, column=2)

        Button(ioframe, command=self.on_load_clicked,
               text='Load').grid(row=1, column=3)

        Label(ioframe, text='Output file:').grid(row=2, column=0, sticky='w')

        self.outloc = StringVar()

        outent = Entry(ioframe, textvariable=self.outloc)
        outent.bind('<Escape>', func=lambda x: self.outloc.set(''))
        outent.grid(row=2, column=1)

        Button(ioframe, command=self.on_saveas_clicked,
               text='SaveAs').grid(row=2, column=2)

        # settings
        # ==========
        setframe = Frame(page)
        setframe.pack(fill='both', expand=1)

        itemframe = LabelFrame(setframe, text='Items')
        itemframe.grid(row=0, column=0, sticky='nesw')

        self.itembox = Listbox(itemframe, state='disabled', height=20)
        self.itembox.pack(fill='both', expand=1)

        butframe = Frame(setframe)
        butframe.grid(row=0, column=1)

        kw = [(self.on_addx_clicked, 'Add to X'),
              (self.on_addy_clicked, 'Add to Y'),
              (self.on_delx_clicked, 'Remove from X'),
              (self.on_dely_clicked, 'Remove from Y'),
              (self.on_upy_clicked, 'Up in Y'),
              (self.on_downy_clicked, 'Down in Y')]

        for c, t in kw:
            Button(butframe, command=c, text=t, width=16).grid()

        xyframe = Frame(setframe)
        xyframe.grid(row=0, column=2, sticky='nesw')

        xframe = LabelFrame(xyframe, text='X-axis')
        xframe.pack(side='top', fill='x', expand=1)

        self.xbox = Listbox(xframe, state='disabled', height=1)
        self.xbox.pack(fill='both', expand=1)

        yframe = LabelFrame(xyframe, text='Y-axis')
        yframe.pack(fill='x', expand=1)

        self.ybox = Listbox(yframe, state='disabled', height=16)
        self.ybox.pack(fill='both', expand=1)

        Separator(self.parent, orient='horizontal').pack(fill='x', expand=1)

        butframe = Frame(self.parent)
        butframe.pack(fill='both', expand=1)

        outbut = Button(butframe, text='Output',
                        command=self.on_output_clicked, default='active')
        plotbut = Button(butframe, text='Plot', command=self.on_plot_clicked,
                         state='normal' if HAS_PLOTLIB else 'disabled')
        quitbut = Button(butframe, text='Quit', command=self.parent.destroy)
        quitbut.pack(side='right', pady=4)
        plotbut.pack(side='right', pady=4)
        outbut.pack(side='right', pady=4)

    def on_browse_clicked(self):
        ext = INPTYPES[self.inptype.get()]
        files = askopenfilenames(defaultextension=ext[1],
                                 filetypes=[ext, ('All Files', '.*')])
        if files:
            self.inploc.set(files)

    def on_load_clicked(self):
        # check inputs
        if not self.inploc.get():
            showerror('ERROR!',
                      'Please specify input files.',
                      parent=self.parent)
        else:
            dialog = SortFileDialog(main=self, parent=self.parent,
                                    title='Sort Selected Files')
            if not dialog.ok_clicked:
                return
            self.inplocs = self.parent.tk.splitlist(self.inploc.get())
            ana = LogAnalyzer(self.inptype.get())
            try:
                self.data = ana.analyze(*self.inplocs)
            except Exception:
                showerror('ERROR!',
                          'Failed to parse the input files.',
                          parent=self.parent)
                return

            # clear/activate listboxes
            if self.itembox['state'] == 'normal':
                for w in self.itembox, self.xbox, self.ybox:
                    w.delete(0, 'end')
            else:
                for w in self.itembox, self.xbox, self.ybox:
                    w['state'] = 'normal'

            # put found items into the item box
            for k in self.data:
                self.itembox.insert('end', k)
            self.itembox.selection_set(0)

    def on_saveas_clicked(self):
        ext = OUTTYPES[self.outtype.get()]
        files = asksaveasfilename(defaultextension=ext[1],
                                  filetypes=[ext, ('All Files', '.*')])
        if files:
            self.outloc.set(files)

    def change_box(self, from_, to, idx):
        item = from_.get(idx)
        to.insert('end', item)
        from_.delete(idx)

    def update_box_sel(self, box, idx):
        if idx == box.size():
            idx = 0
        box.selection_set(idx)
        box.see(idx)

    def on_addx_clicked(self):
        # curselection() returns a tuple containing the line numbers
        # of the selected element or elements, counting from 0. if
        # nothing is selected, returns an empty tuple.
        ids = self.itembox.curselection()
        if not ids or self.xbox.size():
            return
        idx = int(ids[0])
        self.change_box(self.itembox, self.xbox, idx)
        self.update_box_sel(self.itembox, idx)

    def on_addy_clicked(self):
        ids = self.itembox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        self.change_box(self.itembox, self.ybox, idx)
        self.update_box_sel(self.itembox, idx)

    def on_delx_clicked(self):
        ids = self.xbox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        self.change_box(self.xbox, self.itembox, idx)

    def on_dely_clicked(self):
        ids = self.ybox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        self.change_box(self.ybox, self.itembox, idx)
        self.update_box_sel(self.ybox, idx)

    def move_item(self, box, idx, direc):
        offset = {'up': -1, 'down': 1}[direc]
        item = box.get(idx)
        box.delete(idx)
        box.insert(idx+offset, item)
        self.update_box_sel(box, idx+offset)

    def on_upy_clicked(self):
        ids = self.ybox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        if not idx:
            return
        self.move_item(self.ybox, idx, 'up')

    def on_downy_clicked(self):
        ids = self.ybox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        if idx == self.ybox.size()-1:
            return
        self.move_item(self.ybox, idx, 'down')

    def on_output_clicked(self):
        outloc = self.outloc.get()
        if not outloc or not self.xbox.size() or not self.ybox.size():
            showerror('ERROR!',
                      'Please specify X- and Y-axes and output file name.',
                      parent=self.parent)
        else:
            xlb = self.xbox.get(0)
            ylbs = self.ybox.get(0, 'end')
            x = self.data[xlb]
            ys = [self.data[i] for i in ylbs]
            try:
                if self.outtype.get() == 'Simple':
                    DatFile(outloc, 'w').write(x, *ys)
                else:
                    CsvFile(outloc, 'w').write(x, *ys)
            except Exception:
                showerror('ERROR!',
                          'Failed to generate output file.',
                          parent=self.parent)
            else:
                showinfo('INFO',
                         'Output file has been generated.',
                         parent=self.parent)

    def on_plot_clicked(self):
        if not HAS_PLOTLIB:
            return
        if not self.xbox.size() or not self.ybox.size():
            showerror('ERROR!',
                      'Please specify X- and Y-axes.',
                      parent=self.parent)
        else:
            xlb = self.xbox.get(0)
            ylbs = self.ybox.get(0, 'end')
            x = self.data[xlb]
            ys = [self.data[i] for i in ylbs]
            try:
                show_plots(x, ys, xlb, ylbs)
            except Exception:
                showerror('ERROR!',
                          'Failed to plot.',
                          parent=self.parent)


class SortFileDialog(Dialog):
    """Show selected files and sort."""

    def __init__(self, main, *args, **kwargs):
        self.main, self.ok_clicked, self.changed = main, False, False
        Dialog.__init__(self, *args, **kwargs)

    def body(self, master):
        frame = Frame(master)
        frame.pack(side='left', fill='both', expand=1)

        self.files = StringVar(value=self.main.inploc.get())
        self.lbox = Listbox(frame, listvariable=self.files, width=40)

        sbar = Scrollbar(frame, orient='vertical', command=self.lbox.yview)
        self.lbox.config(yscrollcommand=sbar.set)
        self.lbox.pack(side='left', fill='both', expand=1)
        sbar.pack(side='right', fill='y')
        self.lbox.selection_set(0)

        butbox = Frame(master)
        butbox.pack(side='right', fill='both', expand=1)

        kw = [(self.on_sort_clicked, 'Sort'),
              (self.on_up_clicked, 'Up'),
              (self.on_down_clicked, 'Down')]

        for c, t in kw:
            Button(butbox, command=c, text=t).grid()

        return self.lbox

    def buttonbox(self):
        """Use ttk widgets to override the original."""
        box = Frame(self)
        box.pack(fill='both', expand=1)

        okbut = Button(box, text='OK', command=self.ok, default='active')
        cclbut = Button(box, text='Cancel', command=self.cancel)
        cclbut.pack(side='right', padx=4)
        okbut.pack(side='right', pady=4)

    def apply(self):
        self.ok_clicked = True
        if self.changed:
            locs = self.lbox.get(0, 'end')
            self.main.inploc.set(' '.join(locs) if locs else locs[0])

    def update_box_sel(self, box, idx):
        if idx == box.size():
            idx = 0
        box.selection_set(idx)
        box.see(idx)

    def on_sort_clicked(self):
        locs = sorted(self.lbox.get(0, 'end'),
                      key=lambda f: os.path.basename(f))
        self.files.set(' '.join(locs) if len(locs) > 1 else locs[0])
        self.changed = True

    def move_item(self, box, idx, direc):
        offset = {'up': -1, 'down': 1}[direc]
        item = box.get(idx)
        box.delete(idx)
        box.insert(idx+offset, item)
        self.update_box_sel(box, idx+offset)

    def on_up_clicked(self):
        ids = self.lbox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        if not idx:
            return
        self.move_item(self.lbox, idx, 'up')
        self.changed = True

    def on_down_clicked(self):
        ids = self.lbox.curselection()
        if not ids:
            return
        idx = int(ids[0])
        if idx == self.lbox.size()-1:
            return
        self.move_item(self.lbox, idx, 'down')
        self.changed = True


def run_gui():
    """GUI mode."""
    root = Tk()
    root.title('%s %s' % (NAME, VER))
    PyMDLogGUI(root)
    root.mainloop()
