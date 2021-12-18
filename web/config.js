module.exports = {
  FLASK_BASE: 'http://api:5000',
  API_BASE: process.env.NODE_ENV === 'development' ?
                           'http://api.local.pics' : 'https://api.focal.pics',
  DEFAULT_TIMEOUT: 5000,
}
