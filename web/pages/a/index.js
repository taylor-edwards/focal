/**
 * Login page
 *
 * Redirect authenticated users to their account page
 */

import { useState } from 'react'
import { useRouter } from 'next/router'
import Copyright from 'components/Copyright'
import DocumentFill from 'components/DocumentFill'
import Logo from 'components/Logo'

import SignInForm from 'components/SignInForm'
import SignUpForm from 'components/SignUpForm'

const AuthenticationPage = () => {
  const router = useRouter()
  // if user does not have a name or handle, prompt them to submit info
  // once user is authenticated, redirect to /a/account_name
  const [magicLinkSent, setMagicLinkSent] = useState(false)
  return (
    <>
      <DocumentFill />
      <main className="login-page">
        <article className="card col">
          <Logo includeSubtext />
          <SignUpForm
            onSuccess={({ accountSafename }) =>
              router.push(`/a/${encodeURIComponent(accountSafename)}`)
            }
          />
          {!magicLinkSent && (
            <SignInForm onSuccess={() => setMagicLinkSent(true)} />
          )}
          {magicLinkSent && (
            <p>Check your email for a sign in link</p>
          )}
        </article>
      </main>
      <Copyright />
    </>
  )
}

export default AuthenticationPage
