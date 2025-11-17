## ADDED Requirements

### Requirement: Stripe 支付集成
系统 SHALL 集成 Stripe 作为支付处理平台。

#### Scenario: Stripe 初始化配置
- **WHEN** 后端服务启动
- **THEN** 从环境变量读取 STRIPE_SECRET_KEY 和 STRIPE_WEBHOOK_SECRET
- **AND** 初始化 Stripe SDK
- **AND** 验证 API Key 有效性（测试模式或生产模式）

#### Scenario: Stripe Checkout 会话创建
- **WHEN** 用户选择积分套餐并点击购买
- **THEN** 后端创建 Stripe Checkout Session
- **AND** 配置成功/取消回调 URL
- **AND** 返回 session_url 给前端
- **AND** 前端重定向到 Stripe 托管支付页面

#### Scenario: 支付成功回调
- **WHEN** 用户完成支付
- **THEN** Stripe 重定向到成功页面（带 session_id）
- **AND** 前端显示"支付成功"提示
- **AND** 更新用户积分余额显示

#### Scenario: 支付取消
- **WHEN** 用户取消支付
- **THEN** Stripe 重定向到取消页面
- **AND** 显示"支付已取消"提示
- **AND** 提供返回购买页面的按钮

### Requirement: Webhook 事件处理
系统 SHALL 通过 Webhook 处理 Stripe 支付事件。

#### Scenario: Webhook 签名验证
- **WHEN** 接收 Stripe Webhook 请求
- **THEN** 验证请求签名（使用 STRIPE_WEBHOOK_SECRET）
- **AND** 如果签名无效，返回 400 错误
- **AND** 如果签名有效，继续处理事件

#### Scenario: checkout.session.completed 事件
- **WHEN** 收到支付成功事件
- **THEN** 解析 session 数据（customer, amount, metadata）
- **AND** 获取用户 ID（从 metadata）
- **AND** 获取积分套餐 ID
- **AND** 增加用户积分
- **AND** 创建 Transaction 记录
- **AND** 返回 200 OK

#### Scenario: payment_intent.payment_failed 事件
- **WHEN** 收到支付失败事件
- **THEN** 记录失败日志
- **AND** 创建失败的 Transaction 记录
- **AND** 可选：发送邮件通知用户

### Requirement: 积分套餐管理
系统 SHALL 提供多种积分套餐供用户选择。

#### Scenario: 积分套餐定义
- **WHEN** MVP 阶段
- **THEN** 提供 3-4 个套餐：
  - **基础套餐**：10 积分 - $4.99
  - **热门套餐**：30 积分 - $12.99（标记为 "Most Popular"）
  - **超值套餐**：100 积分 - $39.99
  - **企业套餐**：300 积分 - $99.99

#### Scenario: 套餐列表 API
- **WHEN** 前端请求套餐列表
- **THEN** GET /api/credits/packages 返回
  ```json
  {
    "success": true,
    "data": {
      "packages": [
        {
          "id": "basic",
          "name": "基础套餐",
          "credits": 10,
          "price": 4.99,
          "currency": "USD",
          "popular": false
        },
        {
          "id": "popular",
          "name": "热门套餐",
          "credits": 30,
          "price": 12.99,
          "currency": "USD",
          "popular": true
        }
      ]
    }
  }
  ```

### Requirement: 积分余额管理
系统 SHALL 管理用户的积分余额和交易记录。

#### Scenario: 查询积分余额
- **WHEN** 用户请求积分余额
- **THEN** GET /api/credits/balance 返回当前余额
  ```json
  {
    "success": true,
    "data": {
      "balance": 25,
      "last_purchase_at": "2025-01-15T10:00:00Z"
    }
  }
  ```

#### Scenario: 积分增加
- **WHEN** 用户购买成功
- **THEN** 增加用户 credits 字段
- **AND** 使用数据库事务确保原子性
- **AND** 创建 CreditTransaction 记录（type: purchase）

#### Scenario: 积分扣除
- **WHEN** 用户生成图片
- **THEN** 扣除指定积分数
- **AND** 使用数据库事务确保原子性
- **AND** 创建 CreditTransaction 记录（type: consumption）
- **AND** 如果余额不足，回滚事务并返回错误

### Requirement: 交易记录
系统 SHALL 记录所有积分相关的交易。

#### Scenario: 交易历史查询
- **WHEN** 用户请求交易历史
- **THEN** GET /api/credits/transactions 返回
  ```json
  {
    "success": true,
    "data": {
      "transactions": [
        {
          "id": "uuid",
          "type": "purchase",
          "amount": 30,
          "balance_after": 55,
          "description": "购买热门套餐",
          "created_at": "2025-01-16T10:00:00Z"
        },
        {
          "id": "uuid",
          "type": "consumption",
          "amount": -1,
          "balance_after": 54,
          "description": "生成图片 - 卡通风格",
          "created_at": "2025-01-16T10:05:00Z"
        }
      ],
      "total": 25,
      "page": 1,
      "per_page": 20
    }
  }
  ```

### Requirement: UI 组件设计
支付相关 UI SHALL 遵循简洁设计风格，使用 shadcn/ui 组件。

