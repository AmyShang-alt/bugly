# Author 尚欣雨
# coding=utf-8
# @Time    : 2020-07-18 17:28
# @Site    : 
# @File    : http_call.py
# @Software: PyCharm
# @contact: xinyu.shang@zozo.cn
from datetime import date
from typing import Dict, List, Any

import requests

from const import HttpConst

HOST = 'https://bugly.qq.com/v4/api/old'


class HttpCall(object):

    def __init__(self, headers: Dict):

        self.session = requests.Session()
        self.session.headers.update(headers)

    @staticmethod
    def __get_app_id(platform_id: int) -> str:
        if platform_id == HttpConst.ANDROID_PLATFORM_ID:
            return HttpConst.ANDROID_APP_ID

        if platform_id == HttpConst.IOS_PLATFORM_ID:
            return HttpConst.IOS_APP_ID

        raise AssertionError

    @staticmethod
    def _get_fsn(platform_id: int) -> str:
        if platform_id == HttpConst.ANDROID_PLATFORM_ID:
            return HttpConst.ANDROID_FSN

        if platform_id == HttpConst.IOS_PLATFORM_ID:
            return HttpConst.IOS_FSN

    def get_version_list(self, platform_id: int) -> List[str]:
        url = f'{HOST}/get-app-info'
        params = {'appId': self.__get_app_id(platform_id),
                  'pid': platform_id,
                  'types': 'version,member,tag,channel',
                  'fsn': self._get_fsn(platform_id)
                  }
        resp = self.session.get(url, params=params)

        return [x['name'] for x in resp.json()['data']['versionList']]

    def get_trend_result(self, platform_id: int, version: str, start_date: date, end_date: date, type_name: str) -> \
            List[Dict[str, Any]]:
        url = f'{HOST}/get-crash-trend'

        params = {'appId': self.__get_app_id(platform_id),
                  'dataType': 'trendData',
                  'pid': platform_id,
                  'type': type_name,
                  'version': version,
                  'startDate': start_date.strftime("%Y%m%d"),
                  'endDate': end_date.strftime("%Y%m%d"),
                  'fsn': self._get_fsn(platform_id)
                  }
        resp = self.session.get(url, params=params)
        return resp.json()["data"]["data"]
