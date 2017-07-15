import argparse
import sys
import lib.Scanless
import queue
import threading
import time

CONST_SERVICE_PATH = "services/"



def worker():
    print(threading.current_thread())
    while True:
        item = q.get()
        if item is None:
            break
        print(item)
        q.task_done()

q = queue.Queue()
threads = []

def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    scanless = lib.Scanless.Scanless()
    scanless.load_services(CONST_SERVICE_PATH)
    route_command(parser, args, scanless)



def route_command(parser, args, scanless):
    print(args)
    for i in range(3):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for s in args['scanner']:
        q.put(s)

    q.join()
    for i in range(3):
        q.put(None)
    for t in threads:
        t.join()
    return

    #
    if len(sys.argv) <= 1:
        parser.print_help()
        return
    #
    if args['list']:
        scanless.get_helpers()
    #
    if args['scanner'] and args['target']:
        scanless.execute_service(args['scanner'],args['target'])
def banner():
    print("Welcome in RHPCOscanless")

def get_parser():
    banner()
    parser = argparse.ArgumentParser(description='RHPCOscanless, public port scan scrapper')
    parser.add_argument('-t', '--target', help='ip or domain to scan', type=str)
    parser.add_argument('-s', '--scanner', help='scanner to use', type=str, default='ipservice', nargs='*')
    parser.add_argument('-l', '--list', help='list scanners', action='store_true')
    #parser.add_argument('-a', '--all', help='use all the scanners', action='store_true')
    return parser


if __name__ == "__main__":
    main()
else:
    print("Please, run as  a script")
