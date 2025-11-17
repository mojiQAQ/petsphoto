# AI Generation Capability

## Overview

AI 图像生成是 PetsPhoto 的核心功能，负责调用 Veo3 API 将用户上传的宠物照片转换为艺术风格的头像。本规范定义了生成任务的创建、管理、执行和结果处理流程。

## ADDED Requirements

### Requirement: Generation Job Creation

后端 SHALL 提供 API 端点用于创建 AI 图像生成任务。

#### Scenario: Create generation job with valid inputs

**GIVEN** 用户已上传图片并选择了风格
**WHEN** 前端发送 POST 请求到 `/api/generations` 包含 `source_image_id` 和 `style_id`
**THEN** 系统 SHALL:
- 验证 `source_image_id` 对应的图片存在且有效
- 验证 `style_id` 在支持的风格列表中
- 创建 `GenerationJob` 记录，状态为 `PENDING`
- 更新源图片的 `is_temp` 为 `False`
- 返回 201 Created 状态码和任务信息（包括任务 ID）
- 异步触发生成流程（后台任务）

响应示例：
```json
{
  "id": "gen_550e8400-e29b-41d4-a716-446655440000",
  "user_id": "guest",
  "source_image_id": "img_123",
  "style_id": "cartoon",
  "status": "pending",
  "created_at": "2025-01-16T10:35:00Z"
}
```

#### Scenario: Create job with non-existent image

**GIVEN** 用户尝试创建生成任务
**WHEN** `source_image_id` 不存在于数据库中
**THEN** 系统 SHALL:
- 拒绝请求
- 返回 404 Not Found 状态码
- 返回错误信息：`{"error": "源图片不存在"}`

#### Scenario: Create job with invalid style

**GIVEN** 用户尝试创建生成任务
**WHEN** `style_id` 不在预设风格列表中
**THEN** 系统 SHALL:
- 拒绝请求
- 返回 400 Bad Request 状态码
- 返回错误信息：`{"error": "不支持的风格ID"}`

### Requirement: Veo3 API Integration

后端 SHALL 集成 Veo3 API 进行图像生成。

#### Scenario: Call Veo3 API for image generation

**GIVEN** 生成任务已创建，状态为 `PENDING`
**WHEN** 后台任务开始处理
**THEN** 系统 SHALL:
- 更新任务状态为 `PROCESSING`
- 读取源图片文件
- 从 `GenerationStyle` 表获取风格的 `prompt_template`
- 构建完整的 Veo3 API 请求 payload
- 调用 Veo3 API 的图像生成端点
- 使用配置的 API key 进行认证

Veo3 API 请求示例：
```json
{
  "prompt": "cartoon style, vibrant colors, cute pet illustration, professional artwork",
  "image_url": "http://localhost:8000/uploads/images/source.jpg",
  "num_outputs": 1,
  "guidance_scale": 7.5,
  "num_inference_steps": 50
}
```

#### Scenario: Veo3 API returns successful result

**GIVEN** Veo3 API 调用已发送
**WHEN** API 返回成功响应（200 OK），包含生成的图片 URL
**THEN** 系统 SHALL:
- 下载生成的图片到本地存储
- 保存图片到 `backend/uploads/generated/` 目录
- 生成唯一文件名（UUID + .jpg）
- 更新 `GenerationJob` 记录：
  - `status = COMPLETED`
  - `result_image_url` = 本地图片的相对路径
  - `completed_at` = 当前时间戳
- 保留完整的 API 响应日志用于调试

#### Scenario: Veo3 API returns error

**GIVEN** Veo3 API 调用已发送
**WHEN** API 返回错误响应（4xx 或 5xx）
**THEN** 系统 SHALL:
- 更新 `GenerationJob` 状态为 `FAILED`
- 记录错误信息到 `error_message` 字段
- 记录详细的错误日志（状态码、响应体）
- 不进行自动重试（人工介入或后续功能）

错误响应示例：
```json
{
  "id": "gen_550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error_message": "Veo3 API 限流：请求过于频繁，请稍后重试"
}
```

#### Scenario: Veo3 API timeout

**GIVEN** Veo3 API 调用已发送
**WHEN** 超过 60 秒未收到响应
**THEN** 系统 SHALL:
- 取消 HTTP 请求
- 更新任务状态为 `FAILED`
- 记录错误信息："API 请求超时"
- 记录日志用于监控和告警

