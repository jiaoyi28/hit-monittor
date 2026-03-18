# GitHub 个人监控台 V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个运行在 Windows 本机上的单用户 GitHub 公开仓库监控台，支持后台抓取 issue、PR、release，并使用 OpenAI 兼容接口进行热点摘要与趋势预分析。

**Architecture:** 项目采用前后端分离结构：`frontend` 基于 React、Vite、Tailwind CSS 和 shadcn/ui 提供仪表盘体验，`backend` 基于 FastAPI、SQLAlchemy 和 SQLite 提供 API、任务调度和数据分析。后端以“抓取与预分析任务中心”为核心，前端只消费已经归一化并落库的结果。

**Tech Stack:** `npm`, `React`, `Vite`, `TypeScript`, `Tailwind CSS`, `shadcn/ui`, `Vitest`, `Python`, `uv`, `FastAPI`, `SQLAlchemy`, `SQLite`, `pytest`

---

## 实施约束

- 所有文档、代码文件、中文注释、中文文案统一使用 UTF-8 编码。
- SQLite 数据库目录固定为 `D:\sqlite`，默认数据库文件为 `D:\sqlite\hit-monittor.db`。
- V1 仅支持 GitHub 公开仓库，不实现私有仓库鉴权。
- 模型接口采用 OpenAI 协议，必须支持自定义 `api_key`、`model`、`base_url`。
- 调度配置必须来自数据库设置，不允许将抓取间隔和分析间隔写死在代码中。

## 目标目录结构

### 根目录

- Create: `D:\dev\hit-monittor\.editorconfig`
- Modify: `D:\dev\hit-monittor\.gitignore`
- Create: `D:\dev\hit-monittor\frontend\package.json`
- Create: `D:\dev\hit-monittor\frontend\vite.config.ts`
- Create: `D:\dev\hit-monittor\frontend\tsconfig.json`
- Create: `D:\dev\hit-monittor\frontend\src\main.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\App.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\lib\api.ts`
- Create: `D:\dev\hit-monittor\frontend\src\lib\types.ts`
- Create: `D:\dev\hit-monittor\frontend\src\components\layout\app-shell.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\dashboard\summary-cards.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\repositories\repository-table.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\repository-detail\detail-sections.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\settings\settings-form.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\dashboard-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\repositories-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\repository-detail-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\settings-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\test\app-shell.test.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\test\dashboard-page.test.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\test\settings-form.test.tsx`
- Create: `D:\dev\hit-monittor\backend\pyproject.toml`
- Create: `D:\dev\hit-monittor\backend\uv.lock`
- Create: `D:\dev\hit-monittor\backend\app\main.py`
- Create: `D:\dev\hit-monittor\backend\app\core\config.py`
- Create: `D:\dev\hit-monittor\backend\app\core\database.py`
- Create: `D:\dev\hit-monittor\backend\app\models\repository.py`
- Create: `D:\dev\hit-monittor\backend\app\models\issue.py`
- Create: `D:\dev\hit-monittor\backend\app\models\pull_request.py`
- Create: `D:\dev\hit-monittor\backend\app\models\release.py`
- Create: `D:\dev\hit-monittor\backend\app\models\analysis_result.py`
- Create: `D:\dev\hit-monittor\backend\app\models\sync_job.py`
- Create: `D:\dev\hit-monittor\backend\app\models\app_setting.py`
- Create: `D:\dev\hit-monittor\backend\app\schemas\dashboard.py`
- Create: `D:\dev\hit-monittor\backend\app\schemas\repository.py`
- Create: `D:\dev\hit-monittor\backend\app\schemas\settings.py`
- Create: `D:\dev\hit-monittor\backend\app\services\github_client.py`
- Create: `D:\dev\hit-monittor\backend\app\services\ingestion.py`
- Create: `D:\dev\hit-monittor\backend\app\services\analysis_client.py`
- Create: `D:\dev\hit-monittor\backend\app\services\analysis_pipeline.py`
- Create: `D:\dev\hit-monittor\backend\app\services\dashboard_service.py`
- Create: `D:\dev\hit-monittor\backend\app\services\settings_service.py`
- Create: `D:\dev\hit-monittor\backend\app\services\sync_service.py`
- Create: `D:\dev\hit-monittor\backend\app\scheduler\runner.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\dashboard.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\repositories.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\settings.py`
- Create: `D:\dev\hit-monittor\backend\tests\conftest.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_config.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_repository_api.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_settings_api.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_github_ingestion.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_analysis_pipeline.py`
- Create: `D:\dev\hit-monittor\backend\tests\test_scheduler_runner.py`
- Create: `D:\dev\hit-monittor\README.md`

