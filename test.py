import os
import re

# class FFF:
#     def __init__(self, name):
#         self.name = name
#
#     def dk(self):
#         os.system(f'mkdir -p {self.name} && cd {self.name} && touch {self.name}_submit_job.bash')
#         # 任务提交脚本
#         with open(f'{self.name}/{self.name}_submit_job.bash', 'w' )as f:
#             f.write('#!/bin/bash\n'
#                     "CONTAINER_ID=`docker ps -aqf 'name=fate_python'`\n"
#                     f"name={self.name}/{self.name}_submit_job\n"
#                     'sudo docker exec -it ${CONTAINER_ID} bash -c "python /fate/python/fate_flow/fate_flow_client.py '
#                     '-f submit_job -c ${name}_conf.json -d ${name}_dsl.json"')
#
#
# if __name__ == '__main__':
#     a = FFF('hello')
#     a.dk()
with open('upload.yaml')as f:
    for line in f:
        # print(line, end="")
        # # print(type(line))
        if re.findall('.*file: /fate/my_fate/.*', line):
            print(line,end="")
            print('\x20')
            print('\000')
            print('aaa')
# line = "Cats are smarter than dogs"
# matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
# if matchObj:
#     print("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(1) : ", matchObj.group(1))
#     print("matchObj.group(2) : ", matchObj.group(2))
# else:
#     print("No match!!")
