import time

import yaml

import utils

with open('setting.yml', 'r') as setting:
    setting = yaml.load(setting, Loader=yaml.FullLoader)
    proxies = {
        'http': setting['ip'] + ':' + str(setting['port']),
        'https': setting['ip'] + ':' + str(setting['port'])
    }
    chunkSize = setting['chunk_size']
    query_type = setting['query_type']


def login(page) -> None:
    """
    This function is responsible for logging into the website.

    Parameters:
    page (Page): The page object from the playwright library, representing the current page in the browser.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exceptions.

    Note:
    This function assumes that the 'setting' dictionary is already defined and contains the necessary login
    credentials and URL.
    """

    page.goto(setting['url'] + '/login')
    user_input = page.query_selector('//input[@name="email"]')
    password_input = page.query_selector('//input[@name="password"]')

    user_input.fill(setting['email'])
    password_input.fill(setting['password'])
    button = page.query_selector(
        "//button[contains(@class, 'button--primary') and contains(@class, 'button--solid') and @type='submit']")
    button.click(button='left')
    time.sleep(setting['interval_time'] * 2)


def get_home_video(page) -> None:
    utils.go_home(page)
    get_now_page_video(page)


def get_now_page_video(page) -> None:
    urls, titles, authors = get_featured_video(page)
    for url, title, author in zip(urls, titles, authors):
        print('title:' + title + '\n' + 'author:' + author)
        is_download = input(str())
        if is_download == 'y':
            download_video(page, url, title)


def get_featured_video(page) -> tuple[list[str], list[str], list[str]]:
    video_list = page.query_selector_all('//a[@class="videoTeaser__title"]')
    video_url_list = [element.get_attribute('href') for element in video_list]
    video_title_list = [element.get_attribute('title') for element in video_list]
    author_element = page.query_selector_all('//div[@class="videoTeaser__bottom"]//a[contains(@class, "username")]')
    author_list = [element.get_attribute('title') for element in author_element]
    return video_url_list, video_title_list, author_list


def download_video(page, url, title) -> None:
    page.goto(setting['url'] + url)
    time.sleep(setting['interval_time'])
    adult_button = page.query_selector("(//div[@class='adultWarning__actions']/button)[last()-1]")
    if adult_button:
        adult_button.click(button='left')
        time.sleep(setting['interval_time'] / 5)
    download_button = page.query_selector("//button[contains(@class, 'download')]")
    download_button.click(button='left')
    download_a = page.query_selector('(//div[@class="dropdown__content"])[last()]//li[1]/a')
    download_url = download_a.get_attribute('href')
    utils.download(download_url, title)


def get_featured_user(page):
    pagination = page.query_selector_all('//li[@class="pagination__item"]')
    print(len(pagination))
    user_url_list = []
    user_title_list = []
    user_list = page.query_selector_all("//a[@class='userTeaser']")
    user_url_list = user_url_list + [element.get_attribute('href') for element in user_list]
    user_title_divs = page.query_selector_all("//div[@class='username']")
    user_title_list = user_title_list + [element.get_attribute('title') for element in user_title_divs]
    for pagination_item in pagination:
        pagination_item.click(button='left')
        time.sleep(setting['interval_time'] / 2)
        user_list = page.query_selector_all("//a[@class='userTeaser']")
        user_url_list = user_url_list + [element.get_attribute('href') for element in user_list]
        user_title_divs = page.query_selector_all("//div[@class='username']")
        user_title_list = user_title_list + [element.get_attribute('title') for element in user_title_divs]
    return user_url_list, user_title_list
