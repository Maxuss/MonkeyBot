# DOWNLOADS WHOLE AH API
# THX FOR RANDOM USER ON HYPIXEL FORUMS FOR THIS
# <3
import requests, json, pretty_errors, discord, asyncio, aiohttp, os, time
import data


async def fetch_one_url(session, url, save_path=None):
    # print_timestamp()
    async with session.get(url) as response:
        time.sleep(0.1)
        response_text = await response.text()
        if save_path is not None:
            with open(save_path, "wb") as text_file:
                text_file.write(response_text.encode("UTF-8"))
        return url, response_text

# dowloads everything from urls, then returns with response
def download_urls(urls: list, save_as={}):
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(download_urls_helper(urls, save_as))
    return htmls


async def download_urls_helper(urls: list, save_as: dict):

    # print("Downloading:")
    # print(urls)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if url in save_as:
                save_path = save_as[url]
            else:
                save_path = None
            tasks.append(fetch_one_url(session, url, save_path))
        htmls = await asyncio.gather(*tasks)

        # print("Finished downloading")
        # print_timestamp()
        return htmls

# end DOWNLOAD URLS

def get_number_of_pages():
    with open('auction/0.json', 'rb') as f:
        ah_dict = json.load(f)
        if ah_dict['success']:
            number_of_pages = ah_dict['totalPages']
            return number_of_pages
        else:
            print("number_of_pages error")



def download_auctions():
    global auctions_json_list
    global auction_list
    print("Updating all auctions")
    # print("Deleting old auction files")
    for filename in os.listdir('auction'):
        os.remove('auction/' + filename)

    # print("Downloading page 0")
    r = requests.get('https://api.hypixel.net/skyblock/auctions?key=' + DATACENTRE.API_KEY + '&page=0')
    with open(r'auction/0.json', 'wb') as f:
        f.write(r.content)
    number_of_pages = get_number_of_pages()
    print("Downloading", number_of_pages, "pages")

    if number_of_pages is None:
        print('number_of_pages doesnt exist for some reason, downloading 2 pages, so the script does not crash')
        number_of_pages = 2

    urls = []
    save_as = {}
    for page_number in range(1, number_of_pages):
        url = 'https://api.hypixel.net/skyblock/auctions?key=' + DATACENTRE.API_KEY + '&page=' + str(page_number)
        urls.append(url)
        save_as[url] = r'auction/' + str(page_number) + '.json'

    download_urls(urls, save_as)
    print("auctions updated")


download_auctions()
