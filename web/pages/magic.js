import { useRouter } from 'next/router'
import { useClientside } from 'hooks'
import Link from 'components/Link'
import SignUpForm from 'components/SignUpForm'

export const getServerSideProps = async context => {
  if (context.query.hasOwnProperty('token')) {
    try {
      const { authorizeSession } = require('api')
      const { token } = await authorizeSession(context.query.token)
      if (!token) {
        throw new Error('Invalid session token provided')
      }
      const secure = process.env.NODE_ENV === 'development' ? '' : ';Secure'
      context.res.setHeader('set-cookie', [
        `token=${encodeURIComponent(token)};max-age=31536000;HttpOnly${secure}`,
      ])
    } catch (err) {
      console.warn('Could not authorize session:\n', err)
    }
  }
  return {
    redirect: {
      destination: '/a',
      permanent: false,
    },
    props: {},
  }
}

const MagicPage = () => {
  const router = useRouter()
  useClientside(() => router.push('/a'))
  return (
    <main>
      <h1>Redirecting now...</h1>
      <Link href="/a">Click here if you&rsquo;re not automatically redirected</Link>
    </main>
  )
}

export default MagicPage
