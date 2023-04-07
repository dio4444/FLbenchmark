# -- coding: utf-8 --**
import json
from typing import List
import os, sys


# json.load()从json文件中读取数据
#
# json.loads()将str类型的数据转换为dict类型
#
# json.dumps()将dict类型的数据转成str
#
# json.dump()将数据以json的数据类型写入文件中


# class JsonPathFinder:
#     def __init__(self, json_str):
#         self.data = json.loads(json_str)
#
#     def iter_node(self, rows, road_step, target):
#         if isinstance(rows, dict):
#             key_value_iter = (x for x in rows.items())
#         elif isinstance(rows, list):
#             key_value_iter = (x for x in enumerate(rows))
#         else:
#             return
#         for key, value in key_value_iter:
#             current_path = road_step.copy()
#             current_path.append(key)
#             if key == target:
#                 yield current_path
#             if isinstance(value, (dict, list)):
#                 yield from self.iter_node(value, current_path, target)
#
#     def find_one(self, key: str) -> list:
#         path_iter = self.iter_node(self.data, [], key)
#         for path in path_iter:
#             return path
#         return []
#
#     def find_all(self, key) -> List[list]:
#         path_iter = self.iter_node(self.data, [], key)
#         return list(path_iter)
#
#
# if __name__ == '__main__':
#     with open('upload_data.json') as f:
#         json_data = f.read()
#         print(type(json.load(f)))
#     print(json.loads(json_data))
#     finder = JsonPathFinder(json_data)
#     path_list = finder.find_all('id')
#     data = finder.data
#     for path in path_list:
#         content = data.copy()
#         for step in path:
#             content = content[step]
#         print('>>>>', content)
#

class FateBench:
    def __init__(self, dsl, conf, mode, data):
        self.dsl = dsl
        self.conf = conf
        self.mode = mode
        self.data = data

    def exec(self):
        # 不进入容器，直接调用bash脚本运行后续操作，根据创建
        # os.system('CONTAINER_ID=`docker ps -aqf "name=fate_python"` && docker exec -t -i ${CONTAINER_ID} bash')
        # # 进入容器内部，如果不是容器部署跳过这个步骤
        match self.mode:
            case 'data_process':
                os.system(f'python /fate/python/fate_flow/fate_flow_client.py -f upload -c {self.conf}')
            # case 'model_train':
            #     os.system(f'python /fate/python/fate_flow/fate_flow_client.py -f submit_job -d {self.dsl} '
            #               f'-c {self.conf}')
            case 'model_eval':
                os.system(f'python /fate/python/fate_flow/fate_flow_client.py -f submit_job -d {self.dsl} '
                          f'-c {self.conf}')

    def upload_json(self, ):
        os.system(f'cp upload.yaml')


# def dsl_conf_(file_name, key, value):
#     key_list = key.split('.')
#     key_len = len(key_list)
#     with open(file_name, 'rb') as f:
#         json_content = json.load(f)
#         a = json_content
#         for i in range(key_len):
#             if i + 1 == key_len:
#                 a[key_list[i]] = value
#             else:
#                 a = a[key_list[i]]
#     f.close()
#     return json_content
#
#
# def json_write(file_name, json_content):
#     with open(file_name, 'w') as f:
#         json.dump(json_content, f)
#     f.close()
#
#
# if __name__ == '__main__':
#     content = dsl_conf_('upload_data.json', 'id', '?????****')
#     json_write('upload_data.json', content)
# # if __name__ == '__main__':
# #     key = sys.argv[1]
# #     value = sys.argv[2]
# #     file_name = sys.argv[3]
# #     content = dsl_conf_(file_name, key, value)
# #     json_write(file_name, content)
