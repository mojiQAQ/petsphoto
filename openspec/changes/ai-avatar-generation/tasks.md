# Implementation Tasks

本文档列出了实现 AI 头像生成功能的所有开发任务，按照逻辑顺序和依赖关系组织。

## 任务组织原则

- ✅ 每个任务应该是独立可验证的
- ✅ 任务按照依赖顺序排列
- ✅ 标注任务的优先级和预估工时
- ✅ 明确任务的验收标准

## Legend

- **Priority**: P0 (关键路径) | P1 (重要) | P2 (可选优化)
- **Estimate**: 小时数（单人开发）
- **Dependencies**: 依赖的任务编号

---

## Phase 1: Backend Foundation (后端基础)

### Task 1.1: Create Guest User in Seed Data
**Priority**: P0
**Estimate**: 0.5h
**Dependencies**: None
**Spec**: `ai-generation`

**Description**:
在数据库 seed data 中创建一个固定的访客用户，用于 MVP 阶段的无认证开发。

**Acceptance Criteria**:
- [ ] 在 `backend/app/core/seed_data.py` 中添加创建 guest 用户的逻辑
- [ ] Guest user ID 固定为 `"guest"`
- [ ] Email 设置为 `"guest@petsphoto.local"`
- [ ] Credits 设置为 `999999`（无限积分用于测试）
- [ ] `is_active = True`
- [ ] 运行 seed data 脚本后，数据库中存在该用户
- [ ] 编写验证测试，查询用户是否创建成功

**Implementation Notes**:
```python
def create_guest_user(db: Session):
    guest = User(
        id="guest",
        email="guest@petsphoto.local",
        credits=999999,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(guest)
    db.commit()
```

---

### Task 1.2: Backend Upload Directory Setup
**Priority**: P0
**Estimate**: 0.5h
**Dependencies**: None
**Spec**: `image-upload`

**Description**:
配置后端的文件上传目录和静态文件服务。

**Acceptance Criteria**:
- [ ] 创建目录结构：`backend/uploads/images/` 和 `backend/uploads/generated/`
- [ ] 在 `backend/app/main.py` 中配置 FastAPI StaticFiles 中间件
- [ ] 挂载路径：`/uploads` → `backend/uploads/`
- [ ] 在应用启动时自动创建目录（如果不存在）
- [ ] 测试静态文件访问：访问 `http://localhost:8000/uploads/images/test.jpg` 返回文件

**Implementation Notes**:
```python
from fastapi.staticfiles import StaticFiles
import os

# Ensure upload directories exist
os.makedirs("uploads/images", exist_ok=True)
os.makedirs("uploads/generated", exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
```

---

### Task 1.3: Image Upload API Endpoint
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 1.2
**Spec**: `image-upload`

**Description**:
实现图片上传 API 端点，支持文件接收、验证和存储。

**Acceptance Criteria**:
- [ ] 创建 `backend/app/api/v1/endpoints/images.py`
- [ ] 实现 `POST /api/v1/images/upload` 端点
- [ ] 验证文件类型（MIME type: `image/jpeg`, `image/png`, `image/webp`）
- [ ] 验证文件大小（≤ 10MB）
- [ ] 使用 Pillow 提取图片元数据（宽度、高度）
- [ ] 生成 UUID 文件名并保存到 `uploads/images/`
- [ ] 创建 `UploadedImage` 数据库记录
- [ ] 返回 201 Created 和图片信息（JSON）
- [ ] 错误处理：400 (无效类型)、413 (文件过大)、500 (服务器错误)
- [ ] 编写单元测试覆盖各种场景

**Implementation Notes**:
- 使用 `FastAPI.UploadFile` 接收文件
- 使用 `aiofiles` 进行异步文件写入（可选优化）
- Pillow: `Image.open(file).size` 获取尺寸

---

