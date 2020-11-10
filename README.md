# Himalaya Album Downloader

喜马拉雅专辑音频下载器, Himalaya album track media files downloader. 
An experimental spider program for downloading album track media files from famous audio-sharing platfrom Himalaya(喜马拉雅), only for researching and learning, do not use this for commercial purpose.

## Technical information

This spider is developed based on Python3.0 and [scrapy](https://github.com/scrapy/scrapy) 2.4.0。

## Usage

Start spider with crawl.py script with album's url as only parameter, for example:

```shell
python crawl.py https://www.ximalaya.com/youshengshu/40387701
```
Downloaded media file will saved in *data* directory in top-level directory of this project  as default, a directory with album id as its name will be created, and all media file is preserved in this directory. 
```
data/
└── 40387701
    ├── 1.m4a
    ├── 2.m4a
    ├── 3.m4a
    └── tracks.txt
```
