/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for simple deployment
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Keep Turbopack scoped to the UI app when the repository root also has a lockfile.
  turbopack: {
    root: __dirname,
  },
}

module.exports = nextConfig
