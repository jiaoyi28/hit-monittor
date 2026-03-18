# hit-monittor

运行在 Windows 本机环境的个人 GitHub 监控台。

## 技术栈

- 前端：`npm + React + Tailwind CSS + shadcn/ui`
- 后端：`Python + uv + FastAPI`
- 数据库：`SQLite`

## 约束

- 文档、代码、中文注释和中文文案统一使用 UTF-8 编码
- SQLite 默认目录为 `D:\sqlite`
- V1 仅支持 GitHub 公开仓库

## 目录结构

- `frontend/`：前端应用，负责仪表盘、仓库列表、仓库详情和配置页
- `backend/`：后端 API、SQLite 初始化、GitHub 抓取、AI 分析和调度器
- `docs/superpowers/specs/`：设计文档
- `docs/superpowers/plans/`：实施计划

## 本地启动

### 1. 启动后端

在 `backend/` 目录执行：

```powershell
uv run uvicorn app.main:app --reload
```

默认会：

- 自动检查并创建 `D:\sqlite`
- 自动初始化数据库文件和默认配置
- 暴露后端接口到 `http://127.0.0.1:8000`

### 2. 启动前端

在 `frontend/` 目录执行：

```powershell
npm run dev
```

前端默认由 Vite 提供开发服务器。

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
- `GET /api/repositories/{id}`：仓库详情
- `GET /api/settings`：当前抓取与分析配置
- `PATCH /api/settings`：更新抓取与分析间隔

## 运行时配置

后端当前通过 `Settings` 读取配置，默认前缀为 `HIT_MONITTOR_`。当前已覆盖的核心配置包括：

- `HIT_MONITTOR_DATABASE_DIR`
- `HIT_MONITTOR_DATABASE_NAME`

后续接入 OpenAI 兼容模型时，建议继续沿用相同方式扩展：

- `api_key`
- `base_url`
- `model`