### 文件职责说明

- `.editorconfig`：强制 UTF-8、LF/CRLF 和基础缩进规则。
- `frontend/src/lib/*`：前端接口封装和共享类型。
- `frontend/src/components/*`：纯展示与交互组件，按页面领域拆分。
- `frontend/src/pages/*`：页面级组合逻辑。
- `backend/app/core/*`：配置与数据库初始化。
- `backend/app/models/*`：SQLAlchemy 数据模型。
- `backend/app/services/*`：GitHub 抓取、AI 分析、任务编排、设置管理。
- `backend/app/api/routes/*`：HTTP API 路由。
- `backend/app/scheduler/*`：进程内调度。
- `backend/tests/*`：后端单元测试与 API 测试。

## 任务清单

### Task 1: 初始化仓库骨架与 UTF-8 编码护栏

**Files:**
- Create: `D:\dev\hit-monittor\.editorconfig`
- Modify: `D:\dev\hit-monittor\.gitignore`
- Modify: `D:\dev\hit-monittor\README.md`
- Create: `D:\dev\hit-monittor\frontend\package.json`
- Create: `D:\dev\hit-monittor\backend\pyproject.toml`

- [ ] **Step 1: 写一个失败的配置存在性检查**

```powershell
Test-Path .editorconfig
Test-Path frontend\package.json
Test-Path backend\pyproject.toml
```

- [ ] **Step 2: 运行检查并确认缺失**

Run: `Test-Path .editorconfig; Test-Path frontend\package.json; Test-Path backend\pyproject.toml`
Expected: 至少一个返回 `False`

- [ ] **Step 3: 创建 `.editorconfig` 并强制 UTF-8**

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4
```

- [ ] **Step 4: 初始化前后端包清单**

```json
{
  "name": "hit-monittor-frontend",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "test": "vitest run"
  }
}
```

```toml
[project]
name = "hit-monittor-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi", "sqlalchemy", "pydantic-settings", "httpx"]
```

- [ ] **Step 5: 更新 `README.md`，声明技术栈、UTF-8 约束和本地目录约束**

```md
# hit-monittor

Windows 本机运行的 GitHub 个人监控台。

## 约束

- 文档和代码中的中文统一使用 UTF-8 编码
- SQLite 默认目录：`D:\sqlite`
```

- [ ] **Step 6: 重新运行存在性检查**

Run: `Test-Path .editorconfig; Test-Path frontend\package.json; Test-Path backend\pyproject.toml`
Expected: 全部返回 `True`

- [ ] **Step 7: 提交骨架初始化**

```bash
git add .editorconfig .gitignore README.md frontend/package.json backend/pyproject.toml
git commit -m "chore: initialize repo scaffolding"
```

### Task 2: 搭建后端配置层与数据库入口

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\core\config.py`
- Create: `D:\dev\hit-monittor\backend\app\core\database.py`
- Create: `D:\dev\hit-monittor\backend\app\main.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_config.py`
- Test: `D:\dev\hit-monittor\backend\tests\conftest.py`

- [ ] **Step 1: 先写配置测试**

```python
def test_default_database_path_uses_d_sqlite():
    settings = Settings()
    assert str(settings.database_path) == r"D:\sqlite\hit-monittor.db"
```

- [ ] **Step 2: 运行单测确认失败**

Run: `uv run pytest backend/tests/test_config.py -v`
Expected: FAIL with `NameError: name 'Settings' is not defined`

