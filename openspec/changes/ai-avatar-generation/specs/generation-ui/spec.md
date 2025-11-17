# Generation UI Capability

## Overview

生成器用户界面是用户与 AI 头像生成功能交互的主要界面，整合了图片上传、风格选择、生成过程跟踪和结果展示等功能。本规范定义了生成器页面的布局、交互逻辑和用户体验要求。

## ADDED Requirements

### Requirement: Generator Page Layout

前端 SHALL 提供一个专门的生成器页面，整合所有生成相关的功能。

#### Scenario: User navigates to generator page

**GIVEN** 用户在应用中
**WHEN** 用户点击导航栏的"生成器"链接或首页的"开始创作"按钮
**THEN** 系统 SHALL:
- 导航到 `/generator` 路由
- 显示生成器页面布局
- 左侧/顶部显示图片上传区域
- 右侧/下方显示风格选择器
- 底部显示"生成"按钮（初始禁用状态）

#### Scenario: Responsive layout - Desktop

**GIVEN** 用户在桌面设备上（屏幕宽度 ≥ 768px）
**WHEN** 访问生成器页面
**THEN** 系统 SHALL:
- 使用两列布局
- 左列：图片上传区域（占 40-50% 宽度）
- 右列：风格选择器（占 50-60% 宽度）
- 生成按钮固定在右列底部
- 两列之间有适当的间距（gap-6 或 gap-8）

#### Scenario: Responsive layout - Mobile

**GIVEN** 用户在移动设备上（屏幕宽度 < 768px）
**WHEN** 访问生成器页面
**THEN** 系统 SHALL:
- 使用单列堆叠布局
- 从上到下顺序：上传区域 → 风格选择器 → 生成按钮
- 生成按钮固定在底部（sticky footer）
- 各部分有清晰的视觉分隔

### Requirement: Style Selector

前端 SHALL 提供风格选择器，展示所有预设的艺术风格。

#### Scenario: Display preset styles

**GIVEN** 生成器页面已加载
**WHEN** 页面从后端获取风格列表
**THEN** 系统 SHALL:
- 发送 GET 请求到 `/api/styles`
- 渲染风格选择器，显示所有可用风格
- 每个风格显示为一个卡片，包含：
  - 风格名称（如 "卡通风格"）
  - 风格描述或示例图（可选）
  - 选中状态指示器
- 使用网格布局：桌面端 2-3 列，移动端 1 列

#### Scenario: User selects a style

**GIVEN** 风格选择器已显示
**WHEN** 用户点击某个风格卡片
**THEN** 系统 SHALL:
- 高亮选中的风格卡片（边框加粗、背景变化或 checkmark 图标）
- 取消其他风格的选中状态（单选）
- 保存选中的 `style_id` 到组件状态
- 如果图片已上传，启用"生成"按钮

#### Scenario: No style selected initially

**GIVEN** 用户刚进入生成器页面
**WHEN** 页面加载完成
**THEN** 系统 SHALL:
- 所有风格卡片都处于未选中状态
- 不预选任何风格（用户必须主动选择）
- "生成"按钮保持禁用状态

### Requirement: Generation Button State

前端 SHALL 根据上传和选择状态动态控制"生成"按钮的可用性。

#### Scenario: Button enabled conditions

**GIVEN** 用户在生成器页面
**WHEN** 同时满足以下条件：
  - 图片已成功上传
  - 风格已选择
  - 没有正在进行的生成任务
**THEN** 系统 SHALL:
- 启用"生成"按钮
- 按钮显示为可点击状态（primary 样式）
- 鼠标悬停时显示 hover 效果

#### Scenario: Button disabled - no image

**GIVEN** 用户在生成器页面
**WHEN** 未上传图片（即使已选择风格）
**THEN** 系统 SHALL:
- 禁用"生成"按钮
- 按钮显示为灰色/不可点击状态
- 可选：显示提示文字 "请先上传图片"

#### Scenario: Button disabled - no style

**GIVEN** 用户在生成器页面
**WHEN** 已上传图片但未选择风格
**THEN** 系统 SHALL:
- 禁用"生成"按钮
- 按钮显示为灰色/不可点击状态
- 可选：显示提示文字 "请选择风格"

#### Scenario: Button disabled - generating

**GIVEN** 生成任务正在进行中
**WHEN** 任务状态为 `processing`
**THEN** 系统 SHALL:
- 禁用"生成"按钮
- 按钮显示 loading spinner 和文字 "生成中..."
- 防止用户重复提交请求

### Requirement: Generation Process

前端 SHALL 处理生成请求的提交和状态跟踪。

#### Scenario: User clicks generate button

