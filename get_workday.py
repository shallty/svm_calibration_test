# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:25:34 2018

@author: H.T
"""

#
# 获取两个日期之间的交易日天数
# get_workday.py
#
import pandas as pd

def get_workday(startdate, enddate):
    ''' 获取开始日期与到期日期之间的交易日天数。
    
    Parameters
    ==========
    startdate : str
        开始日期
    enddate : str
        结束日期
    
    Results
    =======
    wdc : int
        开始日到结束日期之间的交易日天数
    '''
    wdc = len(pd.date_range(startdate, enddate, freq='B'))
    return wdc