- [ ] **Step 3: 实现 `Settings` 和数据库 URL 组装**

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HIT_MONITTOR_", extra="ignore")
    database_dir: Path = Path(r"D:\sqlite")
    database_name: str = "hit-monittor.db"

    @property
    def database_path(self) -> Path:
        return self.database_dir / self.database_name
```

- [ ] **Step 4: 实现数据库引擎与启动检查**

```python
def create_sqlite_url(settings: Settings) -> str:
    return f"sqlite:///{settings.database_path.as_posix()}"
```

- [ ] **Step 5: 启动 FastAPI 基础应用并挂上健康检查**

```python
app = FastAPI(title="hit-monittor")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 6: 运行测试确认通过**

Run: `uv run pytest backend/tests/test_config.py -v`
Expected: PASS

- [ ] **Step 7: 提交后端基础设施**

```bash
git add backend/app/core backend/app/main.py backend/tests/test_config.py backend/tests/conftest.py
git commit -m "feat: add backend settings and database bootstrap"
```

### Task 3: 建立数据库模型与设置表

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\models\repository.py`
- Create: `D:\dev\hit-monittor\backend\app\models\issue.py`
- Create: `D:\dev\hit-monittor\backend\app\models\pull_request.py`
- Create: `D:\dev\hit-monittor\backend\app\models\release.py`
- Create: `D:\dev\hit-monittor\backend\app\models\analysis_result.py`
- Create: `D:\dev\hit-monittor\backend\app\models\sync_job.py`
- Create: `D:\dev\hit-monittor\backend\app\models\app_setting.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_repository_api.py`

- [ ] **Step 1: 写一个仓库模型和设置默认值的失败测试**

```python
def test_default_settings_seed_intervals(session):
    settings = session.query(AppSetting).all()
    assert any(item.key == "sync_interval_minutes" for item in settings)
    assert any(item.key == "analysis_interval_minutes" for item in settings)
```

- [ ] **Step 2: 运行测试确认模型缺失**

Run: `uv run pytest backend/tests/test_repository_api.py::test_default_settings_seed_intervals -v`
Expected: FAIL with import or table errors

- [ ] **Step 3: 实现核心模型**

```python
class Repository(Base):
    __tablename__ = "repositories"
    id = mapped_column(Integer, primary_key=True)
    full_name = mapped_column(String(255), unique=True, nullable=False)
    enabled = mapped_column(Boolean, default=True, nullable=False)
```

```python
class AppSetting(Base):
    __tablename__ = "app_settings"
    key = mapped_column(String(100), primary_key=True)
    value = mapped_column(Text, nullable=False)
```

- [ ] **Step 4: 在数据库初始化时写入默认设置**

```python
DEFAULT_SETTINGS = {
    "sync_interval_minutes": "60",
    "analysis_interval_minutes": "240",
    "analysis_candidate_limit": "10",
}
```

- [ ] **Step 5: 运行模型相关测试**

Run: `uv run pytest backend/tests/test_repository_api.py::test_default_settings_seed_intervals -v`
Expected: PASS

- [ ] **Step 6: 提交模型层**

```bash
git add backend/app/models backend/tests/test_repository_api.py backend/app/core/database.py
git commit -m "feat: add persistence models and default settings"
```

### Task 4: 实现 GitHub 抓取客户端与归一化入库

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\services\github_client.py`
- Create: `D:\dev\hit-monittor\backend\app\services\ingestion.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_github_ingestion.py`

- [ ] **Step 1: 先写归一化入库测试**

```python
def test_ingestion_upserts_repository_issue_pr_release(httpx_mock, session):
    httpx_mock.add_response(json={"items": []})
    service = GitHubIngestionService(...)
    result = service.sync_repository("openai/openai-python")
    assert result.repository_full_name == "openai/openai-python"
```

- [ ] **Step 2: 运行测试确认服务不存在**

Run: `uv run pytest backend/tests/test_github_ingestion.py -v`
Expected: FAIL with import error for `GitHubIngestionService`

- [ ] **Step 3: 实现 GitHub API 客户端**

