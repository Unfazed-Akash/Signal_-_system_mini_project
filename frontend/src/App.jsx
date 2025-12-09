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
        {/* Navigation Bar - Top Command Strip */}
        <nav style={{
          position: 'fixed',
          top: '0',
          left: '0',
          width: '100%',
          background: 'rgba(2, 6, 23, 0.95)',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          padding: '0 40px',
          height: '50px',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          gap: '30px',
          justifyContent: 'center',
          backdropFilter: 'blur(10px)'
        }}>
          <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: '800', fontSize: '0.8rem', letterSpacing: '2px', opacity: 0.8 }}>GOD EYE</Link>
          <Link to="/lea" style={{ color: 'var(--accent-success, #00ff00)', textDecoration: 'none', fontWeight: '800', fontSize: '0.8rem', letterSpacing: '2px' }}>LEA OPS</Link>
          <Link to="/bank" style={{ color: 'var(--accent-primary, #3498db)', textDecoration: 'none', fontWeight: '800', fontSize: '0.8rem', letterSpacing: '2px' }}>BANKING CORE</Link>
          <Link to="/portal" style={{ color: 'var(--accent-warning, #f1c40f)', textDecoration: 'none', fontWeight: '800', fontSize: '0.8rem', letterSpacing: '2px' }}>USER PORTAL</Link>
        </nav>
        <div style={{ height: '50px' }}></div> {/* Spacer for fixed header */}

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
