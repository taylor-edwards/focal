/**
 * Account/profile canonical page
 */

import { useRouter } from 'next/router'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  const { fetchAccount } = require('queries')
  try {
    // pre-render only public profile pages
    const accountSafename = context.params?.account_safename
    const response = await fetchAccount({ accountSafename })
    if (!response || response.data.account === null) {
      throw new Error('Account not found')
    }
    return {
      props: {
        account: response.data.account,
      },
      revalidate: 60,
    }
  } catch (err) {
    console.warn(
      'Issuing 404 for account page',
      JSON.stringify({ params: context.params }),
      err.message,
    )
    return {
      notFound: true,
      revalidate: 30,
    }
  }
}

export const getStaticPaths = async () => {
  try {
    const { fetchAccounts } = require('queries')
    const response = await fetchAccounts()
    return {
      paths: response.data.accounts.map(
        ({ accountSafename }) => `/a/${encodeURIComponent(accountSafename)}`),
      fallback: true,
    }
  } catch (err) {
    console.warn('Caught error fetching all accounts:', err)
  }
  return {
    paths: [],
    fallback: true,
  }
}

const AccountPage = ({ account }) => {
  const router = useRouter()
  if (router.isFallback) {
    return <Loading />
  }
  // If logged in user is the same as account, fetch the account details via
  // GET /api/a/{accountSafename} with a valid session cookie
  // Account page
  return (
    <div>
      <h1>Account</h1>
      {account && <p>{account.name}</p>}
      {account.email && <p>{account.email}</p>}
      {account.createdAt && (
        <p>Member since {new Date(account.createdAt).getFullYear()}</p>
      )}
      {account.photos && account.photos.length > 0 ? (
        <ul>
          <p className="subheading">Photos</p>
          {account.photos.map(photo => (
            <li key={photo.id}>
              <p>{photo.title}</p>
              {photo.previewFile && (
                <img
                  src={photo.previewFile.path.replace(/^.+(\/uploads\/[A-z0-9]+\.\w+)$/, '$1')}
                  alt={photo.title ?? photo.text?.substr(0, 20) ?? ''}
                  height={photo.previewFile.height}
                  width={photo.previewFile.width}
                />
              )}
            </li>
          ))}
        </ul>
      ) : null}
      {account.edits && account.edits.length > 0 ? (
        <>
          <p className="subheading">Edits</p>
          <ul>
            {account.edits.map(edit => (
              <li key={edit.id}>
                <p>{edit.title}</p>
                {edit.previewFile && <img src={edit.previewFile.path} />}
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </div>
  )
}

export default AccountPage
