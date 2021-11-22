/**
 * Account/profile canonical page
 */

import { useRouter } from 'next/router'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  try {
    // Authenticate session context stored in cookie, and
    // if the authenticated user is looking at their own account page, then
    // import and use this function instead:
    //
    //     const { fetchPrivateAccount } = require('queries')
    const { fetchPublicAccount } = require('queries')
    const { PAGE_REVALIDATION_INTERVAL } = require('config')
    const accountName = context.params?.account_name
    const response = await fetchPublicAccount({ accountName })
    const json = await response.json()
    return {
      props: json.data,
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  } catch (err) {
    console.warn('Caught error fetching public account:', err)
  }
  return {
    notFound: true,
    revalidate: 60,
  }
}

export const getStaticPaths = async () => {
  try {
    const { fetchAccounts } = require('queries')
    const { PAGE_REVALIDATION_INTERVAL } = require('config')
    const response = await fetchAccounts()
    const json = await response.json()
    const paths = json.data.accounts.map(
      ({ accountName }) => `/a/${accountName}`,
    )
    return {
      paths,
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
  // Account page
  return (
    <div>
      <h1>Account</h1>
      {account && <p>{account.name}</p>}
      {account?.email && <p>{account.email}</p>}
      {account?.createdAt && (
        <p>Member since {new Date(account.createdAt).getFullYear()}</p>
      )}
      {account?.photos && account.photos.length > 0 ? (
        <ul>
          <p className="subheading">Photos</p>
          {account.photos.map(photo => (
            <li key={photo.id}>
              <p>{photo.title}</p>
              {photo.preview && <img src={photo.preview.filePath} />}
            </li>
          ))}
        </ul>
      ) : null}
      {account?.edits && account.edits.length > 0 ? (
        <>
          <p className="subheading">Edits</p>
          <ul>
            {account.edits.map(edit => (
              <li key={edit.id}>
                <p>{edit.title}</p>
                {edit.preview && <img src={edit.preview.filePath} />}
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </div>
  )
}

export default AccountPage
