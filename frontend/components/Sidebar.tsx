import { LayoutDashboard, MessageSquare, GitMerge, ShieldAlert, Settings } from "lucide-react";
import Link from "next/link";

export default function Sidebar() {
  const menuItems = [
    { icon: LayoutDashboard, label: "Command Center", href: "/" },
    { icon: MessageSquare, label: "AI Console", href: "/console" },
    { icon: GitMerge, label: "Resolution", href: "/resolution" },
    { icon: ShieldAlert, label: "Safety Suite", href: "/safety" },
    { icon: Settings, label: "Settings", href: "/settings" },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900 flex flex-col">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-brand-primary">OpenClaw</h1>
        <p className="text-xs text-slate-400">Conflict Resolution OS</p>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <Link 
            key={item.href} 
            href={item.href}
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition-colors text-slate-300 hover:text-white"
          >
            <item.icon size={20} />
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500 text-center">
        v0.1.0-alpha
      </div>
    </aside>
  );
}
