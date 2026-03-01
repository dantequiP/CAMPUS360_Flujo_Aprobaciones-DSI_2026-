import React, { useState } from 'react';
import { approvalService } from '../services/approvalService';
import { ROLES, ACTIONS } from '../constants/appConstants';
import RequestInfo from '../components/approval/RequestInfo';

const RequestDetail = ({ selectedRequest, setSelectedRequest, userRole,isReadOnly }) => {

  const [isProcessing, setIsProcessing] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [comment, setComment] = useState('');
  const API_BASE_URL = 'http://localhost:8000/api/v1';

  
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
  setIsProcessing(true);
  try {
    const result = await approvalService.submitVerdict(
      selectedRequest.id,
      userRole,
      tipo,
      comment
    );

    alert(`${result.mensaje}`);
    setIsModalOpen(false);
    setSelectedRequest(null);
    
  } catch (err) {
    console.error("Error en la conexión:", err);
    alert(`Error: ${err.message}`);
  }finally {
    setIsProcessing(false);
  };
};

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
          <span className={`tag-status ${(selectedRequest.estado_final || selectedRequest.estado)?.toLowerCase()}`}>
            {(selectedRequest.estado_final || selectedRequest.estado)?.replace('_', ' ') || 'PROCESANDO'}
          </span>
        </div>
        <h1 className="request-title">{selectedRequest.tipo_tramite}</h1>
      </div>

      {!isReadOnly && (
          <div className="header-actions">
            <button className="btn-action-main" onClick={() => setIsModalOpen(true)}>
              {userRole === ROLES.SECRETARIA ? '⚙️ Gestionar Derivación' : '⚖️ Tomar Decisión'}
            </button>
          </div>
        )}
    </header>

    {(isReadOnly || selectedRequest.comentario) && (
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
          {userRole === ROLES.SECRETARIA ? (
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
              <button className="btn-main approve" onClick={() => handleDecision('Aprobado')}disabled={isProcessing}>
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
                disabled={isProcessing || !isCommentValid}
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

      <RequestInfo request={selectedRequest} />

      
    </div>
  );
};

export default RequestDetail;