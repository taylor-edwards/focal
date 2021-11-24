/**
 * Login page
 *
 * Redirect authenticated users to their account page
 */

import { useRouter } from 'next/router'

import LoginForm from 'components/LoginForm'

const LoginPage = () => {
  const router = useRouter()
  // if user is already authenticated, immediately redirect to /a/account_name
  return (
    <main>
      <LoginForm
        onSubmit={(_e, { accountName }) => router.push(`/a/${accountName}`)}
      />
    </main>
  )
}

export default LoginPage
