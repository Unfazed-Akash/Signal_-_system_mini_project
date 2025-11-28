# KAVACH TITANIUM 🛡️
### Real-Time Cybercrime Prediction & Fraud Detection System

**KAVACH TITANIUM** is an advanced, AI-driven surveillance system designed to detect, visualize, and prevent complex financial fraud patterns in real-time. It combines **Graph Algorithms** (NetworkX) with **Machine Learning** (Random Forest) to identify "Mule Fan-Out" attacks and "Circular Trading" schemes instantly.

---

## 🚀 Key Features

### 1. 🧠 Hybrid Detection Engine
*   **Graph Analysis**: Uses a directed graph (DiGraph) to detect structural fraud patterns like **Star Topologies** (Mule Fan-Out) and **Cycles** (Circular Trading).
*   **AI Risk Scoring**: A trained **Random Forest Classifier** analyzes transaction behavior (velocity, amount, time) to assign a risk probability (0-100%).

### 2. ⚡ Real-Time Dashboard
*   **Live Map**: Visualizes fraudulent transactions on a dark-themed, interactive map restricted to the Indian region.
*   **Instant Alerts**: WebSocket integration pushes alerts to the frontend within milliseconds of detection.
*   **Hotspot Visualization**: Displays historical high-risk zones.

### 3. 🕵️ Astra Panel (Investigation Suite)
*   **Interactive Network Graph**: Click on any alert to open the Astra Panel, which renders the fraud ring using force-directed graphs.
*   **Actionable Intelligence**: View critical metrics (Velocity, Geo-Cluster) and take immediate action.
*   **Freeze Capability**: "INITIATE FREEZE" button to simulate blocking the fraudulent account instantly.

### 4. 🎮 God Mode (Simulation)
*   **Historical Replay**: Includes a built-in simulation engine that feeds 50,000+ synthetic transactions into the system to demonstrate detection capabilities under load.

---

## 🛠️ Tech Stack

### Backend
*   **Framework**: FastAPI (Python)
*   **Real-Time**: Python-SocketIO
*   **Graph Engine**: NetworkX
*   **ML Library**: Scikit-Learn
*   **Data Processing**: Pandas, NumPy

### Frontend
*   **Framework**: React (Vite)
*   **Mapping**: Leaflet (React-Leaflet)
*   **Network Viz**: React-Force-Graph
*   **Styling**: CSS Modules (Dark Theme, Glassmorphism)

---

## 📦 Installation & Setup

### Prerequisites
*   Python 3.8+
*   Node.js 16+

### 1. Backend Setup
Navigate to the backend directory and install dependencies:

```bash
cd backend
# Create a virtual environment (optional but recommended)
python -m venv venv
# Activate it:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Frontend Setup
Navigate to the frontend directory and install Node modules:

```bash
cd frontend
npm install
```

---

## 🏃‍♂️ How to Run

### Step 1: Start the Backend Server
The backend handles the AI logic and WebSocket connections.

```bash
# From the root directory or inside /backend
python -m uvicorn backend.main:socket_app --host 0.0.0.0 --port 8000 --reload
```
*Server will start at `http://localhost:8000`*

### Step 2: Start the Frontend Dashboard
The frontend visualizes the data.

```bash
# Inside /frontend
npm run dev
```
*Dashboard will be available at `http://localhost:5173` (or similar)*

---

## 📖 Usage Guide

1.  **Open the Dashboard**: Go to the frontend URL in your browser.
2.  **Check Status**: Ensure the status indicator in the sidebar says **"LIVE"** (Green).
3.  **Start Simulation**: Click the **"Start Simulation (God Mode)"** button in the sidebar.
4.  **Monitor Alerts**:
    *   Watch as red markers appear on the map.
    *   See the "Recent Alerts" feed populate in the sidebar.
5.  **Investigate**:
    *   **Click** on any red marker on the map.
    *   The **Astra Panel** will open, showing the fraud network.
    *   Review the **Risk Score** and **Factors**.
6.  **Take Action**:
    *   Click **"INITIATE FREEZE"** in the Astra Panel to block the account.

---

## 📂 Project Structure

```
KAVACH_TITANIUM/
├── backend/
│   ├── data/               # Synthetic training data
│   ├── models/             # Serialized AI models (.pkl)
│   ├── main.py             # FastAPI App & Logic
│   ├── train_model.py      # ML Training Script
│   ├── data_generator.py   # Data Generation Script
│   └── requirements.txt    # Python Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # AstraPanel, etc.
│   │   ├── pages/          # Dashboard.jsx
│   │   ├── utils/          # Socket.js configuration
│   │   └── App.jsx         # Main React Component
│   └── package.json        # Node Dependencies
└── README.md               # Project Documentation
```

---

## 🛡️ Security Note
This project is a prototype. In a production environment, ensure to:
*   Secure WebSocket connections (WSS).
*   Implement JWT Authentication for API endpoints.
*   Use a persistent database (PostgreSQL/Neo4j) instead of in-memory graphs.

---

*Built for the Kavach 2023 Hackathon / Cybercrime Prevention Initiative.*
