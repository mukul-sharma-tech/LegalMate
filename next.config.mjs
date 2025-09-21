/** @type {import('next').NextConfig} */
const nextConfig = {
  // The option is now at the top level, not inside 'experimental'
  serverExternalPackages: ['pdf-parse'],
};

export default nextConfig;