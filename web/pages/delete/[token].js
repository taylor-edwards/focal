import Link from 'components/Link'

export const getServerSideProps = async context => {
  const { deleteAccount } = require('api')
  try {
    const account = await deleteAccount(context.params.token)
    return {
      props: {},
      redirect: '/',
    }
  } catch (err) {
    console.error(err)
    return {
      props: {
        error: err,
      }
    }
  }
}

const DeleteAccount = ({ error }) => {
  return (
    <div>
      <h1>Deleting your account...</h1>
      {error && <p>{error}</p>}
      <Link href="/">Click here if you are not automatically redirected</Link>
    </div>
  )
}

export default DeleteAccount
