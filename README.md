# FofaSpider
Fofa通过页来获取爬取，换言之，你能访问多少页，就能爬取多少条

本脚本基于Python开发，根据查询后得到的数据进行按页爬取，结果以xls格式输出。
由于中途没执行完查看结果会导致数据加载excel失败，所以我用了两个xls文件，后缀分别为.xls和.xls.bak。
程序执行中间，可查看.xls文件，当.xls文件查看完毕，可以关闭.xls文件，等一两秒，.xls.bak把数据复制一份给.xls文件，如果再次打开.xls文件和没关闭之前一样，则程序运行完成，无法给.xls文件复制数据，只需要把.xls.bak文件修改为xls即可，即使中途断网或者ctrl+c了也没事，后面我断网试了下

## 免责声明

依据中华人民共和国网络安全法第二十七条：任何个人和组织不得从事非法侵入他人网络、干扰他人网络正常功能、窃取网络数据等危害网络安全的活动；不得提供专门用于侵入网络、干扰网络正常功能及防护措施、窃取网络数据等危害网络安全活动的程序、工具；明知他人从事危害网络安全的活动的不得为其提供技术支持、广告推广、支付结算等帮助。

使用本工具则默认遵守网络安全法

# config文件说明

    Cookie=""     //Fofa查询时的Cookie值
    Size=10000    //查询条数
   
# 使用说明

关于语法上面和Fofa有点出入，需要把双引号变成单引号，例如<br/>
 ``` app="Landray-OA系统" && country="CN"```
<br/>变成<br/>
 ``` app='Landray-OA系统' && country='CN'```

![image](https://user-images.githubusercontent.com/57057346/145268567-ecaf8191-eee0-46f7-9b77-a2ed09ceec93.png)

```python FofaPage.py -q "app='Landray-OA系统'&&country='CN'"```

![image](https://user-images.githubusercontent.com/57057346/145269043-0bbee363-18bc-4d6f-8b3d-bc913826d1d4.png)

![image](https://user-images.githubusercontent.com/57057346/145274282-bcea3a2a-9744-4a02-beac-13a5801ee984.png)

![image](https://user-images.githubusercontent.com/57057346/145275102-022ffb0f-690e-482f-bc7a-1726bef60787.png)

可以看到断网了，日志加载到了62页，excel也加载到了62页了

<br/>最后，希望大佬多多指教，要是能点个Star那就更好了
