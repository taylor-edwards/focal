const { FLASK_BASE } = require('./config')

module.exports = {
  reactStrictMode: true,
  async rewrites() {
    // Enable unauthorized access to certain Flask APIs by proxying them
    // through here to the internal network. Do not add to this list unless
    // the endpoint must be anonymously accessible on the public internet.
    return [
      {
        source: '/api/file_support',
        destination: `${FLASK_BASE}/config/supported_file_extensions`,
      },
      {
        source: `/api/session`,
        destination: `${FLASK_BASE}/session`,
      },
    ]
  },
}
