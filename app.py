import src
import shutil
import threading
import subprocess

def main():
    ''' log '''
    log = src.log()
    log.type = 1
    log.value_prefix = "datetime.datetime.now().strftime('[%H:%M:%S]{clear}')"

    browser = 'chromium-browser'
    for x in ['chromium-browser','firefox','termux-open-url']:
        if shutil.which(x):
            browser = x
            break

    ''' samehadaku '''
    samehadaku = src.samehadaku()
    samehadaku.liblog = log
    samehadaku.post_list()

    try:
        while True:
            ''' command '''
            result = str(input(':: '))
            if not result:
                samehadaku.post_list()
            elif result.startswith('v'):
                samehadaku.post_view(result.split('v')[1])
            elif result.startswith('o'):
                process = subprocess.Popen(f"{browser} {samehadaku.download_link.get(result.split('o')[1])}".split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                threading.Thread(target=process.communicate).start()
    except KeyboardInterrupt:
        log.keyboard_interrupt()
    finally:
        pass

if __name__ == '__main__':
    main()
