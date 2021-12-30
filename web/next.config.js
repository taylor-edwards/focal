const { PRIVATE_API } = require('./config')

module.exports = {
  reactStrictMode: true,
  async rewrites() {
    const routes = []
    if (process.env.NODE_ENV === 'development') {
      routes.push({
        source: '/api/graphql',
        destination: `${PRIVATE_API}/graphql`,
      })
    }
    return routes
  },
}
