import psutil
import os


def get_process_info(pid):
    p = psutil.Process(pid)
    print('name:', p.name())
    print('status:',p.status())
    print('create_time:',p.create_time())
    print('uids:',p.uids())
    print('gids:',p.gids())
    print('cpu_times:',p.cpu_times())
    print('memory_percent:',p.memory_percent())
    print('memory_info:',p.memory_info())
    # print('io_counters:',p.io_counters())
    print('num_threads:',p.num_threads())


if __name__ == '__main__':

    os.system("gnome-terminal -e 'ls'")
