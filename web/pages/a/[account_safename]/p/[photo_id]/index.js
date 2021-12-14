/**
 * Photo canonical page
 */

import { useRouter } from 'next/router'
import Image from 'components/Image'
import Link from 'components/Link'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  const { fetchPhoto } = require('queries')
  try {
    const { account_safename, photo_id } = context.params
    const response = await fetchPhoto(photo_id)
    if (account_safename !== response.data.photo.account.safename) {
      // just because the photo exists doesn't mean it belongs to this account
      throw new Error('Account names do not match')
    }
    return {
      props: {
        photo: response.data.photo,
      },
      revalidate: 60,
    }
  } catch (err) {
    console.warn(
      'Issuing 404 for photo page request',
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
  const { fetchPhotos } = require('queries')
  try {
    const response = await fetchPhotos()
    return {
      paths: response.data.photos.map(
        p => `/a/${encodeURIComponent(p.account.safename)}/p/${p.id}`),
      fallback: true,
    }
  } catch (err) {
    console.warn('Caught error fetching photos for paths\n', err)
    return {
      paths: [],
      fallback: true,
    }
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
      {photo.previewFile && <Image srcFile={photo.previewFile} />}
      <p>{photo.text}</p>
      {/* <ReactionForm /> */}
      {/* <ReplyForm /> */}
      {/* <EditForm /> */}
      {photo.rawFile && (
        <Link file={photo.rawFile}>&darr; Download .{photo.rawFile.ext.toUpperCase()}</Link>
      )}
      {/* Reactions */}
      {/* Download raw */}
      {/* Replies */}
      {/* Add reply */}
      {/* Edits */}
      {/* Add edit */}
    </main>
  )
}

export default PhotoPage
