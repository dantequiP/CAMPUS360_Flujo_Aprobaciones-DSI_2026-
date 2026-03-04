import React from 'react';
import '../styles/Home.css';

const Home = ({ onNavigate }) => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Campus360 – Flujo de Aprobaciones</h1>
        <p>Sistema de gestión de solicitudes académicas - Módulo G4</p>
      </header>

      {/* Tarjetas de Acceso Directo */}
      <div className="home-cards">
        <div className="card">
          <div className="card-icon blue">👤</div>
          <h3>Bandeja de Aprobador</h3>
          <p>Vista completa con permisos para aprobar, observar y rechazar solicitudes</p>
          <button className="btn-primary" onClick={() => onNavigate('bandeja')}>
            Acceder como Aprobador
          </button>
        </div>

        <div className="card">
          <div className="card-icon purple">📄</div>
          <h3>Bandeja de Secretaría</h3>
          <p>Revisión preliminar de documentos y derivación al siguiente nivel</p>
          <button className="btn-secondary">Acceder como Secretaría</button>
        </div>

        <div className="card">
          <div className="card-icon gray">🔳</div>
          <h3>Demo de Modales</h3>
          <p>Explora todos los modales y acciones del sistema</p>
          <button className="btn-outline">Ver Modales</button>
        </div>
      </div>

      {/* Sección de Características */}
      <section className="features-section">
        <h3>Características del Sistema</h3>
        <div className="features-grid">
          <div className="feature-item">
            <strong>• Gestión de estados</strong>
            <p>5 estados: Pendiente, Por Aprobar, Observada, Aprobada, Rechazada</p>
          </div>
          <div className="feature-item">
            <strong>• Niveles de aprobación</strong>
            <p>Sistema de aprobación en dos niveles (N1 y N2)</p>
          </div>
          <div className="feature-item">
            <strong>• Indicadores SLA</strong>
            <p>Semáforo visual para cumplimiento de tiempos</p>
          </div>
          <div className="feature-item">
            <strong>• Historial completo</strong>
            <p>Auditoría detallada de todas las acciones</p>
          </div>
        </div>
      </section>
      {/* Sección de Pantallas Disponibles */}
      <section className="available-screens">
        <h3>Pantallas Disponibles</h3>
        <div className="screens-list">
          <div className="screen-item">
            <div className="number-circle n1">1</div>
            <div className="screen-info">
              <strong>Bandeja de Aprobador</strong>
              <p>Vista con acciones: Ver detalle, Aprobar, Observar, Rechazar</p>
            </div>
          </div>
          <div className="screen-item">
            <div className="number-circle n2">2</div>
            <div className="screen-info">
              <strong>Bandeja de Secretaría</strong>
              <p>Revisión preliminar con acciones: Ver detalle, Observar, Derivar/Aprobar N1→N2</p>
            </div>
          </div>
          <div className="screen-item">
            <div className="number-circle n3">3</div>
            <div className="screen-info">
              <strong>Detalle de Solicitud</strong>
              <p>4 tabs: Resumen, Adjuntos, Historial/Auditoría, Checklist</p>
            </div>
          </div>
          <div className="screen-item">
            <div className="number-circle n4">4</div>
            <div className="screen-info">
              <strong>Historial de Decisiones</strong>
              <p>Registro completo con métricas y tabla de solicitudes procesadas</p>
            </div>
          </div>
          <div className="screen-item">
            <div className="number-circle n5">5</div>
            <div className="screen-info">
              <strong>Configuración</strong>
              <p>Preferencias de perfil, notificaciones, seguridad y sistema</p>
            </div>
          </div>
          <div className="screen-item">
            <div className="number-circle n6">+</div>
            <div className="screen-info">
              <strong>Estados especiales</strong>
              <p>Vista Vacía, Loading, Error (demostrable en Bandeja Aprobador)</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;