```python
class GitHubClient:
    async def fetch_repository_bundle(self, full_name: str) -> dict[str, Any]:
        return {
            "repository": await self._get(f"/repos/{full_name}"),
            "issues": await self._get(f"/repos/{full_name}/issues"),
            "pulls": await self._get(f"/repos/{full_name}/pulls"),
            "releases": await self._get(f"/repos/{full_name}/releases"),
        }
```

- [ ] **Step 4: 实现归一化和 upsert**

```python
def sync_repository(self, full_name: str) -> SyncSummary:
    bundle = self.client.fetch_repository_bundle(full_name)
    repository = self.repository_repo.upsert(bundle["repository"])
    self.issue_repo.upsert_many(repository.id, bundle["issues"])
    self.pull_request_repo.upsert_many(repository.id, bundle["pulls"])
    self.release_repo.upsert_many(repository.id, bundle["releases"])
    return SyncSummary(repository_full_name=repository.full_name)
```

- [ ] **Step 5: 运行抓取测试**

Run: `uv run pytest backend/tests/test_github_ingestion.py -v`
Expected: PASS

- [ ] **Step 6: 提交抓取与入库逻辑**

```bash
git add backend/app/services/github_client.py backend/app/services/ingestion.py backend/tests/test_github_ingestion.py
git commit -m "feat: add github ingestion pipeline"
```

### Task 5: 实现 OpenAI 兼容分析客户端与热点分析管线

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\services\analysis_client.py`
- Create: `D:\dev\hit-monittor\backend\app\services\analysis_pipeline.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_analysis_pipeline.py`

- [ ] **Step 1: 写一个分析结果结构化测试**

```python
def test_analysis_pipeline_saves_structured_summary(session, httpx_mock):
    httpx_mock.add_response(json={"choices": [{"message": {"content": "{\"summary\":\"test\"}"}}]})
    pipeline = AnalysisPipeline(...)
    result = pipeline.analyze_repository(repository_id=1)
    assert result.summary == "test"
```

- [ ] **Step 2: 运行测试确认分析管线不存在**

Run: `uv run pytest backend/tests/test_analysis_pipeline.py -v`
Expected: FAIL with import error for `AnalysisPipeline`

- [ ] **Step 3: 实现 OpenAI 兼容客户端**

```python
class AnalysisClient:
    def analyze(self, prompt: str) -> dict[str, Any]:
        payload = {
            "model": self.settings.openai_model,
            "messages": [{"role": "user", "content": prompt}],
        }
        return self.http.post(f"{self.settings.openai_base_url}/chat/completions", json=payload).json()
```

- [ ] **Step 4: 实现候选筛选和结构化解析**

```python
def build_repository_prompt(bundle: RepositoryBundle) -> str:
    return json.dumps(
        {
            "issues": bundle.hot_issues[:10],
            "pull_requests": bundle.hot_pull_requests[:10],
            "releases": bundle.latest_releases[:5],
        },
        ensure_ascii=False,
    )
```

- [ ] **Step 5: 将分析结果写入 `analysis_results`**

```python
analysis = AnalysisResult(
    object_type="repository",
    object_id=repository_id,
    analysis_type="summary",
    payload_json=result_json,
)
```

- [ ] **Step 6: 运行分析测试**

Run: `uv run pytest backend/tests/test_analysis_pipeline.py -v`
Expected: PASS

- [ ] **Step 7: 提交分析层**

```bash
git add backend/app/services/analysis_client.py backend/app/services/analysis_pipeline.py backend/tests/test_analysis_pipeline.py
git commit -m "feat: add ai analysis pipeline"
```

### Task 6: 实现可配置调度器与手动触发入口

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\scheduler\runner.py`
- Create: `D:\dev\hit-monittor\backend\app\services\sync_service.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_scheduler_runner.py`

- [ ] **Step 1: 写调度间隔读取测试**

```python
def test_scheduler_reads_intervals_from_app_settings(session):
    service = SchedulerRunner(...)
    plan = service.build_plan()
    assert plan.sync_interval_minutes == 60
    assert plan.analysis_interval_minutes == 240
```

