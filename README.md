# ESE5023_Assignments_12631525

Comments on HW2 from Yali （97/100）

仅提交.ipynb文件即可，另外请运行.ipynb，jupyter会自动保存运行结果（.pdf只写处理思路即可）。谢谢！

1.1 ["Deaths"]分组不对，应考虑按["Total Deaths"]分组 （-1p)

2 根据质量代码筛选有效气温时，有效的数据应该只有qc=1，5，其他qc代码的仅仅是gross limits应该剔除，
值不存在时（`+9999` ）是纯粹的缺测标记，所以qc=9时也应该剔除（-2p)