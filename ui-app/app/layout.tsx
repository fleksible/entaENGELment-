import type { Metadata, Viewport } from 'next';
import { Navigation } from '@/components/layout/Navigation';
import './globals.css';

export const metadata: Metadata = {
  title: 'EntaENGELment UI',
  description: 'Guard & Void Dashboard for EntaENGELment',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#09090b',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de" className="dark">
      <body className="bg-zinc-950 text-zinc-100 antialiased">
        <Navigation />

        {/* Main content area */}
        <main className="
          min-h-screen
          pb-20 md:pb-0
          md:ml-64
        ">
          <div className="max-w-5xl mx-auto p-4 md:p-6 lg:p-8">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
