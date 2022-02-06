/**
 * Home page
 */

import Head from 'next/head'
import Image from 'components/Image'
import Link from 'components/Link'
import styles from 'styles/Home.module.css'

const HomePage = () => (
  <div className={styles.container}>
    <Head>
      <title>Focal</title>
      <meta name="description" content="Learn and share photography editing tips" />
    </Head>
    <main className="card">
      <Image src="/focal.svg" className="logo" />
      <ul className={styles.table}>
        <li>
          <Link className={styles.row} href="/a">
            <span>/a</span>
            <span>Signup</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/l">
            <span>/l</span>
            <span>Logout</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/p">
            <span>/p</span>
            <span>Photo feed</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/e">
            <span>/e</span>
            <span>Edit feed</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/c">
            <span>/c</span>
            <span>Submit photo</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/a/nacho">
            <span>/a/nacho</span>
            <span>Nacho&apos;s Account</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/a/nacho/p">
            <span>/a/nacho/p</span>
            <span>Nacho&apos;s Photo feed</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/a/nacho/p/205">
            <span>/a/nacho/p/205</span>
            <span>Nacho&apos;s &lsquo;SPICY CHIP&rsquo; Photo</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/a/nacho/e">
            <span>/a/nacho/e</span>
            <span>Nacho&apos;s Edit feed</span>
          </Link>
        </li>
        <li>
          <Link className={styles.row} href="/a/nacho/e/300">
            <span>/a/nacho/e/300</span>
            <span>Nacho&apos;s &lsquo;Insta&apos;d washout filter&rsquo; Edit</span>
          </Link>
        </li>
      </ul>
    </main>
  </div>
)

export default HomePage
