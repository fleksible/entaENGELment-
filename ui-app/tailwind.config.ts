import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for EntaENGELment
        void: {
          open: '#fbbf24',      // amber-400
          progress: '#3b82f6',  // blue-500
          closed: '#22c55e',    // green-500
        },
        guard: {
          ok: '#10b981',        // emerald-500
          warning: '#f59e0b',   // amber-500
          error: '#ef4444',     // red-500
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'focus-switch': 'focusSwitch 0.5s ease-in-out infinite',
      },
      keyframes: {
        focusSwitch: {
          '0%, 100%': {
            borderColor: 'rgb(239 68 68)',
            boxShadow: '0 0 0 0 rgb(239 68 68 / 0.4)'
          },
          '50%': {
            borderColor: 'rgb(239 68 68)',
            boxShadow: '0 0 20px 4px rgb(239 68 68 / 0.6)'
          },
        },
      },
    },
  },
  plugins: [],
}
export default config