### Requirement: Generation Job Status Tracking

后端 SHALL 提供 API 端点用于查询生成任务状态。

#### Scenario: Query job status - still processing

**GIVEN** 生成任务正在进行中
**WHEN** 前端发送 GET 请求到 `/api/generations/{job_id}`
**THEN** 系统 SHALL:
- 返回 200 OK 状态码
- 返回任务当前状态和相关信息

响应示例：
```json
{
  "id": "gen_550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "created_at": "2025-01-16T10:35:00Z",
  "updated_at": "2025-01-16T10:35:10Z"
}
```

#### Scenario: Query job status - completed

**GIVEN** 生成任务已完成
**WHEN** 前端发送 GET 请求到 `/api/generations/{job_id}`
**THEN** 系统 SHALL:
- 返回 200 OK 状态码
- 返回任务信息，包括结果图片 URL

响应示例：
```json
{
  "id": "gen_550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result_image_url": "/uploads/generated/result_abc123.jpg",
  "created_at": "2025-01-16T10:35:00Z",
  "completed_at": "2025-01-16T10:35:45Z"
}
```

#### Scenario: Query job status - failed

**GIVEN** 生成任务失败
**WHEN** 前端发送 GET 请求到 `/api/generations/{job_id}`
**THEN** 系统 SHALL:
- 返回 200 OK 状态码
- 返回任务信息，包括错误消息

响应示例：
```json
{
  "id": "gen_550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error_message": "Veo3 API 限流：请求过于频繁，请稍后重试",
  "created_at": "2025-01-16T10:35:00Z",
  "updated_at": "2025-01-16T10:35:30Z"
}
```

#### Scenario: Query non-existent job

**GIVEN** 前端请求查询任务状态
**WHEN** `job_id` 不存在于数据库中
**THEN** 系统 SHALL:
- 返回 404 Not Found 状态码
- 返回错误信息：`{"error": "生成任务不存在"}`

### Requirement: Asynchronous Task Processing

系统 SHALL 使用异步机制处理生成任务，避免阻塞 HTTP 请求。

#### Scenario: Background task execution

**GIVEN** 生成任务已创建
**WHEN** 任务进入处理队列
**THEN** 系统 SHALL:
- 使用 FastAPI BackgroundTasks 或独立的异步函数处理
- 在后台执行 Veo3 API 调用
- 允许创建任务的 HTTP 请求立即返回（不等待生成完成）
- 确保任务失败时不影响 API 服务的稳定性

#### Scenario: Concurrent generation limits

**GIVEN** 多个生成任务同时提交
**WHEN** 系统处理任务队列
**THEN** 系统 SHALL:
- 最多同时处理 3 个生成任务（初期限制）
- 其他任务保持 `PENDING` 状态，排队等待
- 按照创建时间（FIFO）顺序处理任务

**Note**: 并发限制是临时的保护措施，后续可以引入 Celery 或 Redis Queue 进行更好的任务管理。

### Requirement: Generated Image Storage

后端 SHALL 管理生成的图片文件存储。

#### Scenario: Download and store generated image

**GIVEN** Veo3 API 返回生成的图片 URL
**WHEN** 下载图片
**THEN** 系统 SHALL:
- 使用 HTTP GET 请求下载图片
- 验证图片文件有效性（可以被 Pillow 读取）
- 生成唯一文件名（UUID + .jpg）
- 保存到 `backend/uploads/generated/` 目录
- 确保目录存在，不存在则自动创建

#### Scenario: Generated image file naming

**GIVEN** 需要保存生成的图片
**WHEN** 确定文件名
**THEN** 系统 SHALL:
- 格式：`result_{uuid}.jpg`
- 例如：`result_550e8400-e29b-41d4-a716-446655440000.jpg`
- 存储相对路径：`/uploads/generated/result_{uuid}.jpg`

#### Scenario: Serve generated images

**GIVEN** 生成的图片已保存
**WHEN** 前端请求访问图片 URL
**THEN** 系统 SHALL:
- 通过 FastAPI StaticFiles 提供访问
- URL 格式：`http://localhost:8000/uploads/generated/{filename}`
- 设置正确的 Content-Type (image/jpeg)
- 支持浏览器缓存

