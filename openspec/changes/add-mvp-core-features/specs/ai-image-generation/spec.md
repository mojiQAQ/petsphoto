## ADDED Requirements

### Requirement: Veo3 API 集成
系统 SHALL 集成 Google Veo3 API 进行 AI 图像生成。

#### Scenario: API 认证配置
- **WHEN** 后端服务启动
- **THEN** 从环境变量读取 VEO3_API_KEY
- **AND** 验证 API Key 有效性
- **AND** 如果 API Key 无效或缺失，记录错误日志

#### Scenario: 调用 Veo3 生成图像
- **WHEN** 系统请求生成图片
- **THEN** 发送 HTTP POST 请求到 Veo3 API 端点
- **AND** 包含认证 header（API Key）
- **AND** 请求体包含：源图片（base64 或 URL）、风格提示词、参数
- **AND** 设置超时时间为 60 秒

#### Scenario: 处理 API 响应
- **WHEN** Veo3 API 返回成功响应
- **THEN** 解析返回的图片 URL 或 base64 数据
- **AND** 下载生成的图片到本地存储
- **AND** 保存图片元数据到数据库

#### Scenario: API 调用失败
- **WHEN** Veo3 API 返回错误（4xx 或 5xx）
- **THEN** 记录错误日志（包括错误代码、消息）
- **AND** 根据错误类型返回友好的中文错误提示
- **AND** 如果是限流错误（429），返回"请求过于频繁，请稍后再试"
- **AND** 如果是服务器错误（500），返回"AI 服务暂时不可用，请稍后再试"

### Requirement: 预设风格管理
系统 SHALL 提供预设的图片生成风格。

#### Scenario: 风格列表定义
- **WHEN** MVP 阶段
- **THEN** 提供至少 5 种预设风格
  - **卡通风格**："cartoon style, vibrant colors, cute pet illustration"
  - **油画风格**："oil painting style, artistic, classical portrait"
  - **水彩风格**："watercolor painting, soft colors, gentle brush strokes"
  - **像素艺术**："pixel art, 8-bit style, retro gaming aesthetic"
  - **赛博朋克**："cyberpunk style, neon lights, futuristic pet portrait"

#### Scenario: 风格数据存储
- **WHEN** 系统需要风格数据
- **THEN** 从配置文件或数据库读取
- **AND** 每个风格包含：ID、名称、描述、提示词、缩略图 URL

#### Scenario: 获取风格列表 API
- **WHEN** 前端请求风格列表
- **THEN** 返回所有可用风格
  ```json
  {
    "success": true,
    "data": {
      "styles": [
        {
          "id": "cartoon",
          "name": "卡通风格",
          "description": "色彩鲜艳的卡通画风",
          "prompt": "cartoon style, vibrant colors...",
          "thumbnail_url": "/assets/styles/cartoon.jpg",
          "is_premium": false
        }
      ]
    }
  }
  ```

### Requirement: 图片生成流程
系统 SHALL 协调完整的图片生成流程。

#### Scenario: 用户发起生成请求
- **WHEN** 用户选择风格并点击"生成"按钮
- **THEN** 前端验证已上传图片
- **AND** 验证已选择风格
- **AND** 检查用户积分余额是否足够
- **AND** 发送生成请求到后端 API

#### Scenario: 后端处理生成请求
- **WHEN** 后端接收生成请求
- **THEN** 验证用户身份和积分
- **AND** 获取上传的源图片
- **AND** 获取选择的风格提示词
- **AND** 创建 GenerationJob 记录（状态：pending）
- **AND** 将任务加入后台队列或立即处理
- **AND** 返回 job_id 给前端

#### Scenario: 异步生成处理
- **WHEN** 生成任务开始执行
- **THEN** 更新 job 状态为 processing
- **AND** 调用 Veo3 API
- **AND** 等待 API 响应（最多 60 秒）
- **AND** 下载生成的图片
- **AND** 保存到永久存储
- **AND** 扣除用户积分
- **AND** 更新 job 状态为 completed

#### Scenario: 生成成功通知
- **WHEN** 图片生成完成
- **THEN** 通过 WebSocket 或轮询通知前端
- **AND** 前端显示生成结果
- **AND** 显示成功 Toast 提示

#### Scenario: 生成失败处理
- **WHEN** 生成过程中发生错误
- **THEN** 更新 job 状态为 failed
- **AND** 记录失败原因
- **AND** 不扣除用户积分
- **AND** 通知前端显示错误提示

