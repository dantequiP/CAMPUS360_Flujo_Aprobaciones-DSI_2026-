// src/components/approval/RequestInfo.jsx
import React from 'react';

const RequestInfo = ({ request }) => {
  if (!request) return null;

  return (
    <div className="data-grid-container">
      <h2 className="section-title">Información del Expediente</h2>
      
      <div className="request-info-grid">
        <div className="info-card">
          <label>Código de Solicitud</label>
          <p className="highlight-text">SOL-{request.id}</p>
        </div>

        <div className="info-card">
          <label>Solicitante</label>
          <p>{request.alumno || request.solicitante}</p>
        </div>

        <div className="info-card">
          <label>Fecha de Ingreso</label>
          <p>{request.fecha_creacion || '2026-02-21'}</p>
        </div>

        <div className="info-card">
          <label>Documentos Adjuntos</label>
          <div className="attachment-list">
            <span className="file-tag">fut_firmado.pdf</span>
            <span className="file-tag">reporte_notas.pdf</span>
          </div>
        </div>
      </div>

      <div className="description-section">
        <label>Descripción / Motivo del Trámite</label>
        <div className="motive-box">
          {request.motivo || "Solicitud tramitada según normativa vigente de la UNMSM - FISI."}
        </div>
      </div>
    </div>
  );
};

export default RequestInfo;