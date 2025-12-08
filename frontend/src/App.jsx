import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import LEADashboard from './pages/LEADashboard';
import BankDashboard from './pages/BankDashboard';
import UserPortal from './pages/UserPortal';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar (Hidden in kiosks, useful for demo) */}
        <nav style={{ position: 'fixed', bottom: '20px', left: '50%', transform: 'translateX(-50%)', background: 'rgba(0,0,0,0.8)', padding: '10px 20px', borderRadius: '30px', zIndex: 9999, display: 'flex', gap: '20px' }}>
          <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>🛡️ GOD EYE</Link>
          <Link to="/lea" style={{ color: '#00ff00', textDecoration: 'none', fontWeight: 'bold' }}>🚓 LEA</Link>
          <Link to="/bank" style={{ color: '#3498db', textDecoration: 'none', fontWeight: 'bold' }}>🏛️ BANK</Link>
          <Link to="/portal" style={{ color: '#f1c40f', textDecoration: 'none', fontWeight: 'bold' }}>👤 PORTAL</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/lea" element={<LEADashboard />} />
          <Route path="/bank" element={<BankDashboard />} />
          <Route path="/portal" element={<UserPortal />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
