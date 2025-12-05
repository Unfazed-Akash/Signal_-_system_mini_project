import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Marker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import io from 'socket.io-client';
import L from 'leaflet';
import AstraPanel from '../components/AstraPanel';

// Fix Leaflet icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const socket = io('http://localhost:8000');

const Dashboard = () => {
    const [transactions, setTransactions] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [atms, setAtms] = useState([]);
    const [selectedAlert, setSelectedAlert] = useState(null);
    const [simulating, setSimulating] = useState(false);
    const [stats, setStats] = useState({ fraudCount: 0, protected: 0 });

    useEffect(() => {
        // Fetch static ATM data
        fetch('http://localhost:8000/api/atms')
            .then(res => res.json())
            .then(data => setAtms(data))
            .catch(err => console.error("Failed to load ATMs", err));

        // Socket listeners
        socket.on('connect', () => console.log("Connected to KAVACH Brain"));

        socket.on('new_transaction', (txn) => {
            setTransactions(prev => [...prev.slice(-50), txn]); // Keep last 50
        });

        socket.on('new_alert', (alert) => {
            setAlerts(prev => [...prev.slice(-10), alert]);
            setStats(prev => ({ ...prev, fraudCount: prev.fraudCount + 1 }));
        });

        socket.on('sim_status', (status) => {
            setSimulating(status.running);
        });

        return () => socket.off();
    }, []);

    const toggleSimulation = () => {
        if (simulating) {
            socket.emit('stop_simulation');
        } else {
            socket.emit('start_simulation');
        }
    };

    return (
        <div className="dashboard-container">
            {/* Header */}
            <div className="header">
                <h1>🛡️ KAVACH <span className="highlight">TITANIUM</span></h1>
                <div className="stats-bar">
                    <div className="stat-item">
                        <span className="label">Protected ATMs</span>
                        <span className="value">{atms.length}</span>
                    </div>
                    <div className="stat-item danger">
                        <span className="label">Threats Detected</span>
                        <span className="value">{stats.fraudCount}</span>
                    </div>
                    <button
                        className={`sim-btn ${simulating ? 'active' : ''}`}
                        onClick={toggleSimulation}
                    >
                        {simulating ? '⏹ Stop Simulation' : '🎮 Start Simulation (God Mode)'}
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="content-grid">
                <div className="map-view">
                    <MapContainer center={[22.5937, 78.9629]} zoom={5} style={{ height: "100%", width: "100%" }}>
                        <TileLayer
                            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                        />

                        {/* ATMs - White markers */}
                        {atms.map(atm => (
                            <CircleMarker
                                key={atm.id}
                                center={[atm.lat, atm.lng]}
                                radius={4}
                                pathOptions={{ color: '#4a90e2', fillColor: '#4a90e2', fillOpacity: 0.8 }}
                            >
                                <Popup>{atm.location} ({atm.id})</Popup>
                            </CircleMarker>
                        ))}

                        {/* Transactions - Green (Normal) / Red (Fraud) */}
                        {transactions.map((txn, i) => (
                            <CircleMarker
                                key={i}
                                center={[txn.lat, txn.lng]}
                                radius={txn.is_fraud ? 8 : 3}
                                pathOptions={{
                                    color: txn.is_fraud ? '#ff4444' : '#00C851',
                                    fillColor: txn.is_fraud ? '#ff4444' : '#00C851',
                                    fillOpacity: 0.6
                                }}
                            >
                                <Popup>
                                    Amount: ₹{txn.amount.toFixed(2)}<br />
                                    Prob: {txn.fraud_probability}
                                </Popup>
                            </CircleMarker>
                        ))}

                        {/* Predictions - Yellow Pulsing Circles */}
                        {alerts.map(alert =>
                            alert.predicted_atms.map((pred, idx) => (
                                <CircleMarker
                                    key={`pred-${alert.id}-${idx}`}
                                    center={[pred.lat, pred.lng]}
                                    radius={15}
                                    pathOptions={{ color: '#ffbb33', fillColor: 'transparent', dashArray: '5, 5' }}
                                    className="pulsing-marker" // We'll add this class in CSS
                                    eventHandlers={{
                                        click: () => setSelectedAlert(alert)
                                    }}
                                >
                                    <Popup>
                                        <strong>⚠️ PREDICTED WITHDRAWAL</strong><br />
                                        Location: {pred.location}<br />
                                        Prob: {(pred.probability * 100).toFixed(0)}%
                                    </Popup>
                                </CircleMarker>
                            ))
                        )}
                    </MapContainer>
                </div>

                {/* Right Panel - Astra / Feed */}
                <div className="side-panel">
                    {selectedAlert ? (
                        <AstraPanel
                            alert={selectedAlert}
                            onClose={() => setSelectedAlert(null)}
                        />
                    ) : (
                        <div className="feed">
                            <h3>Live Intelligence Feed</h3>
                            {alerts.length === 0 ? <p className="empty-state">System Secure. Waiting for signals...</p> :
                                alerts.slice().reverse().map(alert => (
                                    <div key={alert.id} className="feed-item" onClick={() => setSelectedAlert(alert)}>
                                        <div className="feed-header">
                                            <span className="badge high">CRITICAL</span>
                                            <span className="time">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                                        </div>
                                        <p>Fraud detected in <strong>{alert.transaction.city}</strong></p>
                                        <p className="pred-count">{alert.predicted_atms.length} withdrawal targets projected</p>
                                    </div>
                                ))
                            }
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;