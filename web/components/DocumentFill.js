import Head from 'next/head'

const DocumentFill = ({ pattern = 'memphis.png' }) => (
  <Head>
    <style>
      {`
        html {
          background: url("/${pattern}"), #000 !important;
        }
      `}
    </style>
  </Head>
)

export default DocumentFill
