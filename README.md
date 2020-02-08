# Computer-simulation-of-virus-spread
## 使用Python创建了一个病毒在人群中传播的计算机仿真模型

本文件是使用Python写的一个简单的计算机模拟病毒在人群中传播的仿真模型.并使用matplotlib绘图的程序.

人群分布使用简单的正态分布,人员活动也暂时使用简单的正态分布.当认为传染者和正常人的具体小到一定范围后,正常人就被感染.感染后有病毒潜伏期和发病期.在经过潜伏期和发病期后,病人才被隔离,隔离就认为这个人不会再被感染,也不会传播.

![病毒传播仿真](assets/病毒传播仿真.gif)

可以根据自己的喜好调整如下参数来查看不同的效果.

注意,这些参数的单位并没有对应实际的物理量.

```python
# 总共的人数统计
sum_of_human = 2000
# 潜伏期 表示患者感染上病毒后多少天才患病
incubation_period = 40
# 诊疗意愿，患者发病后多少天去医院
treat_willingness=40
isolation_all_day=incubation_period+treat_willingness
# 可容纳的隔离数
isolation_pos = 400
# 感染范围
infection_area = 0.02
# 运动范围参数 大小为1左右较好
move_area_param =1
# 初始感染者
first_infected_cnt = 10

```


