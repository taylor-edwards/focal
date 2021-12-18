import Document, { Html, Head, Main, NextScript } from 'next/document'

class Doc extends Document {
  render () {
    return (
      <Html>
        <Head>
          <style>{`
            html {
              background: #000;
              color: #fff;
            }
            body {
              background: transparent;
              color: inherit;
            }
          `}</style>
          <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
          <link rel="icon" href="/favicon.ico" type="image/x-icon" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default Doc
