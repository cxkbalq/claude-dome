# Claude Computer Use - 前后端分离版本

这是 Claude Computer Use Demo 的前后端分离实现，提供完整的 API 服务和现代化的 Web 界面。

## 项目结构

```
.
├── api/                    # FastAPI 后端
│   ├── main.py            # 应用入口
│   ├── models/            # 数据库模型
│   ├── routes/            # API 路由
│   ├── services/          # 业务逻辑
│   ├── core/              # 核心功能
│   └── README.md          # 后端文档
│
├── vue-dome/              # Vue 3 前端
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── services/      # API 服务
│   │   └── assets/        # 静态资源
│   └── README.md          # 前端文档
│
├── computer_use_demo/     # 原始核心逻辑
│   ├── loop.py           # 对话引擎
│   └── tools/            # 工具集合
│
└── PROJECT_README.md      # 本文件
```

## 功能特性

### 后端 (FastAPI)
- ✅ RESTful API 设计
- ✅ 会话管理（创建、查询、删除）
- ✅ 消息持久化（SQLite）
- ✅ SSE 实时流式传输
- ✅ 并发控制（会话级别锁）
- ✅ 完整错误处理
- ✅ 集成 Claude API
- ✅ 支持所有计算机控制工具

### 前端 (Vue 3)
- ✅ 会话列表管理
- ✅ 