- [ ] **Step 2: 运行测试确认调度器不存在**

Run: `uv run pytest backend/tests/test_scheduler_runner.py -v`
Expected: FAIL with import error for `SchedulerRunner`

- [ ] **Step 3: 实现调度计划读取**

```python
@dataclass
class SchedulerPlan:
    sync_interval_minutes: int
    analysis_interval_minutes: int
```

- [ ] **Step 4: 实现同步与分析任务执行器**

```python
def run_sync_cycle(self) -> None:
    for repository in self.repository_repo.list_enabled():
        self.sync_service.sync_repository(repository.full_name)
```

```python
def run_analysis_cycle(self) -> None:
    for repository in self.repository_repo.list_enabled():
        self.sync_service.analyze_repository(repository.id)
```

- [ ] **Step 5: 运行调度器测试**

Run: `uv run pytest backend/tests/test_scheduler_runner.py -v`
Expected: PASS

- [ ] **Step 6: 提交调度器**

```bash
git add backend/app/scheduler/runner.py backend/app/services/sync_service.py backend/tests/test_scheduler_runner.py
git commit -m "feat: add configurable scheduler"
```

### Task 7: 暴露后端 API

**Files:**
- Create: `D:\dev\hit-monittor\backend\app\schemas\dashboard.py`
- Create: `D:\dev\hit-monittor\backend\app\schemas\repository.py`
- Create: `D:\dev\hit-monittor\backend\app\schemas\settings.py`
- Create: `D:\dev\hit-monittor\backend\app\services\dashboard_service.py`
- Create: `D:\dev\hit-monittor\backend\app\services\settings_service.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\dashboard.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\repositories.py`
- Create: `D:\dev\hit-monittor\backend\app\api\routes\settings.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_repository_api.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_settings_api.py`

- [ ] **Step 1: 写仪表盘和设置 API 测试**

```python
def test_get_dashboard_returns_hot_sections(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    assert "hot_issues" in response.json()
```

```python
def test_patch_settings_updates_intervals(client):
    response = client.patch("/api/settings", json={"sync_interval_minutes": 30})
    assert response.status_code == 200
    assert response.json()["sync_interval_minutes"] == 30
```

- [ ] **Step 2: 运行 API 测试确认失败**

Run: `uv run pytest backend/tests/test_repository_api.py backend/tests/test_settings_api.py -v`
Expected: FAIL with `404` or router import errors

- [ ] **Step 3: 实现响应 schema**

```python
class DashboardResponse(BaseModel):
    hot_issues: list[HotItem]
    hot_pull_requests: list[HotItem]
    latest_releases: list[HotItem]
```

- [ ] **Step 4: 实现路由和服务层**

```python
router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.patch("")
def update_settings(payload: SettingsUpdate, session: SessionDep) -> SettingsResponse:
    return settings_service.update(session, payload)
```

- [ ] **Step 5: 将路由注册到 `app/main.py`**

```python
app.include_router(dashboard_router)
app.include_router(repositories_router)
app.include_router(settings_router)
```

- [ ] **Step 6: 运行 API 测试**

Run: `uv run pytest backend/tests/test_repository_api.py backend/tests/test_settings_api.py -v`
Expected: PASS

- [ ] **Step 7: 提交 API 层**

```bash
git add backend/app/api backend/app/schemas backend/app/services/dashboard_service.py backend/app/services/settings_service.py backend/tests/test_repository_api.py backend/tests/test_settings_api.py
git commit -m "feat: add dashboard repository and settings api"
```

### Task 8: 初始化前端应用壳和 API 客户端

**Files:**
- Create: `D:\dev\hit-monittor\frontend\vite.config.ts`
- Create: `D:\dev\hit-monittor\frontend\tsconfig.json`
- Create: `D:\dev\hit-monittor\frontend\src\main.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\App.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\lib\api.ts`
- Create: `D:\dev\hit-monittor\frontend\src\lib\types.ts`
- Create: `D:\dev\hit-monittor\frontend\src\components\layout\app-shell.tsx`
- Test: `D:\dev\hit-monittor\frontend\src\test\app-shell.test.tsx`

