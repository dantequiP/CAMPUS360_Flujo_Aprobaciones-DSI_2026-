// src/services/approvalService.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const approvalService = {
  // Ahora consultará al backend real
  getPendingApprovals: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/approvals/pending`);
      if (!response.ok) throw new Error('Error en la API');
      return await response.json();
    } catch (error) {
      console.error("Fallo de conexión:", error);
      throw error;
    }
  }
};