import Link from 'components/Link'

export const getServerSideProps = async context => {
  const { authenticateSession } = require('api')
  const { fetchAccount } = require('queries')
  const session = await authenticateSession(context.params.token)
  const account = await fetchAccount(session.accountSafename)
  return {
    props: {
      session,
      account,
    },
    // redirect: `/a/${account.safename}`,
  }
}

const Magic = () => {
  return (
    <div>
      <h1>Signing you in...</h1>
      <Link href="/a">Click here if you are not automatically redirected</Link>
    </div>
  )
}

export default Magic