### Requirement: 生成参数配置
系统 SHALL 支持配置图片生成参数。

#### Scenario: 默认生成参数
- **WHEN** MVP 阶段
- **THEN** 使用固定参数：
  - **输出尺寸**：1024x1024
  - **生成数量**：1 张
  - **引导强度**：7.5（CFG scale）
  - **步数**：30 steps

#### Scenario: 参数验证
- **WHEN** 接收生成请求参数
- **THEN** 验证参数在允许范围内
- **AND** 如果参数无效，使用默认值
- **AND** 记录参数到日志

### Requirement: 生成结果展示
系统 SHALL 在前端展示生成的图片结果。

#### Scenario: 结果页面布局
- **WHEN** 图片生成完成
- **THEN** 在 Dialog 或全屏模式显示结果
- **AND** 中心显示生成的大图
- **AND** 下方显示操作按钮：下载、重新生成、分享

#### Scenario: 图片下载功能
- **WHEN** 用户点击下载按钮
- **THEN** 触发浏览器下载
- **AND** 文件名格式："petsphoto-{timestamp}.jpg"
- **AND** 下载原图（非压缩版本）

#### Scenario: 重新生成功能
- **WHEN** 用户点击"重新生成"按钮
- **THEN** 使用相同的源图片和风格
- **AND** 再次发起生成请求
- **AND** 扣除积分（新的生成）
- **AND** 关闭当前结果 Dialog

### Requirement: 生成历史记录
系统 SHALL 保存用户的生成历史。

#### Scenario: 自动保存历史
- **WHEN** 图片生成成功
- **THEN** 自动保存到用户的生成历史
- **AND** 关联源图片、风格、生成图片
- **AND** 记录生成时间和消耗积分

#### Scenario: 历史记录列表
- **WHEN** 用户访问历史记录页面（Phase 2 功能，这里预留）
- **THEN** 显示所有生成记录（时间倒序）
- **AND** 每条记录显示缩略图、风格、日期
- **AND** 点击查看大图和详情

### Requirement: 积分消耗机制
系统 SHALL 在图片生成时扣除用户积分。

#### Scenario: 生成前检查积分
- **WHEN** 用户发起生成请求
- **THEN** 检查用户积分余额
- **AND** 如果积分不足（< 1 积分），拒绝请求
- **AND** 返回错误"积分不足，请购买积分"
- **AND** 提供跳转到购买页面的链接

#### Scenario: 生成成功扣除积分
- **WHEN** 图片生成完成
- **THEN** 扣除 1 积分（MVP 固定价格）
- **AND** 更新用户积分余额
- **AND** 创建积分消费记录

#### Scenario: 生成失败不扣积分
- **WHEN** 图片生成失败
- **THEN** 不扣除用户积分
- **AND** 记录失败原因，便于分析和改进

### Requirement: 生成队列管理
系统 SHALL 使用队列管理生成任务，防止并发过载。

#### Scenario: 任务排队
- **WHEN** 同时有多个生成请求
- **THEN** 将任务加入队列（先进先出）
- **AND** 返回队列位置给用户
- **AND** 显示"排队中，前面有 X 个任务"

#### Scenario: 并发限制
- **WHEN** MVP 阶段
- **THEN** 限制同时处理的任务数为 3
- **AND** 超过限制的任务在队列中等待
- **AND** 任务完成后自动处理下一个

### Requirement: UI 组件设计
生成相关 UI SHALL 遵循简洁设计风格，使用 shadcn/ui 组件。

#### Scenario: 风格选择卡片
- **WHEN** 显示风格选择器
- **THEN** 使用 Grid 布局（2-3 列）
- **AND** 每个风格为 shadcn/ui Card 组件
- **AND** 卡片包含：缩略图、风格名称、简短描述
- **AND** 选中状态：边框高亮（border-primary）、背景稍微加深
- **AND** 悬停状态：轻微阴影加深、微妙缩放

#### Scenario: 生成按钮
- **WHEN** 显示生成按钮
- **THEN** 使用 shadcn/ui Button（primary variant, lg size）
- **AND** 固定在风格选择区域底部或右下角
- **AND** 文字"开始生成" + Sparkles 图标
- **AND** 禁用状态：未上传图片或未选择风格时灰色禁用

