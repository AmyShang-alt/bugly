# Author 尚欣雨
# coding=utf-8
# @Time    : 2020-07-16 11:03
# @Site    : 
# @File    : file_util.py
# @Software: PyCharm
# @contact: xinyu.shang@zozo.cn
from typing import List, Tuple

import xlsxwriter


def save_excel(file_name: str, sheet_data: List[Tuple[str, List[str], List[Tuple]]]):
    workbook = xlsxwriter.Workbook(
        filename='./report/%s.xlsx' % file_name)
    for sheet_name, headers, data_list in sheet_data:
        st = workbook.add_worksheet(sheet_name)
        for i in range(0, len(headers)):
            st.write(i, 0, headers[i])

        for i in range(0, len(data_list)):
            data = data_list[i]
            for c in range(0, len(data)):
                st.write(c, i + 1, data[c])

    workbook.close()
