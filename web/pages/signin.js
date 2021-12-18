import Link from 'components/Link'

export const getServerSideProps = async context => {
  try {
    const { verifySession } = require('api')
    if (context.query.hasOwnProperty('token')) {
      const { token } = await verifySession(context.query.token)
      return {
        props: {
          token,
        },
      }
    }
  } catch (err) {
    console.warn('Could not verify session:\n', err)
  }
  return {
    props: {},
    // redirect: '/',
  }
}

const SignInPage = ({ token }) => {
  console.log({ token })
  return (
    <div>
      <h1>Signing you in...</h1>
      <Link href="/a">Click here if you are not automatically redirected</Link>
    </div>
  )
}

export default SignInPage
