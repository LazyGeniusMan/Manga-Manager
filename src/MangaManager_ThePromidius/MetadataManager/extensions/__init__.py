import glob
import importlib
import os
import tkinter

from MangaManager_ThePromidius.Common.Templates.extension import ExtensionGUI


class ExtensionManaging:
    """
    Reads and parses the extensions in the package. Display buttons in the main app to open the extension
    """
    extension_window = None
    extension_window_exists = False
    extensions_tab_frame: tkinter.Frame
    master: tkinter.Tk

    def build_extension_tab(self):
        ext_frame = self.extensions_tab_frame

        modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
        extensions = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]

        for ext in extensions:
            extension_app: ExtensionGUI = importlib.import_module(f'.extensions.{ext}',
                                                                  package="src.MangaManager_ThePromidius"
                                                                          ".MetadataManager").ExtensionApp(self)
            tkinter.Button(ext_frame, text=extension_app.name, command=lambda:
                           self._create_ext_window(extension_app)
                           ).pack()

    def _close_ext_window(self):
        self.check = False
        self.extension_window.destroy()

    def _create_ext_window(self, extension_app):
        if self.extension_window_exists:
            self._close_ext_window()
        self.extension_window_exists = True
        # noinspection PyTypeChecker
        self.extension_window = tkinter.Toplevel(self)

        self.extension_window.protocol('WM_DELETE_WINDOW', self._close_ext_window)
        self.extension_window.title(f'Extension: {extension_app.name}')

        # frame = tkinter.Frame(self.extension_window)
        # frame.pack(expand=True, fill="both")
        # top_level_frame = ScrolledFrameWidget(frame, scrolltype="vertical", expand=True, fill="both")
        # self.extension_window.top_level_frame = top_level_frame.create_frame(expand=False,fill="none")
        extension_app.serve_gui(self.extension_window)

