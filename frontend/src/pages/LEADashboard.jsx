import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:8000');

const LEADashboard = () => {
    const [stats, setStats] = useState({ active_operations: 0, suspects_tracked: 0, recent_alerts: [] });

    useEffect(() => {
        const fetchStats = async () => {
            const res = await fetch('http://127.0.0.1:8000/api/lea/stats');
            const data = await res.json();
            setStats(data);
        };
        fetchStats();

        socket.on('new_alert', (alert) => {
            setStats(prev => ({
                ...prev,
                active_operations: prev.active_operations + 1,
                recent_alerts: [alert.transaction, ...prev.recent_alerts].slice(0, 15) // Incr to 15
            }));
        });

        return () => socket.off('new_alert');
    }, []);

    return (
        <div style={{ height: '100vh', background: 'var(--bg-core)', color: 'white', display: 'flex', fontFamily: "'Inter', sans-serif" }}>
            {/* Sidebar */}
            <div style={{ width: '280px', background: 'var(--bg-panel)', borderRight: 'var(--glass-border)', padding: '24px', display: 'flex', flexDirection: 'column' }}>
                <div style={{ marginBottom: '40px' }}>
                    <h2 style={{ color: 'var(--accent-success)', fontSize: '1.8rem', fontWeight: '900', letterSpacing: '1px', margin: 0 }}>
                        CYBER<span style={{ color: 'white' }}>POL</span>
                    </h2>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: '4px', letterSpacing: '2px' }}>UNIT-774 // NEW DELHI</div>
                </div>

                <div style={{ display: 'grid', gap: '20px' }}>
                    <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid var(--accent-success)' }}>
                        <div style={{ fontSize: '0.75rem', color: 'var(--accent-success)', fontWeight: 'bold' }}>ACTIVE INTERCEPTIONS</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: '800' }}>24</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>+3 in last hour</div>
                    </div>

                    <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid var(--accent-primary)' }}>
                        <div style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 'bold' }}>SUSPECTS UNDER WATCH</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: '800' }}>{stats.suspects_tracked}</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>High Confidence Targets</div>
                    </div>
                </div>

                <div style={{ marginTop: 'auto' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        <div style={{ width: '8px', height: '8px', background: 'var(--accent-success)', borderRadius: '50%', boxShadow: '0 0 10px var(--accent-success)' }}></div>
                        SYSTEM ONLINE
                    </div>
                </div>
            </div>

            {/* Main Feed */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
                <header style={{ padding: '30px 40px', borderBottom: 'var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(15, 23, 42, 0.5)' }}>
                    <div>
                        <h1 style={{ fontSize: '2rem', fontWeight: '800', margin: 0 }}>LIVE OPERATIONS CENTER</h1>
                        <p style={{ color: 'var(--text-secondary)', margin: '5px 0 0 0' }}>Real-time fraud interception and geospatial tracking.</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <button style={{
                            background: 'var(--accent-danger)',
                            color: 'white',
                            border: 'none',
                            padding: '10px 20px',
                            borderRadius: '4px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            marginBottom: '10px',
                            boxShadow: '0 0 15px rgba(239, 68, 68, 0.4)'
                        }}>
                            🚀 DEPLOY UNITS
                        </button>
                        <div style={{ fontSize: '2.5rem', fontWeight: '900', color: 'var(--accent-danger)', lineHeight: 1, textShadow: '0 0 20px rgba(239, 68, 68, 0.3)' }}>{stats.active_operations}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--accent-danger)', letterSpacing: '1px', fontWeight: 'bold' }}>CRITICAL ALERTS</div>
                    </div>
                </header>

                <div style={{ flex: 1, padding: '30px 40px', overflowY: 'auto' }}>
                    <div className="glass-panel" style={{ overflow: 'hidden' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                            <thead style={{ background: 'rgba(0,0,0,0.3)', borderBottom: 'var(--glass-border)' }}>
                                <tr>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>TIMESTAMP</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>SUSPECT ID</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>LOCATION (IP)</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>DEVICE / TYPE</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>AMOUNT</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>RISK SCORE</th>
                                    <th style={{ padding: '15px 20px', color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: '700' }}>STATUS</th>
                                </tr>
                            </thead>
                            <tbody>
                                {stats.recent_alerts.length === 0 ? (
                                    <tr><td colSpan="7" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>Scanning network traffic... No threats detected yet.</td></tr>
                                ) : (
                                    stats.recent_alerts.map((alert, i) => (
                                        <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)', background: i === 0 ? 'rgba(239, 68, 68, 0.05)' : 'transparent', transition: 'background 0.2s' }}>
                                            <td style={{ padding: '15px 20px', fontFamily: 'monospace', color: '#cbd5e1' }}>{new Date(alert.timestamp).toLocaleTimeString()}</td>
                                            <td style={{ padding: '15px 20px', fontFamily: 'monospace', color: 'var(--accent-primary)' }}>{alert.sender_id}</td>
                                            <td style={{ padding: '15px 20px' }}>
                                                <div style={{ fontWeight: '600' }}>{alert.city}</div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontFamily: 'monospace' }}>{alert.ip_address || '192.168.1.X'}</div>
                                            </td>
                                            <td style={{ padding: '15px 20px' }}>
                                                <div style={{ fontSize: '0.85rem' }}>{alert.device_id || 'Unknown Device'}</div>
                                                <span style={{ background: 'rgba(255, 255, 255, 0.05)', color: '#94a3b8', padding: '2px 6px', borderRadius: '4px', fontSize: '0.65rem' }}>
                                                    {alert.fraud_type}
                                                </span>
                                            </td>
                                            <td style={{ padding: '15px 20px', fontFamily: 'monospace', fontSize: '1rem', fontWeight: 'bold' }}>₹{alert.amount.toLocaleString()}</td>
                                            <td style={{ padding: '15px 20px' }}>
                                                {/* Fake Risk Score bar */}
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                    <div style={{ flex: 1, height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', width: '60px' }}>
                                                        <div style={{ width: '92%', height: '100%', background: 'var(--accent-danger)', borderRadius: '3px' }}></div>
                                                    </div>
                                                    <span style={{ color: 'var(--accent-danger)', fontWeight: 'bold', fontSize: '0.8rem' }}>92%</span>
                                                </div>
                                            </td>
                                            <td style={{ padding: '15px 20px' }}>
                                                <span style={{
                                                    background: 'rgba(239, 68, 68, 0.15)',
                                                    color: '#ef4444',
                                                    border: '1px solid rgba(239, 68, 68, 0.3)',
                                                    padding: '4px 10px',
                                                    borderRadius: '4px',
                                                    fontSize: '0.7rem',
                                                    fontWeight: 'bold',
                                                    display: 'inline-flex',
                                                    alignItems: 'center',
                                                    gap: '6px'
                                                }}>
                                                    <span style={{ width: '6px', height: '6px', background: '#ef4444', borderRadius: '50%', boxShadow: '0 0 5px #ef4444' }}></span>
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
        </div>
    );
};

export default LEADashboard;
