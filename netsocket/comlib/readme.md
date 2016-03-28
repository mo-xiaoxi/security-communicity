# comlib


```
.
├── __init__.py				<---加解密库初始化文件
├── File.py					<---文件读取操作
├── Subcontracting.py			<--- 包切分（处理传入消息太大的情况）
├── aes.py					<---aes加解密	
├── getNeededKey.py			<---从key从获取相应部分密钥
├── hmac.py					<---hmac实现	
├── messageExchangge.py		<---密钥前后交换，用于ack
├── keyExpand.py				<---密钥衍生
├── packetFill.py			 	<---数据填充
└─── readme.md				  <---代码库说明文件
```