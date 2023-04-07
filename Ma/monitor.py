import psutil
import time
from datetime import datetime
import curses
import argparse


def get_ecs_cpu_and_memory():
    data = psutil.virtual_memory()
    total = data.total  # 总内存,单位为byte
    total = round(total / 1024 / 1024 / 1024, 2)  # 转换成GB
    free = data.available  # 可用内存
    free = round(free / 1024 / 1024 / 1024, 2)  # 转换成GB
    memory = "Memory usage:%0.2f" % (int(round(data.percent))) + "%"  # 内存使用情况
    cpu = "CPU:%0.2f" % psutil.cpu_percent(interval=1) + "%"  # CPU占用情况
    return cpu, memory, total, free


def get_network_data():
    # 获取网卡流量信息
    recv = {}
    sent = {}
    data = psutil.net_io_counters(pernic=True)  # 获取网络读写字节／包的个数
    # interfaces = data.keys()
    # for interface in interfaces:
    #     recv.setdefault(interface, data.get(interface).bytes_recv)
    #     sent.setdefault(interface, data.get(interface).bytes_sent)
    # return interfaces, recv, sent
    interface = 'eth0'
    recv.setdefault(interface, data.get(interface).bytes_recv)
    sent.setdefault(interface, data.get(interface).bytes_sent)
    return interface, recv, sent


def get_network_rate(num):
    # # 计算网卡流量速率
    # interfaces, oldRecv, oldSent = get_network_data()
    # time.sleep(num)  # 推迟执行的秒数
    # interfaces, newRecv, newSent = get_network_data()
    # networkIn = {}
    # networkOut = {}
    # for interface in interfaces:
    #     networkIn.setdefault(interface, float("%.3f" % ((newRecv.get(interface) - oldRecv.get(interface)) / num)))
    #     networkOut.setdefault(interface, float("%.3f" % ((newSent.get(interface) - oldSent.get(interface)) / num)))
    # return interfaces, networkIn, networkOut
    interface, oldRecv, oldSent = get_network_data()
    time.sleep(num)
    interface, newRecv, newSent = get_network_data()
    networkIn = {}
    networkOut = {}
    networkIn.setdefault(interface, float("%.3f" % ((newRecv.get(interface) - oldRecv.get(interface)) / (num + 1))))
    networkOut.setdefault(interface, float("%.3f" % ((newSent.get(interface) - oldSent.get(interface)) / (num + 1))))
    return interface, networkIn, networkOut


