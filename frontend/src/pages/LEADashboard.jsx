import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:8000');

const LEADashboard = () => {
    const [stats, setStats] = useState({ active_operations: 0, suspects_tracked: 0, recent_alerts: [] });

    useEffect(() => {
        // Initial Fetch
        const fetchStats = async () => {
            const res = await fetch('http://127.0.0.1:8000/api/lea/stats');
            const data = await res.json();
            setStats(data);
        };
        fetchStats();

        // Real-time Listeners
        socket.on('new_alert', (alert) => {
            setStats(prev => ({
                ...prev,
                active_operations: prev.active_operations + 1,
                recent_alerts: [alert.transaction, ...prev.recent_alerts].slice(0, 10)
            }));
        });

        return () => socket.off('new_alert');
    }, []);

    return (
        <div style={{ height: '100vh', background: '#020617', color: 'white', display: 'flex' }}>
            {/* Sidebar */}
            <div style={{ width: '250px', background: 'rgba(15, 23, 42, 0.6)', borderRight: '1px solid #1e293b', padding: '20px' }}>
                <h2 style={{ color: '#00ff00', fontSize: '1.5rem', marginBottom: '40px', letterSpacing: '2px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    🚓 CYBER<span style={{ color: 'white' }}>POL</span>
                </h2>

                <div style={{ display: 'grid', gap: '15px' }}>
                    <div style={{ padding: '15px', background: 'rgba(34, 197, 94, 0.1)', border: '1px solid #22c55e', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.8rem', color: '#86efac' }}>ACTIVE UNITS</div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>24</div>
                    </div>

                    <div style={{ padding: '15px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6', borderRadius: '8px' }}>
                        <div style={{ fontSize: '0.8rem', color: '#93c5fd' }}>SUSPECTS TRACKED</div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.suspects_tracked}</div>
                    </div>
                </div>
            </div>

            {/* Main Feed */}
            <div style={{ flex: 1, padding: '40px', overflowY: 'auto' }}>
                <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '40px', alignItems: 'flex-end' }}>
                    <div>
                        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: 0 }}>LIVE OPERATIONS</h1>
                        <p style={{ color: '#94a3b8', margin: '5px 0 0 0' }}>Real-time interception feed authorized by Kavach Titanium.</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '3rem', fontWeight: '900', color: '#ef4444', lineHeight: 1 }}>{stats.active_operations}</div>
                        <div style={{ fontSize: '0.9rem', color: '#94a3b8', letterSpacing: '1px' }}>CRITICAL ALERTS</div>
                    </div>
                </header>

                <div className="table-container" style={{ background: 'rgba(30, 41, 59, 0.4)', borderRadius: '12px', border: '1px solid #334155', overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ background: '#0f172a', borderBottom: '1px solid #334155' }}>
                            <tr>
                                <th style={{ padding: '20px', color: '#94a3b8', fontSize: '0.8rem' }}>TIMESTAMP</th>
                                <th style={{ padding: '20px', color: '#94a3b8', fontSize: '0.8rem' }}>LOCATION</th>
                                <th style={{ padding: '20px', color: '#94a3b8', fontSize: '0.8rem' }}>TYPE</th>
                                <th style={{ padding: '20px', color: '#94a3b8', fontSize: '0.8rem' }}>AMOUNT</th>
                                <th style={{ padding: '20px', color: '#94a3b8', fontSize: '0.8rem' }}>STATUS</th>
                            </tr>
                        </thead>
                        <tbody>
                            {stats.recent_alerts.length === 0 ? (
                                <tr><td colSpan="5" style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>No active threats detected. System scanning...</td></tr>
                            ) : (
                                stats.recent_alerts.map((alert, i) => (
                                    <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', background: i === 0 ? 'rgba(239, 68, 68, 0.05)' : 'transparent' }}>
                                        <td style={{ padding: '20px', fontFamily: 'monospace', color: '#cbd5e1' }}>{new Date(alert.timestamp).toLocaleTimeString()}</td>
                                        <td style={{ padding: '20px', fontWeight: '600' }}>{alert.city}</td>
                                        <td style={{ padding: '20px' }}>
                                            <span style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#fca5a5', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold' }}>
                                                {alert.fraud_type}
                                            </span>
                                        </td>
                                        <td style={{ padding: '20px', fontFamily: 'monospace', fontSize: '1.1rem' }}>₹{alert.amount.toLocaleString()}</td>
                                        <td style={{ padding: '20px' }}>
                                            <span style={{ color: '#ef4444', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                                <span style={{ width: '8px', height: '8px', background: '#ef4444', borderRadius: '50%', display: 'inline-block', boxShadow: '0 0 10px #ef4444' }}></span>
                                                INTERCEPTED
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default LEADashboard;
