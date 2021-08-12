# Author 尚欣雨
# coding=utf-8
# @Time    : 2020-07-16 15:05
# @Site    : 
# @File    : log.py
# @Software: PyCharm
# @contact: xinyu.shang@zozo.cn

import logging
import time


class LogUtil(object):
    def get_log(self):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关

        # 第二步，创建一个handler，用于写入日志文件
        logfile = './log_txt/%s-log.txt' % time.time()
        fh = logging.FileHandler(logfile, mode='a')
        fh.setLevel(logging.DEBUG)  # 用于写到file的等级开关

        # 第三步，再创建一个handler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

        # 第四步，定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger


if __name__ == '__main__':
    logger = LogUtil().get_log()
    print('\n')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