### Task 1.4: Generation Styles API Endpoint
**Priority**: P0
**Estimate**: 1h
**Dependencies**: None
**Spec**: `generation-ui`

**Description**:
实现获取生成风格列表的 API 端点。

**Acceptance Criteria**:
- [ ] 创建 `backend/app/api/v1/endpoints/styles.py`
- [ ] 实现 `GET /api/v1/styles` 端点
- [ ] 从数据库查询所有 `GenerationStyle` 记录
- [ ] 返回 JSON 数组，包含 id, name, description, prompt_template
- [ ] 编写测试验证返回 5 条预设风格数据

**Implementation Notes**:
```python
@router.get("/", response_model=List[schemas.GenerationStyleResponse])
def get_styles(db: Session = Depends(get_db)):
    styles = db.query(GenerationStyle).all()
    return styles
```

---

### Task 1.5: Veo3 API Client Implementation
**Priority**: P0
**Estimate**: 3h
**Dependencies**: None
**Spec**: `ai-generation`

**Description**:
实现 Veo3 API 客户端封装，用于调用图像生成服务。

**Acceptance Criteria**:
- [ ] 创建 `backend/app/services/veo3_client.py`
- [ ] 实现 `Veo3Client` 类，包含 `generate_image()` 方法
- [ ] 使用 `httpx` 或 `aiohttp` 进行异步 HTTP 请求
- [ ] 读取环境变量 `VEO3_API_KEY` 和 `VEO3_API_URL`
- [ ] 设置 60 秒请求超时
- [ ] 错误处理：捕获 HTTP 错误、超时、网络错误
- [ ] 创建 `MockVeo3Client` 用于本地测试（返回示例图片）
- [ ] 编写单元测试（Mock HTTP 响应）

**Implementation Notes**:
- 根据 Veo3 实际 API 文档调整请求格式
- 如果 Veo3 API 细节未知，先实现 Mock 版本

---

### Task 1.6: Generation Job Creation API
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 1.3, Task 1.4
**Spec**: `ai-generation`

**Description**:
实现创建生成任务的 API 端点。

**Acceptance Criteria**:
- [ ] 创建 `backend/app/api/v1/endpoints/generations.py`
- [ ] 实现 `POST /api/v1/generations` 端点
- [ ] 接收 `source_image_id` 和 `style_id`
- [ ] 验证图片存在（查询 `UploadedImage` 表）
- [ ] 验证风格存在（查询 `GenerationStyle` 表）
- [ ] 创建 `GenerationJob` 记录，状态为 `PENDING`
- [ ] 设置 `user_id = "guest"`
- [ ] 更新源图片的 `is_temp = False`
- [ ] 触发后台任务（使用 `BackgroundTasks`）
- [ ] 返回 201 Created 和任务 ID
- [ ] 错误处理：404 (图片不存在)、400 (风格无效)
- [ ] 编写集成测试

---

### Task 1.7: Background Generation Task Processor
**Priority**: P0
**Estimate**: 3h
**Dependencies**: Task 1.5, Task 1.6
**Spec**: `ai-generation`

**Description**:
实现后台任务处理器，执行 AI 图像生成流程。

**Acceptance Criteria**:
- [ ] 创建 `backend/app/services/generation_service.py`
- [ ] 实现 `process_generation_job(job_id)` 异步函数
- [ ] 更新任务状态为 `PROCESSING`
- [ ] 读取源图片和风格信息
- [ ] 调用 `Veo3Client.generate_image()`
- [ ] 下载生成的图片到 `uploads/generated/`
- [ ] 生成唯一文件名（`result_{uuid}.jpg`）
- [ ] 更新任务状态为 `COMPLETED`，保存 `result_image_url`
- [ ] 异常处理：捕获错误并更新状态为 `FAILED`，记录 `error_message`
- [ ] 记录详细日志（info, error）
- [ ] 编写单元测试（Mock Veo3 API）

