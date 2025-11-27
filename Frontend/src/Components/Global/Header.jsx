import { useState } from 'react'
import styles from './Header.module.css'
import { Navbar } from './Navbar'
export const Header = () => {

  const [showNavbar, setShowNavbar] = useState(false)

  const toggleNavbar = () => {
    setShowNavbar(prev => !prev)
  }

  return (
    <>
      <header>
        <nav>
            <div className={styles.rowHeaderContent}>
              
              <div className={styles.titleContainer}>
                <h1>Sistema de deteccion de amenazas</h1>
              </div>

              <div className={styles.hamburgerContainer} onClick={toggleNavbar} aria-label='boton_hamburgesa'>
                <i className="fa-solid fa-bars"></i>
              </div>
            </div>

            <Navbar show={showNavbar} toggleNavbar={toggleNavbar} />
        </nav>
      </header>
    </>
  )
}

