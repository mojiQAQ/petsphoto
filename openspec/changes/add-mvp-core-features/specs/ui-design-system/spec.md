## ADDED Requirements

### Requirement: shadcn/ui 初始化和配置
系统 SHALL 在前端项目中正确集成和配置 shadcn/ui 组件库。

#### Scenario: shadcn/ui 安装和初始化
- **WHEN** 首次设置前端项目
- **THEN** 运行 `npx shadcn-ui@latest init`
- **AND** 选择配置：
  - Style: Default
  - Base color: Slate 或 Zinc（中性灰色系）
  - CSS variables: Yes
- **AND** 生成配置文件：`components.json`, `tailwind.config.ts`, `globals.css`

#### Scenario: 基础组件安装
- **WHEN** MVP 阶段初始化
- **THEN** 安装核心组件：
  ```bash
  npx shadcn-ui@latest add button
  npx shadcn-ui@latest add card
  npx shadcn-ui@latest add input
  npx shadcn-ui@latest add dialog
  npx shadcn-ui@latest add toast
  npx shadcn-ui@latest add progress
  npx shadcn-ui@latest add skeleton
  npx shadcn-ui@latest add dropdown-menu
  npx shadcn-ui@latest add tabs
  ```
- **AND** 组件安装到 `src/components/ui/` 目录

### Requirement: 主题配置
系统 SHALL 配置符合简洁欧美风格的主题。

#### Scenario: CSS 变量配置
- **WHEN** 配置主题
- **THEN** 在 `globals.css` 中定义 CSS 变量：
  ```css
  @layer base {
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --card: 0 0% 100%;
      --card-foreground: 222.2 84% 4.9%;
      --primary: 221.2 83.2% 53.3%;  /* 现代蓝色 */
      --primary-foreground: 210 40% 98%;
      --muted: 210 40% 96.1%;
      --muted-foreground: 215.4 16.3% 46.9%;
      --border: 214.3 31.8% 91.4%;
      --radius: 0.5rem;  /* 8px */
    }

    .dark {
      --background: 222.2 84% 4.9%;
      --foreground: 210 40% 98%;
      /* ... 深色模式变量 */
    }
  }
  ```

#### Scenario: Tailwind 配置
- **WHEN** 配置 Tailwind
- **THEN** 在 `tailwind.config.ts` 中扩展主题：
  ```typescript
  export default {
    content: ["./index.html", "./src/**/*.{ts,tsx}"],
    theme: {
      extend: {
        colors: {
          border: "hsl(var(--border))",
          background: "hsl(var(--background))",
          // ...
        },
        borderRadius: {
          lg: "var(--radius)",
          md: "calc(var(--radius) - 2px)",
          sm: "calc(var(--radius) - 4px)",
        },
      },
    },
    plugins: [require("tailwindcss-animate")],
  }
  ```

### Requirement: 浅色/深色模式切换
系统 SHALL 支持用户切换浅色和深色主题。

#### Scenario: 主题 Provider 设置
- **WHEN** 应用初始化
- **THEN** 创建 ThemeProvider 组件
- **AND** 使用 React Context 管理主题状态
- **AND** 从 localStorage 读取用户偏好
- **AND** 应用 `.dark` 类到 `<html>` 元素

#### Scenario: 主题切换按钮
- **WHEN** 用户点击主题切换按钮
- **THEN** 切换 浅色 ↔ 深色
- **AND** 保存偏好到 localStorage
- **AND** 平滑过渡动画（transition-colors duration-200）

#### Scenario: 系统主题跟随
- **WHEN** 用户选择"跟随系统"
- **THEN** 使用 `window.matchMedia('(prefers-color-scheme: dark)')`
- **AND** 监听系统主题变化
- **AND** 自动切换

### Requirement: 字体配置
系统 SHALL 使用现代、清晰的字体栈。

#### Scenario: 西文字体
- **WHEN** 显示西文内容
- **THEN** 使用字体栈：
  ```css
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
               'Helvetica Neue', Arial, sans-serif;
  ```
- **AND** 如果使用 Inter，通过 Google Fonts 或本地引入

#### Scenario: 中文字体
- **WHEN** 显示中文内容
- **THEN** 使用字体栈：
  ```css
  font-family: 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei',
               '微软雅黑', sans-serif;
  ```

