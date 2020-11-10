# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TrackItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    track_id = scrapy.Field()
    album_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

class TrackFileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class AlbumItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    filename = scrapy.Field()
