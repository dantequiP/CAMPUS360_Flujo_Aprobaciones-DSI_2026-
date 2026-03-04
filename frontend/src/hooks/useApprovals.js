// src/hooks/useApprovals.js
import { useState, useEffect } from 'react';
import { approvalService } from '../services/approvalService';

/* =========================================================
   CAPA DE APLICACIÓN: useApprovals.js (Custom Hook)
   =========================================================
   Descripción:
   Actúa como controlador lógico entre el servicio (approvalService)
   y los componentes visuales.

   Lógica de Negocio:
   Implementa el filtrado de estados según el rol:
   - Secretaría
   - Jefatura
*/

export const useApprovals = (allowedStates = []) => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const data = await approvalService.getPendingApprovals();

      const filteredData = allowedStates.length > 0 
        ? data.filter(s => allowedStates.includes(s.estado))
        : data;
      
      setRequests(filteredData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchRequests(); }, []);

  return { requests, loading, error, refresh: fetchRequests };
};