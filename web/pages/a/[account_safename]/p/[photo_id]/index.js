/**
 * Photo canonical page
 */

import { useRouter } from 'next/router'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  const { PAGE_REVALIDATION_INTERVAL } = require('config')
  const { fetchPhoto } = require('queries')
  try {
    const { account_safename, photo_id } = context.params
    const response = await fetchPhoto(photo_id).then(r => r.json())
    if (account_safename !== response.data.photo.account.safename) {
      // just because the photo exists doesn't mean it belongs to this account
      throw new Error('Account names do not match')
    }
    return {
      props: {
        photo: response.data.photo,
      },
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  } catch (err) {
    console.warn(
      'Issuing 404 for photo page request',
      JSON.stringify({ params: context.params }),
      err.message,
    )
    return {
      notFound: true,
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  }
}

export const getStaticPaths = async () => {
  const { fetchPhotos } = require('queries')
  const response = await fetchPhotos().then(r => r.json())
  return {
    paths: response.data.photos.map(p => `/a/${encodeURIComponent(p.account.safename)}/p/${p.id}`),
    fallback: true,
  }
}

const PhotoPage = ({ photo }) => {
  const router = useRouter()
  if (router.isFallback) {
    return <Loading />
  }
  return (
    <main>
      <h1>{photo.title ?? 'Photo'}</h1>
      <p>{photo.text}</p>
      {photo.previewFile && (
        <img
          src={photo.previewFile.path?.replace(/^.+(\/uploads\/[A-z0-9]+\.\w+)$/, '$1')}
          alt={photo.title ?? photo.text?.substr(0, 20) ?? ''}
          height={photo.previewFile.height}
          width={photo.previewFile.width}
        />
      )}
      {/* <ReactionForm /> */}
      {/* <ReplyForm /> */}
      {/* <EditForm /> */}
    </main>
  )
}

export default PhotoPage