/**
 * Photo canonical page
 */

import { useRouter } from 'next/router'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  const { account_name, photo_id } = context.params
  const { fetchPhoto } = require('queries')
  const { PAGE_REVALIDATION_INTERVAL } = require('config')
  const response = await fetchPhoto(photo_id)
    .then(r => r.json())
    .catch(() => null)
  if (!response || account_name !== response.data?.photo?.account?.name) {
    return {
      notFound: true,
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  }
  return {
    props: {
      photo: response.data.photo,
    },
    revalidate: PAGE_REVALIDATION_INTERVAL,
  }
}

export const getStaticPaths = async () => {
  const { fetchPhotos } = require('queries')
  const response = await fetchPhotos().then(r => r.json())
  console.log(response)
  return {
    paths: response.data.photos.map(p => `/a/${p.account.name}/p/${p.id}`),
    fallback: true,
  }
}

const PhotoPage = ({ photo }) => {
  const router = useRouter()
  if (router.isFallback) {
    return <Loading />
  }
  console.log(photo)
  return (
    <main>
      <h1>{photo?.title ?? 'Photo'}</h1>
      <p>{photo?.text}</p>
      {photo?.preview && (
        <img
          src={photo.preview.path?.replace(/^.+(\/uploads\/[A-z0-9]+\.\w+)$/, '$1')}
          alt={photo.title ?? photo.text?.substr(0, 20) ?? ''}
          height={photo.preview.height}
          width={photo.preview.width}
        />
      )}
      {/* <ReactionForm /> */}
      {/* <ReplyForm /> */}
      {/* <EditForm /> */}
    </main>
  )
}

export default PhotoPage
