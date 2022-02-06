import DocumentFill from 'components/DocumentFill'
import Footer from 'components/Footer'
import Nav from 'components/Nav'
import styles from 'styles/Frame.module.css'

const Frame = ({ children, className = '' }) => (
  <>
    <DocumentFill />
    <div className={`${styles.frame} ${className}`}>
      <Nav />
      {children}
      <Footer />
    </div>
  </>
)

export default Frame