### Requirement: Guest User Handling

在没有认证系统的情况下，系统 SHALL 使用访客用户机制。

#### Scenario: Create job for guest user

**GIVEN** 应用运行在 MVP 模式（无认证）
**WHEN** 创建生成任务
**THEN** 系统 SHALL:
- 自动将 `user_id` 设置为固定的访客用户 ID（"guest"）
- 访客用户记录在数据库 seed data 中已创建
- 所有任务都关联到同一个访客用户

#### Scenario: Guest user in database

**GIVEN** 应用初始化
**WHEN** 执行 seed data 脚本
**THEN** 系统 SHALL:
- 创建一个 `User` 记录，`id = "guest"`
- `email = "guest@petsphoto.local"`
- `credits = 999999`（无限积分，用于测试）
- `is_active = True`

**Note**: 访客用户是临时方案，引入认证后将移除或修改这一机制。

### Requirement: Prompt Engineering

系统 SHALL 使用预设的 prompt template 构建高质量的生成提示词。

#### Scenario: Build prompt from style template

**GIVEN** 用户选择了某个预设风格（如 "cartoon"）
**WHEN** 调用 Veo3 API
**THEN** 系统 SHALL:
- 从 `GenerationStyle` 表读取该风格的 `prompt_template`
- 可选：添加通用的质量提升词（如 "high quality", "detailed"）
- 构建完整 prompt
- 示例：`"cartoon style, vibrant colors, cute pet illustration, high quality, professional artwork"`

#### Scenario: Prompt template from database

**GIVEN** 数据库中存在预设风格
**WHEN** 查询风格信息
**THEN** 系统 SHALL:
- 使用 seed data 中定义的 prompt templates
- 风格示例：
  - `cartoon`: "cartoon style, vibrant colors, cute pet illustration"
  - `oil_painting`: "oil painting style, artistic, classical portrait"
  - `watercolor`: "watercolor painting, soft colors, gentle brush strokes"
  - `pixel_art`: "pixel art, 8-bit style, retro gaming aesthetic"
  - `cyberpunk`: "cyberpunk style, neon lights, futuristic pet portrait"

## Technical Specifications

### Backend API Endpoints

#### Create Generation Job

```python
# File: backend/app/api/v1/endpoints/generations.py

@router.post("/", response_model=schemas.GenerationJobResponse, status_code=201)
async def create_generation_job(
    request: schemas.GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> schemas.GenerationJobResponse:
    """
    Create a new AI image generation job.

    - Requires: source_image_id, style_id
    - Returns: job_id, status
    - Triggers background task for processing
    """
    # Implementation...
```

#### Get Generation Job Status

```python
@router.get("/{job_id}", response_model=schemas.GenerationJobResponse)
async def get_generation_job(
    job_id: str,
    db: Session = Depends(get_db),
) -> schemas.GenerationJobResponse:
    """
    Get the status of a generation job.

    - Returns: job details including status and result_image_url (if completed)
    """
    # Implementation...
```

### Pydantic Schemas

```python
# File: backend/app/schemas/generation.py

class GenerationJobCreate(BaseModel):
    source_image_id: str
    style_id: str

class GenerationJobResponse(BaseModel):
    id: str
    user_id: str
    source_image_id: str
    style_id: str
    status: str  # "pending", "processing", "completed", "failed"
    result_image_url: Optional[str] = None
    error_message: Optional[str] = None
    credits_cost: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

### Veo3 API Client

```python
# File: backend/app/services/veo3_client.py

