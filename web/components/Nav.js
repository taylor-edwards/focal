import { useEffect, useState } from 'react'
import Button from 'components/Button'
import Link from 'components/Link'
import Logo from 'components/Logo'
import styles from 'styles/Nav.module.css'

const Nav = ({ className = "" }) => {
  const [menuShown, showMenu] = useState(false)
  const stopProp = e => e.stopPropagation()
  useEffect(() => {
    const exitHandler = e => showMenu(false)
    const opts = { passive: true }
    const events = ['mousedown', 'touchstart']
    events.forEach(
      event => window.addEventListener(event, exitHandler, opts),
    )
    return () => events.forEach(
      event => window.removeEventListener(event, exitHandler, opts),
    )
  }, [])
  return (
    <nav
      className={`${styles.nav} ${className}`}
      onMouseDown={stopProp}
      onTouchStart={stopProp}
    >
      <Link href="/">
        <Logo size={60} />
      </Link>

      <div className={styles.menu}>
        <Button
          onClick={() => showMenu(!menuShown)}
          className={styles.btn}
          appearance="link"
        >
          {menuShown ? '-' : '+'}
        </Button>
        <div className={`${styles.links} ${menuShown ? '' : styles.hidden}`}>
          <Link href="/p">photos</Link>
          <Link href="/e">edits</Link>
          <Link href="/c">create</Link>
          <Link href="/a">account</Link>
          <Link href="/l">logout</Link>
        </div>
      </div>
    </nav>
  )
}

export default Nav
