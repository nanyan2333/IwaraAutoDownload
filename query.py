import time

import spider
import utils


def handle_query(page, argv: list[str]) -> None:
    page.goto(utils.handle_query_url(argv[1], argv[2], argv[3]))
    time.sleep(spider.setting['interval_time'])
    if argv[1] == 'video':
        spider.get_featured_video(page)
        spider.get_now_page_video(page)
    else:
        urls, users = spider.get_featured_user(page)
        for url, user in zip(urls, users):
            print('user:' + user)
            is_goto = input(str())
            if is_goto == 'y':
                page.goto(spider.setting['url'] + url)
                time.sleep(spider.setting['interval_time'])
                spider.get_now_page_video(page)
