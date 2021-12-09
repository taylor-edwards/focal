/**
 * Login page
 *
 * Redirect authenticated users to their account page
 */

import { useRouter } from 'next/router'
import Copyright from 'components/Copyright'
import DocumentFill from 'components/DocumentFill'
import Logo from 'components/Logo'

import SignupForm from 'components/SignupForm'

const LoginPage = () => {
  const router = useRouter()
  // if user does not have a name or handle, prompt them to submit info
  // once user is authenticated, redirect to /a/account_name
  return (
    <>
      <DocumentFill />
      <main className="login-page">
        <article className="card">
          <Logo includeSubtext />
          <SignupForm
            onSubmit={(_e, { accountSafename }) =>
              router.push(`/a/${encodeURIComponent(accountSafename)}`)
            }
          />
        </article>
      </main>
      <Copyright />
    </>
  )
}

export default LoginPage
