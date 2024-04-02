![img.png](img.png)
API

/NotCheckedMission

``{"page":page}``

返回未审核的任务信息，状态码为200

/CheckedMission

``{"page":page}``

返回已审核的任务信息，状态码为200

![img_1.png](img_1.png)
这里不通过暂时没在用户界面反馈，也就暂时不写api，做的时候可以先当个返回键处理

/passmission

要求格式
``{"id":id}`` --这里的id是个序号，不是用户名哦，前面都会返回id的

/SelectNotCheckedMission

/SelectCheckedMission

两个api传入的都是

``{"input":input}``

还剩下个提交任务审核没做，这个要根据志愿者那边的情况来做（看具体使用哪个数据表单）