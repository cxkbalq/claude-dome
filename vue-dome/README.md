# Computer Use Frontend

Vue 3 前端应用，提供 Claude Computer Use 的用户界面。

## 功能特性

- 会话管理（创建、切换、删除）
- 实时聊天界面
- SSE 流式消息接收
- VNC 远程桌面查看器
- 设置面板（API 密钥、模型配置等）
- 响应式设计
- 简约美观的 UI

## 技术栈

- Vue 3 (Composition API)
- Axios (HTTP 客户端)
- noVNC (VNC 客户端)
- Vite (构建工具)

## 安装依赖

```bash
npm install
```

## 开发模式

```bash
npm run dev
```

访问 http://localhost:5173

## 生产构建

```bash
npm run build
```

构建产物在 `dist/` 目录

## 预览生产构建

```bash
npm run preview
```

## 环境变量

创建 `.env` 文件配置：

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api

# VNC Configuration
VITE_VNC_HOST=localhost
VITE_VNC_PORT=6080
VITE_VNC_PATH=websockify
```

## 项目结构

```
vue-dome/src/
├── main.js              # 应用入口
├── App.vue              # 根组件
├── assets/              # 静态资源
│   └── main.css         # 全局样式
├── components/          # Vue 组件
│   ├── ComputerUse.vue  # 主组件
│   ├── SessionList.vue  # 会话列表
│   ├── Chat.vue         # 聊天组件
│   ├── MessageRenderer.vue  # 消息渲染器
│   ├── Settings.vue     # 设置面板
│   └── VNCViewer.vue    # VNC 查看器
└── services/            # 服务层
    ├── api.js           # API 服务
    └── sse.js           # SSE 客户端
```

## 使用说明

1. 启动后端服务（见 api/README.md）
2. 启动前端开发服务器：`npm run dev`
3. 打开浏览器访问 http://localhost:5173
4. 点击 Settings 配置 API 密钥
5. 创建新会话开始对话
6. 可选：点击 Show VNC 查看虚拟桌面

## 组件说明

### ComputerUse
主组件，整合所有功能，管理全局状态。

### SessionList
显示会话列表，支持创建、选择、删除会话。

### Chat
聊天界面，显示消息历史，支持发送消息和实时流式更新。

### MessageRenderer
渲染不同类型的消息（用户、助手、工具结果），支持文本、思考内容、工具调用、截图等。

### Settings
设置面板，配置 API 密钥、模型、系统提示词等参数。

### VNCViewer
VNC 远程桌面查看器，连接到虚拟机显示屏幕。

## 开发说明

- 使用 Vue 3 Composition API
- 响应式数据管理
- 组件化设计
- 事件驱动通信
- 本地存储持久化配置
