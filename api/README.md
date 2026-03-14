# Computer Use API - Backend

FastAPI 后端服务，提供 Claude Computer Use 功能的 RESTful API 和 SSE 流式传输。

## 功能特性

- 会话管理（创建、查询、删除）
- 消息持久化（SQLite 数据库）
- 实时流式传输（Server-Sent Events）
- 并发控制（会话级别锁）
- 完整的错误处理
- 集成 Claude API 和计算机控制工具

## 安装依赖

```bash
pip install -r requirements.txt
```

## 初始化数据库

```bash
python api/init_db.py
```

## 启动服务

```bash
# 开发模式
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API 端点

### 会话管理

- `POST /api/sessions` - 创建新会话
- `GET /api/sessions` - 获取会话列表
- `GET /api/sessions/{session_id}` - 获取会话详情
- `DELETE /api/sessions/{session_id}` - 删除会话

### 消息

- `POST /api/sessions/{session_id}/messages` - 发送消息

### 流式传输

- `GET /api/sessions/{session_id}/stream` - SSE 流式获取响应

### 健康检查

- `GET /api/health` - 健康检查

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 环境变量

- `DATABASE_URL` - 数据库连接字符串（默认：sqlite+aiosqlite:///./fastapi_app.db）
- `CORS_ORIGINS` - CORS 允许的源（默认：*）
- `LOG_LEVEL` - 日志级别（默认：INFO）

## 项目结构

```
api/
├── __init__.py
├── main.py              # FastAPI 应用入口
├── config.py            # 配置管理
├── init_db.py           # 数据库初始化脚本
├── requirements.txt     # Python 依赖
├── models/              # 数据库模型
│   ├── session.py
│   └── message.py
├── routes/              # API 路由
│   ├── sessions.py
│   ├── messages.py
│   ├── streaming.py
│   └── health.py
├── services/            # 业务逻辑
│   ├── session_service.py
│   └── message_service.py
└── core/                # 核心功能
    ├── database.py      # 数据库引擎
    ├── loop_wrapper.py  # 对话引擎封装
    └── session_manager.py  # 会话管理器
```

## 使用示例

### 创建会话

```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "provider": "anthropic",
    "api_key": "your-api-key",
    "max_tokens": 16384
  }'
```

### 发送消息

```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, Claude!"
  }'
```

### 流式获取响应

```bash
curl -N http://localhost:8000/api/sessions/{session_id}/stream
```

## 开发说明

- 使用 Python 3.11+
- 异步编程（asyncio）
- SQLAlchemy 2.0+ (async)
- FastAPI 最佳实践
- 类型提示
