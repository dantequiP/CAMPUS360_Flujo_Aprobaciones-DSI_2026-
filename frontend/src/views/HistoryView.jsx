import React, { useState, useEffect } from 'react';
import { approvalService } from '../services/approvalService';
import ApprovalTable from '../components/approval/ApprovalTable';
import '../styles/ApproverInbox.css';

const HistoryView = ({ onSelectRequest }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  // 1. Carga de datos delegada al servicio (Arquitectura en Capas)
  const loadHistoryData = async () => {
    setLoading(true);
    try {
      const data = await approvalService.getHistory();
      setHistory(data);
    } catch (err) {
      console.error("Error al recuperar la bitácora:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistoryData();
  }, []);

  if (loading) return <div className="loading">Accediendo a la bitácora técnica de la FISI...</div>;

  // 2. Lógica de filtrado simple (KISS)
  const filteredHistory = (history || []).filter(item => 
    String(item.id).includes(searchTerm) || 
    (item.alumno || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Historial de Decisiones G4</h1>
        <p>Registro inmutable de trámites procesados (RN7 - Auditoría)</p>
      </header>

      <div className="filters-panel">
        <input 
          type="text" 
          placeholder="🔍 Buscar por ID o alumno..." 
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button className="btn-clear" onClick={loadHistoryData}>🔄 Refrescar</button>
      </div>

      {/* 3. Reutilización de tabla para cumplir con DRY y consistencia */}
      <ApprovalTable 
        data={filteredHistory} 
        onSelect={onSelectRequest} 
        onApprove={() => {}} // El historial es de solo lectura (RN7)
      />

      {filteredHistory.length === 0 && (
        <p className="empty-state">No se encontraron registros en el historial.</p>
      )}
    </div>
  );
};

export default HistoryView;