**Implementation Notes**:
- 使用 `httpx.AsyncClient` 下载图片
- 使用 `aiofiles` 异步写入文件

---

### Task 1.8: Generation Job Status API
**Priority**: P0
**Estimate**: 1h
**Dependencies**: Task 1.6
**Spec**: `ai-generation`

**Description**:
实现查询生成任务状态的 API 端点。

**Acceptance Criteria**:
- [ ] 实现 `GET /api/v1/generations/{job_id}` 端点
- [ ] 查询数据库获取任务信息
- [ ] 返回任务状态、创建时间、完成时间、结果 URL、错误信息等
- [ ] 错误处理：404 (任务不存在)
- [ ] 编写测试覆盖各种任务状态（pending, processing, completed, failed）

---

### Task 1.9: API Rate Limiting (Optional)
**Priority**: P2
**Estimate**: 1h
**Dependencies**: Task 1.6
**Spec**: `ai-generation`

**Description**:
添加 API 请求频率限制，防止滥用。

**Acceptance Criteria**:
- [ ] 使用 `slowapi` 或 FastAPI 中间件实现 rate limiting
- [ ] 限制：每 IP 每分钟最多 10 次生成请求
- [ ] 超过限制返回 429 Too Many Requests
- [ ] 返回友好的错误信息

**Implementation Notes**:
- 可以在后续优化时实现
- 开发环境可以禁用

---

## Phase 2: Frontend UI Components (前端 UI 组件)

### Task 2.1: Install React Router
**Priority**: P0
**Estimate**: 0.5h
**Dependencies**: None
**Spec**: `generation-ui`

**Description**:
安装并配置 React Router 用于页面路由。

**Acceptance Criteria**:
- [ ] 安装 `react-router-dom` (v6)
- [ ] 在 `App.tsx` 中配置 `BrowserRouter` 和 `Routes`
- [ ] 添加路由：`/` (HomePage) 和 `/generator` (GeneratorPage)
- [ ] 测试路由导航正常工作

---

### Task 2.2: ImageUploader Component
**Priority**: P0
**Estimate**: 3h
**Dependencies**: None
**Spec**: `image-upload`

**Description**:
实现图片上传组件，支持拖拽和点击上传。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/image-upload/ImageUploader.tsx`
- [ ] 使用 HTML5 `<input type="file">` 或 `react-dropzone` 库
- [ ] 支持拖拽上传和点击选择
- [ ] 客户端验证：文件类型（jpg/png/webp）、大小（≤ 10MB）
- [ ] 显示上传进度（可选：使用 axios 的 onUploadProgress）
- [ ] 调用 `/api/v1/images/upload` API
- [ ] 上传成功后调用 `onUploadSuccess(image)` 回调
- [ ] 上传失败显示错误（调用 `onUploadError(error)` 回调）
- [ ] 显示拖拽悬停状态（边框高亮）
- [ ] 编写组件测试

**Implementation Notes**:
- 使用 FormData 构建 multipart/form-data 请求
- 可以使用 `react-dropzone` 简化拖拽逻辑

---

### Task 2.3: ImagePreview Component
**Priority**: P0
**Estimate**: 1.5h
**Dependencies**: Task 2.2
**Spec**: `image-upload`

**Description**:
实现图片预览组件，显示已上传的图片。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/image-upload/ImagePreview.tsx`
- [ ] 显示图片缩略图（最大宽度 400px）
- [ ] 显示文件名和文件大小（格式化为 MB/KB）
- [ ] 提供"清除"按钮（调用 `onClear()` 回调）
- [ ] 提供"重新上传"按钮（调用 `onReupload()` 回调）
- [ ] 使用 shadcn/ui Card 组件包裹
- [ ] 响应式设计（移动端友好）
- [ ] 编写组件测试

---

### Task 2.4: StyleSelector Component
**Priority**: P0
**Estimate**: 2h
**Dependencies**: None
**Spec**: `generation-ui`

