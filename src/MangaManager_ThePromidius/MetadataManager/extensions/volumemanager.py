import tkinter as tk
from tkinter.ttk import Treeview

from MangaManager_ThePromidius.Common.Templates.extension import ExtensionGUI
from MangaManager_ThePromidius.MetadataManager import comicinfo

_GRID_ARGS = {"sticky": "nwse"}
_PACK_ARGS = {"expand": True, "fill": "both"}


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
        starting_volume = tk.Spinbox(master, justify="center")
        starting_volume.grid()

        tk.Button(master, text="Preview", command=self._preview_changes).grid()
        _treeview_1 = Treeview(master)
        _treeview_1_cols = ['old_name', 'to', 'new_name']
        _treeview_1_dcols = ['old_name', 'to', 'new_name']
        _treeview_1.configure(columns=_treeview_1_cols, displaycolumns=_treeview_1_dcols)
        _treeview_1.column('#0', anchor='w', stretch=True, width=0, minwidth=0)
        _treeview_1.column('old_name', anchor='center', stretch=False, width=525, minwidth=20)
        _treeview_1.column('to', anchor='center', stretch=False, width=26, minwidth=26)
        _treeview_1.column('new_name', anchor='center', stretch=True, width=525, minwidth=20)
        _treeview_1.heading('#0', anchor='w', text='column_1')
        _treeview_1.heading('old_name', anchor='center', text='OLD NAME')
        _treeview_1.heading('to', anchor='center', text='to')
        _treeview_1.heading('new_name', anchor='center', text='NEW NAME')
        _treeview_1.grid()
        _treeview_1.grid_propagate(False)

        control_buttons = tk.Frame(master)
        control_buttons.grid()

        tk.Button(control_buttons, text="Clear Queue", width=15, font="{Custom} 11 {bold}").grid(row=0, column=0)
        tk.Button(control_buttons, text="Proceed", width=15, font="{Custom} 11 {bold}").grid(row=0, column=1)
        # a.pack(fill="both", expand=True)

    def process(self) -> comicinfo.ComicInfo:
        ...

    def _preview_changes(self, event):
        ...

    # def validateIntVar(self, *args):
    #     try:
    #         # if self.spinbox_3_volume_var.get() < -1 or
    #         if not isinstance(self._spinbox_1_volume_number_val.get(), int):
    #             self.mainwindow.bell()
    #             self._spinbox_1_volume_number_val.set(-1)
    #         else:
    #             self._spinbox_1_volume_number_val_prev.set(self._spinbox_1_volume_number_val.get())
    #     except tk.TclError as e:
    #         if str(e) == 'expected floating-point number but got ""' or str(
    #                 e) == 'expected floating-point number but got "-"':
    #             return
    #         elif re.match(r"-[0-9]*", str(e)):
    #             return
    #         self.mainwindow.bell()
    #         if self._spinbox_1_volume_number_val_prev.get() != (-1):
    #             self._spinbox_1_volume_number_val.set(self._spinbox_1_volume_number_val_prev.get())
    #             return
    #         self._spinbox_1_volume_number_val.set(-1)


def runnnning():
    print("dffsdfsdfsdfsdf")
