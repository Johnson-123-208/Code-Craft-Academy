/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  experimental: {
    optimizePackageImports: ["lucide-react", "@monaco-editor/react"],
    serverComponentsExternalPackages: ["shiki", "mermaid"],
  },
  images: {
    remotePatterns: [],
  },
  webpack: (config) => {
    config.resolve.alias.canvas = false;
    return config;
  },
};

export default nextConfig;
