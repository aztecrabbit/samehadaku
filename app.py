import src
import sys
import shutil


def main():
    del sys.argv[0]

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
        if sys.argv and sys.argv[0]:
            samehadaku.get_post(sys.argv[0])
        else:
            samehadaku.get_post_list()
        while True:
            data_input = str(input(':: '))
            if not data_input.startswith('p'):
                data_input = data_input.split(' ')
            else:
                data_input = [data_input]
            for data in data_input:
                if not data:
                    samehadaku.get_post_list()
                elif data.startswith('p'):
                    samehadaku.get_post(data.lstrip('p').strip())
                elif data.startswith('v'):
                    samehadaku.view_post(data.split('v')[1])
                elif data.startswith('o'):
                    samehadaku.open_download_link(data.split('o')[1])
    except KeyboardInterrupt:
        log.keyboard_interrupt()


if __name__ == '__main__':
    main()
