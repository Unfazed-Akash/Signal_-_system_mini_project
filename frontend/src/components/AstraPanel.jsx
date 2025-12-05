import React from 'react';

const AstraPanel = ({ alert, onClose }) => {
    const { transaction, predicted_atms, timestamp } = alert;

    return (
        <div className="astra-panel">
            <div className="astra-header">
                <h2>🦅 ASTRA INTELLIGENCE</h2>
                <button className="close-btn" onClick={onClose}>×</button>
            </div>

            <div className="astra-body">
                <div className="section threat-level">
                    <label>THREAT LEVEL</label>
                    <div className="level-bar">
                        <div className="fill critical" style={{ width: '95%' }}>CRITICAL</div>
                    </div>
                </div>

                <div className="section details">
                    <div className="row">
                        <span><strong>Suspect ID:</strong></span>
                        <span className="code">{transaction.sender_id}</span>
                    </div>
                    <div className="row">
                        <span><strong>Amount:</strong></span>
                        <span className="value">₹{transaction.amount.toFixed(2)}</span>
                    </div>
                    <div className="row">
                        <span><strong>Origin:</strong></span>
                        <span>{transaction.city}</span>
                    </div>
                    <div className="row">
                        <span><strong>Velocity:</strong></span>
                        <span className="warning">HIGH (5.2 tx/hr)</span>
                    </div>
                </div>

                <div className="section predictions">
                    <h3>🔮 PREDICTED WITHDRAWAL POINTS</h3>
                    <div className="prediction-list">
                        {predicted_atms.map((atm, idx) => (
                            <div key={atm.id} className="prediction-item">
                                <div className="p-header">
                                    <span className="rank">#{idx + 1}</span>
                                    <span className="p-prob">{(atm.probability * 100).toFixed(0)}% Match</span>
                                </div>
                                <div className="p-loc">{atm.location}</div>
                                <div className="p-meta">
                                    <span>Lat: {atm.lat.toFixed(4)}</span>
                                    <span>ETA: {atm.estimated_time || '30 mins'}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="section actions">
                    <button className="action-btn deploy">🚀 DEPLOY LEA TEAMS</button>
                    <button className="action-btn freeze">❄️ FREEZE ACCOUNTS</button>
                </div>
            </div>
        </div>
    );
};

export default AstraPanel;