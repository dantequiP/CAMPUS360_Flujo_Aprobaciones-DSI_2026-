import React from 'react';

/* =========================================================
   COMPONENTE TRANSVERSAL: ApprovalTable.jsx
   =========================================================
   Descripción:
   Componente reutilizable para mostrar datos
   en formato tabla.

   Regla de Diseño (RN-08):
   Incluye columna de Semaforización SLA:
   - VERDE
   - AMBAR
   - ROJO
   (Transforma texto en indicadores visuales).

*/

const ApprovalTable = ({ data, onSelect, onApprove }) => (
  <table className="main-table">
    <thead>
      <tr>
        <th>Código</th>
        <th>Tipo de Trámite</th>
        <th>Solicitante</th>
        <th>Prioridad</th>
        <th>Fecha</th>
        <th>Estado</th>
        <th style={{ textAlign: 'center' }}>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {data.map((sol) => (
        <tr key={sol.id}>
          <td><strong>{sol.id}</strong></td>
          <td>{sol.tipo_tramite}</td>
          <td>{sol.alumno}</td>
          <td>
            <span className={`tag-prio ${sol.prioridad?.toLowerCase()}`}>
              {sol.prioridad}
            </span>
          </td>
          <td>{sol.fechaCreacion?.split(' ')[0] || sol.fecha_ingreso || 'Pendiente'}</td>
          <td>
            <span className="tag-status-text">
                {(sol.estado_final || sol.estado)?.replace('_', ' ') || 'SIN ESTADO'}
            </span>
          </td>
          <td className="actions-cell" style={{ textAlign: 'center' }}>
            <button className="action-view" onClick={() => onSelect(sol)}>👁️</button>
            <button className="action-approve-fast" onClick={() => onApprove(sol.id)}>✔️</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default ApprovalTable;