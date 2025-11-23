/**
 * OAuth 回调页面
 * 处理 Google 和 GitHub OAuth 登录后的重定向
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '@/lib/supabase';
import { Card } from '@/components/ui/card';

export function AuthCallbackPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 处理 OAuth 回调
    const handleCallback = async () => {
      try {
        // Supabase 会自动处理 URL 中的认证参数并创建 session
        const { data, error } = await supabase.auth.getSession();

        if (error) {
          console.error('OAuth 回调错误:', error);
          setError(error.message);
          // 3 秒后重定向到登录页
          setTimeout(() => {
            navigate('/login');
          }, 3000);
          return;
        }

        if (data.session) {
          // 认证成功，重定向到首页
          navigate('/');
        } else {
          // 没有 session，可能是用户取消了登录
          setError('认证失败，请重试');
          setTimeout(() => {
            navigate('/login');
          }, 3000);
        }
      } catch (err) {
        console.error('处理 OAuth 回调时出错:', err);
        setError('发生未知错误，请重试');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    };

    handleCallback();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <Card className="w-full max-w-md p-8 text-center">
        {error ? (
          <>
            <div className="mb-4">
              <svg
                className="mx-auto h-12 w-12 text-red-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              认证失败
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
            <p className="text-sm text-gray-500">正在返回登录页...</p>
          </>
        ) : (
          <>
            <div className="mb-4">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              正在处理登录...
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              请稍候，我们正在验证您的身份
            </p>
          </>
        )}
      </Card>
    </div>
  );
}
