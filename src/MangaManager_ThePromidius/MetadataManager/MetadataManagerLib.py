from __future__ import annotations

import abc
import logging
from abc import ABC
from io import StringIO

from . import comicinfo
from .cbz_handler import LoadedComicInfo
from .comicinfo import ComicInfo
from .errors import NoComicInfoLoaded, CorruptedComicInfo, BadZipFile, EditedCinfoNotSet

logger = logging.getLogger("MetadataManager.Core")


class _IMetadataManagerLib(abc.ABC):
    @abc.abstractmethod
    def on_badzipfile_error(self, exception, file_path):
        """
        Called while loading a file and it's not a valid zip or it's broken
        """

    @abc.abstractmethod
    def on_corruped_metadata_error(self, exception, loaded_info: LoadedComicInfo):
        """
        Called while loading a file, and it's metadata can't be read.
        """

    @abc.abstractmethod
    def on_writing_error(self, exception, loaded_info: LoadedComicInfo):
        """
        Called while trying to save to the file.
        Posible callees (but not limited to): FailedBackup,
        """

    @abc.abstractmethod
    def on_writing_exception(self, exception, loaded_info: LoadedComicInfo):
        """
        Called when an unhandled exception occurred trying to save the file
        """


class MetadataManagerLib(_IMetadataManagerLib, ABC):
    """
    The core of metadata editor.
    It has the logic to merge all the data of each fields across multiple files.
    """
    selected_files_path = None
    new_edited_cinfo: ComicInfo | None = None
    loaded_cinfo_list: list[LoadedComicInfo] = list()
    CINFO_TAGS: list[str] = ('Title', 'Series', 'LocalizedSeries', 'SeriesSort', 'Summary', 'Genre', 'Tags', 'AlternateSeries', 'Notes', 'AgeRating', 'CommunityRating', 'ScanInformation', 'StoryArc', 'AlternateCount', 'Writer', 'Inker', 'Colorist', 'Letterer', 'CoverArtist', 'Editor', 'Translator', 'Publisher', 'Imprint', 'Characters', 'Teams', 'Locations', 'Number', 'AlternateNumber', 'Count', 'Volume', 'PageCount', 'Year', 'Month', 'Day', 'StoryArcNumber', 'LanguageISO', 'Format', 'BlackAndWhite', 'Manga')
    MULTIPLE_VALUES_CONFLICT = "~~## Multiple Values in this Field - Keep Original Values ##~~"

    def proces(self, tags_to_process=None):
        """
        Core function
        Reads the new cinfo class and compares it against all LoadedComicInfo.
        Applies the changes to the LoadedComicInfo unless the value in cinfo is a special one (-1 -keep current,-2 - clear field)
        :param tags_to_process list of cinfo tags that should be processed. Default is all of
        :return: list of loadedcinfo that failed to update :
        """
        if not self.loaded_cinfo_list:
            raise NoComicInfoLoaded()
        if tags_to_process:
            self.CINFO_TAGS = tags_to_process
        self.merge_changed_metadata()
        self.preview_export()
        for loaded_info in self.loaded_cinfo_list:
            # noinspection PyBroadException
            try:
                loaded_info.write_metadata()
            except PermissionError as e:
                logger.error("Failed to write changes because of missing permissions "
                             "or because other program has the file opened", exc_info=True)
                self.on_writing_error(exception=e, loaded_info=loaded_info)
                # failed_processing.append(loaded_info)
            except Exception as e:
                logger.exception("Unhandled exception saving changes")
                self.on_writing_exception(exception=e, loaded_info=loaded_info)

    def load_cinfo_list(self) -> None:
        """
        Creates a list of comicinfo with the comicinfo metadata from the selected files.
        :param string file_path: the path to the zip-like file

        :raises CorruptedComicInfo: If the data inside ComicInfo.xml could not be read after trying to fix te data
        :raises BadZipFile: If the provided zip is not a valid zip or is broken
        """

        logger.debug("Loading files")
        self.loaded_cinfo_list: list[LoadedComicInfo] = list()
        for file_path in self.selected_files_path:
            try:
                loaded_cinfo = LoadedComicInfo(path=file_path)
            except CorruptedComicInfo as e:
                # Logging is handled already in LoadedComicInfo load_metadata method
                loaded_cinfo = LoadedComicInfo(path=file_path, comicinfo=comicinfo.ComicInfo())
                self.on_corruped_metadata_error(e, loaded_info=loaded_cinfo or file_path)
                continue
            except BadZipFile as e:
                logger.error("Bad zip file. Either the format is not correct or the file is broken", exc_info=False)
                self.on_badzipfile_error(e, file_path=file_path)
                continue
            self.loaded_cinfo_list.append(loaded_cinfo)
        logger.debug("Files selected")

    def merge_changed_metadata(self):
        """
        Edited comic info gets applied to each loaded ComicInfo
        If edited version == '~~## Multiple Values in this Field ##~~' then original values are kept
        Else it applies the edited version.
        :return:
        """
        if self.new_edited_cinfo is None:
            raise EditedCinfoNotSet("Runtime error: Edited CINFO not set")

        for loaded_cinfo in self.loaded_cinfo_list:
            logger.debug(f"[Merging] Merging changes to {loaded_cinfo.file_path}")

            for cinfo_tag in self.CINFO_TAGS:
                new_value = self.new_edited_cinfo.get_attr_by_name(cinfo_tag)
                old_value = loaded_cinfo.cinfo_object.get_attr_by_name(cinfo_tag)
                # If the value in the ui is to keep original values then we continue with the next field
                if new_value == self.MULTIPLE_VALUES_CONFLICT:
                    logger.debug(
                        f"[Merging][{cinfo_tag:15s}] Keeping \x1b[31;1mOld\x1b[0m '\x1b[33;20m{old_value}\x1b[0m' vs New: '{new_value}'")
                    continue
                # Write whatever is in the new (edited) cinfo
                logger.debug(f"[Merging][{cinfo_tag:15s}] Keeping \x1b[31;1mNew\x1b[0m '{old_value}' vs "
                             f"New: '\x1b[33;20m{new_value}\x1b[0m' - Keeping new value")
                loaded_cinfo.cinfo_object.set_attr_by_name(cinfo_tag, new_value)

    def preview_export(self):
        for loaded_cinfo in self.loaded_cinfo_list:
            print(loaded_cinfo.__dict__)
            export = StringIO()
            print(loaded_cinfo.cinfo_object is None)
            loaded_cinfo.cinfo_object.export(export, 0)



