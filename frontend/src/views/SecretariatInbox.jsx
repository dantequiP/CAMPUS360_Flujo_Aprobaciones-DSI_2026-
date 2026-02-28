import React, { useState, useEffect } from 'react';
import '../styles/ApproverInbox.css'; 

const SecretariatInbox = ({ onSelectRequest }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterLevel, setFilterLevel] = useState('');
  const [filterPriority, setFilterPriority] = useState('');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [solicitudes, setSolicitudes] = useState([]);
  const [loading, setLoading] = useState(true);
  
  


  useEffect(() => {
    const cargarPendientes = async () => {
      try {
        const respuesta = await fetch('http://localhost:8000/api/v1/approvals/pending');
        const datos = await respuesta.json();
        
        console.log("Datos brutos del servidor:", datos);

        // FILTRO MAESTRO: Solo Pendientes y Observados para Secretaría
        const gestionables = datos.filter(s =>
          s.estado === 'PENDIENTE' || s.estado === 'OBSERVADO'
        ); 
        
        setSolicitudes(gestionables);
      } catch (error) {
        console.error("Error en Secretaría:", error);
      } finally {
        setLoading(false);
      }
    };
    cargarPendientes();
  }, []);

  const solicitudesFiltradas = solicitudes.filter((sol) => {
    // 1. Filtro por Buscador (ID o Alumno)
    const cumpleBusqueda = 
      String(sol.id).toLowerCase().includes(searchTerm.toLowerCase()) ||
      (sol.alumno || "").toLowerCase().includes(searchTerm.toLowerCase());

    // 2. Filtro por Prioridad
    const cumplePrioridad = filterPriority === '' || sol.prioridad === filterPriority;

    // 4. Filtro por Estado (por ahora Henry/Gustavo vienen como POR_APROBAR)
    const cumpleEstado = filterStatus === '' || sol.estado === filterStatus;

    // Retorna true solo si cumple todos los filtros activos
    return cumpleBusqueda && cumplePrioridad && cumpleEstado;
  });

  if (loading) return <div className="loading">Cargando trámites N1...</div>;

  const handleForward = async (id) => {
    // 1. Preparamos el salto temporal (Payload para FastAPI)
    const payload = {
      area_destino: "Jefatura", // Destino para el Aprobador
      checklist_valido: true,   // Es una derivación positiva
      comentario: "Derivación automática desde bandeja principal."
    };

    try {
      // 2. Apuntamos al endpoint correcto: /workflow/{id}/escalate
      const response = await fetch(`http://localhost:8000/api/v1/workflow/${id}/escalate`, {
        method: 'POST', // Tu controller usa POST para escalar
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const result = await response.json();
        alert(`${result.mensaje}`); // "Solicitud validada y derivada..."
        
        // 3. Actualizamos la lista local sin recargar toda la página (Más pro)
        setSolicitudes(prev => prev.filter(sol => sol.id !== id));
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (err) {
      console.error("Fallo en el salto temporal:", err);
    }
  };

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Bandeja de Secretaría</h1>
        <p>Revisión preliminar de documentos y derivación</p>
      </header>

      {/* Cuadro de Guía Azul de tu boceto */}
      <div className="info-guide-box" style={{ backgroundColor: '#eff6ff', border: '1px solid #bfdbfe', padding: '15px', borderRadius: '10px', margin: '20px 0', color: '#1e40af', fontSize: '0.85rem' }}>
        <strong>Guía:</strong> Si falta información, usa <strong>Observar</strong>. Si está completo, usa <strong>Derivar/Aprobar</strong> para enviar al siguiente nivel (N2).
      </div>

    <section className="filters-panel">
        <div className="filters-title">
          <span>🔍</span> <strong>Filtros</strong>
        </div>

        {/* Fila 1: Buscador y Selectores */}
        <div className="filter-row-main">
          <div className="search-box">
            <input 
              type="text" 
              placeholder="🔍 ID o solicitante..." 
              className="search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <select className="filter-select" value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="">Todos los Estados</option>
            <option value="PENDIENTE">Nuevos (Pendientes)</option>
            <option value="OBSERVADO">Con Observaciones</option>
          </select>
        </div>

        {/* Fila 2: Fechas y Botón Limpiar */}
        <div className="filter-row-secondary">
          <div className="date-filter">
            <span>📅 Rango de fechas:</span>
            <input type="date" className="date-input" value={dateRange.start} onChange={(e) => setDateRange({...dateRange, start: e.target.value})} />
            <span className="date-separator">hasta</span>
            <input type="date" className="date-input" value={dateRange.end} onChange={(e) => setDateRange({...dateRange, end: e.target.value})} />
          </div>
          
          <button className="btn-clear-filters" onClick={() => {
            setSearchTerm('');
            setFilterStatus('');
            setFilterLevel('');
            setFilterPriority('');
            setFilterArea('');
            setDateRange({start: '', end: ''});
          }}>
            Limpiar filtros
          </button>
        </div>
      </section>

      <table className="main-table">
      <thead>
        <tr>
          <th>Código</th>
          <th>Tipo de Solicitud</th>
          <th>Solicitante</th>
          <th>Prioridad</th>

          <th>Estado</th>
          <th style={{ textAlign: 'center' }}>Acciones</th>
        </tr>
      </thead>
      <tbody>
          {solicitudes.length > 0 ? (
            solicitudes.map((sol) => (
              <tr key={sol.id}>
                {/* Usamos los nombres del DTO de FastAPI */}
                <td><strong>SOL-{sol.id}</strong></td>
                <td>{sol.tipo_tramite}</td>
                <td>{sol.alumno}</td>
                <td>
                  <span className={`tag-prio ${sol.prioridad?.toLowerCase()}`}>
                    {sol.prioridad}
                  </span>
                </td>
                <td>
                  <span className="tag-status-text">
                    {sol.estado?.replace('_', ' ')}
                  </span>
                </td>
                <td className="actions-cell" style={{ textAlign: 'center' }}>
                  <button 
                    className="action-view" 
                    onClick={() => onSelectRequest(sol)}
                    title="Ver Detalle"
                  >
                    👁️
                  </button>
                  <button className="action-forward" title="Derivar" onClick={() => handleForward(sol.id)}
                    >➡️</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>
                No hay trámites pendientes en esta línea de universo.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default SecretariatInbox;