**GIVEN** 图片已上传且风格已选择
**WHEN** 用户点击"生成"按钮
**THEN** 系统 SHALL:
- 发送 POST 请求到 `/api/generations`
- Payload: `{"source_image_id": "...", "style_id": "..."}`
- 显示加载状态（按钮变为 "生成中..."）
- 隐藏或禁用上传和风格选择区域（防止修改）

#### Scenario: Generation request accepted

**GIVEN** 生成请求已发送
**WHEN** 后端返回 201 Created 和任务 ID
**THEN** 系统 SHALL:
- 保存任务 ID
- 开始轮询任务状态（每 2-3 秒查询一次）
- 显示生成进度界面（替代或覆盖当前页面内容）
- 显示加载动画或进度指示器

#### Scenario: Generation request fails

**GIVEN** 生成请求已发送
**WHEN** 后端返回错误响应（4xx 或 5xx）
**THEN** 系统 SHALL:
- 解析错误信息
- 使用 Toast 组件显示错误提示
- 恢复按钮为可点击状态
- 允许用户重新尝试

### Requirement: Status Polling

前端 SHALL 使用轮询机制实时跟踪生成任务状态。

#### Scenario: Poll job status while processing

**GIVEN** 生成任务已创建，状态为 `pending` 或 `processing`
**WHEN** 轮询定时器触发
**THEN** 系统 SHALL:
- 发送 GET 请求到 `/api/generations/{job_id}`
- 每 2-3 秒请求一次
- 更新 UI 上的状态指示（如进度条、loading 文字）
- 继续轮询直到状态变为 `completed` 或 `failed`

#### Scenario: Job completes successfully

**GIVEN** 正在轮询任务状态
**WHEN** API 返回状态为 `completed` 且包含 `result_image_url`
**THEN** 系统 SHALL:
- 停止轮询
- 显示成功提示（Toast 或页面文字）
- 展示生成结果界面（显示生成的图片）
- 提供"下载"和"重新生成"按钮

#### Scenario: Job fails

**GIVEN** 正在轮询任务状态
**WHEN** API 返回状态为 `failed` 且包含 `error_message`
**THEN** 系统 SHALL:
- 停止轮询
- 显示错误提示（Toast），内容为 `error_message`
- 恢复生成器页面到初始状态
- 保留已上传的图片和选择的风格（允许重试）

#### Scenario: Polling timeout protection

**GIVEN** 轮询已持续超过 90 秒
**WHEN** 任务仍未完成或失败
**THEN** 系统 SHALL:
- 停止轮询
- 显示提示："生成时间过长，请刷新页面查看结果"
- 记录日志用于调试

### Requirement: Result Display

前端 SHALL 在生成完成后展示结果图片。

#### Scenario: Show generated image

**GIVEN** 生成任务完成
**WHEN** 系统获取到 `result_image_url`
**THEN** 系统 SHALL:
- 显示生成结果界面（可以是 Dialog 或页面内容替换）
- 展示生成的图片（大图预览）
- 图片使用 `<img>` 标签，src 为完整 URL
- 图片加载时显示骨架屏或 spinner
- 图片周围有适当的边距和边框

#### Scenario: Result image loading

**GIVEN** 结果图片 URL 已获取
**WHEN** 浏览器加载图片
**THEN** 系统 SHALL:
- 显示加载占位符（Skeleton 或 Spinner）
- 图片加载完成后淡入显示
- 处理图片加载失败的情况（显示错误图标和提示）

### Requirement: Download Functionality

前端 SHALL 提供下载生成结果的功能。

#### Scenario: User downloads result

**GIVEN** 生成结果正在显示
**WHEN** 用户点击"下载"按钮
**THEN** 系统 SHALL:
- 创建一个隐藏的 `<a>` 标签
- 设置 `href` 为图片 URL
- 设置 `download` 属性为合理的文件名（如 `petsphoto_cartoon_20250116.jpg`）
- 触发点击事件，开始下载
- 可选：显示 Toast 提示 "下载已开始"

#### Scenario: Download filename format

**GIVEN** 下载图片
**WHEN** 生成下载文件名
**THEN** 系统 SHALL:
- 格式：`petsphoto_{style_id}_{timestamp}.jpg`
- 示例：`petsphoto_cartoon_20250116_103045.jpg`
- 使用有意义的命名，便于用户识别

### Requirement: Regeneration

前端 SHALL 提供重新生成功能，允许用户使用相同设置再次生成。

#### Scenario: User clicks regenerate

**GIVEN** 生成结果正在显示
**WHEN** 用户点击"重新生成"按钮
**THEN** 系统 SHALL:
- 关闭结果展示界面
- 保留当前的图片和风格选择
- 重新触发生成流程（相当于再次点击"生成"按钮）
- 创建新的生成任务

#### Scenario: User changes settings after generation

