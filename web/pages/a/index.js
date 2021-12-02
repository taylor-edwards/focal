/**
 * Login page
 *
 * Redirect authenticated users to their account page
 */

import { useRouter } from 'next/router'
import Copyright from 'components/Copyright'
import Logo from 'components/Logo'

import SignupForm from 'components/SignupForm'

const LoginPage = () => {
  const router = useRouter()
  // if user does not have a name or handle, prompt them to submit info
  // once user is authenticated, redirect to /a/account_name
  return (
    <main className="login-page">
      <article className="card">
        <Logo includeSubtext />
        <SignupForm
          onSubmit={(_e, { accountSafename }) =>
            router.push(`/a/${encodeURIComponent(accountSafename)}`)
          }
        />
      </article>
      <Copyright className="login-page--copyright" />
    </main>
  )
}

export default LoginPage
