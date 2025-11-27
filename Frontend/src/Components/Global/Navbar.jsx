import styles from './Navbar.module.css'
import { NavLink } from 'react-router-dom';

export const Navbar = ({show, toggleNavbar}) => {
  

  return (
    <>
        <div className={`${styles.modalBackground} ${show ? styles.showBackground : ""}`}>
            <div className={`${styles.navbarContainer} ${show ? styles.showNavbar : ""}`}>
                <div className={styles.closeModalContainer} onClick={toggleNavbar}>
                    <i className="fa-solid fa-x"></i>
                </div>

                <div className={styles.pagesContainer}>     
                    <div className={styles.sectionNavListContainer}>
                        <div className={styles.sectionNavContainer}>
                            <NavLink to='/alertManager' className={styles.navLink}>
                                <i className="fa-solid fa-bell"></i>
                                <h3>Ver Alertas</h3>
                            </NavLink>
                        </div>
                        <div className={styles.sectionNavContainer}>
                            <NavLink to='/metricsManager' className={styles.navLink}>
                                <i className="fa-solid fa-book"></i>
                                <h3>Ver Metricas</h3>
                            </NavLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>
  )
}
