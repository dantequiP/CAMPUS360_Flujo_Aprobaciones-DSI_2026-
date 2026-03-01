import { API_CONFIG, ROLES, ACTIONS } from '../constants/appConstants';

export const approvalService = {
  // GET: Obtener lista de pendientes [cite: 83]
  getPendingApprovals: async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}/approvals/pending`);
      if (!response.ok) throw new Error('Error al obtener pendientes');
      return await response.json();
    } catch (error) {
      console.error("Fallo de conexión:", error);
      throw error;
    }
  },

  // POST: Registrar dictamen final o derivar [cite: 83]
  submitVerdict: async (requestId, userRole, tipo, comment) => {
    let url = "";
    let payload = {};

    if (!requestId) throw new Error("ID de solicitud inválido");

    if (userRole === ROLES.SECRETARIA) {
      url = `${API_CONFIG.BASE_URL}/workflow/${requestId}/escalate`;
      payload = {
        area_destino: tipo === ACTIONS.DERIVADO ? "Jefatura" : "Alumno",
        checklist_valido: tipo === ACTIONS.DERIVADO,
        comentario: comment
      };
    } else {
      url = `${API_CONFIG.BASE_URL}/approvals/${requestId}/verdict`;
      payload = {
        decision: tipo.toUpperCase(),
        comentario: comment
      };
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error en el servidor");
    }
    return await response.json();
  },

  // PUT: Acción rápida desde la tabla
  quickApprove: async (id) => {
    const response = await fetch(`${API_CONFIG.BASE_URL}/approvals/${id}/approve`, {
      method: 'PUT',
    });
    if (!response.ok) throw new Error('Error en aprobación rápida');
    return await response.json();
  },

  getHistory: async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}/approvals/history`);
      if (!response.ok) throw new Error('Fallo al recuperar la bitácora');
      return await response.json();
    } catch (error) {
      console.error("Error en el Historial:", error);
      throw error;
    }
  }


};