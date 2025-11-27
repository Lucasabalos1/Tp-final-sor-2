import { useEffect, useState } from "react";
import { Header } from "../Components/Global/Header";
import styles from "./MetricsManager.module.css";

export const MetricsManager = () => {
  const [alertsMetrics, setAlertsMetrics] = useState([]);

  const getMetics = async () => {
    const resp = await fetch("http://192.168.1.20:5000/api/metrics");

    const data = await resp.json();

    setAlertsMetrics(data.data);
  };

  useEffect(() => {
    getMetics();
  }, []);

  return (
    <>
      <Header />
      <div className={styles.mainContainer}>
        <div className={styles.titleSection}>
          <h2>Metricas de alertas</h2>
        </div>

        {alertsMetrics && (
          <div className={styles.cardGrid}>
            <div className={styles.metricCard}>
              <div className={styles.metricLabel}>Tasa de bloqueo</div>
              <div className={styles.metricValue}>{alertsMetrics.block_success_rate}</div>
            </div>

            <div className={styles.metricCard}>
              <div className={styles.metricLabel}>Ataques bloqueados</div>
              <div className={styles.metricValue}>{alertsMetrics.blocked_attacks_count}</div>
            </div>

            <div className={styles.metricCard}>
              <div className={styles.metricLabel}>Alertas procesadas</div>
              <div className={styles.metricValue}>{alertsMetrics.total_alerts_processed}</div>
            </div>

            <div className={styles.metricCard}>
              <div className={styles.metricLabel}>Última actualización</div>
              <div className={styles.metricValue}>{alertsMetrics.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};
