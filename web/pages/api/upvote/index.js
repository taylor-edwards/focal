import { FLASK_ENDPOINT } from 'config'

export default function handler(req, res) {
  if (req.method !== 'PUT') {
    return res.status(405).send('')
  }
  const controller = new AbortController()
  const timer = setTimeout(
    () => controller.abort(),
    FLASK_ENDPOINT.DEFAULT_TIMEOUT,
  )
  return fetch(`${FLASK_ENDPOINT.BASE}/upvote`, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'PUT',
    body: JSON.stringify(req.body),
    signal: controller.signal,
  }).then(response => {
    if (response.ok) {
      res.status(response.status).json(response.body)
    } else {
      res.status(response.status).send('')
    }
  }).catch(err => {
    console.log(
      'Caught exception on PUT to /upvote',
      JSON.stringify(req.body),
      err,
    )
    res.status(503).send('')
  }).finally(() => {
    clearTimeout(timer)
  })
}
