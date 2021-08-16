import configparser
import os

# 创建实例
# 加载配置文件
# 根据section option获取值
base_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.join(base_dir, 'config.ini')


class Readconfig:
    # 初始化函数：实例化conf对象，读取传入的配置文件
    def __init__(self):
        self.conf = configparser.RawConfigParser()
        file = os.path.join(conf_dir)
        self.conf.read(file)

    def get_config_str(self, section, option):
        return self.conf.get(section, option)


if __name__ == '__main__':
    Readconfig().get_config_str('data', 'HOST')
    Readconfig().get_config_str('data', 'Cookie')
    Readconfig().get_config_str('data', 'X-token')
