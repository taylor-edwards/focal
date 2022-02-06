import styles from "styles/Footer.module.css"

const Footer = ({ className = "" }) => (
  <footer className={`${styles.footer} ${className}`}>
    <p className={styles.copyright}>
      &copy; Focal 2020&ndash;{new Date().getFullYear()}
    </p>
  </footer>
)

export default Footer
