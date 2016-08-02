# 文件目录说明
本文件夹下所有文件

```

├── Rec										接受者文件夹
│   ├── config.json							配置文件
│   ├── key									48位key
│   ├── msg									已发送但是未收到ack的信息
│   ├── seq									序列号
│   └── state								状态机状态
└── send									发送者文件夹
    ├── config.json							配置文件
    ├── key									48+48位key 保存keynow和keypast
    ├── msg									已收到但是未交付给上层的信息
    ├── seq									序列号
    └── state								状态机状态
```