from abc import ABC, abstractmethod

from MangaManager_ThePromidius.MetadataManager import comicinfo


class Extension(ABC):
    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def process(self) -> comicinfo.ComicInfo:
        ...


class ExtensionGUI(Extension, ABC):
    name: str
    def __init__(self):
        super(ExtensionGUI, self).__init__()

    @abstractmethod
    def serve_gui(self,master):
        ...
