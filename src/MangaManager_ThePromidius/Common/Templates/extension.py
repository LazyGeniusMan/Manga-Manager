from abc import ABC, abstractmethod

import src.MangaManager_ThePromidius.MetadataManager.MetadataManagerLib
from MangaManager_ThePromidius.MetadataManager import comicinfo


class Extension(ABC):
    def __init__(self, parent_class):
        self.parent:src.MangaManager_ThePromidius.MetadataManager.MetadataManagerLib.MetadataManagerLib = parent_class

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def process(self) -> comicinfo.ComicInfo:
        ...


class ExtensionGUI(Extension, ABC):
    name: str
    def __init__(self, parent_class):
        super(ExtensionGUI, self).__init__(parent_class)

    @abstractmethod
    def serve_gui(self,master):
        ...
