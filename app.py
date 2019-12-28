import src
import shutil
import threading
import subprocess


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
        samehadaku.get_post_list()
        while True:
            for data in str(input(':: ')).split(' '):
                if not data:
                    samehadaku.get_post_list()
                elif data.startswith('v'):
                    samehadaku.view_post(data.split('v')[1])
                elif data.startswith('o'):
                    download_link = samehadaku.download_link.get(data.split('o')[1])
                    if browser:
                        process = subprocess.Popen(
                            f"{browser} {download_link}".split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                        )
                        threading.Thread(target=process.communicate).start()
                    else:
                        log.log(download_link)
                elif data == 'exit':
                    break
    except KeyboardInterrupt:
        log.keyboard_interrupt()


if __name__ == '__main__':
    main()
