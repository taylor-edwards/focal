import Body from 'partials/Body'
import DocumentFill from 'components/DocumentFill'
import Footer from 'components/Footer'
import Nav from 'components/Nav'
import styles from 'styles/Frame.module.css'

const Frame = ({ children, className = '' }) => (
  <>
    <DocumentFill />
    <div className={`${styles.frame} ${className}`}>
      <Nav className={styles.nav} />
      <Body>{children}</Body>
      <Footer className={styles.footer} />
    </div>
  </>
)

export default Frame
