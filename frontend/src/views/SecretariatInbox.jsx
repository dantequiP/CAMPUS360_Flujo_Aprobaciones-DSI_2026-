import React, { useState } from 'react';
import { useApprovals } from '../hooks/useApprovals';
import { approvalService } from '../services/approvalService';
import { ROLES, ACTIONS, REQUEST_STATES } from '../constants/appConstants';
import ApprovalTable from '../components/approval/ApprovalTable';
import '../styles/ApproverInbox.css'; 

const SecretariatInbox = ({ onSelectRequest }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Definimos qué estados puede ver el secretario según el informe (Caso de Uso 04)
  const allowedStates = [REQUEST_STATES.PENDIENTE, REQUEST_STATES.OBSERVADO];
  const { requests, loading, refresh } = useApprovals(allowedStates);

  const handleForward = async (id) => {
    try {
      // Usamos el servicio centralizado (submitVerdict) para derivar
      await approvalService.submitVerdict(id, ROLES.SECRETARIA, ACTIONS.DERIVADO, "Derivación técnica");
      alert("Solicitud derivada a Jefatura exitosamente");
      refresh(); // Actualiza la lista sin recargar la página
    } catch (err) {
      alert(`Error al derivar: ${err.message}`);
    }
  };

  if (loading) return <div className="loading">Cargando trámites N1 (Secretaría)...</div>;

  const filtradas = requests.filter(sol => 
    String(sol.id).toLowerCase().includes(searchTerm.toLowerCase()) ||
    (sol.alumno || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Bandeja de Secretaría</h1>
        <p>Revisión preliminar y derivación técnica [cite: 69]</p>
      </header>

      <div className="info-guide-box" style={{ backgroundColor: '#eff6ff', padding: '15px', borderRadius: '10px', color: '#1e40af' }}>
        <strong>Guía:</strong> Valide requisitos formales antes de derivar al Jefe de Área[cite: 193].
      </div>

      <section className="filters-panel">
        <input 
          type="text" 
          placeholder="🔍 Buscar ID o alumno..." 
          className="search-input"
          onChange={(e) => setSearchTerm(e.target.value)} 
        />
        <button className="btn-clear" onClick={refresh}>🔄 Actualizar</button>
      </section>

      {/* REUTILIZACIÓN: Usamos la misma tabla que el aprobador (DRY) */}
      <ApprovalTable 
        data={filtradas} 
        onSelect={onSelectRequest} 
        onApprove={handleForward} // Aquí 'Approve' actúa como 'Derivar' para el secretario
      />
    </div>
  );
};

export default SecretariatInbox;