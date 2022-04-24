# KHInsiderScraper
Small script made in Python to scrape KHInsider links to download game soundtracks.
___
## Dependencies
Python3
```
$ sudo pip install bs4
$ sudo pip install requests
```
___
## Usage
After requirements have been fulfilled, simply input an album link (when asked) with the following format: https://downloads.khinsider.com/*/album/*.

Every song from the KHInsider link will be downloaded, including the disc art (if there's any) and organized in the following structure.
- Album name
  - Disc Art
  - Disc # (if the album has more than one disc)
    - Songs
