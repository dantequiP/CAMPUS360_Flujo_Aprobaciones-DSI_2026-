import React, { useState } from 'react';

const RequestDetail = ({ selectedRequest, setSelectedRequest, userRole,isReadOnly }) => {


  const [isModalOpen, setIsModalOpen] = useState(false);
  const [comment, setComment] = useState('');

  // 2. LOG DE SEGURIDAD (Para que veas en la consola qué llega)
  console.log("Datos recibidos en el Detalle:", selectedRequest);

  // 3. VERIFICACIÓN (Si por algún error llega nulo, se detiene aquí)
  if (!selectedRequest) {
    return (
      <div className="loading-state">
        <p>Cargando datos de la solicitud...</p>
        <button onClick={() => setSelectedRequest(null)}>Volver a intentar</button>
      </div>
    );
  }

  const handleDecision = async (tipo) => {
    // 1. Definir URL y Payload según el rol
    let url = "";
    let payload = {};

    if (userRole === 'secretaria') {
      // Endpoint de Escalado
      url = `http://localhost:8000/api/v1/workflow/${selectedRequest.id}/escalate`;
      payload = {
        area_destino: tipo === 'Derivado' ? "Jefatura" : "Alumno",
        checklist_valido: tipo === 'Derivado',
        comentario: comment
      };
    } else {
      // Endpoint de Dictamen
      url = `http://localhost:8000/api/v1/approvals/${selectedRequest.id}/verdict`;
      payload = {
        // Mapeo exacto a DictamenInput (Importante: Mayúsculas)
        decision: tipo.toUpperCase() === 'OBSERVADO' ? 'OBSERVADO' : 
                  tipo.toUpperCase() === 'RECHAZADO' ? 'RECHAZADO' : 'APROBADO',
        comentario: comment
      };
    }

    try {
      const response = await fetch(url, {
        method: 'POST', // Tus endpoints son POST
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error en el servidor");
      }

      const result = await response.json();
      alert(`${result.mensaje}`);
      
      // 2. Cerrar y Volver
      setIsModalOpen(false);
      setSelectedRequest(null); // Esto nos regresa a la bandeja automáticamente
      
    } catch (err) {
      console.error("Error en la conexión:", err);
      alert(`Error: ${err.message}`);
    }
  };

  // 1. Añadimos el nuevo estado al inicio de los Hooks  react Hooks "useState" is called condinionatlly. ruct hooks must be called in the exacted same order in the evert component render

const isCommentValid = comment.trim().length >= 10;

return (
  <div className="detail-container">
    <button className="btn-back" onClick={() => setSelectedRequest(null)}>
      ← Volver a la Bandeja
    </button>

    <header className="detail-header-top">
      <div className="header-titles">
        <div className="id-status-row">
          <span className="request-id">SOL-{selectedRequest.id}</span>
          // Busca esta línea en el Header de RequestDetail.jsx
          <span className={`tag-status ${(selectedRequest.estado_final || selectedRequest.estado)?.toLowerCase()}`}>
            {(selectedRequest.estado_final || selectedRequest.estado)?.replace('_', ' ') || 'PROCESANDO'}
          </span>
        </div>
        <h1 className="request-title">{selectedRequest.tipo_tramite}</h1>
      </div>

      {!isReadOnly && (
        <div className="header-actions">
          <button 
            className="btn-action-main" 
            onClick={() => setIsModalOpen(true)}
          >
            {userRole === 'secretaria' ? '⚙️ Gestionar Derivación' : '⚖️ Tomar Decisión'}
          </button>
        </div>
      )}
    </header>

    {isReadOnly && (
      <div className="audit-box-g4">
        <h3>Resumen del Veredicto Técnico</h3>
        <p><strong>Comentario Registrado:</strong></p>
        <p>{selectedRequest.comentario || "Trámite finalizado según normativa vigente."}</p>
      </div>
    )}

    {isModalOpen && (
      <div className="modal-overlay-g4">
        <div className="decision-window-g4">
          <div className="window-header">
            <h3>Panel de Decisiones Técnicas</h3>
            <button className="btn-close" onClick={() => setIsModalOpen(false)}>×</button>
          </div>
          
          <textarea
            className="comment-input"
            placeholder="Escriba aquí el sustento técnico..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />

          <div className="action-buttons-group">
          {userRole === 'secretaria' ? (
            /* 1. SECRETARÍA: Mantiene Derivar y Observar */
            <>
              <button className="btn-main approve" onClick={() => handleDecision('Derivado')}>
                <span>➡️</span> Derivar
              </button>
              <button 
                className="btn-main observe" 
                onClick={() => handleDecision('Observado')}
                disabled={!isCommentValid} 
              >
                <span>💬</span> Observar
              </button>
            </>
          ) : (
            /* 2. APROBADOR: Solo Aprobar o Rechazar (Eliminamos 'Observar') */
            <>
              <button className="btn-main approve" onClick={() => handleDecision('Aprobado')}>
                <span>✅</span> Aprobar
              </button>
              <button 
                  className="btn-main observe" 
                  onClick={() => handleDecision('Observado')}
                  disabled={!isCommentValid}
                >
                  <span>💬</span> Observar
                </button>
              <button 
                className="btn-main reject" 
                onClick={() => handleDecision('Rechazado')}
                disabled={!isCommentValid}
              >
                <span>🚫</span> Rechazar
              </button>
            </>
          )}
        </div>
          {!isCommentValid && (
            <p className="helper-text">* Justificación obligatoria para observar/rechazar.</p>
          )}
        </div>
      </div>
    )}

      {selectedRequest.comentario && (
      <div className="audit-box-g4">
        <h3>Resumen del Veredicto</h3>
        <p><strong>Comentario registrado:</strong></p>
        <p>{selectedRequest.comentario}</p>
      </div>
    )}

      

      <div className="data-grid-container">
        <h2 className="section-title">Información del Expediente</h2>
        
        <div className="request-info-grid">
          {/* 1. Código de Solicitud mejorado */}
          <div className="info-card">
            <label>Código de Solicitud</label>
            <p className="highlight-text">SOL-{selectedRequest.id}</p>
          </div>

          {/* 2. Solicitante con fallback para nombres de campos */}
          <div className="info-card">
            <label>Solicitante</label>
            <p>{selectedRequest.alumno || selectedRequest.solicitante}</p>
          </div>

          {/* 3. Fecha de Ingreso formateada */}
          <div className="info-card">
            <label>Fecha de Ingreso</label>
            <p>{selectedRequest.fecha_creacion || selectedRequest.fechaCreacion || '2026-02-21'}</p>
          </div>

          {/* 4. Documentos Adjuntos (Simulado por ahora) */}
          <div className="info-card">
            <label>Documentos Adjuntos</label>
            <div className="attachment-list">
              <span className="file-tag">fut_firmado.pdf</span>
              <span className="file-tag">reporte_notas.pdf</span>
            </div>
          </div>
        </div>

        {/* 5. Descripción/Motivo en ancho completo */}
        <div className="description-section">
          <label>Descripción / Motivo del Trámite</label>
          <div className="motive-box">
            {selectedRequest.motivo || "Solicitud tramitada según normativa vigente de la UNMSM - FISI."}
          </div>
        </div>
      </div>

      
    </div>
  );
};

export default RequestDetail;