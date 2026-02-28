import React, { useState, useEffect } from 'react';
import '../styles/ApproverInbox.css';

  const ApproverInbox = ({ onSelectRequest }) => {

  const [searchTerm, setSearchTerm] = useState('');
  // 1. Creamos un "saco" vacío para las solicitudes reales
  const [solicitudes, setSolicitudes] = useState([]);
  const [loading, setLoading] = useState(true);

  // 2. Traemos los datos de la BD de tu compañero
    useEffect(() => {
      const cargarDatosReales = async () => {
        try {
          const respuesta = await fetch('http://localhost:8000/api/v1/approvals/pending');
          const datos = await respuesta.json();

          // 1. Aquí filtras para que solo pasen los que están listos
          const solicitudesParaAprobar = datos.filter(s => s.estado === 'POR_APROBAR');

          // 2. EL CAMBIO CLAVE: Guardamos la lista filtrada, NO los 'datos' crudos
          setSolicitudes(solicitudesParaAprobar); 

        } catch (error) {
          console.error("Error al conectar con el Backend:", error);
        } finally {
          setLoading(false);
        }
      };
      cargarDatosReales();
    }, []);

  const handleApprove = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/approvals/${id}/approve`, {
        method: 'PUT'
      });
      if (response.ok) {
        alert(`Accion Realizada en la Base de Datos`);
        window.location.reload(); 
      }
    } catch (error) {
      console.error("Error al aprobar:", error);
    }
  };

  if (loading) return <div className="loading">Cargando trámites de San Marcos...</div>;

  // Filtramos la lista asegurándonos de que el ID sea tratado como texto
  const solicitudesFiltradas = solicitudes.filter((sol) => {
    // Convertimos el id a String para evitar que el sistema explote si es un número
    const idTexto = String(sol.id).toLowerCase();
    const alumnoTexto = (sol.alumno || "").toLowerCase();
    const busqueda = searchTerm.toLowerCase();

    return idTexto.includes(busqueda) || alumnoTexto.includes(busqueda);
  });

  return (
    <div className="inbox-container">
      <header className="inbox-header">
        <h1>Bandeja de Aprobaciones</h1>
        <p>Solicitudes asignadas a tu rol para evaluación</p>
      </header>

      {/* Panel de Filtros Avanzados */}
      <section className="filters-panel">
        <div className="filter-row">
           <div className="search-box">
            <input 
              type="text" 
              placeholder="🔍 Buscar por código o solicitante..." 
              className="search-input"
              onChange={(e) => setSearchTerm(e.target.value)} 
            />
          </div>
        </div>

        <div className="filter-row secondary">  
           <div className="date-range">
             <span>Rango de fechas:</span>
              <input type="date" className="date-input" /> 
              <span>hasta</span> 
              <input type="date" className="date-input" />
            </div>
            <button className="btn-clear" onClick={() => window.location.reload()}>
              Limpiar filtros
            </button>
          </div>
      </section> 

      {/* Tabla de Datos según boceto */}
      <table className="main-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Tipo de Trámite</th>
            <th>Solicitante</th>
            <th>Prioridad</th>
            <th>Fecha de Ingreso</th>
            <th>Estado</th>
            <th style={{ textAlign: 'center' }}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {solicitudesFiltradas.map((sol) => (
            <tr key={sol.id}>
              {/* 1. Código: idSolicitud */}
              <td><strong>{sol.id}</strong></td>

              {/* 2. Tipo: tipoSolicitud */}
              <td>{sol.tipo_tramite}</td>

              {/* 3. Solicitante: alumno */}
              <td>{sol.alumno}</td>

              {/* 4. Prioridad: prioridad */}
              <td>
                <span className={`tag-prio ${sol.prioridad?.toLowerCase()}`}>
                  {sol.prioridad}
                </span>
              </td>

              {/* 5. Fecha de Ingreso: Buscamos el nombre exacto de tu BD */}
              <td>
                {sol.fechaCreacion 
                  ? sol.fechaCreacion.split(' ')[0] // Esto corta la hora y deja solo YYYY-MM-DD
                  : sol.fecha_ingreso || 'Pendiente'} 
              </td>

              {/* 6. Estado: estado_id -> Texto */}
              <td>
                <span className="tag-status-text">
                  {sol.estado?.replace('_', ' ') || 'POR APROBAR'}
                </span>
              </td>

              {/* 7. Acciones: Solo las que acordamos */}
              <td className="actions-cell" style={{ textAlign: 'center' }}>
                <button className="action-view" onClick={() => onSelectRequest(sol)}>👁️</button>
                <button className="action-approve-fast" onClick={() => handleApprove(sol.id)}>✔️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ApproverInbox;