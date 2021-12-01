/**
 * Login page
 *
 * Redirect authenticated users to their account page
 */

import { useRouter } from 'next/router'

import SignupForm from 'components/SignupForm'

const LoginPage = () => {
  const router = useRouter()
  // if user is already authenticated, immediately redirect to /a/account_name
  return (
    <main>
      <SignupForm
        onSubmit={(_e, { accountSafename }) =>
          router.push(`/a/${encodeURIComponent(accountSafename)}`)
        }
      />
    </main>
  )
}

export default LoginPage
