import src
import shutil


def main():
    log = src.log()
    log.type = 1

    browser = ''
    for x in ['chromium-browser', 'firefox', 'termux-open-url']:
        if shutil.which(x):
            browser = x
            break

    try:
        samehadaku = src.samehadaku()
        samehadaku.liblog = log
        samehadaku.browser = browser
        samehadaku.get_post_list()
        while True:
            for data in str(input(':: ')).split(' '):
                if not data:
                    samehadaku.get_post_list()
                elif data.startswith('v'):
                    samehadaku.view_post(data.split('v')[1])
                elif data.startswith('o'):
                    samehadaku.open_download_link(data.split('o')[1])
    except KeyboardInterrupt:
        log.keyboard_interrupt()


if __name__ == '__main__':
    main()
