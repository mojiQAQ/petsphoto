# Image Upload Capability

## Overview

图片上传是 AI 头像生成流程的第一步，允许用户上传宠物照片作为生成的源图片。本规范定义了前后端的图片上传功能，包括文件选择、验证、预览、上传和存储。

## ADDED Requirements

### Requirement: Frontend Upload Component

前端 SHALL 提供一个拖拽上传组件，支持点击选择和拖放两种上传方式。

#### Scenario: User drags an image file

**GIVEN** 用户在生成器页面
**WHEN** 用户拖拽一个有效的图片文件到上传区域
**THEN** 系统 SHALL:
- 显示拖拽悬停状态（边框高亮或背景变化）
- 接受文件并触发上传流程
- 显示上传进度指示

#### Scenario: User clicks to select an image

**GIVEN** 用户在生成器页面
**WHEN** 用户点击上传区域
**THEN** 系统 SHALL:
- 打开文件选择对话框
- 过滤只显示图片文件（JPG, PNG, WEBP）
- 接受用户选择的文件并触发上传流程

#### Scenario: User uploads invalid file type

**GIVEN** 用户尝试上传文件
**WHEN** 文件类型不是 JPG、PNG 或 WEBP
**THEN** 系统 SHALL:
- 拒绝上传
- 显示错误提示 "仅支持 JPG、PNG 和 WEBP 格式"
- 保持上传区域空白状态

#### Scenario: User uploads oversized file

**GIVEN** 用户尝试上传图片文件
**WHEN** 文件大小超过 10MB
**THEN** 系统 SHALL:
- 拒绝上传
- 显示错误提示 "图片大小不能超过 10MB"
- 保持上传区域空白状态

### Requirement: Image Preview

前端 SHALL 在上传成功后显示图片预览，并提供清除和重新上传功能。

#### Scenario: Image uploaded successfully

**GIVEN** 用户上传了有效的图片文件
**WHEN** 上传完成
**THEN** 系统 SHALL:
- 显示图片缩略图预览（最大宽度 400px，保持宽高比）
- 显示图片文件名
- 显示图片文件大小（格式化为 MB/KB）
- 显示"清除"和"重新上传"按钮

#### Scenario: User clears uploaded image

**GIVEN** 已上传图片正在预览中
**WHEN** 用户点击"清除"按钮
**THEN** 系统 SHALL:
- 移除图片预览
- 清空上传状态
- 恢复到初始上传区域状态
- 禁用"生成"按钮（如果之前启用）

#### Scenario: User re-uploads a different image

**GIVEN** 已上传图片正在预览中
**WHEN** 用户点击"重新上传"或拖拽新图片
**THEN** 系统 SHALL:
- 替换当前图片
- 显示新图片的预览
- 更新文件信息（名称、大小）

### Requirement: Backend Upload Endpoint

后端 SHALL 提供一个 RESTful API 端点用于接收和存储上传的图片。

#### Scenario: Valid image upload request

**GIVEN** 前端发送 POST 请求到 `/api/images/upload`
**WHEN** 请求包含有效的图片文件（multipart/form-data）
**THEN** 系统 SHALL:
- 验证文件类型（MIME type 为 `image/jpeg`, `image/png`, 或 `image/webp`）
- 验证文件大小（≤ 10MB）
- 提取图片元数据（宽度、高度、格式）
- 生成唯一的文件名（UUID + 原始扩展名）
- 保存文件到 `backend/uploads/images/` 目录
- 在数据库中创建 `UploadedImage` 记录
- 返回 201 Created 状态码和图片信息（包括 ID、URL、元数据）

