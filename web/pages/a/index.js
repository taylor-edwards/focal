/**
 * Account sign-up, sign-in and management page
 */

export const getServerSideProps = async context => {
  try {
    const { parseCookie } = require('utils')
    const { getAccountDetails, getSession } = require('api')
    const token = parseCookie(context.req.headers.cookie)
    if (token) {
      const { account = null } = await getAccountDetails(token)
      const { session = null } = await getSession(token)
      return {
        props: {
          account,
          session,
        },
      }
    }
  } catch (err) {
    console.warn('Could not find account:\n', err)
  }
  return {
    props: {},
  }
}

import { useState } from 'react'
import Logo from 'components/Logo'
import SignInForm from 'components/SignInForm'
import SignUpForm from 'components/SignUpForm'
import styles from 'styles/Account.module.css'

const PersonalAccountPage = ({ account, session }) => {
  const [magicLinkSent, setMagicLinkSent] = useState(false)
  const showSignin = !session
  const showAccountSetup = !showSignin && !account
  const showAccount = !!account
  return (
    <section className={styles.page}>
      {!showAccount && <Logo includeSubtext className={styles.logo} />}

      {showSignin && (
        <>
          {!magicLinkSent && (
            <SignInForm onSuccess={() => setMagicLinkSent(true)} />
          )}
          {magicLinkSent && (
            <>
              <h1>Email sent</h1>
              <p>Check your email for a link to finish signing in</p>
            </>
          )}
        </>
      )}

      {showAccountSetup && (
        <>
          <h1>Account details</h1>
          <p>Finish setting up your account on Focal.</p>
          <SignUpForm />
        </>
      )}

      {showAccount && (
        <>
          <h1>Your Account</h1>
          <p>Name: {account.name}</p>
          <p>Handle: {account.handle}</p>
          <p>Email: {account.email}</p>
        </>
      )}
    </section>
  )
}

export default PersonalAccountPage
