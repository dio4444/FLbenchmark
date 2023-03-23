import os


class FateBench:
    def __init__(self, mode, data, name):
        self.mode = mode
        self.data = data
        self.name = name

    def bash_cre(self):
        """
        创建bash脚本
        :return:
        """
        os.system(f'mkdir -p {self.name} && cd {self.name} && touch {self.name}.bash')
        # 将conf和dsl传进容器内的相应位置   /fate/my_fate/
        with open(f'{self.name}/{self.name}_upload.bash', 'w') as f:
            f.write('#!/bin/bash\n'
                    "CONTAINER_ID=`docker ps -aqf 'name=fate_python'`\n"
                    f'docker cp {self.name}/{self.name}_dsl.json '
                    '${CONTAINER_ID}:/fate/'
                    f'{self.name}\n'
                    f'docker cp {self.name}/{self.name}_conf.json '
                    '${CONTAINER_ID}:/fate/'
                    f'{self.name}\n'
                    )
        os.system(f'mkdir -p {self.name} && cd {self.name} && touch {self.name}_upload.bash')
        # 数据上传脚本
        with open(f'{self.name}/{self.name}_upload.bash', 'w') as f:
            f.write('#!/bin/bash\n'
                    "CONTAINER_ID=`docker ps -aqf 'name=fate_python'`\n"
                    f"name={self.name}/{self.name}_upload.json\n"
                    'sudo docker exec -it ${CONTAINER_ID} bash -c "python /fate/python/fate_flow/fate_flow_client.py '
                    '-f upload -c ${name}"')
        os.system(f'mkdir -p {self.name} && cd {self.name} && touch {self.name}_submit_job.bash')
        # 任务提交脚本
        with open(f'{self.name}/{self.name}_submit_job.bash', 'w')as f:
            f.write('#!/bin/bash\n'
                    "CONTAINER_ID=`docker ps -aqf 'name=fate_python'`\n"
                    f"name={self.name}/{self.name}_submit_job\n"
                    'sudo docker exec -it ${CONTAINER_ID} bash -c "python /fate/python/fate_flow/fate_flow_client.py '
                    '-f submit_job -c ${name}_conf.json -d ${name}_dsl.json"')

    def exec(self):
        # 不进入容器，直接调用bash脚本运行后续操作
        os.system(f'bash {self.name}/{self.name}.bash && bash {self.name}/{self.name}_upload.bash '
                  f'&& {self.name}/{self.name}_submit_job.bash')

    def conf_dsl_(self):

        os.system(f'mkdir -p {self.name}')
        os.system(f'cp -i upload.json {self.name}/{self.name}_upload.json')

        os.system(f'cp -i train_dsl.json {self.name}/{self.name}_train_dsl.json')
        os.system(f'cp -i train_conf.json {self.name}/{self.name}_train_conf.json')



