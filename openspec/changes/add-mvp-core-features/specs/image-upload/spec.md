## ADDED Requirements

### Requirement: 图片拖拽上传
系统 SHALL 支持用户通过拖拽方式上传宠物图片。

#### Scenario: 拖拽上传区域显示
- **WHEN** 用户访问生成器页面
- **THEN** 显示大而明显的上传区域
- **AND** 包含拖拽图标（Upload 图标）
- **AND** 提示文字"拖拽图片到此处或点击上传"
- **AND** 支持的格式提示"支持 JPG、PNG 格式，最大 10MB"

#### Scenario: 拖拽文件到上传区
- **WHEN** 用户将文件拖拽到上传区域
- **THEN** 上传区域高亮显示（边框变色或背景变化）
- **AND** 提示文字变为"松开以上传"

#### Scenario: 成功上传图片
- **WHEN** 用户释放拖拽的有效图片文件
- **THEN** 显示上传进度条或 spinner
- **AND** 上传完成后显示图片预览
- **AND** 隐藏上传区域或移到侧边
- **AND** 显示图片文件名和大小

#### Scenario: 拖拽无效文件
- **WHEN** 用户拖拽非图片文件或不支持的格式
- **THEN** 显示错误提示"仅支持 JPG、PNG 格式"
- **AND** 不执行上传操作

### Requirement: 点击上传
系统 SHALL 支持用户点击上传区域选择文件。

#### Scenario: 点击触发文件选择器
- **WHEN** 用户点击上传区域
- **THEN** 打开系统文件选择对话框
- **AND** 限制文件类型为 image/jpeg, image/png

#### Scenario: 选择文件后上传
- **WHEN** 用户在文件选择器中选择有效图片
- **THEN** 自动开始上传
- **AND** 显示上传进度
- **AND** 完成后显示预览

### Requirement: 文件验证
系统 SHALL 在客户端和服务端验证上传的图片文件。

#### Scenario: 客户端文件大小验证
- **WHEN** 用户选择文件大小 > 10MB 的图片
- **THEN** 阻止上传
- **AND** 显示错误提示"图片大小不能超过 10MB"

#### Scenario: 客户端文件类型验证
- **WHEN** 用户选择非 JPG/PNG 格式的文件
- **THEN** 阻止上传
- **AND** 显示错误提示"仅支持 JPG、PNG 格式"

#### Scenario: 服务端文件验证
- **WHEN** 后端接收上传文件
- **THEN** 验证文件 MIME 类型
- **AND** 验证文件大小
- **AND** 验证图片尺寸（至少 256x256 像素）
- **AND** 如果验证失败，返回 400 错误

#### Scenario: 恶意文件检测
- **WHEN** 上传的文件包含可疑内容或脚本
- **THEN** 拒绝上传
- **AND** 返回错误"文件验证失败"

### Requirement: 图片预览
系统 SHALL 在上传后显示图片预览。

#### Scenario: 显示图片预览
- **WHEN** 图片上传成功
- **THEN** 在预览区域显示图片
- **AND** 保持图片宽高比
- **AND** 限制预览尺寸（最大宽度 500px）
- **AND** 显示图片元数据（文件名、大小、尺寸）

#### Scenario: 图片预览控制
- **WHEN** 用户查看已上传图片
- **THEN** 显示删除按钮（X 图标）
- **AND** 显示重新上传按钮
- **AND** 可以点击图片查看大图（Dialog）

#### Scenario: 删除已上传图片
- **WHEN** 用户点击删除按钮
- **THEN** 显示确认对话框"确定删除这张图片吗？"
- **AND** 用户确认后移除图片
- **AND** 恢复显示上传区域
- **AND** 清除后端临时文件（如果已上传）

### Requirement: 上传进度指示
系统 SHALL 显示图片上传的实时进度。

#### Scenario: 上传进度条
- **WHEN** 图片开始上传
- **THEN** 显示进度条（shadcn/ui Progress）
- **AND** 实时更新百分比（0% - 100%）
- **AND** 显示上传状态文字"上传中... 45%"

#### Scenario: 上传成功反馈
- **WHEN** 图片上传完成
- **THEN** 进度条变为绿色
- **AND** 显示"上传成功"提示（Toast 通知）
- **AND** 自动隐藏进度条

#### Scenario: 上传失败处理
- **WHEN** 图片上传失败（网络错误、服务器错误）
- **THEN** 进度条变为红色
- **AND** 显示"上传失败"错误提示（Toast）
- **AND** 提供"重试"按钮

#### Scenario: 取消上传
- **WHEN** 用户在上传过程中点击"取消"按钮
- **THEN** 中断上传请求
- **AND** 隐藏进度条
- **AND** 恢复上传区域

