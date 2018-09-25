# 数据整合 #
## 大致思路 ##
1. 分别获取pre-Precipitation和pre-Waterlevel预处理数据后的output，并作为inputRainfall和inputWaterLevel两个文件夹中的输入文件
2. 生成与降雨数据结束时间对应的水位数据信息，也同时生成延后一段时间(pretime)的水位数据信息(genData中引用的rain_level_Data/AllData()):
> 1. 将降雨与水位信息的数据文件对应上，并读取降雨数据（corrLevel中的corrRain()，rainfallInterval()）
> 2. 根据想要获取的时间差，即每一个降雨数据与对应水位的时间差，选用对应mod的水位数据
> 3. 将每一个降雨数据与每一个水位数据对应上（corrLevel中的rain_corrLine()）
> 4. 返回获取到的降雨数据，水位数据，降雨-水位对应规则
3. 根据对应规则及需要的降雨量数据数（numOfX）、水位数据数（numOfY），编排输入的降雨水位与输出的预测水位数据，返回所需要的数据集（genData中的genData()/genData_AllTime()）

## Block ##
* genData.py
  * genData 返回有降雨的降雨-水位数据集
  * genData_AllTime 返回所有时间段的降雨-水位数据集
* corrLevel.py
  * corrRain 返回对应井盖的雨量站
  * rain_corrLine 返回与输入降雨数据对应的水位数据
  * level_corrLine 返回与输入水位数据对应的水位数据
* corrData.py
  * rain_level_Data 返回固定时间差的降雨-水位数据及对应规则
  * level_level_Data 返回固定时间差的水位-水位数据及对应规则
  * rain_level_AllData 返回所有时间的固定时间差的降雨-水位数据及对应规则
* rainfallInterval.py 返回场雨结果
* timeNorm.py 各种与时间相关的函数

# Contact us
* 主程序员：[lflfdxfn](caoz@mail.sustc.edu.cn)
* 由于具体的处理思路与各种情况的应对都在编写过程中不断地添加与实现，代码实现比较混乱，过程也有很多不足。数据处理后大项目也急需跟近，不能再继续花费时间完善，还望谅解。如有更多问题，可邮箱联系我。