- [ ] **Step 1: 写应用壳测试**

```tsx
it("renders navigation links", () => {
  render(<AppShell />);
  expect(screen.getByText("总览")).toBeInTheDocument();
  expect(screen.getByText("配置")).toBeInTheDocument();
});
```

- [ ] **Step 2: 运行前端测试确认失败**

Run: `npm --prefix frontend test -- --run frontend/src/test/app-shell.test.tsx`
Expected: FAIL with component import error

- [ ] **Step 3: 初始化 Vite + React + TypeScript 入口**

```tsx
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- [ ] **Step 4: 实现 API 客户端和共享类型**

```ts
export async function getDashboard(): Promise<DashboardResponse> {
  const response = await fetch("/api/dashboard");
  return response.json();
}
```

- [ ] **Step 5: 实现应用壳导航**

```tsx
<nav>
  <a href="#/">总览</a>
  <a href="#/repositories">仓库</a>
  <a href="#/settings">配置</a>
</nav>
```

- [ ] **Step 6: 运行前端测试**

Run: `npm --prefix frontend test -- --run frontend/src/test/app-shell.test.tsx`
Expected: PASS

- [ ] **Step 7: 提交前端壳**

```bash
git add frontend/vite.config.ts frontend/tsconfig.json frontend/src
git commit -m "feat: add frontend app shell"
```

### Task 9: 实现总览页与仓库列表页

**Files:**
- Create: `D:\dev\hit-monittor\frontend\src\pages\dashboard-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\repositories-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\dashboard\summary-cards.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\repositories\repository-table.tsx`
- Test: `D:\dev\hit-monittor\frontend\src\test\dashboard-page.test.tsx`

- [ ] **Step 1: 先写总览页渲染测试**

```tsx
it("shows hot issue and release sections", async () => {
  render(<DashboardPage />);
  expect(await screen.findByText("热点 Issues")).toBeInTheDocument();
  expect(await screen.findByText("最新 Releases")).toBeInTheDocument();
});
```

- [ ] **Step 2: 运行测试确认页面不存在**

Run: `npm --prefix frontend test -- --run frontend/src/test/dashboard-page.test.tsx`
Expected: FAIL with page import error

- [ ] **Step 3: 实现总览页数据加载和摘要卡片**

```tsx
useEffect(() => {
  void getDashboard().then(setData);
}, []);
```

- [ ] **Step 4: 实现仓库列表表格和筛选输入**

```tsx
<input
  value={keyword}
  onChange={(event) => setKeyword(event.target.value)}
  placeholder="筛选仓库"
/>
```

- [ ] **Step 5: 运行页面测试**

Run: `npm --prefix frontend test -- --run frontend/src/test/dashboard-page.test.tsx`
Expected: PASS

- [ ] **Step 6: 提交总览和仓库列表**

```bash
git add frontend/src/pages frontend/src/components/dashboard frontend/src/components/repositories frontend/src/test/dashboard-page.test.tsx
git commit -m "feat: add dashboard and repository list pages"
```

### Task 10: 实现仓库详情页与配置页

**Files:**
- Create: `D:\dev\hit-monittor\frontend\src\pages\repository-detail-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\pages\settings-page.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\repository-detail\detail-sections.tsx`
- Create: `D:\dev\hit-monittor\frontend\src\components\settings\settings-form.tsx`
- Test: `D:\dev\hit-monittor\frontend\src\test\settings-form.test.tsx`

- [ ] **Step 1: 写配置表单测试**

```tsx
it("submits sync and analysis intervals", async () => {
  render(<SettingsForm initialValues={{ syncIntervalMinutes: 60, analysisIntervalMinutes: 240 }} />);
  await user.type(screen.getByLabelText("抓取间隔（分钟）"), "30");
  expect(screen.getByDisplayValue("30")).toBeInTheDocument();
});
```

- [ ] **Step 2: 运行测试确认组件不存在**

Run: `npm --prefix frontend test -- --run frontend/src/test/settings-form.test.tsx`
Expected: FAIL with component import error

- [ ] **Step 3: 实现仓库详情视图**

```tsx
<section>
  <h2>热点 PR</h2>
  <DetailSections items={data.hotPullRequests} />
