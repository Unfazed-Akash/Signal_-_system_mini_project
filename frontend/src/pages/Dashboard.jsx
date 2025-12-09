import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Marker, useMap, Polyline } from 'react-leaflet';
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

// Custom Tactical Icon
const createTacticalIcon = () => {
    return L.divIcon({
        className: 'glow-marker', // Defined in index.css
        iconSize: [20, 20],
        iconAnchor: [10, 10] // Center it
    });
};

const socket = io('http://127.0.0.1:8000');

const Dashboard = () => {
    const [transactions, setTransactions] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [atms, setAtms] = useState([]);
    const [selectedAlert, setSelectedAlert] = useState(null);
    const [simulating, setSimulating] = useState(false);
    const [stats, setStats] = useState({ fraudCount: 0, protected: 0 });
    const [connectionError, setConnectionError] = useState(false);

    useEffect(() => {
        // Fetch static ATM data
        fetch('http://127.0.0.1:8000/api/atms')
            .then(res => {
                if (!res.ok) throw new Error("Backend not reachable");
                return res.json();
            })
            .then(data => {
                setAtms(data);
                setConnectionError(false);
            })
            .catch(err => {
                console.error("Failed to load ATMs:", err);
                setConnectionError(true);
            });

        // Socket listeners
        socket.on('connect', () => {
            setConnectionError(false);
        });

        socket.on('connect_error', (err) => {
            setConnectionError(true);
        });

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
        if (connectionError) return;
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
                {connectionError && (
                    <div className="error-banner" style={{ background: '#ff4444', color: 'white', padding: '5px 10px', borderRadius: '4px', marginLeft: '20px', fontSize: '0.9rem' }}>
                        ⚠️ DISCONNECTED - CHECK BACKEND
                    </div>
                )}
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
                    <MapContainer
                        center={[22.5937, 78.9629]}
                        zoom={5}
                        style={{ height: "100%", width: "100%" }}
                        minZoom={5}
                        maxZoom={18}
                        maxBounds={[[5.0, 65.0], [38.0, 98.0]]} // Lock to India
                        maxBoundsViscosity={1.0} // Sticky bounds
                    >
                        {/* Dark Mode Map Provider */}
                        <TileLayer
                            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
                            noWrap={true} // Stop world repeating
                        />

                        {/* ATMs - Subtle White Dots */}
                        {atms.map(atm => (
                            <CircleMarker
                                key={atm.id}
                                center={[atm.lat, atm.lng]}
                                radius={2}
                                pathOptions={{ color: '#4a90e2', fillColor: '#4a90e2', fillOpacity: 0.5, opacity: 0.5 }}
                            >
                                <Popup>{atm.location} ({atm.id})</Popup>
                            </CircleMarker>
                        ))}

                        {/* Transactions - Green (Normal) / Red (Fraud) */}
                        {transactions.map((txn, i) => (
                            <CircleMarker
                                key={i}
                                center={[txn.lat, txn.lng]}
                                radius={txn.is_fraud ? 6 : 2}
                                pathOptions={{
                                    color: txn.is_fraud ? '#ef4444' : '#10b981',
                                    fillColor: txn.is_fraud ? '#ef4444' : '#10b981',
                                    fillOpacity: 0.8,
                                    weight: 1
                                }}
                            >
                                <Popup>
                                    <div style={{ color: 'black' }}>
                                        <strong>{txn.is_fraud ? "🚨 FRAUD DETECTED" : "✅ Valid Txn"}</strong><br />
                                        Amount: ₹{txn.amount.toLocaleString()}<br />
                                        <hr style={{ margin: '5px 0', border: '0.5px solid #ccc' }} />
                                        Origin: <strong>{txn.user_home_location || "Unknown"}</strong><br />
                                        Location: <strong>{txn.city}</strong><br />
                                    </div>
                                </Popup>
                            </CircleMarker>
                        ))}

                        {/* Predictions - TACTICAL GLOW MARKERS */}
                        {
                            alerts.map(alert => (
                                <React.Fragment key={`alert-group-${alert.id}`}>
                                    {/* 1. The Line of Attack (Red) */}
                                    {alert.transaction.prev_lat && (
                                        <Polyline
                                            positions={[
                                                [alert.transaction.prev_lat, alert.transaction.prev_lng],
                                                [alert.transaction.lat, alert.transaction.lng]
                                            ]}
                                            pathOptions={{ color: '#ef4444', weight: 2, dashArray: '5, 5', opacity: 0.6 }}
                                        >
                                            <Popup>Movement Vector</Popup>
                                        </Polyline>
                                    )}

                                    {/* 2. The Predicted Withdrawals (Gold Glow) */}
                                    {alert.predicted_atms.map((pred, idx) => (
                                        <React.Fragment key={`pred-group-${alert.id}-${idx}`}>
                                            {/* Trajectory Line */}
                                            <Polyline
                                                positions={[
                                                    [alert.transaction.lat, alert.transaction.lng],
                                                    [pred.lat, pred.lng]
                                                ]}
                                                pathOptions={{ color: '#fbbf24', weight: 1, dashArray: '2, 4', opacity: 0.6 }}
                                            />

                                            {/* TACTICAL MARKER - No more moving circle. Just a pulsing glow. */}
                                            <Marker
                                                position={[pred.lat, pred.lng]}
                                                icon={createTacticalIcon()}
                                                eventHandlers={{
                                                    click: () => setSelectedAlert(alert)
                                                }}
                                            >
                                                <Popup>
                                                    <strong>⚠️ PREDICTED TARGET</strong><br />
                                                    Location: {pred.location}<br />
                                                    Confidence: {(pred.probability * 100).toFixed(0)}%
                                                </Popup>
                                            </Marker>
                                        </React.Fragment>
                                    ))}
                                </React.Fragment>
                            ))
                        }
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
                            {alerts.length === 0 ? <p style={{ padding: '20px', color: 'var(--text-secondary)' }}>System Secure. Monitoring Net-Traffic...</p> :
                                alerts.slice().reverse().map(alert => (
                                    <div key={alert.id} className="feed-item" onClick={() => setSelectedAlert(alert)}>
                                        <div className="feed-header">
                                            <span className="badge high">CRITICAL</span>
                                            <span className="time">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                                        </div>
                                        <p style={{ margin: '5px 0', fontSize: '0.9rem' }}>Suspicious Activity in <strong style={{ color: 'white' }}>{alert.transaction.city}</strong></p>
                                        <p className="pred-count">► {alert.predicted_atms.length} locations identified</p>
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