#### Scenario: 字体加载优化
- **WHEN** 加载 Web 字体
- **THEN** 使用 `font-display: swap`
- **AND** 预加载关键字体文件
- **AND** 使用系统字体作为降级

### Requirement: 图标系统
系统 SHALL 使用 Lucide React 图标库。

#### Scenario: 图标库安装
- **WHEN** 安装依赖
- **THEN** 运行 `npm install lucide-react`
- **AND** 在组件中按需导入图标

#### Scenario: 图标使用规范
- **WHEN** 使用图标
- **THEN** 统一使用 Lucide 图标（不混用其他图标库）
- **AND** 图标尺寸：`className="w-4 h-4"` (16px) 或 `w-5 h-5` (20px)
- **AND** 图标颜色：继承文字颜色或使用 `text-muted-foreground`
- **AND** 添加 `aria-label` 或 `aria-hidden="true"`

#### Scenario: 常用图标列表
- **Upload** - 上传
- **Download** - 下载
- **Sparkles** - 生成/魔法
- **RefreshCw** - 刷新/重新生成
- **User** - 用户
- **LogOut** - 登出
- **Settings** - 设置
- **Sun** - 浅色模式
- **Moon** - 深色模式
- **CheckCircle** - 成功
- **XCircle** - 错误
- **AlertCircle** - 警告
- **Coins** - 积分

### Requirement: 响应式布局组件
系统 SHALL 提供响应式布局组件和工具类。

