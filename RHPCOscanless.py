import argparse
import sys
import queue
import threading
import lib.Scanless
import lib.WorkerCommand
import lib.Utils

CONST_SERVICE_PATH = "services/"



def worker(scanless):
    print(threading.current_thread())
    while True:
        item = q.get()
        if item is None:
            break
        # execute command
        scanless.execute_service(item)
        q.task_done()

q = queue.Queue()
threads = []

def main():
    try:
        parser = get_parser()
        args = vars(parser.parse_args())
        scanless = lib.Scanless.Scanless()
        scanless.load_services(CONST_SERVICE_PATH)
        route_command(parser, args, scanless)
    except Exception as detail:
      print("An error occurred, %s" % detail)




def route_command(parser, args, scanless):
    #################################
    if len(sys.argv) <= 1:
        parser.print_help()
        return
    #
    #
    if args['list']:
        scanless.get_helpers()
        return
    #
    print(args)
    serviceList = lib.Utils.Utils.createServiceList(args['scanner'])
    target = args['target']
    if target is None:
        raise Exception('No value for Target')

    for i in range(len(serviceList)):
        t = threading.Thread(target=worker, args=(scanless,))
        t.start()
        threads.append(t)
    #
    for service in lib.Utils.Utils.createServiceList(args['scanner']):
        workerCommand = lib.WorkerCommand.WorkerCommand(service,target,{})
        q.put(workerCommand)

    q.join()
    for i in range(len(serviceList)):
        q.put(None)
    for t in threads:
        t.join()




    #
    #if args['scanner'] and args['target']:
        #scanless.execute_service(args['scanner'],args['target'])

def banner():
    print("Welcome in RHPCOscanless")

def get_parser():
    banner()
    parser = argparse.ArgumentParser(description='RHPCOscanless, public port scan scrapper')
    parser.add_argument('-t', '--target', help='ip or domain to scan', type=str)
    parser.add_argument('-s', '--scanner', help='scanner to use', type=str, default='ipservice', nargs='*')
    parser.add_argument('-l', '--list', help='list scanners', action='store_true')

    return parser


if __name__ == "__main__":
    main()
else:
    print("Please, run as  a script")
