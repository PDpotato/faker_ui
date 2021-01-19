# faker_ui

使用Tinker基于Faker模块设计的模拟数据生成工具

## 使用说明

1. 运行view.py，启动工具

[![sgbhCj.png](https://s3.ax1x.com/2021/01/19/sgbhCj.png)](https://imgchr.com/i/sgbhCj)

2. 选择数据库模拟数据

   [![sgqiVO.png](https://s3.ax1x.com/2021/01/19/sgqiVO.png)](https://imgchr.com/i/sgqiVO)

3. 输入Mysql连接信息，连接数据库，信息正确即可连接成功

4. 依次选择需要使用的数据库，数据表

   [![sgq8iQ.png](https://s3.ax1x.com/2021/01/19/sgq8iQ.png)](https://imgchr.com/i/sgq8iQ)

[![sgqIFe.png](https://s3.ax1x.com/2021/01/19/sgqIFe.png)](https://imgchr.com/i/sgqIFe)



5. 在数据类型处可根据字段选择需要生成的模拟数据类型

[![sgLmY4.png](https://s3.ax1x.com/2021/01/19/sgLmY4.png)](https://imgchr.com/i/sgLmY4)

​		例如：选择地址则会对应生成随机地址，国家则会生成随机国家，不设置，则表示当前字段不生成随机数据，该字段也不会插入。

---



每个字段也可以点击自定义按钮，对当前字段固定一个值，不采用随机生成的方式。

字段过多时可以通过翻页按钮浏览和设置字段需要生成的数据类型，当所有字段设置完毕，可点击插入数据按钮，输入需要插入的数据条数，如果插入成功，默认会根据数据库名和表名生成当前表的设计记录，下次进入该表可点击导入历史记录按钮自动导入

**ps：若字段信息显示不全，可将鼠标光标移动至该信息上，在顶上会显示该字段全部信息**

[![sgXjw6.png](https://s3.ax1x.com/2021/01/19/sgXjw6.png)](https://imgchr.com/i/sgXjw6)



对应的**WEB模拟数据**模块功能相同，只是生成的模拟数据是相对于接口

**生成EXCEL**功能

[![sgvTM9.png](https://s3.ax1x.com/2021/01/19/sgvTM9.png)](https://imgchr.com/i/sgvTM9)



[![sgxUy9.png](https://s3.ax1x.com/2021/01/19/sgxUy9.png)](https://imgchr.com/i/sgxUy9)



[![sgza9S.png](https://s3.ax1x.com/2021/01/19/sgza9S.png)](https://imgchr.com/i/sgza9S)



**以下为生成的EXCEL数据**

[![s2SUV1.png](https://s3.ax1x.com/2021/01/19/s2SUV1.png)](https://imgchr.com/i/s2SUV1)