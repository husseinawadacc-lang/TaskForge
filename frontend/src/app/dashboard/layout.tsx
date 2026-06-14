
"use client"
import Link from "next/link"
import { LayoutDashboard, CheckSquare, CreditCard,Folder, Bell,Sparkles, User } from "lucide-react"
import { usePathname } from "next/navigation"
import { Toaster } from "react-hot-toast"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  const navItems = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Tasks",
    href: "/dashboard/tasks",
    icon: CheckSquare,
  },
  {
    name: "Projects",
    href: "/dashboard/projects",
    icon: Folder,
  },
  {
    name: "Notifications",
    href: "/dashboard/notifications",
    icon: Bell,
  },
  {
    name: "AI Assistant",
    href: "/dashboard/ai",
    icon: Sparkles,
  },
  {
    name: "Billing",
    href: "/dashboard/billing",
    icon: CreditCard,
  },
  {
    name: "Profile",
    href: "/dashboard/profile",
    icon: User,
  }
]
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white p-4">
        <h1 className="text-xl font-bold mb-6">TaskForge</h1>

        <ul className="space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href

            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 p-2 rounded-lg transition ${
                    isActive
                      ? "bg-gray-700"
                      : "hover:bg-gray-800"
                  }`}
                >
                  <item.icon size={18} />
                  {item.name}
                </Link>
              </li>
            )
          })}
        </ul>
      </div>

      {/* Main */}
      <div className="flex-1 bg-gray-100">
        {/* Topbar */}
        <div className="bg-white px-6 py-4 shadow flex justify-between items-center">
          {/* Page Title */}
          <h2 className="text-lg font-semibold">Dashboard</h2>

          {/* Profile */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">Hussein</span>

            <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white">
              H
            </div>
          </div>
        </div>


        {/* Content */}
        <div className="p-6">
          
          {children}
          <Toaster position="top-right" />
          
        </div>
      </div>
    </div>
  )
}