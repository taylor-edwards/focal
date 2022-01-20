import { useRouter } from 'next/router'
import { useClientside } from 'hooks'
import Link from 'components/Link'
import SignUpForm from 'components/SignUpForm'

export const getServerSideProps = async context => {
  try {
    const { parseCookie } = require('utils')
    const { deleteSession } = require('api')
    const cookieOptions = [
      `token=`,
      'path=/',
      'HttpOnly',
      'max-age=0',
      `expires=Thu, 01 Jan 1970 00:00:00 GMT`,
      `domain=${context.req.headers.host}`,
    ]
    context.res.setHeader('set-cookie', cookieOptions.join(';'))
    const token = parseCookie(context.req.headers.cookie)
    if (token) {
      await deleteSession(token)
    }
  } catch (err) {
    console.warn('Could not delete session:\n', err)
  }
  return {
    redirect: {
      destination: '/',
      permanent: false,
    },
    props: {},
  }
}

const LogoutPage = () => {
  const router = useRouter()
  useClientside(() => router.push('/'))
  return (
    <main>
      <h1>Redirecting now...</h1>
      <Link href="/">Click here if you&rsquo;re not automatically redirected</Link>
    </main>
  )
}

export default LogoutPage
