import Head from 'next/head'

const DocumentFill = ({ pattern = 'memphis.png' }) => (
  <Head>
    <style>
      {`body {
        background: url("/${pattern}");
      }`}
    </style>
  </Head>
)

export default DocumentFill
