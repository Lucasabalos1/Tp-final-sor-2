import './App.css'
import { Navigate, Route, Routes } from "react-router-dom";
import { Dashboard } from './Pages/Dashboard';
import { AlertsManager } from './Pages/AlertsManager';
import { MetricsManager } from './Pages/MetricsManager';

export const App = () => {
  return (
    <>
      <Routes>
        <Route path='/dashboard' element={<Dashboard/>} />
        <Route path='/alertManager' element={<AlertsManager/>} />
        <Route path='/metricsManager' element={<MetricsManager/>} />
        <Route path='/*' element={<Navigate to = "/dashboard" />} /> 
      </Routes>
    </>
  )
}


