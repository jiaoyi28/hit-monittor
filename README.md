# hit-monittor

运行在 Windows 本地环境的个人 GitHub 监控台。

## 技术栈

- 前端：`npm + React + Tailwind CSS`
- 后端：`Python + uv + FastAPI`
- 数据存储：`SQLite`

## 约束

- 文档、代码注释和中文文案统一使用 UTF-8 编码。
- SQLite 默认目录为 `D:\sqlite`。
- 当前仅支持 GitHub 公开仓库。

## 目录结构

- `frontend/`：前端应用，负责总览、仓库列表、仓库详情和设置页。
- `backend/`：后端 API、SQLite 初始化、GitHub 抓取、分析服务和调度逻辑。
- `docs/superpowers/specs/`：设计文档。
- `docs/superpowers/plans/`：实现计划。

## 首次初始化

### 1. 初始化后端依赖

在 `backend/` 目录执行：

```powershell
uv sync --dev
```

### 2. 初始化前端依赖

在 `frontend/` 目录执行：

```powershell
npm install
```

## 本地启动

### 一步启动

在项目根目录执行：

```powershell
.\start-dev.bat
```

这个脚本会顺序完成：

- 后端依赖初始化：`uv sync --dev`
- 前端依赖初始化：`npm install`
- 在新窗口启动后端服务
- 在新窗口启动前端开发服务

### 手动启动后端

在 `backend/` 目录执行：

```powershell
uv run uvicorn app.main:app --reload
```

后端启动时会自动：

- 检查并创建 `D:\sqlite`
- 初始化数据库文件和默认设置
- 暴露接口到 `http://127.0.0.1:8000`

### 手动启动前端

在 `frontend/` 目录执行：

```powershell
npm run dev
```

## 测试与构建

### 后端测试

```powershell
cd backend
uv run pytest tests -v
```

### 前端测试

```powershell
cd frontend
npm test
```

### 前端构建

```powershell
cd frontend
npm run build
```

## 关键接口

- `GET /health`：健康检查
- `GET /api/dashboard`：总览页数据
- `GET /api/repositories`：仓库列表
- `POST /api/repositories`：添加仓库
- `GET /api/repositories/{id}`：仓库详情
- `GET /api/settings`：抓取与分析间隔配置
- `PATCH /api/settings`：更新抓取与分析间隔

## 运行时配置

后端统一通过环境变量读取配置，变量前缀为 `HIT_MONITTOR_`。

### 数据库

- `HIT_MONITTOR_DATABASE_DIR`
- `HIT_MONITTOR_DATABASE_NAME`

### OpenAI 分析服务

- `HIT_MONITTOR_OPENAI_BASE_URL`
- `HIT_MONITTOR_OPENAI_API_KEY`
- `HIT_MONITTOR_OPENAI_MODEL`

说明：

- OpenAI 相关配置只走后端环境变量，不写入 SQLite，也不在前端设置页中编辑。
- 大模型分析服务直接使用 OpenAI Python SDK，不再手写 HTTP 调用。
- 如果未配置 `HIT_MONITTOR_OPENAI_API_KEY`，分析客户端不会初始化，分析流程会保持未启用状态。
