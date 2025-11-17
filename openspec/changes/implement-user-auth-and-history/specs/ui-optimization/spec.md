# Spec: ui-optimization

## MODIFIED Requirements

### Requirement: 生成结果图片尺寸 SHALL 优化以避免占用过多空间

生成结果图片尺寸 SHALL 优化以避免占用过多页面空间。

#### Scenario: 桌面端生成结果展示

**Given** 用户在桌面端(屏幕宽度 > 1024px)完成图片生成
**When** 生成完成后弹出 ResultDialog
**Then** Dialog 中的图片最大宽度为 600px
**And** 图片保持原始宽高比
**And** Dialog 两侧有适当留白

#### Scenario: 移动端生成结果展示

**Given** 用户在移动端(屏幕宽度 < 640px)完成图片生成
**When** 生成完成后弹出 ResultDialog
**Then** Dialog 占据屏幕宽度的 90%
**And** 图片宽度为 Dialog 宽度的 100%
**And** 图片保持原始宽高比

#### Scenario: 关闭弹窗后的持久化展示

**Given** 用户生成完成后关闭了 ResultDialog
**When** 生成结果显示在上传区域下方
**Then** 生成结果卡片最大宽度为 400px (桌面端)
**And** 卡片宽度为 100% (移动端,最大 300px)
**And** 卡片显示缩略图、操作按钮(下载、重新生成、清除)

---

### Requirement: 历史记录卡片尺寸 SHALL 优化为紧凑布局

历史记录卡片尺寸 SHALL 优化为紧凑布局,提高信息密度。

#### Scenario: 桌面端历史记录网格布局

**Given** 用户在桌面端查看历史记录
**When** 历史记录区域渲染
**Then** 使用 3 列网格布局(`grid-cols-3`)
**And** 每个卡片尺寸为 200x200px
**And** 卡片间距为 16px (`gap-4`)
**And** 图片填充整个卡片,使用 `object-cover`

#### Scenario: 平板端历史记录网格布局

**Given** 用户在平板端(641px - 1024px)查看历史记录
**When** 历史记录区域渲染
**Then** 使用 2 列网格布局(`grid-cols-2`)
**And** 每个卡片尺寸为 180x180px
**And** 卡片间距为 12px (`gap-3`)

#### Scenario: 移动端历史记录列表布局

**Given** 用户在移动端(< 640px)查看历史记录
**When** 历史记录区域渲染
**Then** 使用 1 列布局(`grid-cols-1`)
**And** 每个卡片宽度为 100%,高度为 150px
**And** 卡片使用横向布局: 左侧缩略图(150x150px) + 右侧信息

---

### Requirement: 历史记录 SHALL 显示在生成页面底部

历史记录 SHALL 集中显示在生成器页面的底部区域。

#### Scenario: 历史记录区域位置

**Given** 用户访问生成器页面
**When** 页面加载完成
**Then** 历史记录区域位于页面底部
**And** 位于"生成按钮"下方
**And** 与上方内容有明显间距(64px, `mt-16`)
**And** 历史记录区域有标题"生成历史"

#### Scenario: 历史记录区域最大高度

**Given** 用户有大量历史记录
**When** 历史记录区域渲染
**Then** 初始显示最新 20 条
**And** 区域最大高度不限制(使用无限滚动)
**And** 滚动到底部时自动加载更多

---

### Requirement: 图片加载和展示 SHALL 优化以提升用户体验

图片 SHALL 使用懒加载和占位符来优化加载体验和提升用户体验。

#### Scenario: 历史记录图片懒加载

**Given** 用户查看历史记录
**When** 历史记录列表渲染
**Then** 只加载可视区域内的图片
**And** 图片加载前显示 Skeleton 占位符
**And** 图片进入可视区域时开始加载
**And** 图片加载完成后淡入显示

#### Scenario: 图片加载失败处理

**Given** 某个历史记录的图片 URL 失效
**When** 系统尝试加载该图片
**Then** 图片加载失败后显示占位图标
**And** 占位图标为灰色图片icon + "图片不可用"文字
**And** 其他操作按钮保持可用(如删除记录)
