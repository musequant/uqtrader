# uqtrader

* 利用easytrader实现[优矿网](https://uqer.io)策略一键下单功能
* 支持选择"我的交易"中任意策略


## 安装步骤

> install [anaconda](https://www.continuum.io/downloads)

> pip install -r requirements.txt

> 安装tesseract或java（二选一）用于识别验证码
* windows用户直接点击：[tesseract](http://tesseract-ocr.googlecode.com/files/tesseract-ocr-setup-3.02.02.exe)
* linux用户： apt-get install tesseract-ocr
* mac用户： brew install tesseract

## 用法

> python trader.py 启动uqtrader

> 获取加密后的交易密码的步骤：

1. 打开IE浏览器，输入[华泰证券官网](https://service.htsc.com.cn/service/login.jsp)，填写客户号密码，此时不登陆；
2. 点击F12，打开调试器；
3. 选择`网络`标签；
4. 点击F5，启动网络流量捕获；
5. `摘要`标签里，选择第一个请求：https://service.htsc.com.cn/service/loginAction.do?method=login；
6. 点击`详细信息`标签；
7. 点击`请求正文`标签，找到：trdpwdEns=f2cdf33b2ba8e98c4b1c71a459d2a649，trdpwdEns对应的就是加密后的交易密码。

> 在uqtrader客户端依次输入优矿网账号密码，华泰证券账号，加密后的交易密码，和通讯密码。

> 可以选择保存账号密码，避免下次重新输入。点击登陆按钮，成功登陆将会进入策略操作页面，否则请检查账号密码。