### Requirement: 图片存储
系统 SHALL 安全地存储上传的图片文件。

#### Scenario: 临时文件存储
- **WHEN** 用户上传图片但未生成
- **THEN** 将图片保存到临时目录
- **AND** 生成唯一文件名（UUID + 原始扩展名）
- **AND** 返回临时文件 ID 给前端

#### Scenario: 永久文件存储
- **WHEN** 用户完成图片生成
- **THEN** 将临时文件移动到永久存储目录
- **AND** 更新数据库中的文件路径
- **AND** 清理临时文件

#### Scenario: 临时文件清理
- **WHEN** 临时文件创建时间 > 24 小时
- **THEN** 后台任务自动删除临时文件
- **AND** 释放存储空间

### Requirement: 图片优化
系统 SHALL 对上传的大尺寸图片进行自动优化处理。

#### Scenario: 自动压缩大图片
- **WHEN** 上传的图片尺寸 > 2048x2048
- **THEN** 自动缩放到 2048x2048（保持宽高比）
- **AND** 优化图片质量（JPEG 质量 85%）
- **AND** 减小文件大小

#### Scenario: 图片格式转换
- **WHEN** 上传 PNG 格式且文件较大
- **THEN** 可选择转换为 JPEG 格式
- **AND** 显示转换选项给用户

### Requirement: UI 组件设计
图片上传相关 UI SHALL 遵循简洁设计风格，使用 shadcn/ui 组件。

#### Scenario: 上传区域样式
- **WHEN** 显示上传区域
- **THEN** 使用虚线边框（border-2 border-dashed）
- **AND** 圆角 (rounded-lg)
- **AND** 浅灰色背景 (bg-gray-50)
- **AND** 内边距 (p-8 或 p-12)
- **AND** 图标居中显示（Lucide Upload，w-12 h-12）
- **AND** 文字居中、灰色 (text-gray-600)

#### Scenario: 拖拽悬停状态
- **WHEN** 用户拖拽文件到上传区域上方
- **THEN** 边框变为主题色 (border-primary)
- **AND** 背景稍微加深 (bg-primary/5)
- **AND** 图标和文字颜色变为主题色

#### Scenario: 图片预览卡片
- **WHEN** 显示上传的图片
- **THEN** 使用 shadcn/ui Card 组件
- **AND** 图片居中显示
- **AND** 底部显示文件信息（小号字体）
- **AND** 右上角显示删除按钮（圆形、半透明背景、X 图标）
- **AND** 悬停时显示重新上传按钮

#### Scenario: 进度指示器
- **WHEN** 显示上传进度
- **THEN** 使用 shadcn/ui Progress 组件
- **AND** 主题色进度条
- **AND** 下方显示百分比文字
- **AND** 平滑动画过渡

### Requirement: API 端点
后端 SHALL 提供图片上传相关的 API 端点。

#### Scenario: API 端点列表
- **POST /api/images/upload** - 上传图片
- **GET /api/images/{image_id}** - 获取图片信息
- **DELETE /api/images/{image_id}** - 删除图片
- **GET /api/images/temp/{temp_id}** - 获取临时图片

#### Scenario: 上传 API 请求
- **WHEN** 前端上传图片
- **THEN** 使用 multipart/form-data 格式
- **AND** 字段名为 "file"
- **AND** 包含认证 token（Authorization header）

#### Scenario: 上传 API 响应
- **WHEN** 图片上传成功
- **THEN** 返回 JSON 格式
  ```json
  {
    "success": true,
    "data": {
      "image_id": "uuid-string",
      "filename": "original-name.jpg",
      "size": 1024000,
      "width": 1920,
      "height": 1080,
      "url": "/uploads/temp/uuid-string.jpg",
      "temp": true
    }
  }
  ```

### Requirement: 数据库模型
系统 SHALL 存储上传图片的元数据。

#### Scenario: UploadedImage 表结构
- **id**: UUID (主键)
- **user_id**: UUID (外键，关联 User)
- **filename**: String (原始文件名)
- **storage_path**: String (存储路径)
- **file_size**: Integer (字节)
- **width**: Integer (像素)
- **height**: Integer (像素)
- **mime_type**: String (MIME 类型)
- **is_temp**: Boolean (是否临时文件，默认 true)
- **created_at**: DateTime (创建时间)
- **updated_at**: DateTime (更新时间)

#### Scenario: 关联到生成记录
- **WHEN** 图片用于生成后
- **THEN** 将 is_temp 设置为 false
- **AND** 在 GeneratedImage 表中创建关联
