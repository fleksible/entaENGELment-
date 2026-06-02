const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for simple deployment
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Point Turbopack at the pnpm workspace root: in a pnpm monorepo the virtual
  // store (node_modules/.pnpm) lives at the repo root, so `next` and friends are
  // only resolvable when the root encompasses it.
  turbopack: {
    root: path.join(__dirname, '..'),
  },
}

module.exports = nextConfig
