import React, { useState, useEffect } from 'react';
import '../styles/ApproverInbox.css'; // Reutilizamos estilos para mantener la estética G4

const HistoryView = ({ onSelectRequest }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  // 1. Sincronización con el registro histórico del Backend
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/approvals/history');
        if (!response.ok) throw new Error('Fallo al recuperar la bitácora');
        const data = await response.json();
        setHistory(data);
      } catch (err) {
        console.error("Error en el Historial:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  // 2. Filtro de búsqueda por ID o Alumno
  const filteredHistory = history.filter(item => 
    String(item.id).includes(searchTerm) || 
    item.alumno.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div className="loading">Accediendo a los archivos del laboratorio...</div>;

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Historial de Decisiones G4</h1>
        <p>Registro inmutable de trámites procesados en la FISI</p>
      </header>

      <div className="filters-panel">
        <div className="search-box">
          <input 
            type="text" 
            placeholder="🔍 Buscar por ID o alumno..." 
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <table className="main-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Trámite</th>
            <th>Solicitante</th>
            <th>Veredicto Final</th>
            <th>Fecha de Decisión</th>
            <th style={{ textAlign: 'center' }}>Detalle</th>
          </tr>
        </thead>
        <tbody>
          {filteredHistory.length > 0 ? (
            filteredHistory.map((item) => (
              <tr key={item.id}>
                <td><strong>SOL-{item.id}</strong></td>
                <td>{item.tramite}</td>
                <td>{item.alumno}</td>
                <td>
                  {/* Los estados vienen del controller: APROBADO, RECHAZADO, etc. */}
                  <span className={`tag-status ${item.estado_final?.toLowerCase()}`}>
                    {item.estado_final}
                  </span>
                </td>
                <td style={{ textAlign: 'center' }}>
                    <button 
                        className="action-view" 
                        onClick={() => onSelectRequest(item)} // <--- Dispara la vista de detalle
                    >
                        👁️
                    </button>
                    </td>
                <td>{new Date(item.fecha_decision).toLocaleString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                No hay registros en esta línea de universo todavía.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryView;