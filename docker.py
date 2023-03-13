import os


class FateBench:
    def __init__(self, mode, data, name):
        self.mode = mode
        self.data = data
        self.name = name

    def bash_cre(self):

        os.system('rz -y')

    def exec(self):
        # 不进入容器，直接调用bash脚本运行后续操作
        match self.mode:
            case 'data_process':
                os.system()
            case 'model_eval':
                os.system()
