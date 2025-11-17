import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Container } from "@/components/layout/Container"
import { ThemeToggle } from "@/components/theme-toggle"
import { Menu, Sparkles, LogOut, User, Coins } from "lucide-react"
import { useAuth } from "@/contexts/AuthContext"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
  }

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <Container>
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-xl font-semibold">PetsPhoto</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className="text-sm font-medium text-foreground/60 transition-colors hover:text-foreground"
            >
              首页
            </Link>
            <Link
              to="/generator"
              className="text-sm font-medium text-foreground/60 transition-colors hover:text-foreground"
            >
              生成器
            </Link>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            <ThemeToggle />

            {isAuthenticated && user ? (
              <div className="hidden md:flex items-center gap-4">
                {/* Credits Display */}
                <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                  <Coins className="h-4 w-4" />
                  <span>{user.credits} 积分</span>
                </div>

                {/* User Dropdown */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm" className="gap-2">
                      <User className="h-4 w-4" />
                      <span>{user.email}</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>我的账号</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={handleLogout} className="text-destructive">
                      <LogOut className="h-4 w-4 mr-2" />
                      退出登录
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link to="/login">
                  <Button variant="ghost" size="sm">登录</Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">注册</Button>
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </Container>
    </nav>
  )
}
