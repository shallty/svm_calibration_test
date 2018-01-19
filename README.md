# svm_calibration_test
`版本号：`0.0.1
`发布日期：`January 19, 2018

一个采用随机波动率模型（heston，1993）和蒙特卡洛模拟（MCS）进行50ETF校准及定价的简单库。

另外，由于采用MCS方法进行期权的定价，且标的资产路径模拟以每一个交易日为单位，所以当期权到期日较长时，会存在较多的迭代，明显拖慢运行速度。另外，此实验仅仅针对欧式看涨期权进行。

（第一次完整的写一个功能，请各位路过的大神多提意见~）

***
|Author|shallty_ht|
|---|---
|E-mail|hulinfeng.ht@foxmail.com
***
# 依赖环境注意！
本库中包含的市场数据抓取模块采用的是Wind资讯API，所以，如果要使用本库当中的数据调用函数，请务必安装好依赖包。
附：[Wind资讯API说明网址](http://www.dajiangzhang.com/document "悬停显示")
若不能安装此API，你可以利用其他方法获取期权市场实际数据。
其他依赖：
numpy
pandas
scipy
***
## 目录
* [svm_calibration_test](#svm_calibration_test)
  * [StoVolaMoMsc](#StoVolaMoMsc)
      * [get_underlying](#get_underlying)
      * [get_option_price](#get_option_price)
  * [get_wind_optiondata](#get_wind_optiondata)
  * [get_underlying_vol](#get_underlying_vol)
  * [CalibrationIns](#CalibrationIns)
      * [add_***](#add_***)
      * [get_dif](#get_dif)
  * [Calibrate](#Calibrate)
      * [loc_fmin](#loc_fmin)
      * [opti_param](#opti_param)
***

 # svm_calibration_test
 `from svm_calibration_test import *`
 50ETF期权蒙特卡洛模拟参数校准实验
目标：利用最小均方误差求得蒙特卡洛模拟的参数估计能模拟样本外期权价格
采用每月月初第一天不同到期日期权收盘价格作为市场价格
利用H93随机波动率模型进行校准
利用下月期权在第一天不同到期日期权收盘价作为验证标准

设计思路：
1. 首先构建蒙特卡洛模拟方法的期权价格计算，路径单位日度单位，年度单位为交易日252天。
2. 构建一个校准函数，这个函数输入变量只有期权定价函数和期权到期时间及期权价格，输出变量为最后的最优化参数
3. 最优化函数设置，目标函数为最小均方误差，结果显示是否优化成功。
***
## StoVolaMoMsc
`StoVolaMoMsc(S0, r, V0, kappa_v, theta_v, sigma_v, rho, K, startdate, enddate)`
欧式看涨期权蒙特卡洛方法定价对象
``` Python
  Parameters
  ==========
    S0 : float
        标的资产初始价格
    r : float
        无风险利率
    V0 : float
        随机波动率初始数值
    kappa_v : float
        均值回复因子
    theta_v : float
        长期均值因子
    sigma_v : float
        波动率扩散项
    rho : float
        随机波动率和标的资产的相关系数
    K : float
        行权价格
    startdate : str
        开始日
    enddate : str
        到期日
    
    Returns
    =======
    op : float
        期权价格
```
### get_underlying
`StoVolaMoMsc().get_underlying(fixseed=False)`
返回标的资产价格变动路径
``` Python
    Parameters
    ==========
    fixseed : bool
        是否设定随机数种子
```
### get_option_price
`StoVolaMoMsc().get_option_price(fixseed=False, mul=False)`
返回期权价格
mul如果设置成True将进行多次MCS，并且返回依次为多次MCS的均值、方差、最大、最小的list。
``` Python
    Parameters
    ==========
    fixseed : bool
        是否设定随机数种子
    mul : bool
        是否进行多次循环
           
    Returns
    =======
    option_price_describe_list : list
        期权价格
```
***
## get_wind_optiondata
`get_wind_optiondata(startdate, enddate)`
利用Wind数据接口获取期权交易市场数据。
``` Python
    Parameters
    ==========
    startdate : str
        行情数据开始日期
    enddate : str
        行情数据结束日期
    
    Returns
    =======
    option_data_set : DataFrame
        包含收盘价及到期日等信息的期权数据集
```
***
## get_underlying_vol
`get_underlying_vol(enddate)`
利用Wind数据接口获取标的资产市场波动率。
```Python
    Parameters
    ==========
    enddate : str
        行情数据结束日期
    
    Returns
    =======
    volatility : float
        标的资产传入参数日期为止的一年期历史对数收益率波动率
```
***
## CalibrationIns
`CalibrationIns()`
 参数校准工具，需要校准参数为kappa_v, theta_v, sigma_v, rho，在get_dif()方法中传入list[kappa_v, theta_v, sigma_v, rho]，返回MCS模拟结果与市场实际期权价格的均方误差。
```Python
    Methods
    =======
    add_underlying : pandas.Series
        向容器中添加标的资产市场价格数据
    add_volatility : pandas.Series
        向容器中添加标的资产历史波动率数据
    add_strike_price : pandas.Series
        向容器中添加期权行权价格数据
    add_startdate : pandas.Series
        向容器中添加期权合约市场数据获取日期
    add_enddate : pandas.Series
        向容器中添加期权合约到期日
    add_rate : pandas.Series
        向容器中添加市场实际无风险一年期利率（shibor）
    add_mar_price : pandas.Series
        向容器中添加期权合约市场价格  
    get_dif :
        取得不同参数下模拟数据与市场实际价格均方误差
```
注意各传入市场数据要保持顺序上的一致。
例如若校准期权合约为3个，则每一个传入容器中的数据要保证所有的Series[0]中皆是第一个合约相关的数据，Series[1]中皆为第二个合约相关数据，依此类推。
### get_dif
`CalibrationIns().get_dif(p)`
`p = [kappa_v, theta_v, sigma_v, rho]`
返回根据传入参数计算的期权价格与实际市场期权价格之间的均方误差。
***
## Calibrate
`Calibrate(price_diff_class)`
最终校准对象。采用scipy.optimize包进行最终的参数校准。
此对象仅仅是一个对CalibrationIns().get_dif()进行最小化处理并返回相应的最小化参数的对象，所以务必要传入上一级目录中已经初始化的CalibrationIns()对象，否则无法运行。
###  loc_fmin
`Calibrate(price_diff_class).loc_fmin()`
返回使得price_diff局部最小的参数值。
### opti_param
`Calibrate(price_diff_class).opti_param(initial_list)`
`initial_list=[kappa_v, theta_v, sigma_v, rho]`为全局最优化其实参数。用户可以先根据局部最优的结果传入全局最优起始参数。
返回使得price_diff全局最小的参数值。