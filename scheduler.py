from playwright.sync_api import sync_playwright

import query
import spider
import utils


def main():
    with sync_playwright() as Spider:
        browser = Spider.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        spider.login(page)
        # spider.get_home_video(page)
        argv_str = input(str())
        argv = argv_str.split(' ')
        if argv[0] == '-h':
            utils.show_help_info()
        if utils.check_argv(argv):
            query.handle_query(page, argv)


if __name__ == '__main__':
    try:
        main()
    except AttributeError:
        main()
