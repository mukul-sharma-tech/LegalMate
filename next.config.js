/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/',
        destination: 'https://legal-mcci.vercel.app/',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig
