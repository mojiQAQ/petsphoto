# 日志系统说明

## 概述

PetsPhoto 后端服务已集成完整的日志系统，用于追踪应用行为、调试问题和监控性能。

## 日志配置

### 日志级别
- **开发模式 (DEBUG=True)**: `DEBUG` 级别 - 显示所有详细信息
- **生产模式 (DEBUG=False)**: `INFO` 级别 - 仅显示关键信息

### 日志输出位置

1. **控制台输出**: 实时显示所有日志
2. **文件输出**:
   - `logs/app.log` - 所有级别的日志（自动轮转，最大 10MB，保留 5 个文件）
   - `logs/error.log` - 仅错误日志（自动轮转，最大 10MB，保留 5 个文件）

## 日志格式

```
时间戳 | 级别 | 模块 | 函数:行号 | 消息
```

示例:
```
2025-11-17 01:04:33 | INFO | app | log_requests:32 | → GET /api/v1/styles/ | Client: 127.0.0.1
```

## 启动日志

应用启动时会记录关键配置信息：

```
================================================================================
应用启动 - PetsPhoto
调试模式: True
日志级别: DEBUG
图像提供商: google_ai
================================================================================
初始化数据库表...
数据库表初始化完成
应用已启动，访问地址: http://localhost:8000
API 文档: http://localhost:8000/docs
```

## HTTP 请求日志

每个 HTTP 请求都会记录：
- 请求方向（→ 进入，← 返回）
- 请求方法和路径
- 客户端 IP
- 响应状态码
- 处理时间

示例:
```
→ POST /api/v1/images/upload | Client: 127.0.0.1
← POST /api/v1/images/upload | Status: 201 | Time: 0.123s
```

## 关键业务日志

### 图片上传
```
图片上传请求 - 文件名: photo.jpg, 类型: image/jpeg
文件大小: 1024.50 KB
✓ 图片上传成功 - ID: abc-123, 尺寸: 1920x1080, 大小: 1024.50KB
```

### 图像生成任务
```
创建生成任务请求 - 源图片: abc-123, 风格: cartoon
✓ 生成任务创建成功 - ID: def-456, 风格: 卡通风格
后台生成任务已加入队列 - ID: def-456
```

### 错误日志
```
源图片不存在: invalid-id
风格不存在: invalid-style
数据库保存失败: connection timeout
```

## 查看日志

### 实时查看控制台日志
日志会直接显示在运行 uvicorn 的终端中。

### 查看日志文件

```bash
# 查看所有日志
tail -f backend/logs/app.log

# 查看最新 50 条
tail -50 backend/logs/app.log

# 查看错误日志
tail -f backend/logs/error.log

# 搜索特定内容
grep "图片上传" backend/logs/app.log
```

## 日志级别说明

- **DEBUG**: 详细的调试信息（仅开发模式）
- **INFO**: 一般信息，记录正常操作
- **WARNING**: 警告信息，不影响正常运行但需要注意
- **ERROR**: 错误信息，操作失败但应用继续运行
- **CRITICAL**: 严重错误，可能导致应用崩溃

## 第三方库日志

为减少日志噪音，以下第三方库的日志级别已调整：
- `uvicorn`: INFO
- `uvicorn.access`: WARNING（减少访问日志）
- `httpx`: WARNING
- `httpcore`: WARNING

## 配置修改

日志配置位于 [app/core/logging_config.py](app/core/logging_config.py)

可以修改的配置项：
- 日志格式
- 文件大小限制
- 保留文件数量
- 第三方库日志级别

## 性能监控

HTTP 请求日志包含处理时间，可用于性能分析：

```bash
# 查找慢请求（>1秒）
grep "Time: [1-9]\." backend/logs/app.log

# 统计某个端点的平均响应时间
grep "/api/v1/images/upload" backend/logs/app.log | grep "Time:"
```

## 故障排查

1. **应用无法启动**: 查看 `logs/error.log`
2. **API 请求失败**: 搜索对应的请求路径
3. **生成任务失败**: 搜索任务 ID
4. **性能问题**: 查看请求处理时间

## 注意事项

1. 日志文件会自动轮转，不会无限增长
2. 开发模式下日志非常详细，生产环境建议设置 `DEBUG=False`
3. 日志文件包含敏感信息，注意保护访问权限
4. 定期检查 `error.log` 以发现潜在问题
