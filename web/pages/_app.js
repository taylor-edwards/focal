import Frame from 'partials/Frame'
import "../styles/globals.css";

const App = ({ Component, pageProps }) => (
  <Frame>
    <Component {...pageProps} />
  </Frame>
)

export default App;