def output(num, unit):
    data_file = open('output.txt', 'w')
    header = ['time', 'netIn', 'netOut', 'cpu', 'memory']
    data_file.write('{:<30}{:<15}{:<15}{:<15}{}\n'.format(*header))
    # 将监控输出到终端
    stdscr = curses.initscr()
    curses.start_color()
    # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.noecho()
    curses.cbreak()
    stdscr.clear()
    try:
        # 第一次初始化
        # interfaces, _, _ = get_network_data()
        interface, _, _ = get_network_data()
        currTime = datetime.now()
        timeStr = datetime.strftime(currTime, "%Y-%m-%d %H:%M:%S")  # 格式化时间，返回以可读字符串表示的当地时间
        stdscr.addstr(0, 0, timeStr)  # addstr(y,x,str)移动到窗口内的 y,x 位置，并显示 str
        i = 1
        # for interface in interfaces:
        #
        # if interface != "lo" and bool(1 - interface.startswith("veth")) and bool(
        #         1 - interface.startswith("蓝牙")) and bool(1 - interface.startswith("VMware")):
        # 筛选掉'lo'、'veth'、'蓝牙'、'VMware'开头的接口
        # 根据命令行参数，更改单位，默认B/s
        if interface == "eth0":
            if unit == "K" or unit == "k":
                netIn = "%12.2fKB/s" % 0
                netOut = "%11.2fKB/s" % 0
            elif unit == "M" or unit == "m":
                netIn = "%12.2fMB/s" % 0
                netOut = "%11.2fMB/s" % 0
            elif unit == "G" or unit == "g":
                netIn = "%12.3fGB/s" % 0
                netOut = "%11.3fGB/s" % 0
            else:
                netIn = "%12.1fB/s" % 0
                netOut = "%11.1fB/s" % 0
            stdscr.addstr(i, 0, interface)
            stdscr.addstr(i + 1, 0, "Input:%s" % netIn)
            stdscr.addstr(i + 2, 0, "Output:%s" % netOut)
            stdscr.move(i + 3, 0)
            i += 4
            # stdscr.refresh()  # 更新屏幕显示结果
        cpu, memory, total, free = get_ecs_cpu_and_memory()
        stdscr.addstr(i, 0, '%s' % cpu)
        stdscr.addstr(i + 1, 0, '%s' % memory)
        stdscr.addstr(i + 2, 0, 'total:%s GB' % total)
        stdscr.addstr(i + 3, 0, 'free:%s GB' % free)
        stdscr.move(i + 4, 0)
        i += 5
        stdscr.refresh()
        # 第二次开始循环监控网卡流量,如果用户按下q键结束
        while True:
            _, networkIn, networkOut = get_network_rate(num)
            currTime = datetime.now()
            timeStr = datetime.strftime(currTime, "%Y-%m-%d %H:%M:%S")
            stdscr.erase()
            stdscr.addstr(0, 0, timeStr)
            i = 1
            # for interface in interfaces:
            # if interface != "lo" and bool(1 - interface.startswith("veth")) and bool(
            #         1 - interface.startswith("蓝牙")) and bool(1 - interface.startswith("VMware")):
            if interface == "eth0":
                if unit == "K" or unit == "k":
                    netIn = "%12.2fKB/s" % (networkIn.get(interface) / 1024)
                    netOut = "%11.2fKB/s" % (networkOut.get(interface) / 1024)
                elif unit == "M" or unit == "m":
                    netIn = "%12.2fMB/s" % (networkIn.get(interface) / 1024 / 1024)
                    netOut = "%11.2fMB/s" % (networkOut.get(interface) / 1024 / 1024)
                elif unit == "G" or unit == "g":
                    netIn = "%12.3fGB/s" % (networkIn.get(interface) / 1024 / 1024 / 1024)
                    netOut = "%11.3fGB/s" % (networkOut.get(interface) / 1024 / 1024 / 1024)
                else:
                    netIn = "%12.1fB/s" % networkIn.get(interface)
                    netOut = "%11.1fB/s" % networkOut.get(interface)
                stdscr.addstr(i, 0, interface)
                stdscr.addstr(i + 1, 0, "Input:%s" % netIn)
                stdscr.addstr(i + 2, 0, "Output:%s" % netOut)
                stdscr.move(i + 3, 0)
                i += 4
                # stdscr.refresh()
            cpu, memory, total, free = get_ecs_cpu_and_memory()
            stdscr.addstr(i, 0, '%s' % cpu)
            stdscr.addstr(i + 1, 0, '%s' % memory)
            stdscr.addstr(i + 2, 0, 'total:%s GB' % total)
            stdscr.addstr(i + 3, 0, 'free:%s GB' % free)
            stdscr.move(i + 4, 0)
            i += 5
            stdscr.refresh()
            data_file.write(f"{timeStr}\t{netIn}\t{netOut}\t{cpu}\t{memory}\n")
            data_file.flush()
    except KeyboardInterrupt:
        data_file.close()
        # 还原终端
        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except Exception as e:
        data_file.close()
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        print("ERROR: %s!" % e)
        print("Please increase the terminal size!")
    finally:
        data_file.close()
        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":
    # os.system("gnome-terminal -e 'bash -c \"ls; exec bash\"'")
    parser = argparse.ArgumentParser(
        description="A command for monitoring the traffic of network interface! Ctrl + C: exit")
    parser.add_argument("-t", "--time", type=int, help="the interval time for ouput", default=1)
    parser.add_argument("-u", "--unit", type=str, choices=["b", "B", "k", "K", "m", "M", "g", "G"],
                        help="the unit for ouput", default="B")
    parser.add_argument("-v", "--version", help="output version information and exit", action="store_true")
    args = parser.parse_args()
    if args.version:
        print("v1.0")
        exit(0)
    num = args.time
    unit = args.unit
    output(num, unit)