#### Scenario: 生成进度指示
- **WHEN** 图片正在生成
- **THEN** 显示 Dialog 或全屏遮罩
- **AND** 中心显示 Spinner 或骨架屏
- **AND** 提示文字"正在生成中，请稍候..."
- **AND** 预计时间提示"通常需要 10-30 秒"
- **AND** 不可关闭（防止用户误操作）

#### Scenario: 结果展示 Dialog
- **WHEN** 显示生成结果
- **THEN** 使用 shadcn/ui Dialog（最大宽度 lg 或 xl）
- **AND** 图片居中显示（max-width: 80vw, max-height: 80vh）
- **AND** 底部操作按钮横向排列
  - 下载（Download 图标 + "下载"）
  - 重新生成（RefreshCw 图标 + "重新生成"）
  - 关闭（X 图标）

### Requirement: API 端点
后端 SHALL 提供图片生成相关的 API 端点。

#### Scenario: API 端点列表
- **POST /api/generate** - 创建生成任务
- **GET /api/generate/{job_id}** - 查询任务状态
- **GET /api/generate/{job_id}/result** - 获取生成结果
- **GET /api/styles** - 获取风格列表
- **GET /api/generate/history** - 获取用户生成历史（Phase 2）

#### Scenario: 生成 API 请求
- **WHEN** 前端请求生成
- **THEN** 发送 POST /api/generate
  ```json
  {
    "source_image_id": "uuid-string",
    "style_id": "cartoon",
    "custom_prompt": "",  // Phase 2 功能
    "parameters": {}  // 可选
  }
  ```

#### Scenario: 生成 API 响应
- **WHEN** 后端接收请求
- **THEN** 返回 JSON
  ```json
  {
    "success": true,
    "data": {
      "job_id": "uuid-string",
      "status": "pending",
      "queue_position": 2,
      "estimated_time": 30
    }
  }
  ```

#### Scenario: 任务状态 API
- **WHEN** 前端轮询任务状态
- **THEN** GET /api/generate/{job_id} 返回
  ```json
  {
    "success": true,
    "data": {
      "job_id": "uuid-string",
      "status": "completed",  // pending | processing | completed | failed
      "result_image_url": "/uploads/generated/uuid.jpg",
      "created_at": "2025-01-16T10:30:00Z",
      "completed_at": "2025-01-16T10:30:25Z",
      "error_message": null
    }
  }
  ```

### Requirement: 数据库模型
系统 SHALL 存储生成任务和结果的数据。

#### Scenario: GenerationJob 表结构
- **id**: UUID (主键)
- **user_id**: UUID (外键，关联 User)
- **source_image_id**: UUID (外键，关联 UploadedImage)
- **style_id**: String (风格 ID)
- **custom_prompt**: String (自定义提示词，Phase 2，可为空)
- **status**: Enum (pending, processing, completed, failed)
- **queue_position**: Integer (队列位置，可为空)
- **result_image_url**: String (生成图片 URL，可为空)
- **credits_cost**: Integer (消耗积分，默认 1)
- **error_message**: String (错误信息，可为空)
- **api_response**: JSON (Veo3 API 原始响应，调试用)
- **created_at**: DateTime (创建时间)
- **started_at**: DateTime (开始处理时间，可为空)
- **completed_at**: DateTime (完成时间，可为空)

#### Scenario: GenerationStyle 表结构（可选）
- **id**: String (主键，如 "cartoon")
- **name**: String (风格名称，支持多语言)
- **description**: String (风格描述)
- **prompt_template**: String (提示词模板)
- **thumbnail_url**: String (缩略图 URL)
- **is_active**: Boolean (是否启用，默认 true)
- **is_premium**: Boolean (是否高级风格，Phase 2)
- **sort_order**: Integer (排序顺序)

### Requirement: 错误处理和日志
系统 SHALL 记录详细的生成日志，便于调试和优化。

#### Scenario: 详细日志记录
- **WHEN** 生成任务的各个阶段
- **THEN** 记录日志：
  - 任务创建（用户 ID、风格、源图片）
  - API 调用开始（时间戳）
  - API 调用完成（耗时、状态码）
  - 图片下载和保存（文件大小）
  - 积分扣除（扣除前后余额）
  - 任务完成或失败（总耗时）

#### Scenario: 错误日志
- **WHEN** 生成过程中发生错误
- **THEN** 记录 ERROR 级别日志
- **AND** 包含：用户 ID、job ID、错误类型、错误堆栈
- **AND** 发送告警（如果是严重错误）