**Description**:
实现风格选择器组件，展示预设风格。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/generator/StyleSelector.tsx`
- [ ] 调用 `/api/v1/styles` API 获取风格列表
- [ ] 使用 TanStack Query (React Query) 管理 API 状态
- [ ] 渲染风格卡片网格（桌面 2-3 列，移动 1 列）
- [ ] 每个风格卡片显示名称和描述（可选）
- [ ] 支持单选（点击选中，再次点击不取消）
- [ ] 选中状态有视觉反馈（边框加粗、checkmark 图标）
- [ ] 加载状态显示骨架屏（Skeleton）
- [ ] 错误状态显示提示和重试按钮
- [ ] 编写组件测试

---

### Task 2.5: StyleCard Component
**Priority**: P0
**Estimate**: 1h
**Dependencies**: Task 2.4
**Spec**: `generation-ui`

**Description**:
实现单个风格卡片组件。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/generator/StyleCard.tsx`
- [ ] 使用 shadcn/ui Card 组件
- [ ] 显示风格名称（CardTitle）
- [ ] 可选：显示风格示例图或图标
- [ ] 选中状态：边框变色（primary color）+ checkmark 图标
- [ ] 悬停效果（hover）
- [ ] 响应式设计
- [ ] 编写组件测试

---

### Task 2.6: GeneratorPage Layout
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 2.2, Task 2.3, Task 2.4
**Spec**: `generation-ui`

**Description**:
实现生成器页面的整体布局。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/pages/GeneratorPage.tsx`
- [ ] 两列布局（桌面）：左侧上传区，右侧风格选择
- [ ] 单列布局（移动端）：上传区 → 风格选择器 → 生成按钮
- [ ] 集成 `ImageUploader`, `ImagePreview`, `StyleSelector` 组件
- [ ] 管理状态：`uploadedImage`, `selectedStyle`
- [ ] 底部"生成"按钮，根据状态启用/禁用
- [ ] 使用 Container 组件包裹，保持一致的页面边距
- [ ] 响应式设计，测试桌面和移动端布局
- [ ] 编写页面测试

---

### Task 2.7: Generation Button Logic
**Priority**: P0
**Estimate**: 1h
**Dependencies**: Task 2.6
**Spec**: `generation-ui`

**Description**:
实现生成按钮的交互逻辑。

**Acceptance Criteria**:
- [ ] 按钮仅在图片已上传且风格已选择时启用
- [ ] 点击按钮触发 `handleGenerate()` 函数
- [ ] 调用 `POST /api/v1/generations` API
- [ ] 发送请求期间按钮禁用，显示 "生成中..." 和 spinner
- [ ] 成功创建任务后保存任务 ID，开始轮询
- [ ] 失败时显示 Toast 错误提示，恢复按钮状态
- [ ] 编写交互测试

---

### Task 2.8: Generation Polling Hook
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 2.7
**Spec**: `generation-ui`

**Description**:
实现轮询 Hook，监控生成任务状态。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/hooks/useGenerationPolling.ts`
- [ ] 使用 TanStack Query 的 `refetchInterval` 功能
- [ ] 每 2-3 秒查询一次任务状态（`GET /api/v1/generations/{id}`）
- [ ] 当状态为 `completed` 或 `failed` 时停止轮询
- [ ] 返回任务对象和加载状态
- [ ] 超时保护：90 秒后停止轮询并提示
- [ ] 编写 Hook 测试

**Implementation Notes**:
```typescript
export function useGenerationPolling(jobId: string | null) {
  return useQuery({
    queryKey: ["generation-job", jobId],
    queryFn: () => getGenerationJob(jobId!),
    enabled: !!jobId,
    refetchInterval: (data) => {
      if (data?.status === "completed" || data?.status === "failed") {
        return false;
      }
      return 3000; // 3 seconds
    },
  });
}
```

---

### Task 2.9: Loading State UI
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 2.7, Task 2.8
**Spec**: `generation-ui`

