import Head from 'next/head'

const DocumentFill = ({ pattern = 'memphis.png' }) => (
  <Head>
    <style>
      {`
        html, body {
          background: url(/${pattern}), rgb(var(--bg)) !important;
        }
        @media (prefers-color-scheme: light) {
          html, body {
            /* TODO: add light variant of memphis.png */
            background: rgb(var(--bg)) !important;
          }
        }
      `}
    </style>
  </Head>
)

export default DocumentFill
