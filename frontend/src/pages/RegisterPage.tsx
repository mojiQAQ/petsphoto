/**
 * 注册页面
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

export function RegisterPage() {
  const navigate = useNavigate();
  const { register, signInWithGoogle, signInWithGithub } = useAuth();
  const { toast } = useToast();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOAuthLoading, setIsOAuthLoading] = useState(false);

  const validatePassword = (pwd: string): string | null => {
    if (pwd.length < 8) {
      return '密码至少需要 8 个字符';
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      toast({
        title: '输入错误',
        description: '请填写邮箱和密码',
        variant: 'destructive',
      });
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      toast({
        title: '密码不符合要求',
        description: passwordError,
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);
    try {
      await register({
        email,
        password,
        username: fullName || undefined,
      });
      toast({
        title: '注册成功',
        description: '欢迎加入宠物照片生成!',
      });
      navigate('/generator');
    } catch (error) {
      toast({
        title: '注册失败',
        description: error instanceof Error ? error.message : '注册失败,请稍后重试',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleRegister = async () => {
    setIsOAuthLoading(true);
    try {
      await signInWithGoogle();
      // OAuth 会重定向，所以这里不需要额外的导航
    } catch (error) {
      toast({
        title: 'Google 注册失败',
        description: error instanceof Error ? error.message : '请稍后重试',
        variant: 'destructive',
      });
      setIsOAuthLoading(false);
    }
  };

  const handleGithubRegister = async () => {
    setIsOAuthLoading(true);
    try {
      await signInWithGithub();
      // OAuth 会重定向，所以这里不需要额外的导航
    } catch (error) {
      toast({
        title: 'GitHub 注册失败',
        description: error instanceof Error ? error.message : '请稍后重试',
        variant: 'destructive',
      });
      setIsOAuthLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-8">
        <div className="space-y-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold">注册</h1>
            <p className="text-muted-foreground mt-2">
              创建你的宠物照片生成账号
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                邮箱地址
              </label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isLoading}
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                密码
              </label>
              <Input
                id="password"
                type="password"
                placeholder="至少 8 个字符"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
                required
              />
              {password && (
                <p className={`text-xs ${
                  validatePassword(password)
                    ? 'text-destructive'
                    : 'text-green-600'
                }`}>
                  {validatePassword(password) || '密码强度良好'}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <label htmlFor="fullName" className="text-sm font-medium">
                姓名 <span className="text-muted-foreground">(可选)</span>
              </label>
              <Input
                id="fullName"
                type="text"
                placeholder="你的姓名"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                disabled={isLoading}
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? '注册中...' : '注册'}
            </Button>
          </form>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">
                或使用社交账号注册
              </span>
            </div>
          </div>

          <div className="space-y-3">
            <Button
              variant="outline"
              className="w-full"
              onClick={handleGoogleRegister}
              disabled={isOAuthLoading || isLoading}
            >
              <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              {isOAuthLoading ? '跳转中...' : '使用 Google 注册'}
            </Button>

            <Button
              variant="outline"
              className="w-full"
              onClick={handleGithubRegister}
              disabled={isOAuthLoading || isLoading}
            >
              <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              {isOAuthLoading ? '跳转中...' : '使用 GitHub 注册'}
            </Button>
          </div>

          <div className="text-center text-sm">
            <span className="text-muted-foreground">已有账号? </span>
            <Link
              to="/login"
              className="text-primary hover:underline font-medium"
            >
              立即登录
            </Link>
          </div>
        </div>
      </Card>
    </div>
  );
}
