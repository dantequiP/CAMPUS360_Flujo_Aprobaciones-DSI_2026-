import React from 'react';
import '../../styles/Sidebar.css';

const Sidebar = ({ changeView, currentView, userRole, onLogout }) => {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="logo-placeholder">🎓</div>
        <div className="brand-text">
          <h2>Campus360</h2>
          <span>UNMSM - FISI</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {/* Opción única de Bandeja: Cambia el nombre según el rol */}
        <button 
          className={`nav-item ${currentView === 'bandeja' ? 'active' : ''}`}
          onClick={() => changeView('bandeja')}
        >
          <span className="nav-icon">📥</span>
          <span className="nav-label">
            {userRole === 'secretaria' ? 'Bandeja Secretaría' : 'Bandeja Aprobador'}
          </span>
        </button>

        {/* Historial común para ambos roles */}
        <button 
          className={`nav-item ${currentView === 'historial' ? 'active' : ''}`}
          onClick={() => changeView('historial')}
        >
          <span className="nav-icon">📊</span>
          <span className="nav-label">Historial</span>
        </button>
      </nav>

      {/* SECCIÓN INFERIOR: Usuario y Cerrar Sesión */}
      <div className="sidebar-footer">
        <div className="user-info-mini">
          <div className="user-avatar-mini">J</div>
          <div className="user-details-mini">
            <p className="user-name-mini">Jussel Enrique</p>
            <p className="user-role-mini">{userRole === 'secretaria' ? 'Secretaría' : 'Aprobador'}</p>
          </div>
        </div>
        
        <button className="btn-logout" onClick={onLogout}>
          <span className="nav-icon">🚪</span>
          <span className="nav-label">Cerrar Sesión</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;