响应示例：
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "my-pet.jpg",
  "storage_path": "/uploads/images/550e8400-e29b-41d4-a716-446655440000.jpg",
  "file_size": 2048576,
  "width": 1920,
  "height": 1080,
  "mime_type": "image/jpeg",
  "created_at": "2025-01-16T10:30:00Z"
}
```

#### Scenario: Invalid file type upload

**GIVEN** 前端发送 POST 请求到 `/api/images/upload`
**WHEN** 文件类型不是支持的图片格式
**THEN** 系统 SHALL:
- 拒绝请求
- 返回 400 Bad Request 状态码
- 返回错误信息：`{"error": "不支持的文件类型，仅支持 JPG、PNG 和 WEBP"}`

#### Scenario: Oversized file upload

**GIVEN** 前端发送 POST 请求到 `/api/images/upload`
**WHEN** 文件大小超过 10MB
**THEN** 系统 SHALL:
- 拒绝请求
- 返回 413 Payload Too Large 状态码
- 返回错误信息：`{"error": "文件大小超过限制，最大支持 10MB"}`

#### Scenario: Server error during upload

**GIVEN** 前端发送有效的上传请求
**WHEN** 服务器在保存文件时发生错误（磁盘空间不足、权限问题等）
**THEN** 系统 SHALL:
- 清理已部分上传的文件（如果有）
- 返回 500 Internal Server Error 状态码
- 返回错误信息：`{"error": "上传失败，请稍后重试"}`
- 记录详细错误日志到后端日志文件

### Requirement: File Storage Management

后端 SHALL 管理上传的图片文件，包括存储、清理和访问控制。

#### Scenario: Upload directory initialization

**GIVEN** 应用启动
**WHEN** 检查上传目录
**THEN** 系统 SHALL:
- 确保 `backend/uploads/images/` 目录存在
- 如果不存在，自动创建目录
- 设置适当的目录权限（可读写）

#### Scenario: File naming strategy

**GIVEN** 新图片上传
**WHEN** 保存文件到磁盘
**THEN** 系统 SHALL:
- 使用 UUID v4 生成唯一文件名
- 保留原始文件扩展名（`.jpg`, `.png`, `.webp`）
- 文件名格式：`{uuid}.{extension}`
- 例如：`550e8400-e29b-41d4-a716-446655440000.jpg`

#### Scenario: Static file serving

**GIVEN** 图片已上传到服务器
**WHEN** 前端请求访问图片 URL
**THEN** 系统 SHALL:
- 通过 FastAPI StaticFiles 中间件提供文件访问
- URL 格式：`http://localhost:8000/uploads/images/{filename}`
- 设置适当的 MIME type headers
- 支持浏览器缓存（Cache-Control headers）

### Requirement: Image Metadata Extraction

后端 SHALL 提取并存储上传图片的元数据信息。

#### Scenario: Extract image dimensions

**GIVEN** 图片文件已接收
**WHEN** 保存到数据库之前
**THEN** 系统 SHALL:
- 使用 Pillow 库读取图片
- 提取宽度和高度（像素）
- 保存到 `UploadedImage.width` 和 `height` 字段

#### Scenario: Extract file information

**GIVEN** 图片文件已接收
**WHEN** 保存到数据库之前
**THEN** 系统 SHALL:
- 记录原始文件名（用户上传的名称）
- 计算文件大小（字节）
- 记录 MIME type
- 保存所有信息到 `UploadedImage` 记录

### Requirement: Temporary Image Management

系统 SHALL 标记新上传的图片为临时状态，直到用于生成任务。

#### Scenario: New upload marked as temporary

**GIVEN** 图片上传成功
**WHEN** 创建 `UploadedImage` 记录
**THEN** 系统 SHALL:
- 设置 `is_temp = True`
- 设置 `user_id` 为访客用户 ID（在无认证情况下）
- 记录上传时间戳

#### Scenario: Image used in generation job

**GIVEN** 用户创建生成任务并使用某个上传的图片
**WHEN** 生成任务成功创建
**THEN** 系统 SHALL:
- 更新图片记录的 `is_temp = False`
- 保留图片文件，不自动删除

**Note**: 临时图片的自动清理逻辑将在后续提案中实现（定时任务清理超过 24 小时的临时图片）。

## Technical Specifications

### Frontend Components

#### ImageUploader Component

文件位置：`frontend/src/components/image-upload/ImageUploader.tsx`

Props:
```typescript
interface ImageUploaderProps {
  onUploadSuccess: (image: UploadedImage) => void;
  onUploadError: (error: string) => void;
  maxSizeInMB?: number;  // 默认 10
  acceptedFormats?: string[];  // 默认 ['image/jpeg', 'image/png', 'image/webp']
}
```

State:
- `uploadedImage: UploadedImage | null` - 已上传的图片信息
- `isUploading: boolean` - 上传中状态
- `uploadProgress: number` - 上传进度（0-100）
- `error: string | null` - 错误信息