</section>
```

- [ ] **Step 4: 实现配置表单与保存动作**

```tsx
await updateSettings({
  syncIntervalMinutes,
  analysisIntervalMinutes,
  openaiBaseUrl,
  openaiModel,
});
```

- [ ] **Step 5: 运行配置测试**

Run: `npm --prefix frontend test -- --run frontend/src/test/settings-form.test.tsx`
Expected: PASS

- [ ] **Step 6: 提交详情和配置页**

```bash
git add frontend/src/pages frontend/src/components/repository-detail frontend/src/components/settings frontend/src/test/settings-form.test.tsx
git commit -m "feat: add repository detail and settings pages"
```

### Task 11: 连通前后端、完善 README 并完成端到端验证

**Files:**
- Modify: `D:\dev\hit-monittor\README.md`
- Modify: `D:\dev\hit-monittor\frontend\src\App.tsx`
- Modify: `D:\dev\hit-monittor\backend\app\main.py`
- Modify: `D:\dev\hit-monittor\backend\app\core\config.py`
- Test: `D:\dev\hit-monittor\backend\tests\test_repository_api.py`
- Test: `D:\dev\hit-monittor\frontend\src\test\app-shell.test.tsx`

- [ ] **Step 1: 补一个启动联通性测试或手工验证清单**

```md
1. `uv run uvicorn app.main:app --reload`
2. `npm --prefix frontend run dev`
3. 打开首页确认展示热点卡片
```

- [ ] **Step 2: 运行完整后端测试套件**

Run: `uv run pytest backend/tests -v`
Expected: PASS

- [ ] **Step 3: 运行完整前端测试与构建**

Run: `npm --prefix frontend test`
Expected: PASS

Run: `npm --prefix frontend run build`
Expected: PASS with Vite production bundle output

- [ ] **Step 4: 补充 README 的开发启动、数据库目录、UTF-8 约束、环境变量说明**

```md
## 启动

### 后端
`uv run uvicorn app.main:app --reload`

### 前端
`npm run dev`
```

- [ ] **Step 5: 手工验证关键流**

Run:
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/dashboard
```
Expected:
- `/health` 返回 `{"status":"ok"}`
- `/api/dashboard` 返回包含 `hot_issues`、`hot_pull_requests`、`latest_releases`

- [ ] **Step 6: 提交集成验证与文档**

```bash
git add README.md frontend/src/App.tsx backend/app/main.py backend/app/core/config.py
git commit -m "docs: finalize local setup and integration flow"
```

## 执行顺序建议

1. 先完成 Task 1 到 Task 3，锁定编码规则、运行入口和数据模型。
2. 再完成 Task 4 到 Task 7，确保后端先可用且可测试。
3. 然后完成 Task 8 到 Task 10，逐步接上前端页面。
4. 最后执行 Task 11，补充文档并完成全链路验证。

## 风险与检查点

- GitHub API 限流风险：开发阶段应通过测试桩和本地假数据减少真实请求。
- OpenAI 兼容性风险：分析客户端需要显式处理 `base_url` 尾部斜杠和错误响应格式。
- Windows 路径风险：数据库路径应统一通过 `pathlib.Path` 处理，不要手写反斜杠拼接。
- 中文编码风险：每次新增带中文内容的文件后，优先用 UTF-8 显式读取验证。

## 完成定义

- 后端可在本机启动并返回健康检查、仪表盘、仓库、配置接口。
- 可配置抓取间隔和 AI 分析间隔可以保存到 SQLite，并被调度器读取。
- 前端可展示总览、仓库列表、仓库详情和配置页。
- OpenAI 兼容 `base_url` 可用于完成至少一轮分析调用。
- README 能指导在 Windows 本机完成从启动到验证的全流程。
