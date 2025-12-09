import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:8000');

const BankDashboard = () => {
    const [stats, setStats] = useState({ total_saved_inr: 0, blocked_cards: 0, false_positive_rate: '0.4%' });
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const fetchStats = async () => {
            const res = await fetch('http://127.0.0.1:8000/api/bank/stats');
            const data = await res.json();
            setStats(data);
        };
        fetchStats();

        socket.on('new_alert', (alert) => {
            const txn = alert.transaction;
            setStats(prev => ({
                ...prev,
                total_saved_inr: prev.total_saved_inr + txn.amount,
                blocked_cards: prev.blocked_cards + 1
            }));

            setLogs(prev => [{
                time: new Date(txn.timestamp).toLocaleTimeString(),
                desc: `${txn.sender_id} @ ${txn.city}`,
                amount: txn.amount,
                id: txn.txn_id,
                mcc: txn.mcc || 'N/A'
            }, ...prev].slice(0, 20)); // Keep last 20
        });

        return () => socket.off('new_alert');
    }, []);

    return (
        <div style={{ height: '100vh', background: 'var(--bg-core)', color: 'white', fontFamily: "'Inter', sans-serif", display: 'flex', flexDirection: 'column' }}>
            {/* Top Bar */}
            <div style={{ background: 'var(--bg-panel)', borderBottom: 'var(--glass-border)', padding: '0 40px', height: '70px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 4px 20px rgba(0,0,0,0.2)', zIndex: 10 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <h1 style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-primary)' }}>KAVACH <span style={{ color: 'white' }}>BANKING CORE</span></h1>
                    <span style={{ padding: '4px 12px', background: 'rgba(59, 130, 246, 0.15)', color: 'var(--accent-primary)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '20px', fontSize: '0.7rem', fontWeight: 'bold' }}>LIVE SYNC: HDFC-NET-01</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <button style={{
                        background: 'linear-gradient(45deg, #1e40af, #2563eb)',
                        color: 'white',
                        border: '1px solid #60a5fa',
                        padding: '8px 16px',
                        borderRadius: '6px',
                        fontWeight: 'bold',
                        fontSize: '0.8rem',
                        cursor: 'pointer',
                        boxShadow: '0 0 10px rgba(37, 99, 235, 0.4)'
                    }}>
                        ❄️ FREEZE ACCOUNTS
                    </button>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>ADMINISTRATOR</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Security Level 5</div>
                    </div>
                    <div style={{ width: '35px', height: '35px', background: 'linear-gradient(45deg, #3b82f6, #8b5cf6)', borderRadius: '50%' }}></div>
                </div>
            </div>

            {/* Content */}
            <div style={{ padding: '40px', display: 'flex', flexDirection: 'column', gap: '30px', flex: 1, overflow: 'hidden' }}>

                {/* Metrics Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
                    {/* Metric 1 */}
                    <div className="glass-panel" style={{ padding: '25px', position: 'relative', overflow: 'hidden' }}>
                        <div style={{ position: 'absolute', top: 0, right: 0, padding: '10px', opacity: 0.1 }}>
                            <svg width="60" height="60" fill="currentColor" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z" /></svg>
                        </div>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: '700', letterSpacing: '1px', marginBottom: '5px' }}>LIABILITY PREVENTED</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--accent-success)' }}>₹{stats.total_saved_inr.toLocaleString()}</div>
                        <div style={{ color: 'var(--accent-success)', fontSize: '0.8rem', marginTop: '5px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                            <span>▲ 12.5%</span> <span style={{ color: 'var(--text-secondary)' }}>vs last hour</span>
                        </div>
                    </div>

                    {/* Metric 2 */}
                    <div className="glass-panel" style={{ padding: '25px' }}>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: '700', letterSpacing: '1px', marginBottom: '5px' }}>CARDS AUTO-BLOCKED</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--accent-danger)' }}>{stats.blocked_cards}</div>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: '5px' }}>Actioned by AI Model v2.1</div>
                    </div>

                    {/* Metric 3 */}
                    <div className="glass-panel" style={{ padding: '25px' }}>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: '700', letterSpacing: '1px', marginBottom: '5px' }}>FALSE POSITIVE RATE</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--accent-primary)' }}>{stats.false_positive_rate}</div>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: '5px' }}>Within Optimal Range (&lt;0.5%)</div>
                    </div>
                </div>

                {/* Logs Section */}
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '15px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Real-Time Intervention Logs</h3>

                    <div className="glass-panel" style={{ flex: 1, overflowY: 'auto', padding: '10px' }}>
                        {logs.length === 0 ? (
                            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>System Idle. Listening for transactions...</div>
                        ) : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead style={{ position: 'sticky', top: 0, background: 'rgba(15, 23, 42, 0.95)', zIndex: 1 }}>
                                    <tr>
                                        <th style={{ textAlign: 'left', padding: '15px', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>TIME</th>
                                        <th style={{ textAlign: 'left', padding: '15px', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>ACTION</th>
                                        <th style={{ textAlign: 'left', padding: '15px', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>DESCRIPTION</th>
                                        <th style={{ textAlign: 'left', padding: '15px', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>AMOUNT</th>
                                        <th style={{ textAlign: 'left', padding: '15px', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>TXN ID</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {logs.map((log, i) => (
                                        <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                                            <td style={{ padding: '15px', fontFamily: 'monospace', color: 'var(--text-secondary)' }}>{log.time}</td>
                                            <td style={{ padding: '15px' }}>
                                                <span style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#fca5a5', padding: '4px 8px', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 'bold' }}>BLOCKED</span>
                                            </td>
                                            <td style={{ padding: '15px', fontWeight: '500' }}>{log.desc}</td>
                                            <td style={{ padding: '15px', fontFamily: 'monospace', fontWeight: 'bold' }}>₹{log.amount}</td>
                                            <td style={{ padding: '15px', fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{log.id.slice(0, 12)}...</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BankDashboard;