class Veo3Client:
    """Client for interacting with Veo3 API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.veo3.example.com/v1"  # 示例 URL
        self.timeout = 60  # 60 秒超时

    async def generate_image(
        self,
        prompt: str,
        source_image_url: str,
        **kwargs
    ) -> dict:
        """
        Call Veo3 API to generate an image.

        Args:
            prompt: Text prompt describing the desired style
            source_image_url: URL of the source pet image
            **kwargs: Additional API parameters

        Returns:
            API response dict containing generated image URL

        Raises:
            Veo3APIError: If API call fails
            TimeoutError: If request times out
        """
        # Implementation...
```

### Background Task Processing

```python
# File: backend/app/services/generation_service.py

async def process_generation_job(job_id: str, db: Session):
    """
    Background task to process a generation job.

    1. Update status to PROCESSING
    2. Fetch source image and style
    3. Call Veo3 API
    4. Download and store result
    5. Update job status to COMPLETED or FAILED
    """
    try:
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        job.status = GenerationStatus.PROCESSING
        db.commit()

        # Get source image and style
        source_image = db.query(UploadedImage).filter(...).first()
        style = db.query(GenerationStyle).filter(...).first()

        # Call Veo3 API
        veo3_client = Veo3Client(api_key=settings.VEO3_API_KEY)
        result = await veo3_client.generate_image(
            prompt=style.prompt_template,
            source_image_url=f"{settings.BASE_URL}{source_image.storage_path}"
        )

        # Download and save result
        result_path = await download_generated_image(result["image_url"])

        # Update job
        job.status = GenerationStatus.COMPLETED
        job.result_image_url = result_path
        job.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        job.status = GenerationStatus.FAILED
        job.error_message = str(e)
        db.commit()
        logger.error(f"Generation job {job_id} failed: {e}")
```

### Database Schema

使用已存在的 `GenerationJob` 模型（已在 `backend/app/models/image.py` 中定义）：

```python
class GenerationStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    source_image_id = Column(String, ForeignKey("uploaded_images.id"), nullable=False)
    style_id = Column(String, nullable=False)  # FK to GenerationStyle
    status = Column(SQLEnum(GenerationStatus), default=GenerationStatus.PENDING)
    result_image_url = Column(String, nullable=True)
    credits_cost = Column(Integer, default=1)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
```

### Environment Configuration

新增环境变量：

```bash
# Veo3 API Configuration
VEO3_API_KEY=your-api-key-here
VEO3_API_URL=https://api.veo3.example.com/v1
VEO3_TIMEOUT=60

# Base URL for constructing image URLs
BASE_URL=http://localhost:8000
```

## Testing Requirements

### Unit Tests

1. **Veo3 Client Tests**:
   - Mock API 成功响应
   - Mock API 错误响应
   - 超时处理测试

2. **Generation Service Tests**:
   - 任务状态转换逻辑
   - Prompt 构建逻辑
   - 错误处理逻辑

### Integration Tests

1. **API Endpoint Tests**:
   - POST /api/generations - 各种场景
   - GET /api/generations/{id} - 各种状态

2. **Database Tests**:
   - 任务创建和更新
   - 状态查询
   - 关联关系验证

### E2E Tests

1. 完整生成流程：创建任务 → 处理 → 查询状态 → 获取结果
2. 错误恢复：API 失败 → 任务标记为失败 → 用户收到错误提示

### Mock Veo3 API (开发环境)

创建一个 Mock Veo3 API 服务用于本地测试，避免实际调用付费 API：

```python
# File: backend/app/services/mock_veo3.py

class MockVeo3Client(Veo3Client):
    """Mock Veo3 client for testing without real API calls."""

    async def generate_image(self, prompt: str, source_image_url: str, **kwargs) -> dict:
        # 模拟 5-10 秒的处理时间
        await asyncio.sleep(random.randint(5, 10))

        # 返回一个示例图片 URL（可以是预先准备的测试图片）
        return {
            "image_url": "http://localhost:8000/mock/result.jpg",
            "seed": 12345,
            "model_version": "veo3-mock-v1"
        }
```

## Performance Considerations

- **并发控制**：初期限制为 3 个并发任务，避免 API 限流
- **超时设置**：60 秒 HTTP 超时，确保不会无限等待
- **资源清理**：定期清理失败任务的临时文件
- **缓存策略**：生成结果图片设置浏览器缓存，减少重复下载

## Security Considerations

- **API Key 保护**：Veo3 API key 仅在后端使用，不暴露给前端
- **输入验证**：验证所有输入参数，防止 SQL 注入和路径遍历
- **速率限制**：限制每个 IP 的任务创建频率（如每分钟 10 次）
- **文件验证**：验证下载的图片文件完整性和格式

## Error Messages

用户友好的错误信息：

- `"源图片不存在，请重新上传"`
- `"不支持的风格，请选择预设风格之一"`
- `"图像生成服务暂时不可用，请稍后重试"`
- `"生成失败，请检查上传的图片质量"`
- `"请求过于频繁，请稍后再试"`
