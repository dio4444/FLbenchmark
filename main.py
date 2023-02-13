import os
import json


def fate_data_format(fate_dir: str, file: str, table_name: str, namespace: str, head=1, partition=16, work_mode=0):
    """
    :param fate_dir: fate安装目录
    :param file: 指定数据文件
    :param head:
    :param partition:
    :param work_mode:
    :param table_name: 指定DTable表名
    :param namespace: 指定DTable表名的命名空间
    :return: 日志信息

    该函数用于将本地数据转换成FATE中使用的数据格式
    """
    # 数据输入，将本地数据上传到 'fate_dir/examples/data' 目录
    os.system('fate_dir="{fate_dir}" && cd $fate_dir/examples/data/ && rz -be '.format(fate_dir=fate_dir))
    # 修改配置文件
    with open("{fate_dir}/examples/data/upload_data.json".format(fate_dir=fate_dir), 'w') as f:
        cong_dict = {'file': file, 'head': head, 'partition': partition, 'work_name': work_mode,
                     'table_name': table_name, 'namespace': namespace}
        json.dump(cong_dict, f, indent=4, ensure_ascii=False)
    # 使用配置文件将数据规范化，返回日志信息
    return os.popen('python $fata_dir/fate_flow/fate_flow_client.py -f upload -c upload_data.json')


def fate_model_train(dsl: str, conf: str):
    """
    :param dsl:
    :param conf:
    :return:

    上传配置文件，将算法配置文件替换
    """
    os.system(f'python $fata_dir/fate_flow/fate_flow_client.py -f submit_job -d {dsl} -c {conf}')
    # 需要思考更新DSL和conf文件//或者修改DSL和conf文件中的name，之后每次训练只需修改上传数据文件名


def fate_model_evaluate(dsl: str, conf: str):
    """
    返回任务执行结果URL

    :param dsl:
    :param conf:
    :return:
    """
    log = os.popen(f'python $fata_dir/fate_flow/fate_flow_client.py -f submit_job -d {dsl} -c {conf}')
    return json.load(log)['data']['board_url']


