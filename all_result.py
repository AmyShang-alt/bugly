# Author 尚欣雨
# coding=utf-8
# @Time    : 2020-07-16 11:11
# @Site    : 
# @File    : all_result.py
# @Software: PyCharm
# @contact: xinyu.shang@zozo.cn
import datetime
from typing import List, Tuple
from const import HttpConst
from http_call import HttpCall
from util.file_util import save_excel
from ReadConfig import Readconfig

MIN_USER = 150


def save_trend_data(platform_id: int, type_name: str):
    print(platform_id, type_name)
    http_call = HttpCall({
        'Cookie': Readconfig().get_config_str('data', 'Cookie'),
        'x-csrf-token': 'ZY2nGywbB4E_EuiCLRTkvUGP', 'X-token': Readconfig().get_config_str('data', 'X-token')})

    version_list = list(set(http_call.get_version_list(platform_id)))
    version_list = list(reversed(sorted(version_list)))

    version_list.insert(0, '-1')

    sheet_data: List[Tuple[str, List[str], List[Tuple]]] = []
    for version in version_list:
        print(version)
        anr_result = http_call.get_trend_result(platform_id, version,
                                                datetime.datetime.now() + datetime.timedelta(days=-7),
                                                datetime.datetime.now() + datetime.timedelta(days=-1), type_name)
        data_list: List[Tuple[str, str, int, str, int, int]] = []
        total_access_user = 0
        for i in anr_result:
            date_str: str = i['date']
            crash_num: int = i['crashNum']
            crash_user: int = i['crashUser']
            access_user: int = max(i['accessUser'], 0)

            if crash_num <= 0 or crash_user < 0:
                rate: str = '0.00%'
                crash_num = 0
                crash_user = 0
            elif access_user == 0:
                rate: str = '0.00%'
            else:
                rate_num = crash_user / access_user
                rate: str = '{:.02%}'.format(rate_num)
            data_list.append(('', date_str, access_user, rate, crash_num, crash_user))

            total_access_user += access_user

        if total_access_user <= MIN_USER:
            print(f'7天日活总和小于{MIN_USER}不统计')
            continue

        headers = ['崩溃率统计数据', 'android', f'{version}版本联网用户数', f'{version}版本用户崩溃率', f'{version}版本崩溃次数',
                   f'{version}版本影响用户数']
        sheet_data.append((version, headers, data_list))
    save_excel(f'{datetime.datetime.now().strftime("%Y%m%d")}_{type_name}_{platform_id}', sheet_data)


if __name__ == '__main__':
    save_trend_data(HttpConst.ANDROID_PLATFORM_ID, 'anr')
    save_trend_data(HttpConst.ANDROID_PLATFORM_ID, 'crash')
    save_trend_data(HttpConst.IOS_PLATFORM_ID, 'crash')
