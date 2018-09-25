# mini-bacth sgd user document


- [mini-bacth sgd user document](#mini-bacth-sgd-user-document)
    - [main](#main)
- [data_construction 数据整合](#data-construction)
    - [data_construction 大致思路](#data-construction)
    - [data_construction 内部结构说明](#data-construction)
- [minibatch_sgd 算法](#minibatch-sgd)
    - [minibatch_sgd 大致思路](#minibatch-sgd)
        - [data_process 数据处理](#data-process)
        - [minibatch-sgd 算法](#minibatch-sgd)
        - [direct_minibatch 封装与可视化](#direct-minibatch)
- [Contact us](#contact-us)


main
----
* 结果位于minibatch_sgd/data/result/result.csv

 <pre><code>run(X_num,Y_num,pretime,A_scale,b_scale,batchsize,epochs,rate,sensorcode)</code></pre>
* X_num：输入的历史降雨量的数目。例：“2”代表输入过去20分钟的降雨7信息。
* Y_num：输入的历史水位的数目，历史水位的时间间隔可在代码中调整。例：“2”代表输入相同间隔的两个历史水位数据。
* pretime：预测多少分钟后的水位。例：“12”代表预测12分钟后的井下水位。
* A_scale：用于多元线性规划中变量系数的初始值。例：“1”代表其初始值为0~1间的随机数。
* b_scale：用于多元线性规划中常数的初始值。例：“1”代表其初始值为0~1间的随机数。
* batchsize：mini-batch SGD中每一次梯度下降所使用的batch中训练数据的个数。
* epochs：梯度下降训练的迭代次数。
* rate：梯度下降的学习速率。
* sensorcode：井盖的观测器代码。

data_construction 数据整合
=====
data_construction 大致思路
----
1. 分别获取pre-Precipitation和pre-Waterlevel预处理数据后的output，并作为inputRainfall和inputWaterLevel两个文件夹中的输入文件
2. 生成与降雨数据结束时间对应的水位数据信息，也同时生成延后一段时间(pretime)的水位数据信息(genData中引用的rain_level_Data/AllData()):
> 1. 将降雨与水位信息的数据文件对应上，并读取降雨数据（corrLevel中的corrRain()，rainfallInterval()）
> 2. 根据想要获取的时间差，即每一个降雨数据与对应水位的时间差，选用对应mod的水位数据
> 3. 将每一个降雨数据与每一个水位数据对应上（corrLevel中的rain_corrLine()）
> 4. 返回获取到的降雨数据，水位数据，降雨-水位对应规则
3. 根据对应规则及需要的降雨量数据数（numOfX）、水位数据数（numOfY），编排输入的降雨水位与输出的预测水位数据，返回所需要的数据集（genData中的genData()/genData_AllTime()）

data_construction 内部结构说明
----
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


minibatch_sgd 算法
====

minibatch_sgd 大致思路
----
1. 通过fetch_data获取到数据后，进行归一化，分割为训练集和验证集
2. 在tool中实现了一些常用的方法，减少代码重复
3. 在minibatch中实现了大部分的功能，包括训练相关，验证相关和分析相关
4. 在direct_minibatch中将所有模块联结起来，并使用run(args)来封装所有方法
minibatch_sgd 内部结构说明:
----
### data_process 数据处理
分为两部分，读取数据和工具包

1. fetch_data:读取数据
    * <pre><code>find_M(list)</code></pre>
        <p>读取一个列后，返回最大和最小值</p>

    * <pre><code>single_norm(list)</code></pre>
        <p>根据最大和最小值，对一个列进行归一化</p>
    * <pre><code>all_norm(nlist)</code></pre>
        <p>对多个列进行归一化</p>
    * <pre><code>use_data(X_num,Y_num,pretime,name)</code></pre>
        <p>从data_construction模块获取信息，随后将其分割为训练集和验证集</p>


1. tool 工具
    * combine:
        * <pre><code>first_stack(X1,X2,flag):X1,flag</code></pre>
            <p>把多个列堆叠在一起</p>
    * confuse:
        * <pre><code>shuffle_data(X,y):</code></pre>
            <p>将一组输入和输出打乱</p>
        * <pre><code>shuffle_index(inputs)</code></pre>
            <p>给定输入，打乱并生成打乱的序列</p>
    * sperate:
        * <pre><code>split_num(batchsize)</code></pre>
            <p>根据batchsize的大小按比例返回训练集大小和验证集大小</p>
### minibatch-sgd 算法
主要包含了minibatch-sgd的核心算法

* <pre><code>yp(A,b,X)</code></pre>
    <p>A*X+b</p>
* <pre><code>mean_yp(A,b,Xv)</code></pre>
    <p>取得yp的平均值</p>
* <pre><code>mean_y(yv)</code></pre>
    <p>取得y的平均值</p>
* <pre><code>MAE(Xv,yv,A,b)</code></pre>
    <p>计算平均绝对误差</p>
* <pre><code>RMSE(Xv,yv,A,b)</code></pre>
    <p>计算均方根</p>
* <pre><code>R(Xv,yv,A,b)</code></pre>
    <p>计算相关系数</p>
* <pre><code>adjust_R(R,X_num,Y_num,num)</code></pre>
    <p>计算修正相关系数</p>
* <pre><code>CE(Xv,yv,A,b)</code></pre>
    <p>计算纳什效率系数</p>
* <pre><code>scale(X,A_scale,b_scale,flag)</code></pre>
    <p>根据倍数计算初始A，b</p>
* <pre><code>log(epochs,l_train,l_val)</code></pre>
    <p>生成log</p>
* <pre><code>evaluate(Xv,yv,A,b)</code></pre>
    <p>分析验证集在训练模型里的特征</p>
* <pre><code>predict_regression(A,b,X)</code></pre>
    <p>预测结果和观测结果的回归曲线</p>
* <pre><code>obs_pred_compare(y_obs,y_pred)</code></pre>
    <p>预测结果和观测结果的比对</p>
* <pre><code>dA(y,y_p,X)</code></pre>
    <p>计算A的梯度</p>
* <pre><code>db(y,y_p)</code></pre>
    <p>计算b的梯度</p>
* <pre><code>calibrate(X,y,A,b,rate)</code></pre>
    <p>输入训练样本、初始值与学习率并训练</p>
* <pre><code>validate(Xv,yv,A,b)</code></pre>
    <p>输入验证样本与训练结果，进行验证</p>

### direct_minibatch 封装与可视化
封装并连接各个算法部分并将结果导出成可以理解的形式

* <pre><code>de_norm(value,m)</code></pre>
    <p>去归一化，还原真实水位</p>
* <pre><code>current_time()</code></pre>
    <p>获得当前时间</p>
* <pre><code>divide(input)</code></pre>
    <p>分割输入数据</p>
* <pre><code>rand_select_batch(T,batchsize)</code></pre>
    <p>随机从训练集中选取batchsize个样本</p>
* <pre><code>run</code></pre>
    <p>运行程序，包含训练、验证、分析；生成模型结果、各种参数和图表</p>

Contact us
====
* 主程序员：[lflfdxfn](caoz@mail.sustc.edu.cn)
* 负责模块：data_construction
* 由于具体的处理思路与各种情况的应对都在编写过程中不断地添加与实现，代码实现比较混乱，过程也有很多不足。数据处理后大项目也急需跟近，不能再继续花费时间完善，还望谅解。如有更多问题，可邮箱联系我。
* 主程序员：[DiracSea](sulz@mail.sustc.edu.cn) 
* 负责模块：minibatch-sgd
* 为了能够更快的展示我们的结果，加快了进度，删除了不需要的模块。后期可以添加更多的功能比如regularization，使用其他的优化模型与当前结果比对。
