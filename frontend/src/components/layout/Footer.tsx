import { Container } from "@/components/layout/Container"

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t bg-background">
      <Container>
        <div className="py-8 md:py-12">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {/* Brand */}
            <div>
              <h3 className="text-lg font-semibold">PetsPhoto</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                AI 驱动的宠物头像生成器
              </p>
            </div>

            {/* Links */}
            <div>
              <h4 className="text-sm font-semibold">快速链接</h4>
              <ul className="mt-3 space-y-2 text-sm">
                <li>
                  <a
                    href="/about"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    关于我们
                  </a>
                </li>
                <li>
                  <a
                    href="/privacy"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    隐私政策
                  </a>
                </li>
                <li>
                  <a
                    href="/terms"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    服务条款
                  </a>
                </li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="text-sm font-semibold">联系我们</h4>
              <p className="mt-3 text-sm text-muted-foreground">
                support@petsphoto.com
              </p>
            </div>
          </div>

          {/* Copyright */}
          <div className="mt-8 border-t pt-6">
            <p className="text-center text-sm text-muted-foreground">
              © {currentYear} PetsPhoto. All rights reserved.
            </p>
          </div>
        </div>
      </Container>
    </footer>
  )
}
