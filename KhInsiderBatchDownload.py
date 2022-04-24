#! Python
# KhInsiderBatchDownload.py - Small script to download every song from an album on KHInsider.com
# USAGE: Input a KHInsider album link with the format download.khinsider.com/*/album/* when asked.
import os, requests, bs4, sys, traceback
ALBUM_LINK = ''

# Raise an error if the website returns an error when calling requests.get()
def report_error(website):
    try:
        check_status = requests.get(website)
        check_status.raise_for_status()
    except:
        print('An error ocurred. Check the log file.')
        errorFile = open('KkInsiderBatchDownload log.txt', 'w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        return None
    return check_status

# Ask for the link to the album
while True:
    ALBUM_LINK = input('Enter the album link from downloads.khinsider.com:\n').lower()
    print()
    if not ALBUM_LINK.startswith('https://downloads'):
        print('The program only works on the download.khinsider.com/*/album/* webpage.\n')
        continue
    else:
        break
    
## START ##

# Download the main page.
main_page = report_error(ALBUM_LINK)
if main_page == None:
    sys.exit()

soup = bs4.BeautifulSoup(main_page.text, 'html.parser')

# Get the album name and create a root folder for the songs.
album_name = soup.select('#pageContent > h2')[0].getText()
os.makedirs(album_name, exist_ok=True)

# Download the disc art.
art_elements = soup.find_all('div', 'albumImage')

if art_elements != []:
    art_path = os.path.join(album_name, 'Disc Art')
    os.makedirs(art_path, exist_ok=True)
    
    art_name_count = 0
    for tag in art_elements:
        art_url = tag.find('a').get('href')
        art_name = 'Image%s.jpg' % str(art_name_count).zfill(3)
        art_name_count += 1

        # Save the album art
        print('Downloading disc art: %s' % art_name)
        res = report_error(art_url)
        if res == None:
            sys.exit()
        
        art_file = open(os.path.join(art_path, art_name), 'wb')
        for chunk in res.iter_content(100000):
            art_file.write(chunk)
        art_file.close()
        
    print('\n### Every image has been downloaded. ###\n')
else:
    print('### The album contains no images. ###\n')


# Scrape the header of the songlist (ID) table to check how many discs the album contains.
songlist_header = soup.select('#songlist > #songlist_header > th')
header_second_column = songlist_header[1].getText()

is_cd_organized = True

# If the "CD" text isn't found inside the second th tag in the table header, change disc_path so no extra folders are created.
if header_second_column != 'CD':
    print('### The Album contains a single disc. ###\n')
    song_path = os.path.join(album_name)
    is_cd_organized = False


# Scrape the songlist (ID) table for the CD number (if more than one disc) and redirection links to the songs.
songlist_table = soup.select('#songlist > tr')
for tag in songlist_table:
    # Skip the first tr tag (songlist_header), as it doesn't contain anything necessary.
    if tag.get('id') == 'songlist_header':
        continue
    # Break the look at the last tr tag (songlist_footer), as it's the end of the table.
    if tag.get('id') == 'songlist_footer':
        break
    # If the album has more than one disc, change the song_path variale to include the disc number for the songs.
    if is_cd_organized:
        cd_num_element = tag.find_all('td', attrs={'align':'center'})
        disc_num = 'Disc ' + cd_num_element[-1].getText()
        song_path = os.path.join(album_name, disc_num)
        
    os.makedirs(song_path, exist_ok=True)
    
    # Get the download link located in the table tag for the song.
    url_song = tag.find('td', attrs={'class':'playlistDownloadSong'})
    url_song = url_song.find('a').get('href')
    
    # Download the song.
    res = report_error('https://downloads.khinsider.com' + url_song)
    if res == None:
        sys.exit()
        
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    flac_or_mp3 = soup.select('#pageContent > p > a')
    if len(flac_or_mp3) == 28:
        song_format = '.mp3'
    else:
        song_format = '.flac'
    song_link = flac_or_mp3[-1].get('href')
    song_name = soup.select('#pageContent > p > b')[2].getText()

    # Save the song.
    print('Downloading %s into ./%s' % (song_name, song_path))
    res = report_error(song_link)
    if res == None:
        sys.exit()

    song_file = open(os.path.join(song_path, song_name + song_format), 'wb')
    for chunk in res.iter_content(100000):
        song_file.write(chunk)
    song_file.close()
    
print('\nDone.')