#### Scenario: 积分套餐卡片
- **WHEN** 显示购买页面
- **THEN** 使用 Grid 布局（1-2 列）
- **AND** 每个套餐为 shadcn/ui Card 组件
- **AND** 卡片包含：
  - 套餐名称（Heading 3）
  - 积分数量（大号文字，突出显示）
  - 价格（primary 色，粗体）
  - "Most Popular" 徽章（if applicable）
  - 购买按钮（Button primary）
- **AND** 热门套餐卡片有不同样式（border-primary，轻微高亮）

#### Scenario: 导航栏积分显示
- **WHEN** 用户已登录
- **THEN** 在导航栏显示积分余额
- **AND** 格式："💎 25 积分"或使用 Coins 图标
- **AND** 点击跳转到购买页面
- **AND** 积分不足时显示红色提示

#### Scenario: 支付成功页面
- **WHEN** 支付完成后重定向
- **THEN** 显示成功图标（CheckCircle，绿色）
- **AND** 提示文字"支付成功！已为您充值 X 积分"
- **AND** 显示新的积分余额
- **AND** 提供"开始创作"按钮（跳转到生成器）

#### Scenario: 积分不足提示
- **WHEN** 用户积分不足时点击生成
- **THEN** 显示 Dialog 或 Toast
- **AND** 提示"积分不足，请先购买积分"
- **AND** 提供"立即购买"按钮

### Requirement: API 端点
后端 SHALL 提供积分和支付相关的 API 端点。

#### Scenario: API 端点列表
- **GET /api/credits/packages** - 获取积分套餐列表
- **POST /api/credits/purchase** - 创建支付会话
- **GET /api/credits/balance** - 查询积分余额
- **GET /api/credits/transactions** - 查询交易历史
- **POST /api/webhooks/stripe** - Stripe Webhook 回调

#### Scenario: 创建支付会话 API
- **WHEN** 前端请求创建支付
- **THEN** POST /api/credits/purchase
  ```json
  {
    "package_id": "popular"
  }
  ```
- **AND** 返回
  ```json
  {
    "success": true,
    "data": {
      "session_id": "cs_test_xxx",
      "session_url": "https://checkout.stripe.com/..."
    }
  }
  ```

### Requirement: 数据库模型
系统 SHALL 存储支付和积分相关数据。

#### Scenario: CreditPackage 表结构
- **id**: String (主键，如 "popular")
- **name**: String (套餐名称)
- **credits**: Integer (积分数量)
- **price**: Decimal (价格)
- **currency**: String (货币代码，默认 "USD")
- **stripe_price_id**: String (Stripe Price ID)
- **is_popular**: Boolean (是否热门)
- **is_active**: Boolean (是否启用)
- **sort_order**: Integer (排序)

#### Scenario: CreditTransaction 表结构
- **id**: UUID (主键)
- **user_id**: UUID (外键，关联 User)
- **type**: Enum (purchase, consumption, refund, bonus)
- **amount**: Integer (积分变动，正数为增加，负数为扣除)
- **balance_before**: Integer (交易前余额)
- **balance_after**: Integer (交易后余额)
- **description**: String (交易描述)
- **stripe_session_id**: String (Stripe Session ID，可为空)
- **stripe_payment_intent_id**: String (Stripe Payment Intent ID，可为空)
- **related_job_id**: UUID (关联的生成任务 ID，可为空)
- **metadata**: JSON (额外数据)
- **created_at**: DateTime (交易时间)

#### Scenario: StripeEvent 表结构（用于幂等性）
- **id**: UUID (主键)
- **event_id**: String (Stripe Event ID，唯一索引)
- **event_type**: String (事件类型)
- **processed**: Boolean (是否已处理)
- **payload**: JSON (事件原始数据)
- **created_at**: DateTime
- **processed_at**: DateTime (可为空)

### Requirement: 安全性
系统 SHALL 确保支付过程的安全性。

#### Scenario: 敏感信息保护
- **WHEN** 处理支付数据
- **THEN** 不存储用户信用卡信息
- **AND** 所有支付由 Stripe 托管完成
- **AND** 仅存储 Stripe Customer ID 和 Session ID

#### Scenario: Webhook 幂等性
- **WHEN** 接收重复的 Webhook 事件
- **THEN** 检查 StripeEvent 表中是否已处理
- **AND** 如果已处理，直接返回 200 OK
- **AND** 如果未处理，继续处理并标记为已处理

#### Scenario: 防止重复扣费
- **WHEN** 处理 checkout.session.completed 事件
- **THEN** 使用数据库事务
- **AND** 检查 session_id 是否已处理
- **AND** 如果已处理，跳过积分增加
- **AND** 记录日志并返回成功

### Requirement: 测试模式
系统 SHALL 支持 Stripe 测试模式，便于开发和测试。

#### Scenario: 测试模式配置
- **WHEN** 使用测试 API Key (sk_test_xxx)
- **THEN** 所有支付为测试支付
- **AND** 可以使用 Stripe 测试卡号
- **AND** 不会真实扣款

#### Scenario: 测试卡号
- **WHEN** 在测试模式下支付
- **THEN** 可以使用
  - **成功支付**：4242 4242 4242 4242
  - **支付失败**：4000 0000 0000 0002
  - **需要 3D 验证**：4000 0027 6000 3184
