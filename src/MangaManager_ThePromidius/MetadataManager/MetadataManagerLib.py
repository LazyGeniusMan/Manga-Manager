from __future__ import annotations

import abc
import logging
from abc import ABC
from io import StringIO

from src.MangaManager_ThePromidius import settings as settings_class
from src.MangaManager_ThePromidius.Common.errors import NoComicInfoLoaded, CorruptedComicInfo, BadZipFile, \
    NoModifiedCinfo
from src.MangaManager_ThePromidius.Common.loadedcomicinfo import LoadedComicInfo
from . import comicinfo
from .comicinfo import ComicInfo

logger = logging.getLogger("MetadataManager.Core")
settings =settings_class.get_setting("main")

class _IMetadataManagerLib(abc.ABC):
    def on_item_loaded(self, loadedcomicInfo: LoadedComicInfo):
        """
        Called when a loadedcomicinfo is loaded
        :return:
        """

    @abc.abstractmethod
    def on_badzipfile_error(self, exception, file_path):
        """
        Called while loading a file, and it's not a valid zip or it's broken
        """

    @abc.abstractmethod
    def on_processed_item(self, loaded_info: LoadedComicInfo):
        """
        Called when  a file is successfully processed
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
    cinfo_tags: list[str] = ["Title", "Series", "Number", "Count", "Volume", "AlternateSeries", "AlternateNumber",
                             "AlternateCount", "Summary", "Notes", "Year", "Month", "Day", "Writer", "Penciller",
                             "Inker", "Colorist", "Letterer", "CoverArtist", "Editor", "Translator", "Publisher",
                             "Imprint", "Genre", "Tags", "Web", "PageCount", "LanguageISO", "Format", "BlackAndWhite",
                             "Manga", "Characters", "Teams", "Locations", "ScanInformation", "StoryArc",
                             "StoryArcNumber", "SeriesGroup", "AgeRating", "CommunityRating",
                             "MainCharacterOrTeam", "Review",
	    ]
    # cinfo_tags: list[str] = ['Title', 'Series', 'LocalizedSeries', 'SeriesSort', 'Summary', 'Genre', 'Tags',
    #                          'AlternateSeries', 'Notes', 'AgeRating', 'CommunityRating', 'ScanInformation', 'StoryArc',
    #                          'AlternateCount', 'Writer', 'Inker', 'Colorist', 'Letterer', 'CoverArtist', 'Editor',
    #                          'Translator', 'Publisher', 'Imprint', 'Characters', 'Teams', 'Locations', 'Number',
    #                          'AlternateNumber', 'Count', 'Volume', 'PageCount', 'Year', 'Month', 'Day',
    #                          'StoryArcNumber', 'LanguageISO', 'Format', 'BlackAndWhite', 'Manga']
    MULTIPLE_VALUES_CONFLICT = "~~## Keep Original Value ##~~"
    tags_with_multiple_values = []

    @property
    def loaded_cinfo_list_to_process(self) -> list[LoadedComicInfo]:
        return [loaded_cinfo for loaded_cinfo in self.loaded_cinfo_list if loaded_cinfo.has_changes]

    def process(self):
        """
        Core function
        Reads the new cinfo class and compares it against all LoadedComicInfo.
        Applies the changes to the LoadedComicInfo unless the value in cinfo is a special one (-1 -keep current,-2 - clear field)
        :return: list of loadedcinfo that failed to update :
        """
        try:
            if self.loaded_cinfo_list:
                if not self.loaded_cinfo_list_to_process:
                    raise NoModifiedCinfo()
            else:
                raise NoComicInfoLoaded()

            for loaded_info in self.loaded_cinfo_list_to_process:
                # noinspection PyBroadException
                self.preview_export(loaded_info)
                try:
                    loaded_info.write_metadata()
                    loaded_info.has_changes = False
                    self.on_processed_item(loaded_info)
                except PermissionError as e:
                    logger.error("Failed to write changes because of missing permissions "
                                 "or because other program has the file opened", exc_info=True)
                    self.on_writing_error(exception=e, loaded_info=loaded_info)
                    # failed_processing.append(loaded_info)
                except Exception as e:
                    logger.exception("Unhandled exception saving changes")
                    self.on_writing_exception(exception=e, loaded_info=loaded_info)
        finally:
            self.loaded_cinfo_list_to_proces: list[LoadedComicInfo] = list()

    def merge_changed_metadata(self, new_edited_cinfo: ComicInfo, loaded_cinfo_list: list[LoadedComicInfo]) -> bool:
        """
        Merges new_edited_cinfo with each individual loaded_cinfo.
        If field is ~~Multiple...Values~~, nothing will be changed.
        Else new_cinfo value will be saved
        :return: True if any loaded_cinfo has changes
        """
        LOG_TAG = "[Merging]"
        any_has_changes = False

        for loaded_cinfo in loaded_cinfo_list:
            logger.debug(f"{LOG_TAG} Merging changes to {loaded_cinfo.file_path}")
            for cinfo_tag in self.cinfo_tags:
                new_value = str(new_edited_cinfo.get_attr_by_name(cinfo_tag))
                if new_value == self.MULTIPLE_VALUES_CONFLICT:
                    logger.debug(f"{LOG_TAG} Ignoring {cinfo_tag}. Keeping old values")
                    continue
                old_value = str(loaded_cinfo.cinfo_object.get_attr_by_name(cinfo_tag))
                if old_value == new_value:
                    logger.debug(f"{LOG_TAG} Ignoring {cinfo_tag}. Field has not changed")
                    continue
                loaded_cinfo.has_changes = True
                loaded_cinfo.changed_tags.append((cinfo_tag,old_value,new_value))
                any_has_changes = True
                logger.debug(f"{LOG_TAG}[{cinfo_tag:15s}] Updating \x1b[31;1mNew\x1b[0m '{old_value}' vs "
                             f"New: '\x1b[33;20m{new_value}\x1b[0m' - Keeping new value")
                loaded_cinfo.cinfo_object.set_attr_by_name(cinfo_tag, new_value)
        return any_has_changes

    def open_cinfo_list(self) -> None:
        """
        Creates a list of comicinfo with the comicinfo metadata from the selected files.

        :raises CorruptedComicInfo: If the data inside ComicInfo.xml could not be read after trying to fix te data
        :raises BadZipFile: If the provided zip is not a valid zip or is broken
        """

        logger.debug("Loading files")
        self.loaded_cinfo_list: list[LoadedComicInfo] = list()
        for file_path in self.selected_files_path:
            try:
                loaded_cinfo = LoadedComicInfo(path=file_path)
                if settings.cache_cover_images:
                    loaded_cinfo.load_all()
                else:
                    loaded_cinfo.load_metadata()
            except CorruptedComicInfo as e:
                # Logging is handled already in LoadedComicInfo load_metadata method
                loaded_cinfo = LoadedComicInfo(path=file_path, comicinfo=comicinfo.ComicInfo()).load_metadata()
                self.on_corruped_metadata_error(e, loaded_info=loaded_cinfo or file_path)
                continue
            except BadZipFile as e:
                logger.error("Bad zip file. Either the format is not correct or the file is broken", exc_info=False)
                self.on_badzipfile_error(e, file_path=file_path)
                continue
            self.loaded_cinfo_list.append(loaded_cinfo)
            self.on_item_loaded(loaded_cinfo)
        logger.debug("Files selected")

    def preview_export(self, loaded_cinfo):
        """
        Debug function to preview loaded_cinfo in terminal
        :param loaded_cinfo:
        :return:
        """
        # print(loaded_cinfo.__dict__)
        export = StringIO()
        # print(loaded_cinfo.cinfo_object is None)
        loaded_cinfo.cinfo_object.export(export, 0)
        print(export.getvalue())


