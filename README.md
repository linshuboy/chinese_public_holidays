# 获取法定节假日信息

## 使用说明

* 自动更新
* 更新及时, 保证准确性
* 开源免费

## 可以直接使用

* [all_holidays.json](all_holidays.json) 所有2007年以来的节假日信息
* [holidays.json](holidays.json) 所有2007年以来的节假日信息,按年分组

## 使用方法
* 只需要引入`holidays.json` 或者 `all_holidays,json`文件, 然后使用`json`解析即可
* json中存在的日期有work属性, 为true表示工作日, 没有的为节假日
* json中不存在的日期, 根据当天是周末还是工作日, 自行判断