**Description**:
实现生成过程中的加载状态 UI。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/generator/GeneratingOverlay.tsx`
- [ ] 全屏或模态的加载界面（Dialog）
- [ ] 显示加载动画（spinner 或自定义动画）
- [ ] 显示提示文字："AI 正在生成您的宠物头像，请稍候..."
- [ ] 可选：显示进度条（基于轮询次数估算）
- [ ] 阻止用户关闭或离开（带确认对话框）
- [ ] 编写组件测试

---

### Task 2.10: ResultDialog Component
**Priority**: P0
**Estimate**: 2h
**Dependencies**: Task 2.8
**Spec**: `generation-ui`

**Description**:
实现结果展示对话框。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/components/generator/ResultDialog.tsx`
- [ ] 使用 shadcn/ui Dialog 组件
- [ ] 显示生成的图片（大图预览）
- [ ] 图片加载时显示骨架屏（Skeleton）
- [ ] 提供"下载"按钮（触发文件下载）
- [ ] 提供"重新生成"按钮（调用 `onRegenerate()` 回调）
- [ ] 提供"关闭"按钮（调用 `onClose()` 回调）
- [ ] 响应式设计（移动端友好）
- [ ] 编写组件测试

---

### Task 2.11: Download Functionality
**Priority**: P0
**Estimate**: 1h
**Dependencies**: Task 2.10
**Spec**: `generation-ui`

**Description**:
实现下载生成图片的功能。

**Acceptance Criteria**:
- [ ] 点击"下载"按钮触发文件下载
- [ ] 使用 `<a>` 标签的 `download` 属性
- [ ] 文件名格式：`petsphoto_{style_id}_{timestamp}.jpg`
- [ ] 示例：`petsphoto_cartoon_20250116_103045.jpg`
- [ ] 可选：显示 Toast 提示 "下载已开始"
- [ ] 测试下载功能在不同浏览器中正常工作

**Implementation Notes**:
```typescript
const handleDownload = () => {
  const link = document.createElement("a");
  link.href = imageUrl;
  link.download = `petsphoto_${styleId}_${Date.now()}.jpg`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
```

---

### Task 2.12: Error Handling UI
**Priority**: P0
**Estimate**: 1.5h
**Dependencies**: Task 2.7, Task 2.8
**Spec**: `generation-ui`

**Description**:
实现各种错误场景的 UI 处理。

**Acceptance Criteria**:
- [ ] 使用 shadcn/ui Toast 组件显示错误
- [ ] 处理场景：
  - 上传失败：显示错误信息
  - 创建任务失败：显示错误信息
  - 任务执行失败：显示 `error_message`
  - 网络错误：显示友好提示
- [ ] 错误后允许用户重试
- [ ] 编写错误场景测试

---

### Task 2.13: API Service Layer
**Priority**: P0
**Estimate**: 1.5h
**Dependencies**: None
**Spec**: `generation-ui`

