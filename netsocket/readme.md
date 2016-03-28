# netsocket

```
.
├── Subcontracting.py		<--- 包切分（处理传入消息太大的情况）
├── __init__.py			<--- 初始化文件
├── communication.py		<--- 信息交流文件（最关键）
├── communicationbackup.py<--- 信息交流备份文件
├── cryption				<----密码库
│   ├── __init__.py		<---加解密库初始化文件
│   ├── aes.py			<---aes加解密
│   ├── aesback.py		<---aes加解密备份文件
│   ├── getNeededKey.py	<---从key从获取相应部分密钥
│   ├── hmac.py			<---hmac实现
│   ├── keyExpand.py		<---密钥衍生
│   ├── messageExchangge.py<---密钥前后交换，用于ack
│   ├── packetFill.py		<---数据填充
│   └── readme.md			<---密码库说明文件
├── netSim.py				<---网络仿真测试文件
├── r_count				<----服务端序列计数
├── readme.md				<----说明文件（本文件）
├── s_count				<----客户端序列计数
├── key					<----密钥文件
└── testCryption.py		<----密码库测试文件

```