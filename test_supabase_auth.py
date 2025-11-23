#!/usr/bin/env python3
"""
测试 Supabase 认证集成
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.supabase import supabase_jwt_verifier
from app.core.config import settings

def test_supabase_config():
    """测试 Supabase 配置"""
    print("🔍 检查 Supabase 配置...")
    print(f"  SUPABASE_URL: {settings.SUPABASE_URL}")
    print(f"  SUPABASE_JWT_SECRET: {'已配置 ✓' if settings.SUPABASE_JWT_SECRET else '❌ 未配置'}")

    if not settings.SUPABASE_URL or not settings.SUPABASE_JWT_SECRET:
        print("\n❌ Supabase 配置不完整！")
        print("请确保 .env 文件中配置了:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_JWT_SECRET")
        return False

    print("\n✅ Supabase 配置检查通过！")
    return True

def test_jwt_verifier():
    """测试 JWT 验证器初始化"""
    print("\n🔍 测试 JWT 验证器...")
    try:
        verifier = supabase_jwt_verifier
        print(f"  JWT Secret 长度: {len(verifier.jwt_secret)} 字符")
        print(f"  Supabase URL: {verifier.supabase_url}")
        print("\n✅ JWT 验证器初始化成功！")
        return True
    except Exception as e:
        print(f"\n❌ JWT 验证器初始化失败: {e}")
        return False

def test_api_endpoints():
    """测试 API 端点"""
    import requests

    print("\n🔍 测试 API 端点...")

    try:
        # 测试健康检查
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("  ✓ /health - OK")
        else:
            print(f"  ✗ /health - 失败 ({response.status_code})")

        # 测试 API 文档
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("  ✓ /docs - OK")
        else:
            print(f"  ✗ /docs - 失败 ({response.status_code})")

        # 测试 sync-user 端点（应该返回 422，因为缺少必要参数）
        response = requests.post("http://localhost:8000/api/v1/auth/sync-user", json={})
        if response.status_code == 422:
            print("  ✓ /api/v1/auth/sync-user - 端点存在")
        else:
            print(f"  ✗ /api/v1/auth/sync-user - 意外状态码 ({response.status_code})")

        print("\n✅ API 端点测试完成！")
        return True

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到后端服务！")
        print("请确保后端正在运行: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"\n❌ API 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 70)
    print("  Supabase Authentication 集成测试")
    print("=" * 70)

    tests = [
        ("配置检查", test_supabase_config),
        ("JWT 验证器", test_jwt_verifier),
        ("API 端点", test_api_endpoints),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 测试出错: {e}")
            results.append((name, False))

    print("\n" + "=" * 70)
    print("  测试结果总结")
    print("=" * 70)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name:<20} {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 70)
    if all_passed:
        print("  🎉 所有测试通过！")
        print("=" * 70)
        print("\n下一步:")
        print("  1. 访问 http://localhost:5176")
        print("  2. 尝试使用 Google 或 GitHub 登录")
        print("  3. 检查浏览器控制台是否有错误")
        print("  4. 查看后端日志确认用户同步")
    else:
        print("  ⚠️  部分测试失败，请检查上面的错误信息")
        print("=" * 70)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