#### Scenario: Container 组件
- **WHEN** 创建页面容器
- **THEN** 使用 `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **AND** 最大宽度 1280px
- **AND** 左右内边距：移动端 16px，桌面端 32px

#### Scenario: Grid 布局
- **WHEN** 创建网格布局
- **THEN** 使用 Tailwind grid 类
- **AND** 常用模式：`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`

#### Scenario: 断点使用
- **WHEN** 编写响应式样式
- **THEN** 遵循 Mobile First
- **AND** 使用 Tailwind 断点：sm (640px), md (768px), lg (1024px), xl (1280px)

### Requirement: 通用组件样式规范
系统 SHALL 为常用组件定义统一的样式规范。

#### Scenario: 按钮样式
- **WHEN** 使用 Button 组件
- **THEN** 提供 variants：
  - **default (primary)**: 填充背景，主题色
  - **secondary**: 边框样式，透明背景
  - **ghost**: 无边框，hover 时背景变化
  - **destructive**: 红色，用于删除等危险操作
- **AND** 提供 sizes：sm, default, lg
- **AND** loading 状态：显示 Spinner + 禁用

#### Scenario: 输入框样式
- **WHEN** 使用 Input 组件
- **THEN** 高度 h-10 (40px)
- **AND** 边框 border border-input
- **AND** focus 状态：ring-2 ring-primary
- **AND** 错误状态：border-destructive
- **AND** 占位符：text-muted-foreground

#### Scenario: 卡片样式
- **WHEN** 使用 Card 组件
- **THEN** 背景：bg-card
- **AND** 边框：border
- **AND** 圆角：rounded-lg (8px)
- **AND** 阴影：shadow-sm，hover 时 shadow-md
- **AND** 内边距：p-6

### Requirement: 动画和过渡
系统 SHALL 使用微妙的动画增强用户体验。

#### Scenario: 过渡动画
- **WHEN** 元素状态变化
- **THEN** 使用 `transition-colors duration-200`
- **AND** 缓动函数：ease-in-out
- **AND** 避免过度动画

#### Scenario: 悬停效果
- **WHEN** 鼠标悬停在交互元素上
- **THEN** 按钮：轻微缩放 `hover:scale-105` 或背景变化
- **AND** 卡片：阴影加深 `hover:shadow-md`
- **AND** 链接：下划线或颜色变化

#### Scenario: 加载动画
- **WHEN** 显示加载状态
- **THEN** 使用 shadcn/ui Skeleton 组件
- **AND** 或使用 Spinner（旋转动画）
- **AND** 动画流畅，fps >= 60

### Requirement: 无障碍性 (Accessibility)
系统 SHALL 符合 WCAG 2.1 AA 标准。

#### Scenario: 颜色对比度
- **WHEN** 设计 UI
- **THEN** 文字与背景对比度 >= 4.5:1（正文）
- **AND** 大号文字对比度 >= 3:1
- **AND** 交互元素边界清晰可见

#### Scenario: 键盘导航
- **WHEN** 用户使用键盘
- **THEN** 所有交互元素可通过 Tab 键访问
- **AND** focus 状态清晰可见（ring-2）
- **AND** 支持 Enter/Space 触发操作

#### Scenario: 屏幕阅读器支持
- **WHEN** 使用辅助技术
- **THEN** 所有图片有 alt 属性
- **AND** 图标有 aria-label
- **AND** 表单有 label 关联
- **AND** Dialog 有正确的 aria-modal

### Requirement: 错误和成功状态
系统 SHALL 提供清晰的状态反馈。

#### Scenario: Toast 通知
- **WHEN** 操作完成或失败
- **THEN** 使用 shadcn/ui Toast 组件
- **AND** 成功：绿色 + CheckCircle 图标
- **AND** 错误：红色 + XCircle 图标
- **AND** 警告：黄色 + AlertCircle 图标
- **AND** 自动关闭（3-5 秒）

#### Scenario: 表单验证反馈
- **WHEN** 表单字段验证失败
- **THEN** 字段边框变红 `border-destructive`
- **AND** 下方显示错误文字（红色，小号）
- **AND** 实时验证（onChange）

### Requirement: 空状态设计
系统 SHALL 为空状态提供友好的提示。

#### Scenario: 空状态组件
- **WHEN** 列表或画廊为空
- **THEN** 显示居中的空状态
- **AND** 包含图标（大号，灰色）
- **AND** 提示文字："还没有记录"
- **AND** CTA 按钮："创建第一个"

### Requirement: Loading 状态
系统 SHALL 为异步操作提供加载状态。

#### Scenario: 骨架屏
- **WHEN** 加载列表或卡片
- **THEN** 使用 shadcn/ui Skeleton 组件
- **AND** 模拟实际内容的布局
- **AND** 动画脉冲效果

#### Scenario: 进度条
- **WHEN** 显示上传或生成进度
- **THEN** 使用 shadcn/ui Progress 组件
- **AND** 实时更新百分比
- **AND** 平滑动画

### Requirement: 移动端优化
系统 SHALL 在移动设备上提供良好体验。

#### Scenario: 触摸目标大小
- **WHEN** 设计移动端 UI
- **THEN** 按钮最小高度 44px
- **AND** 点击区域足够大
- **AND** 间距适当，避免误触

#### Scenario: 导航栏适配
- **WHEN** 移动端显示导航栏
- **THEN** 使用汉堡菜单（Menu 图标）
- **AND** 点击展开全屏或侧边抽屉
- **AND** 使用 shadcn/ui Sheet 组件

#### Scenario: 表单适配
- **WHEN** 移动端填写表单
- **THEN** 输入框宽度占满
- **AND** 使用合适的输入类型（email, tel, number）
- **AND** 避免横向滚动

### Requirement: 性能优化
系统 SHALL 优化 UI 渲染性能。

#### Scenario: 组件懒加载
- **WHEN** 组件较大或不常用
- **THEN** 使用 React.lazy 和 Suspense
- **AND** 代码分割，减小初始包体积

#### Scenario: 图片优化
- **WHEN** 显示图片
- **THEN** 使用现代格式（WebP）
- **AND** 响应式图片（srcset）
- **AND** 懒加载（loading="lazy"）

### Requirement: 开发工具和规范
系统 SHALL 配置开发工具确保代码质量。

#### Scenario: ESLint 和 Prettier
- **WHEN** 编写代码
- **THEN** 使用 ESLint 检查代码质量
- **AND** 使用 Prettier 格式化代码
- **AND** 配置 pre-commit hook

#### Scenario: TypeScript 严格模式
- **WHEN** 配置 TypeScript
- **THEN** 启用严格模式
- **AND** 所有组件 props 有类型定义
- **AND** 避免使用 any

#### Scenario: 组件文档
- **WHEN** 创建可复用组件
- **THEN** 添加 JSDoc 注释
- **AND** 说明 props 和用法
- **AND** 提供使用示例