**GIVEN** 生成结果正在显示
**WHEN** 用户关闭结果界面并修改风格或图片
**THEN** 系统 SHALL:
- 允许用户修改任何设置
- 更新组件状态
- 下次生成使用新的设置

### Requirement: Loading States

前端 SHALL 在各个阶段提供清晰的加载状态指示。

#### Scenario: Image uploading state

**GIVEN** 用户上传图片
**WHEN** 文件正在上传中
**THEN** 系统 SHALL:
- 在上传区域显示进度条或 spinner
- 显示文字提示："上传中..."
- 可选：显示上传进度百分比

#### Scenario: Styles loading state

**GIVEN** 页面正在加载风格列表
**WHEN** API 请求未完成
**THEN** 系统 SHALL:
- 在风格选择器区域显示骨架屏（Skeleton）
- 模拟风格卡片的布局
- 加载完成后替换为实际内容

#### Scenario: Generation in progress state

**GIVEN** 生成任务正在处理
**WHEN** 任务状态为 `processing`
**THEN** 系统 SHALL:
- 显示全屏或模态的加载界面
- 包含：
  - Loading 动画（spinner 或自定义动画）
  - 提示文字："AI 正在生成您的宠物头像，请稍候..."
  - 可选：进度条（基于轮询次数估算）
- 阻止用户修改设置或离开页面（带确认）

### Requirement: Error Handling

前端 SHALL 提供友好的错误提示和恢复机制。

#### Scenario: API request fails

**GIVEN** 前端发送 API 请求
**WHEN** 网络错误或服务器返回错误
**THEN** 系统 SHALL:
- 捕获错误
- 使用 Toast 组件显示错误信息
- 如果是可恢复的错误，提示用户重试
- 记录错误到浏览器控制台

#### Scenario: Style list loading fails

**GIVEN** 页面尝试加载风格列表
**WHEN** API 请求失败
**THEN** 系统 SHALL:
- 显示空状态或错误提示："无法加载风格列表"
- 提供"重试"按钮
- 记录错误日志

#### Scenario: Generated image fails to load

**GIVEN** 结果 URL 已获取
**WHEN** 浏览器无法加载图片（404、网络错误等）
**THEN** 系统 SHALL:
- 显示错误占位符图标
- 显示提示文字："图片加载失败"
- 提供"刷新"或"返回"按钮

### Requirement: Empty States

前端 SHALL 在合适的位置提供空状态提示。

#### Scenario: No image uploaded yet

**GIVEN** 用户首次访问生成器页面
**WHEN** 上传区域为空
**THEN** 系统 SHALL:
- 显示大图标（如上传图标或图片占位符）
- 显示引导文字："拖拽图片到这里，或点击上传"
- 使用虚线边框或浅色背景突出上传区域

#### Scenario: No styles available

**GIVEN** 风格列表 API 返回空数组
**WHEN** 渲染风格选择器
**THEN** 系统 SHALL:
- 显示空状态提示："暂无可用风格"
- 可选：提供联系支持或刷新的建议

## Technical Specifications

### Frontend Components

#### Generator Page

文件位置：`frontend/src/pages/GeneratorPage.tsx`

组件结构：
```tsx
export function GeneratorPage() {
  const [uploadedImage, setUploadedImage] = useState<UploadedImage | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null);
  const [generationJob, setGenerationJob] = useState<GenerationJob | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  return (
    <Container className="py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left: Upload Section */}
        <div>
          <h2>上传宠物照片</h2>
          <ImageUploader
            onUploadSuccess={setUploadedImage}
            onUploadError={(error) => toast.error(error)}
          />
          {uploadedImage && (
            <ImagePreview
              image={uploadedImage}
              onClear={() => setUploadedImage(null)}
            />
          )}
        </div>

        {/* Right: Style Selection */}
        <div>
          <h2>选择艺术风格</h2>
          <StyleSelector
            selectedStyleId={selectedStyle}
            onStyleSelect={setSelectedStyle}
          />
        </div>
      </div>

      {/* Generate Button */}
      <div className="mt-8 flex justify-center">
        <Button
          size="lg"
          disabled={!uploadedImage || !selectedStyle || isGenerating}
          onClick={handleGenerate}
        >
          {isGenerating ? "生成中..." : "生成头像"}
        </Button>
      </div>

      {/* Result Modal */}
      {generationJob?.status === "completed" && (
        <ResultDialog
          imageUrl={generationJob.result_image_url}
          onClose={handleCloseResult}
          onRegenerate={handleRegenerate}
        />
      )}
    </Container>
  );
}
```

#### StyleSelector Component

文件位置：`frontend/src/components/generator/StyleSelector.tsx`