**Description**:
创建前端 API 服务层，封装所有 API 调用。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/services/api.ts`
- [ ] 实现函数：
  - `uploadImage(file): Promise<UploadedImage>`
  - `fetchStyles(): Promise<GenerationStyle[]>`
  - `createGenerationJob(imageId, styleId): Promise<GenerationJob>`
  - `getGenerationJob(jobId): Promise<GenerationJob>`
- [ ] 使用 `fetch` 或 `axios`
- [ ] 统一错误处理
- [ ] 从环境变量读取 `VITE_API_BASE_URL`
- [ ] 编写 API 函数测试（Mock fetch）

---

### Task 2.14: TypeScript Types
**Priority**: P0
**Estimate**: 0.5h
**Dependencies**: None
**Spec**: `generation-ui`, `image-upload`, `ai-generation`

**Description**:
定义前端使用的 TypeScript 类型。

**Acceptance Criteria**:
- [ ] 创建 `frontend/src/types/`
- [ ] 定义接口：
  - `UploadedImage`
  - `GenerationStyle`
  - `GenerationJob`
- [ ] 导出所有类型
- [ ] 确保类型与后端 API 响应匹配

---

## Phase 3: Integration & Testing (集成与测试)

### Task 3.1: Frontend-Backend Integration
**Priority**: P0
**Estimate**: 2h
**Dependencies**: 所有前后端任务
**Spec**: All specs

**Description**:
集成前后端，确保端到端流程正常工作。

**Acceptance Criteria**:
- [ ] 配置 CORS（后端允许前端域名）
- [ ] 配置前端 API base URL（`.env.local`）
- [ ] 同时启动前后端服务
- [ ] 测试完整流程：上传 → 选择风格 → 生成 → 查看结果 → 下载
- [ ] 修复集成过程中发现的问题
- [ ] 验证网络请求（使用浏览器 DevTools）

---

### Task 3.2: Backend Unit Tests
**Priority**: P1
**Estimate**: 3h
**Dependencies**: 所有后端任务
**Spec**: `image-upload`, `ai-generation`

**Description**:
编写后端单元测试。

**Acceptance Criteria**:
- [ ] 测试图片上传端点（有效/无效文件）
- [ ] 测试生成任务创建（有效/无效输入）
- [ ] 测试任务状态查询
- [ ] 测试 Veo3Client（Mock HTTP 请求）
- [ ] 测试 generation_service 逻辑
- [ ] 测试覆盖率 > 70%
- [ ] 使用 pytest 运行所有测试

---

### Task 3.3: Frontend Component Tests
**Priority**: P1
**Estimate**: 3h
**Dependencies**: 所有前端任务
**Spec**: `generation-ui`, `image-upload`

**Description**:
编写前端组件测试。

**Acceptance Criteria**:
- [ ] 使用 Vitest + React Testing Library
- [ ] 测试 ImageUploader（文件选择、拖拽、验证）
- [ ] 测试 StyleSelector（渲染、选择交互）
- [ ] 测试 GeneratorPage（按钮状态、交互流程）
- [ ] 测试 ResultDialog（显示、下载、重新生成）
- [ ] Mock API 调用
- [ ] 测试覆盖率 > 70%

---

### Task 3.4: E2E Test
**Priority**: P1
**Estimate**: 2h
**Dependencies**: Task 3.1
**Spec**: All specs

**Description**:
编写端到端测试，验证完整用户流程。

**Acceptance Criteria**:
- [ ] 使用 Playwright 或 Cypress
- [ ] 测试场景：
  1. 访问生成器页面
  2. 上传图片
  3. 选择风格
  4. 点击生成
  5. 等待生成完成
  6. 查看结果
  7. 下载图片
- [ ] 测试错误场景（上传无效文件、API 失败）
- [ ] 测试响应式布局（桌面 + 移动端）

---

### Task 3.5: Manual Testing & Bug Fixes
**Priority**: P0
**Estimate**: 3h
**Dependencies**: Task 3.1
**Spec**: All specs

**Description**:
手动测试所有功能，修复发现的 bug。

**Acceptance Criteria**:
- [ ] 在不同浏览器测试（Chrome, Firefox, Safari）
- [ ] 在不同设备测试（桌面、平板、手机）
- [ ] 测试边界情况（最大文件、网络慢、并发请求）
- [ ] 测试所有错误场景
- [ ] 修复发现的所有 P0/P1 bug
- [ ] 创建 bug 修复的 checklist

---

## Phase 4: Polish & Documentation (优化与文档)

### Task 4.1: UI/UX Polish
**Priority**: P1
**Estimate**: 2h
**Dependencies**: Task 3.5
**Spec**: `generation-ui`

**Description**:
优化 UI 细节和用户体验。

**Acceptance Criteria**:
- [ ] 检查所有动画和过渡（smooth transitions）
- [ ] 优化加载状态（骨架屏、spinner 位置）
- [ ] 检查颜色对比度（符合 WCAG 2.1 AA）
- [ ] 优化移动端布局和间距
- [ ] 添加 hover 效果和视觉反馈
- [ ] 检查所有文字拼写和语法

---

### Task 4.2: Performance Optimization
**Priority**: P2
**Estimate**: 2h
**Dependencies**: Task 3.1
**Spec**: All specs

**Description**:
优化前后端性能。

**Acceptance Criteria**:
- [ ] 前端代码分割（lazy load GeneratorPage）
- [ ] 图片懒加载
- [ ] 优化 API 请求（减少不必要的请求）
- [ ] 后端添加响应压缩（gzip）
- [ ] 检查首屏加载时间 < 3 秒
- [ ] 使用 Lighthouse 检查性能分数

---

### Task 4.3: Error Logging & Monitoring
**Priority**: P2
**Estimate**: 1.5h
**Dependencies**: Task 3.1
**Spec**: `ai-generation`

**Description**:
添加错误日志和监控。

**Acceptance Criteria**:
- [ ] 后端使用 Python logging 记录所有错误
- [ ] 记录 Veo3 API 调用失败的详细信息
- [ ] 前端使用 console.error 记录错误
- [ ] 可选：集成 Sentry（错误跟踪服务）
- [ ] 创建日志查看和分析的文档

---

### Task 4.4: Environment Configuration
**Priority**: P0
**Estimate**: 1h
**Dependencies**: None
**Spec**: All specs

**Description**:
完善环境配置和文档。

**Acceptance Criteria**:
- [ ] 更新 `backend/.env.example` 包含所有必需变量
- [ ] 更新 `frontend/.env.example` 包含所有必需变量
- [ ] 验证环境变量说明清晰
- [ ] 创建开发环境设置指南
- [ ] 文档化 Veo3 API key 的申请流程

---

### Task 4.5: README & Documentation
**Priority**: P1
**Estimate**: 2h
**Dependencies**: All tasks
**Spec**: All specs

**Description**:
更新项目文档和 README。

**Acceptance Criteria**:
- [ ] 更新根目录 README.md
- [ ] 添加功能说明（AI 头像生成）
- [ ] 添加运行步骤（前后端启动命令）
- [ ] 添加测试步骤
- [ ] 添加已知问题和限制（访客用户、无认证）
- [ ] 添加后续计划（认证、支付）
- [ ] 添加截图或 GIF 演示

---

## Summary

**总计任务数**: 33 个
**预估总工时**: 53.5 小时（单人开发）
**关键路径 (P0) 任务**: 25 个
**重要 (P1) 任务**: 7 个
**可选优化 (P2) 任务**: 1 个

**里程碑**:
1. **Backend Foundation 完成** (9 tasks, ~14.5h): 后端 API 和生成逻辑就绪
2. **Frontend UI 完成** (14 tasks, ~21.5h): 前端界面和交互完成
3. **Integration & Testing 完成** (5 tasks, ~13h): 集成测试通过
4. **Polish & Documentation 完成** (5 tasks, ~8.5h): 优化和文档就绪

**依赖关系图**:
```
Phase 1 (Backend) → Phase 2 (Frontend) → Phase 3 (Integration) → Phase 4 (Polish)
     ↓                    ↓                      ↓                      ↓
  1.1-1.9            2.1-2.14                3.1-3.5                4.1-4.5
```

**并行化机会**:
- Phase 1 和 Phase 2 的部分任务可以并行开发
- 例如：前端 UI 组件可以在后端 API 完成之前开发（使用 Mock 数据）
- 测试任务可以在开发完成后并行进行

**风险**:
- Veo3 API 集成可能遇到未知问题（预留额外缓冲时间）
- 轮询机制需要仔细测试，避免内存泄漏
- 性能优化可能需要根据实际情况调整
