// 1. Configuración de API (Centralizamos la URL)
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api/v1',
};

// 2. Roles de Usuario (Basado en el punto 4 del informe: Actores)
export const ROLES = {
  SECRETARIA: 'secretaria',
  APROBADOR: 'aprobador', // o el nombre exacto que devuelva tu login
};

// 3. Estados de la Solicitud (Basado en los Objetivos Específicos 2.2)
export const REQUEST_STATES = {
  PENDIENTE: 'PENDIENTE',
  POR_APROBAR: 'POR_APROBAR',
  APROBADO: 'APROBADO',
  RECHAZADO: 'RECHAZADO',
  OBSERVADO: 'OBSERVADO',
};

// 4. Tipos de Acción (Para la lógica de derivación)
export const ACTIONS = {
  DERIVADO: 'Derivado',
  OBSERVADO: 'Observado',
  APROBADO: 'Aprobado',
  RECHAZADO: 'Rechazado',
};