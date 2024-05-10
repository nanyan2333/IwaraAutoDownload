import os
import time

import requests as axios
from tqdm import tqdm

import spider


class ProgressBar:
    def __init__(self, total_size, title):
        self.progress_bar = tqdm(initial=0, total=total_size, unit='B', unit_scale=True, desc=title)

    def update(self, size):
        self.progress_bar.update(size)

    def close(self):
        self.progress_bar.close()


def output_err(string):
    print(f'\033[1;31m{string}\033[0m')


def check_argv(argv: list[str]) -> bool:
    """
    Checks if the command-line arguments are valid.

    Parameters:
    argv (list[str]): A list of command-line arguments. The expected format is ['-q', 'type', 'page','query'].

    Returns:
    bool: True if the arguments are valid, False otherwise.

    The function checks if the first argument is '-q', the second argument is either 'type1' or 'type2'
    (defined in the 'spider' module), and the third argument is a non-negative integer.
    If the length of argv is less than 4, it returns False.
    If the third argument cannot be converted to an integer, it returns False.
    """
    try:
        page = int(argv[2])
        res = argv[0] == '-q' and (
                spider.query_type[0] == argv[1] or spider.query_type[1] == argv[1]) and page >= 0 and len(argv) >= 4
    except ValueError:
        return False
    else:
        return res


def go_home(page):
    page.goto(spider.setting['url'])
    time.sleep(spider.setting['interval_time'] * 2)


def handle_query_url(query_type: str, page: str, query: str) -> str:
    argv = [f'type={query_type}', f'page={page}', f'query={query}']
    return spider.setting['url'] + '/search?' + '&'.join(argv)


def download(url: str, title: str) -> None:
    """
    Downloads a video from the given URL and saves it with the specified title.

    Parameters:
    url (str): The URL of the video to download.
    title (str): The title of the video to be used as the file name.

    Returns:
    None

    Raises:
    None

    Note:
    This function uses the requests library to download the video in chunks.
    It also creates a progress bar using the tqdm library to display the download progress.
    """
    res = axios.get(url, proxies=spider.proxies, stream=True)
    if res.status_code == 200:
        print('Downloading video......')
        if not os.path.exists(spider.setting['target_dir']):
            os.mkdir(spider.setting['target_dir'])
        progress_bar = ProgressBar(int(res.headers.get('Content-Length', 0)), title)
        with open(spider.setting['target_dir'] + title + '.mp4', 'ab') as file:
            for chunk in res.iter_content(chunk_size=spider.chunkSize):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        print('finished downloading video')
    else:
        output_err(f'Error downloading video code {res.status_code}')


def show_help_info():
    help_info = f"""
-q [query_type(video/user)] [query_page] [query_value]\tsearch function
-h \t\t\t\t\t\t\thelp info
    """
    print('----------------------------------------------------------------------')
    print(help_info)
    print('----------------------------------------------------------------------')
