# 树莓派项目

使用python代码编写一个可抗密钥丢失的点对点通信协议


## 项目目录结构：
```
.
├── appReceieve.py				<--- 外部应用程序
├── appSend.py				<--- 外部应用程序
├── backup						<--- 备份文件
├── netsocket						<--- 通信模块
└── readme.md						<--- 本文件
.
├── 1.pdf
├── appReceieve.py
├── appSend.py
├── backup
│   ├── client.py
│   ├── server.py
│   ├── test1.py
│   ├── test2.py
│   ├── threadutil.py
│   └── ?\210\235?\213?\214\226.cpp
├── netsocket
│   ├── Subcontracting.py
│   ├── __init__.py
│   ├── communication.py
│   ├── communicationbackup.py
│   ├── cryption
│   │   ├── __init__.py
│   │   ├── aes.py
│   │   ├── aesback.py
│   │   ├── getNeededKey.py
│   │   ├── hmac.py
│   │   ├── keyExpand.py
│   │   ├── messageExchangge.py
│   │   ├── packetFill.py
│   │   └── readme.md
│   ├── netSim.py
│   ├── output.txt
│   ├── readme.md
│   ├── s_count.txt
│   └── testCryption.py
└── readme.md
```

## 使用方法
![image](http://momomoxiaoxi.com/img/rpi/1.png)
![image](http://momomoxiaoxi.com/img/rpi/2.png)