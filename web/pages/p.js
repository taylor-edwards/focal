/**
 * Photo feed from accounts the user follows
 * Global feed of photos for visitors
 *
 * Prerender the first page of results and refresh it every minute.
 * Pass initial parameters to component for implementing pagination.
 */

import { useRouter } from 'next/router'
import DateTime from 'components/DateTime'
import Image from 'components/Image'
import Link from 'components/Link'
import Loading from 'components/Loading'

export const getStaticProps = async context => {
  const { fetchPhotos } = require('queries')
  try {
    const response = await fetchPhotos().then(r => r.json())
    return {
      props: {
        photos: response.data.photos,
      },
      revalidate: 60,
    }
  } catch (err) {
    console.warn('Caught error fetching photos for props', err)
    return {
      props: {
        photos: [],
        error: 'Oops, something went wrong loading this feed!',
      },
      revalidate: 30,
    }
  }
}

const PhotoFeed = ({ photos }) => {
  const router = useRouter()
  if (router.isFallback) {
    return <Loading />
  }
  return (
    <main>
      <section>
        <h1>Photo feed</h1>
        {photos.map(photo => {
          const safename = encodeURIComponent(photo.account.safename)
          const photoLink = `/a/${safename}/p/${encodeURIComponent(photo.id)}`
          return (
            <article key={photo.id}>
              <Link href={photoLink}>
                {photo.title && <h4>{photo.title}</h4>}
              </Link>
              <Link href={`/a/${safename}`}>
                <p>{photo.account.name} posted at <DateTime date={photo.createdAt} /></p>
              </Link>
              {photo.previewFile && <Image srcFile={photo.previewFile} />}
              {photo.text && (
                <Link href={photoLink}>{photo.text}</Link>
              )}
              {photo.rawFile && (
                <Link href={photo.rawFile.path}>&darr; Download .{photo.rawFile.ext.toUpperCase()}</Link>
              )}
              {/* Reactions */}
              {/* Download raw */}
              {/* Replies */}
              {/* Add reply */}
              {/* Edits */}
              {/* Add edit */}
            </article>
          )
        })}
      </section>
    </main>
  )
}

export default PhotoFeed
