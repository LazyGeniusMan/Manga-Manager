import glob
import importlib
from os.path import dirname, basename, isfile, join

from MangaManager_ThePromidius.Common.GUI.widgets import ScrolledFrameWidget
from MangaManager_ThePromidius.Common.Templates.extension import ExtensionGUI

modules = glob.glob(join(join(dirname(__file__),"extensions"), "*.py"))
extensions = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
import tkinter
root = tkinter.Tk()
for extension in extensions:
    extension_app: ExtensionGUI = importlib.import_module(f'extensions.{extension}').ExtensionApp()

    a = tkinter.Toplevel(root)
    a.title(f'Extension: {extension_app.name}')
    b = tkinter.Label(a,text="fdsfsfds")
    b.pack()

    top_level_frame = ScrolledFrameWidget(a, scrolltype="vertical")
    top_level_frame.pack()
    a.top_level_frame = top_level_frame.create_frame()

    extension_app.serve_gui(a.top_level_frame)
    ScrolledFrameWidget()

    root.mainloop()