#### ImagePreview Component

文件位置：`frontend/src/components/image-upload/ImagePreview.tsx`

Props:
```typescript
interface ImagePreviewProps {
  image: UploadedImage;
  onClear: () => void;
  onReupload: () => void;
}
```

### Backend API

#### Upload Endpoint

```python
# File: backend/app/api/v1/endpoints/images.py

@router.post("/upload", response_model=schemas.UploadedImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> schemas.UploadedImageResponse:
    """
    Upload a pet image for avatar generation.

    - Accepts JPG, PNG, WEBP formats
    - Maximum file size: 10MB
    - Returns image metadata and storage URL
    """
    # Implementation...
```

#### Pydantic Schemas

```python
# File: backend/app/schemas/image.py

class UploadedImageResponse(BaseModel):
    id: str
    filename: str
    storage_path: str
    file_size: int
    width: int
    height: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True
```

### Database Schema

使用已存在的 `UploadedImage` 模型（已在 `backend/app/models/image.py` 中定义）：

```python
class UploadedImage(Base):
    __tablename__ = "uploaded_images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)  # 原始文件名
    storage_path = Column(String, nullable=False)  # 相对路径
    file_size = Column(Integer, nullable=False)  # 字节
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    is_temp = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

### File Validation

**允许的文件类型**：
- MIME types: `image/jpeg`, `image/png`, `image/webp`
- 文件扩展名: `.jpg`, `.jpeg`, `.png`, `.webp`

**文件大小限制**：
- 最大：10MB (10,485,760 bytes)
- 最小：1KB (1024 bytes) - 避免空文件或损坏文件

**图片尺寸建议**（非强制）：
- 最小推荐：512x512 像素
- 最大推荐：4096x4096 像素

### Error Handling

**前端错误处理**：
- 使用 Toast 组件显示错误信息
- 错误类型：
  - 文件类型不支持
  - 文件大小超限
  - 网络错误
  - 服务器错误

**后端错误处理**：
- 400 Bad Request: 文件类型或格式错误
- 413 Payload Too Large: 文件大小超限
- 500 Internal Server Error: 服务器处理错误
- 所有错误 SHALL 记录到日志文件，包含详细的堆栈信息

### Dependencies

**Frontend**:
- `react-dropzone` - 拖拽上传库（或自行实现）
- `axios` 或 `fetch` - HTTP 客户端

**Backend**:
- `python-multipart` - 处理 multipart/form-data
- `Pillow` - 图片处理和元数据提取
- `aiofiles` - 异步文件操作（可选，提升性能）

## Testing Requirements

### Frontend Tests

1. **Unit Tests**:
   - 文件类型验证逻辑
   - 文件大小验证逻辑
   - 状态管理（上传中、成功、失败）

2. **Component Tests**:
   - ImageUploader 组件渲染
   - 拖拽交互测试
   - 点击上传测试
   - 错误显示测试

### Backend Tests

1. **Unit Tests**:
   - 文件验证函数
   - 元数据提取函数
   - 文件名生成逻辑

2. **Integration Tests**:
   - POST /api/images/upload 成功场景
   - POST /api/images/upload 各种错误场景
   - 数据库记录创建验证
   - 文件系统存储验证

### E2E Tests

1. 完整上传流程：选择文件 → 上传 → 预览
2. 错误处理：上传无效文件 → 显示错误
3. 重新上传：上传 → 清除 → 重新上传

## Performance Considerations

- **前端**：
  - 图片预览使用本地 URL.createObjectURL() 而非 Base64，减少内存占用
  - 上传前进行客户端验证，减少无效请求

- **后端**：
  - 使用流式上传，避免一次性加载整个文件到内存
  - 图片元数据提取使用 Pillow 的高效模式
  - 考虑对大图片进行服务器端压缩（后续优化）

## Security Considerations

- 验证文件的真实 MIME type，而非仅依赖扩展名
- 限制上传频率（rate limiting）防止滥用
- 上传的文件名使用 UUID，防止路径遍历攻击
- 不执行上传的文件内容（仅作为图片处理）
- 设置合理的目录权限，防止未授权访问