```tsx
interface StyleSelectorProps {
  selectedStyleId: string | null;
  onStyleSelect: (styleId: string) => void;
}

export function StyleSelector({ selectedStyleId, onStyleSelect }: StyleSelectorProps) {
  const { data: styles, isLoading } = useQuery({
    queryKey: ["styles"],
    queryFn: fetchStyles,
  });

  if (isLoading) {
    return <StyleSelectorSkeleton />;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {styles?.map((style) => (
        <StyleCard
          key={style.id}
          style={style}
          isSelected={selectedStyleId === style.id}
          onClick={() => onStyleSelect(style.id)}
        />
      ))}
    </div>
  );
}
```

#### ResultDialog Component

文件位置：`frontend/src/components/generator/ResultDialog.tsx`

```tsx
interface ResultDialogProps {
  imageUrl: string;
  onClose: () => void;
  onRegenerate: () => void;
}

export function ResultDialog({ imageUrl, onClose, onRegenerate }: ResultDialogProps) {
  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = `petsphoto_${Date.now()}.jpg`;
    link.click();
  };

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>生成完成！</DialogTitle>
        </DialogHeader>

        <div className="flex justify-center">
          <img
            src={imageUrl}
            alt="Generated avatar"
            className="max-w-full h-auto rounded-lg"
          />
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onRegenerate}>
            重新生成
          </Button>
          <Button onClick={handleDownload}>下载图片</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

### API Service Layer

文件位置：`frontend/src/services/api.ts`

```typescript
// Fetch available styles
export async function fetchStyles(): Promise<GenerationStyle[]> {
  const response = await fetch(`${API_BASE_URL}/api/styles`);
  if (!response.ok) throw new Error("Failed to fetch styles");
  return response.json();
}

// Create generation job
export async function createGenerationJob(
  sourceImageId: string,
  styleId: string
): Promise<GenerationJob> {
  const response = await fetch(`${API_BASE_URL}/api/generations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_image_id: sourceImageId, style_id: styleId }),
  });
  if (!response.ok) throw new Error("Failed to create generation job");
  return response.json();
}

// Get job status
export async function getGenerationJob(jobId: string): Promise<GenerationJob> {
  const response = await fetch(`${API_BASE_URL}/api/generations/${jobId}`);
  if (!response.ok) throw new Error("Failed to fetch job status");
  return response.json();
}
```

### Polling Hook

文件位置：`frontend/src/hooks/useGenerationPolling.ts`

```typescript
export function useGenerationPolling(jobId: string | null, interval = 3000) {
  const { data: job, isLoading } = useQuery({
    queryKey: ["generation-job", jobId],
    queryFn: () => getGenerationJob(jobId!),
    enabled: !!jobId,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (data?.status === "completed" || data?.status === "failed") {
        return false;
      }
      return interval;
    },
  });

  return { job, isLoading };
}
```

### TypeScript Types

文件位置：`frontend/src/types/generation.ts`

```typescript
export interface GenerationStyle {
  id: string;
  name: string;
  description?: string;
  prompt_template: string;
}

export interface GenerationJob {
  id: string;
  user_id: string;
  source_image_id: string;
  style_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  result_image_url?: string;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}
```

### Routing

文件位置：`frontend/src/App.tsx` 或路由配置文件

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/generator" element={<GeneratorPage />} />
        {/* Other routes */}
      </Routes>
    </BrowserRouter>
  );
}
```

## Testing Requirements

### Component Tests

1. **GeneratorPage**:
   - 渲染测试（所有区域正确显示）
   - 按钮状态测试（启用/禁用条件）
   - 交互测试（上传、选择风格、生成）

2. **StyleSelector**:
   - 风格列表渲染
   - 选择交互
   - 加载状态

3. **ResultDialog**:
   - 结果显示
   - 下载功能
   - 重新生成功能

### Integration Tests

1. 完整流程：上传 → 选择风格 → 生成 → 查看结果 → 下载
2. 轮询机制：创建任务 → 轮询状态 → 检测完成
3. 错误处理：API 失败 → 显示错误 → 允许重试

### E2E Tests (Playwright/Cypress)

1. 用户完整旅程测试
2. 响应式布局测试（桌面 + 移动端）
3. 错误恢复测试

## Performance Considerations

- **轮询优化**：使用 React Query 的智能重试和缓存
- **图片懒加载**：大图片使用 lazy loading
- **防抖/节流**：防止用户快速重复点击
- **代码分割**：生成器页面使用动态导入

## Accessibility

- 所有交互元素有适当的 ARIA 标签
- 键盘导航支持（Tab、Enter）
- 高对比度颜色方案
- 屏幕阅读器友好的提示文本
- 图片有 alt 属性

## Browser Compatibility

- 支持 Chrome、Firefox、Safari 最新两个版本
- 使用 Polyfills 处理旧浏览器（如需）
- 测试移动端浏览器（iOS Safari、Android Chrome）
