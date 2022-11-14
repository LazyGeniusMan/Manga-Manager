import logging
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview

from MangaManager_ThePromidius.Common.Templates.extension import ExtensionGUI
from MangaManager_ThePromidius.MetadataManager import comicinfo

_GRID_ARGS = {"sticky": "nwse"}
_PACK_ARGS = {"expand": True, "fill": "both"}

logger = logging.getLogger(__name__)

class ExtensionApp(ExtensionGUI):
    name: str = "Volume Manager"

    # TODO: settings
    #   Auto increase volume numbers after processign
    #   Open File selector Dialog after Processing
    #   Automatic preview
    #   Add volume to cinfo
    #   Don't rename file. Only add to ComicInfo

    def run(self):
        ...

    def serve_gui(self, master: tk.Frame):
        tk.Label(master, text="Volume Manager", font="{Title} 20 {bold}").grid(row=0, **_GRID_ARGS)

        tk.Label(master, text='This script will append Vol.XX just before any Ch X.ext / Chapter XX.ext',
                 font='{subheader} 12 {}').grid(row=1, **_GRID_ARGS)
        tk.Label(master, text='This naming convention must be followed for the script to work properly'). \
            grid(row=2, **_GRID_ARGS)

        tk.Label(master, text='Volume number to apply to the selected files').grid()
        self.starting_volume = tk.Spinbox(master, justify="center")
        self.starting_volume.grid()

        self.preview_btn = tk.Button(master, text="Preview", command=self._preview_changes)
        self.preview_btn.grid()
        self.treeview = Treeview(master)
        _treeview_1_cols = ['old_name', 'to', 'new_name']
        _treeview_1_dcols = ['old_name', 'to', 'new_name']
        self.treeview.configure(columns=_treeview_1_cols, displaycolumns=_treeview_1_dcols)
        self.treeview.column('#0', anchor='w', stretch=True, width=0, minwidth=0)
        self.treeview.column('old_name', anchor='center', stretch=False, width=525, minwidth=20)
        self.treeview.column('to', anchor='center', stretch=False, width=26, minwidth=26)
        self.treeview.column('new_name', anchor='center', stretch=True, width=525, minwidth=20)
        self.treeview.heading('#0', anchor='w', text='column_1')
        self.treeview.heading('old_name', anchor='center', text='OLD NAME')
        self.treeview.heading('to', anchor='center', text='to')
        self.treeview.heading('new_name', anchor='center', text='NEW NAME')
        self.treeview.grid()
        self.treeview.grid_propagate(False)
        s = ttk.Style()
        s.configure('Treeview', rowheight=20, rowpady=5, rowwidth=365)

        control_buttons = tk.Frame(master)
        control_buttons.grid()

        self.clear_btn = tk.Button(control_buttons, text="Clear Queue", width=15, font="{Custom} 11 {bold}")
        self.clear_btn.grid(row=0, column=0)
        self.proceed_btn = tk.Button(control_buttons, text="Proceed", width=15, font="{Custom} 11 {bold}")
        self.proceed_btn.grid(row=0, column=1)
        # a.pack(fill="both", expand=True)

    def process(self) -> comicinfo.ComicInfo:
        ...

    def _clear_queue(self):
        ...
