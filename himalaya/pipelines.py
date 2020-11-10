# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging
import json
from six.moves.urllib.parse import urlparse

from scrapy.utils.project import get_project_settings
from scrapy.pipelines.files import FilesPipeline
from .items import TrackItem, TrackFileItem

SETTING = get_project_settings()
DATA_ROOT = SETTING.get(
    'DATA_ROOT',
    "/data/share"
)
log = logging.getLogger(__name__)


class HimalayaPipeline(object):
    def __init__(self):
        self.prefix = None
        self.track_fh = None

    def open_spider(self, spider):
        album_id = spider.album_id
        self.prefix = os.path.join(
            SETTING.get("FILES_STORE", "data"),
            str(album_id)
        )

        if not os.path.isdir(self.prefix):
            old_mask = os.umask(000)
            os.makedirs(self.prefix)
            os.umask(old_mask)

        self.track_fh = os.open(
            os.path.join(
                self.prefix,
                'tracks.txt'
            ),
            os.O_RDWR | os.O_APPEND | os.O_CREAT
            # os.O_APPEND | os.O_CREAT
        )

    def close_spider(self, spider):
        os.close(self.track_fh)
        with open(os.path.join(
            self.prefix,
            'tracks.txt'
        )) as f:
            for line in f.read().splitlines():
                if not line.strip():
                    continue
                track_info = json.loads(line.strip())
                track_file = os.path.join(
                    self.prefix,
                    os.path.split(track_info.get("url"))[-1]
                )
                if os.path.isfile(track_file):
                    media_ext = os.path.splitext(track_file)[-1]
                    new_path = os.path.join(
                        self.prefix,
                        "{}{}".format(
                            track_info.get("id"),
                            media_ext
                        )
                    )
                    log.debug("{} --> {}".format(
                        track_file,
                        new_path
                    ))
                    os.rename(track_file, new_path)

    def process_item(self, item, spider):
        if not isinstance(item, TrackItem):
            return item
        os.write(
            self.track_fh,
            json.dumps(
                dict(item),
                ensure_ascii=False,
            ).encode('utf-8')
        )
        os.write(self.track_fh, b"\n")
        os.fsync(self.track_fh)
        return item


class TrackFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return os.path.join(
            str(info.spider.album_id),
            os.path.basename(path)
        )
