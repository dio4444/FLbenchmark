# import json
#
#
# with open("upload_data.json", 'w') as f:
#     cong_dict = {'file': 1, 'head': 1, 'partition': 1, 'work_name': 1,
#                  'table_name': 1, 'namespace': 1}
#     json.dump(cong_dict, f, indent=4, ensure_ascii=False)
import json
import os

# fate_dir = "/Users/ma"
# os.system('fate_dir="{fate_dir}" && cd $fate_dir/Desktop/云大所/沙龙照片 && ls'.format(fate_dir=fate_dir))
# p = os.popen('mkdir ./tt')
# print(p)
# log = {
#     "data": {
#         "url": "http://www.123.com",
#         "id": "234",
#     },
#     "jobid": "2023",
#     "metas": "success"
# }
# with open('upload_data.json')as f:
#     data=json.load(f)
#     print(data)
#     print(data['data']['url'])
# import psutil
# import argparse
#
#
# def get_process_info(pid):
#     print(pid)
#
#
# parser = argparse.ArgumentParser(description='Show process information')
# parser.add_argument('--pid', '-p', help='pid', required=True)
# args = parser.parse_args()
#
# if __name__ == '__main__':
#     try:
#         get_process_info(args.pid)
#     except Exception as e:
#         print(e)

import psutil

recv = {}
sent = {}
data = psutil.net_io_counters(pernic=True)  # 获取网络读写字节／包的个数
interfaces = data.keys()
for interface in interfaces:
    recv.setdefault(interface, data.get(interface).bytes_recv)
    sent.setdefault(interface, data.get(interface).bytes_sent)

print(recv, sent)
