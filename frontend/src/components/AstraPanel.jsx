import React from 'react';

const AstraPanel = ({ alert, onClose }) => {
    return (
        <div className="astra-panel" style={{ height: '100%', display: 'flex', flexDirection: 'column', background: 'rgba(15, 23, 42, 0.95)', borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
            <div className="astra-header" style={{ padding: '20px', borderBottom: '1px solid rgba(255,255,255,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#38bdf8', fontSize: '1.2rem', letterSpacing: '1px' }}>ASTRA INTELLIGENCE</h2>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>Threat Analysis Engine v2.0</span>
                </div>
                <button
                    onClick={onClose}
                    style={{ background: 'none', border: 'none', color: '#64748b', fontSize: '1.5rem', cursor: 'pointer', transition: 'color 0.2s' }}
                    onMouseOver={(e) => e.target.style.color = '#fff'}
                    onMouseOut={(e) => e.target.style.color = '#64748b'}
                >
                    &times;
                </button>
            </div>

            <div className="astra-body" style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
                <div className="section" style={{ marginBottom: '30px' }}>
                    <div className="row" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '0.9rem' }}>
                        <span style={{ color: '#94a3b8' }}>TRANSACTION ID</span>
                        <span className="code" style={{ fontFamily: 'monospace', color: '#fff' }}>{alert.transaction.txn_id.split('-')[0]}...</span>
                    </div>
                    <div className="row" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '0.9rem' }}>
                        <span style={{ color: '#94a3b8' }}>AMOUNT</span>
                        <span style={{ color: '#fff', fontWeight: 'bold' }}>₹{alert.transaction.amount.toLocaleString()}</span>
                    </div>
                    <div className="row" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '0.9rem' }}>
                        <span style={{ color: '#94a3b8' }}>RISK SCORE</span>
                        <span className="warning" style={{ color: '#ef4444', fontWeight: 'bold' }}>{(alert.transaction.fraud_probability * 100).toFixed(1)}%</span>
                    </div>

                    <div className="level-bar" style={{ height: '6px', background: '#334155', borderRadius: '3px', marginTop: '10px', overflow: 'hidden' }}>
                        <div className="fill critical" style={{ width: `${alert.transaction.fraud_probability * 100}%`, height: '100%', background: 'linear-gradient(90deg, #f59e0b, #ef4444)' }}></div>
                    </div>
                </div>

                <div className="predictions">
                    <h3 style={{ fontSize: '0.85rem', color: '#94a3b8', textTransform: 'uppercase', borderBottom: '1px solid #334155', paddingBottom: '5px', marginBottom: '15px' }}>Predicted Withdrawal Points</h3>

                    {alert.predicted_atms.map((pred, i) => (
                        <div key={i} className="prediction-item" style={{
                            background: 'rgba(255,255,255,0.03)',
                            borderLeft: '2px solid #fbbf24',
                            padding: '12px',
                            marginBottom: '10px',
                            borderRadius: '0 4px 4px 0'
                        }}>
                            <div className="p-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                                <span className="rank" style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '0.8rem' }}>#{i + 1} TARGET</span>
                                <span className="p-prob" style={{ color: '#fff', fontSize: '0.8rem' }}>{(pred.probability * 100).toFixed(0)}% PROB</span>
                            </div>
                            <div className="p-loc" style={{ color: '#e2e8f0', fontSize: '0.95rem', fontWeight: '600' }}>{pred.location}</div>
                            <div className="p-meta" style={{ display: 'flex', justifyContent: 'space-between', marginTop: '5px', fontSize: '0.75rem', color: '#64748b' }}>
                                <span>ETA: {pred.estimated_time}</span>
                                <span>DIST: {pred.distance} km</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="actions" style={{ padding: '20px', display: 'grid', gap: '10px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                <button className="action-btn deploy" style={{
                    width: '100%', padding: '12px', border: 'none', borderRadius: '4px',
                    background: '#0ea5e9', color: 'white', fontWeight: 'bold', letterSpacing: '0.5px', cursor: 'pointer',
                    boxShadow: '0 4px 6px -1px rgba(14, 165, 233, 0.4)'
                }}>
                    DEPLOY UNITS
                </button>
                <button className="action-btn freeze" style={{
                    width: '100%', padding: '12px', border: '1px solid #ef4444', borderRadius: '4px',
                    background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', fontWeight: 'bold', letterSpacing: '0.5px', cursor: 'pointer'
                }}>
                    FREEZE ACCOUNTS
                </button>
            </div>
        </div>
    );
};

export default AstraPanel;