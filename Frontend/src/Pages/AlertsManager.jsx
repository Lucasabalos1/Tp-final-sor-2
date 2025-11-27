import { useEffect, useState } from "react";
import { Header } from "../Components/Global/Header";
import styles from "./AlertsManager.module.css";

export const AlertsManager = () => {
  
  const [alerts, setAlerts] = useState([])

  const getAlerts = async() => {

    const resp = await fetch("http://192.168.1.20:5000/api/alerts")

    const data = await resp.json()

    setAlerts(data.data)

  }

  useEffect(() => {
    getAlerts()
  },[])
  
  return (
    <>
      <Header />
      <div className={styles.mainContainer}>
        <div className={styles.titleSection}>
          <h2>Control de alertas</h2>
        </div>
        <div className={styles.tableContainer}>
          <table className="table">
            <thead className="table-dark">
              <tr>
                <th scope="col">#</th>
                <th scope="col">Ip Origen</th>
                <th scope="col">Fecha y Hora</th>
                <th scope="col">Estado</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert) => (
                <tr key={alert.id}>
                  <th scope="row">{alert.id}</th>
                  <td>{alert.ip_origen}</td>
                  <td>{alert.fecha_hora}</td>
                  <td className={alert.estado == "BLOQUEADO" ? "table-danger" :  ""}>{alert.estado}</td>
                </tr>
              ))}
              
              {/* <tr>
                <th scope="row">1</th>
                <td>Mark</td>
                <td>Otto</td>
                <td>@mdo</td>
              </tr> */}
              
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};
