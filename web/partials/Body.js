import styles from 'styles/Body.module.css'

const Body = ({ className = '', children }) => (
  <main className={`${styles.body} ${className}`}>
    {children}
  </main>
)

export default Body
