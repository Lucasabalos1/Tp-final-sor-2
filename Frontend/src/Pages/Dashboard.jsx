import { Header } from "../Components/Global/Header"
import styles from "./Dashboard.module.css"
export const Dashboard = () => {
  return (
    <>
        <Header/>
        <div className={styles.mainContainer}>
            <h2>BIENVENIDO AL DASHBOARD</h2>
            <h3>SISTEMA WEB DE DETECCIÓN DE ANOMALÍAS EN TRÁFICO DE RED UTILIZANDO REDES NEURONALES RECURRENTES</h3>
            <h4>TP FINAL - SISTEMAS OPERATIVOS Y REDES 2 - LUCAS ABALOS</h4>
        </div>
    </>
  )
}

