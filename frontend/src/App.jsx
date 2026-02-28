import React, { useState } from 'react'; // Importamos useState para "recordar" la vista
import Sidebar from './components/common/Sidebar';
import RequestDetail from './views/RequestDetail';
import ApproverInbox from './views/ApproverInbox';
import SecretariatInbox from './views/SecretariatInbox';
import './styles/Layout.css';
import './styles/Detail.css';
import HistoryView from './views/HistoryView';
import Home from './views/Home';

function App() {
  // 1. El rol ahora empieza en null (para mostrar el Portal de entrada)
  const [userRole, setUserRole] = useState(null); 
  // 2. La vista activa por defecto ahora será siempre 'bandeja' al entrar a un rol
  const [activeView, setActiveView] = useState('bandeja');
  // 3. Mantenemos el estado de la solicitud seleccionada
  const [selectedRequest, setSelectedRequest] = useState(null);

  // Función para cambiar de vista y resetear la selección de solicitud
  const handleViewChange = (view) => {
    setActiveView(view);
    setSelectedRequest(null); // Si estábamos viendo un detalle, se cierra al cambiar de pestaña
  };
  return (
    <div className="app-container">
    {/* 1. LÓGICA MAQUIAVÉLICA: ¿Tenemos rol seleccionado? */}
    {!userRole ? (
      <div className="portal-container">
        <header className="portal-header">
          <h1>Campus360 – Flujo de Aprobaciones - G4</h1>
          <p>Seleccione su rol para ingresar al sistema de la FISI</p>
        </header>

        <div className="portal-cards">
          {/* Opción Secretaría */}
          <div className="portal-card" onClick={() => setUserRole('secretaria')}>
            <div className="card-icon">📁</div>
            <h2>Secretaría Académica</h2>
          </div>

          {/* Opción Aprobador */}
          <div className="portal-card" onClick={() => setUserRole('aprobador')}>
            <div className="card-icon">⚖️</div>
            <h2>Aprobador / Decanatura</h2>
          </div>
        </div>
      </div>
    ) : (
      /* 2. SI YA HAY ROL: Mostramos el layout con Sidebar y Contenido */
      <div className="layout-container">
        {/* Le pasamos el userRole al Sidebar para que sepa qué mostrar */}
        <Sidebar 
          changeView={handleViewChange} // Usamos la función que resetea la selección
          currentView={activeView} 
          userRole={userRole} 
          onLogout={() => {
            setUserRole(null);
            setSelectedRequest(null);
            setActiveView('bandeja');
          }} 
        />
        
        <main className="main-content">
          {/* VISTA 1: BANDEJA (Depende del Rol) */}
          {activeView === 'bandeja' && (
            !selectedRequest ? (
              // Si no hay solicitud seleccionada, muestra la bandeja que toque
              userRole === 'secretaria' 
                ? <SecretariatInbox onSelectRequest={setSelectedRequest} /> 
                : <ApproverInbox onSelectRequest={setSelectedRequest} />
            ) : (
              // Si hay una seleccionada, muestra el detalle (ya limpio de duplicados)
              <RequestDetail 
                selectedRequest={selectedRequest} 
                setSelectedRequest={setSelectedRequest} 
                userRole={userRole} 
              />
            )
          )}

          {/* VISTA 2: HISTORIAL (Conexión Real G4) */}
          {activeView === 'historial' && (
            !selectedRequest ? (
              // Si no hay seleccionada, muestra la lista de la bitácora
              <HistoryView onSelectRequest={setSelectedRequest} />
            ) : (
              // Si hay una seleccionada, muestra el detalle en modo "Lectura"
              <RequestDetail 
                selectedRequest={selectedRequest} 
                setSelectedRequest={setSelectedRequest} 
                userRole={userRole} 
                isReadOnly={true} // <--- Nueva prop para ocultar botones de decisión
              />
            )
          )}
        </main>
      </div>
    )}
  </div>
  );
}

export default App;