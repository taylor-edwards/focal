export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('')
  }
  try {
    if (typeof req.body !== 'object' || !req.body.hasOwnProperty('email')) {
      return res.status(400).send('Missing email')
    }
    const { email } = req.body
    const { createSession } = require('api')
    await createSession(email)
    return res.status(201).send('{}')
  } catch (err) {
    console.warn('Could not create session:\n', err)
    res.status(503).send('Could not create session')
  }
}
