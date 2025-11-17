/**
 * 首页
 */
import { Container } from "@/components/layout/Container";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Sparkles, Upload, Palette } from "lucide-react";
import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <>
      {/* Hero Section */}
      <section className="py-20 md:py-28">
        <Container>
          <div className="flex flex-col items-center text-center">
            <div className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm mb-8">
              <Sparkles className="h-4 w-4" />
              <span>AI 驱动的宠物头像生成</span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold max-w-3xl mb-6">
              为你的宠物创造
              <span className="text-primary"> 独特艺术头像</span>
            </h1>

            <p className="text-lg text-muted-foreground max-w-2xl mb-10">
              上传宠物照片，选择艺术风格，让 AI 为你的毛孩子生成个性化的艺术头像
            </p>

            <div className="flex gap-4">
              <Link to="/generator">
                <Button size="lg" className="gap-2">
                  <Sparkles className="h-4 w-4" />
                  开始创作
                </Button>
              </Link>
              <Button size="lg" variant="outline">
                查看示例
              </Button>
            </div>
          </div>
        </Container>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/50">
        <Container>
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">如何使用</h2>
            <p className="text-muted-foreground">
              三步即可获得专属宠物头像
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <div className="mb-4 inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10">
                  <Upload className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>上传照片</CardTitle>
                <CardDescription>
                  上传你宠物的清晰照片
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  支持 JPG、PNG 格式，文件大小不超过 10MB
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-4 inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10">
                  <Palette className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>选择风格</CardTitle>
                <CardDescription>
                  从多种艺术风格中选择
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  卡通、油画、水彩、像素艺术等多种风格可选
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-4 inline-flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10">
                  <Sparkles className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>AI 生成</CardTitle>
                <CardDescription>
                  获取专属艺术头像
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  AI 将在几秒钟内生成高质量的艺术头像
                </p>
              </CardContent>
            </Card>
          </div>
        </Container>
      </section>
    </>
  );
}
