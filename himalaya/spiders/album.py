# -*- coding: utf-8 -*-

import os
import json
import scrapy
from himalaya.items import TrackItem, TrackFileItem

TRACK_INFO = "https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1"


class AlbumSpider(scrapy.Spider):
    name = 'album'
    # start_urls = ['https://www.ximalaya.com/youshengshu/40387701']
    # track_info = "https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1"
    album_id = None

    def __init__(self, album_url=None, *args, **kwargs):
        super(AlbumSpider, self).__init__(*args, **kwargs)
        if album_url:
            self.start_urls = [album_url]
            self.album_id = os.path.split(
                album_url.strip().strip("/")
            )[-1]

    def parse(self, response):
        for track_li in response.xpath('//li[@class="lF_"]'):
            idx = track_li.xpath(
                './/span[@class="num lF_"]/text()'
            ).extract_first()
            title = track_li.xpath('./div/a/@title').extract_first()
            link = track_li.xpath('./div/a/@href').extract_first()
            if not idx or not title or not link:
                continue
            track_id = os.path.split(link)[-1]
            album_id = self.album_id

            yield scrapy.Request(
                TRACK_INFO.format(track_id),
                callback=self.parse_track_info,
                dont_filter=True,
                meta={
                    "idx": idx,
                    "title": title,
                    "track_id": track_id,
                    "album_id": album_id
                }
            )
        next_page_url = response.xpath(
            '//li[@class="page-next page-item _Xo"]/a[@class="page-link _Xo"]/@href'
        ).extract_first()
        if next_page_url:
            yield scrapy.Request(
                response.url_join(next_page_url),
                callback=self.parse
            )

    def parse_track_info(self, response):
            try:
                track_info = json.loads(response.body_as_unicode())
            except Exception as e:
                self.logger.error("track info", exc_info=True)
                return None
            # self.logger.debug(json.dumps(track_info))
            track_url = track_info.get("data", {}).get("src")
            if not track_url:
                self.logger.error("No track url")
                return None
            yield TrackItem(
                id=response.meta.get('idx'),
                track_id=response.meta.get('track_id'),
                album_id=response.meta.get('album_id'),
                url=track_url
            )
            yield TrackFileItem(
                file_urls=[track_url]
            )

