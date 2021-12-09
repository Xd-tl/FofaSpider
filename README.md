# FofaSpider
Fofa通过页来获取爬取，换言之，你能访问多少页，就能爬取多少条

本脚本基于Python开发，主要用于区域资产搜索和指定目标资产搜索。爬取每一页的的每一个url的domain、host、ip、port、title、server、protocol等信息，最后进行整合，以xls格式输出。程序运行期间可以查看xls文件，如果看完xls文件，程序还没有运行完，可以关闭xls文件，等几秒钟，再打开xls文件即可，如果重新打开xls数据没变化，则copy一份log目录下的xls.bak文件到当前目录下，并修改后缀为xls即可，即使中途断网或者ctrl+c了也没事，加载过的数据依旧还在

# 免责声明

依据中华人民共和国网络安全法第二十七条：任何个人和组织不得从事非法侵入他人网络、干扰他人网络正常功能、窃取网络数据等危害网络安全的活动；不得提供专门用于侵入网络、干扰网络正常功能及防护措施、窃取网络数据等危害网络安全活动的程序、工具；明知他人从事危害网络安全的活动的不得为其提供技术支持、广告推广、支付结算等帮助。

使用本工具则默认遵守网络安全法

# config文件说明
```
Cookie=""     //Fofa查询时的Cookie值
Size=10000    //查询条数
fragile=["中心", "测试", "登录","登陆","平台", "系统", "管理"] //要搜索的资产，可以根据情况自行添加
```
# 使用说明

关于语法上面和Fofa有点出入，需要把双引号变成单引号，例如<br/>
 ``` app="Landray-OA系统" && country="CN"```
<br/>变成<br/>
 ``` app='Landray-OA系统' && country='CN'```
 
![image](https://user-images.githubusercontent.com/57057346/145408324-66effd60-28fb-4f92-b062-455626737e95.png)<br/>

## 指定搜索<br>

```py FofaPage.py -q "app='Landray-OA系统'&&country='CN'"```<br/>
-q为Fofa查询语句<br/>

![image](https://user-images.githubusercontent.com/57057346/145408997-082c20ee-efa4-4dca-859b-cf18b6b27a6e.png)

## 区域资产收集

搜索语句：title="city"&&title="fragile"&&country="CN"&&region!="HK<br/>
例：<br/>
```py FofaPage.py -c "贵州" -p 1```<br/>
-c为目标城市，-p为0或者1，默认为0，0则爬取该省底下的所有市、区、县，1则爬取该市底下的所有区、县<br/>

![image](https://user-images.githubusercontent.com/57057346/145405007-4026df09-763d-45c4-9f57-2019fb1d8437.png)<br/>

由于全部加载完，太多了我就ctrl+c了，但是并不影响结果，日志也是加载到了中断那块，excel也是差不多块150条

<br/>最后，希望大佬多多指教，要是能点个Star那就更好了
