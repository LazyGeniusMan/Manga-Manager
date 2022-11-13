import tkinter

from MangaManager_ThePromidius.Common.Templates.extension import ExtensionGUI
from MangaManager_ThePromidius.MetadataManager import comicinfo


class ExtensionApp(ExtensionGUI):
    name: str = "Volume Manager"

    def run(self):
        ...
    def serve_gui(self,master):
        a = tkinter.Label(master,text="This label is inside extension")
        a.pack(fill="both",expand=True)
        a = tkinter.Label(master, text="This label is inside extension")
        a.pack(fill="both", expand=True)
        a = tkinter.Label(master, text="This label is inside extension")
        a.pack(fill="both", expand=True)
        a = tkinter.Label(master, text="This label is inside extension")
        a.pack(fill="both", expand=True)
        a = tkinter.Label(master, text="This label is inside extension")
        a.pack(fill="both", expand=True)

        a = tkinter.Label(master, text="This label is inside extension")
        a.pack(fill="both", expand=True)

    def process(self) -> comicinfo.ComicInfo:
        ...
def runnnning():
    print("dffsdfsdfsdfsdf")