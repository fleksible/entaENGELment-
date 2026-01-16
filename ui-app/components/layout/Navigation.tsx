'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { NavItem } from '@/types';

const NAV_ITEMS: NavItem[] = [
  { id: 'home', label: 'Home', icon: '🏠', href: '/' },
  { id: 'metatron', label: 'Fokus', icon: '🎯', href: '/metatron' },
  { id: 'voidmap', label: 'VOIDs', icon: '☐', href: '/voidmap' },
  { id: 'guards', label: 'Guards', icon: '🛡️', href: '/guards' },
  { id: 'nichtraum', label: 'Nichtraum', icon: '◌', href: '/nichtraum' },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Bottom Navigation */}
      <nav className="
        fixed bottom-0 left-0 right-0 z-50
        flex justify-around items-center
        bg-zinc-900/95 backdrop-blur-sm
        border-t border-zinc-800
        pb-safe
        md:hidden
      ">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.id}
              href={item.href}
              className={`
                flex flex-col items-center justify-center
                min-w-[64px] min-h-[56px] p-2
                touch-manipulation
                transition-colors duration-150
                ${isActive
                  ? 'text-emerald-400'
                  : 'text-zinc-400 active:text-zinc-200'
                }
              `}
            >
              <span className="text-xl mb-0.5">{item.icon}</span>
              <span className="text-[10px] font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Desktop Sidebar */}
      <aside className="
        hidden md:flex md:flex-col
        fixed left-0 top-0 bottom-0
        w-64 bg-zinc-900/50
        border-r border-zinc-800
      ">
        {/* Logo / Header */}
        <div className="p-6 border-b border-zinc-800">
          <h1 className="text-lg font-semibold text-zinc-100">
            EntaENGELment
          </h1>
          <p className="text-xs text-zinc-500 mt-1">
            Guard & Void Dashboard
          </p>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 p-4 space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.id}
                href={item.href}
                className={`
                  flex items-center gap-3
                  px-4 py-3 rounded-lg
                  transition-colors duration-150
                  ${isActive
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : 'text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200'
                  }
                `}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="text-sm font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-zinc-800">
          <div className="text-xs text-zinc-600">
            FOKUS: UI-Prototyp
          </div>
        </div>
      </aside>
    </>
  );
}
