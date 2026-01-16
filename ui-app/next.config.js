/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for simple deployment
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
