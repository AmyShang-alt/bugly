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

MIN_USER = 150


def save_trend_data(platform_id: int, type_name: str):
    print(platform_id, type_name)
    http_call = HttpCall({
        'Cookie': 'pgv_pvi=5227054080; ptui_loginuin=3218702409; RK=uSTZc9Z2yy; ptcz=307a2aaec06b073405bef7929ff9e6a6047806cefe6a1c9d153936f89e31b45e; _ga=GA1.2.1939390862.1597295914; btcu_id=876711e194caa4a523f06ffe6df4c1235f34cd2a72929; vc=vc-4557b7fc-b0ae-403a-a44d-938d1f46e7f7; vc.sig=TcUf5la9TieBJoB23OijMd-YL_KHFGxMh1TKj0waroI; pgv_pvid=6497091362; tvfe_boss_uuid=d30b863ad45c1926; o_cookie=1184569493; pac_uid=1_1184569493; uin=o1184569493; skey=@67wuiFxsZ; token-skey=205838f3-7d9d-df85-a4b6-93a9c63a865a; token-lifeTime=1628494414; bugly-session=s%3AsVZC5F-CRx4-17a3JPxVawnj833F6VeS.0YKXjb%2FqdcBcUYyJljNE9I74nqE2YDOmGTjWN9WOx%2Bo; before_login_referer=https%3A%2F%2Fbugly.qq.com%2Fv2%2Fcrash-reporting%2Fcrashes%2Fec7be8aa7a%3Fpid%3D2; bugly_session=eyJpdiI6IkVOdDVvcTJROU9BK0xWWFJod3J5SlE9PSIsInZhbHVlIjoieVlxRmpBZUI5T3BCXC9NSkFzS3VBeTVyQVpJUFA1Q2xzc0lGVE4rMUgzQURJUk1qa1wvVWJKeE13R2ZPT1U2K29MbWpnRmk1M2ZiOWJyR0dEb3gzcjdzdz09IiwibWFjIjoiNzc4ZGUxNTJhMzYzODU1NDhhYjhmODhmZGMxMTQ5NWI3OGNkNmUyZGNiN2FjMDQyZDMyNDc3MTBkMjg2MDY3MyJ9; referrer=eyJpdiI6IjRZZENQQUpzdStaYUIrc0hlSmNsd2c9PSIsInZhbHVlIjoiUFNHMjFvTWphdnd1VXV4czVlSGg2c3hrenBUTkx2K3NsdVFwR0FEUmJzQkt4UXVyc3dQUmtsaU41VUlwR2h4eFwveVpzTnlUSzM3bmZRenpOTkVVSUdDSnFkeW43eUQ0Q2tqRnVtbXVYS0wyKzJ2Sk9hR0Z3NHdaTHU0dkVaUnlnVnpRbk4wbllSZ0ZGOUMydFB0a2xRemExeWJoSCthRSt3TW45OU1QQU9MdUdGYVwvSFNWd04yXC80WEp1N3I4dTk5IiwibWFjIjoiNDNlMTUwZGMwM2ZkZWNkNThmNzM2OWNiMDQ3NDJhZjE1ZjM3OTliYjViM2ZiM2I4NDkxM2UxNzM0NjA0MmQ2ZiJ9',
        'x-csrf-token': 'ZY2nGywbB4E_EuiCLRTkvUGP', 'X-token': '250356735'})

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
