import React, { useState } from 'react';
import { useApprovals } from '../hooks/useApprovals';
import { approvalService } from '../services/approvalService';
import ApprovalTable from '../components/approval/ApprovalTable';
import '../styles/ApproverInbox.css';
import { REQUEST_STATES, ROLES } from '../constants/appConstants';

const ApproverInbox = ({ onSelectRequest }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const allowedStates = [REQUEST_STATES.POR_APROBAR];
  const { requests, loading, error, refresh } = useApprovals(allowedStates);

  const handleApprove = async (id) => {
    try {
      await approvalService.quickApprove(id);
      alert(`Acción Realizada en la Base de Datos`);
      refresh(); // Actualiza la lista sin recargar la página (KISS)
    } catch (error) {
      alert("Error al aprobar: " + error.message);
    }
  };

  if (loading) return <div className="loading">Cargando trámites de San Marcos...</div>;
  if (error) return <div className="error-state">Error al cargar datos: {error}</div>;

  // 2. CAMBIO CLAVE: Filtramos sobre 'requests'
  const filtradas = (requests || []).filter(sol => 
    String(sol.id).toLowerCase().includes(searchTerm.toLowerCase()) ||
    (sol.alumno || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Bandeja de Aprobaciones</h1>
        <p>Solicitudes asignadas para evaluación técnica (UNMSM - FISI)</p>
      </header>

      <section className="filters-panel">
        <input 
          type="text" 
          placeholder="🔍 Buscar por código o solicitante..." 
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)} 
        />
        <button className="btn-clear" onClick={refresh}>🔄 Actualizar</button>
      </section>

      {/* 3. Pasamos las solicitudes filtradas a la tabla reutilizable (SRP) */}
      <ApprovalTable 
        data={filtradas} 
        onSelect={onSelectRequest} 
        onApprove={handleApprove} 
      />
      
      {filtradas.length === 0 && (
        <p className="empty-state">No se encontraron solicitudes pendientes en esta área.</p>
      )}
    </div>
  );
};

export default ApproverInbox;