# KAVACH TITANIUM - DEMO GUIDE 🛡️

## 1. Preparation (Before Judges)
Ensure these are installed:
- **Python 3.8+**
- **Node.js 16+**

Open the project folder in VS Code:
`d:\Kavach_anitgravity - Copy`

---

## 2. Setup (If asked to show installation)
*Run these commands in the VS Code Terminal (Ctrl+`)*

### Backend Setup
1. Open a terminal.
2. Navigate to backend: `cd backend`
3. Create Virtual Environment: `python -m venv venv`
4. Activate it: `.\venv\Scripts\activate`
5. Install Dependencies: `pip install -r requirements.txt`

### Frontend Setup
1. Open a **new** terminal (Split or New).
2. Navigate to frontend: `cd frontend`
3. Install Dependencies: `npm install`

---

## 3. LIFT-OFF (Running the Demo)
*You need two terminal instances running simultaneously.*

### Terminal 1: BRAIN (Backend)
Run this from the **root folder** (`d:\Kavach_anitgravity - Copy`):
```powershell
python -m uvicorn backend.main:socket_app --host 127.0.0.1 --port 8000 --reload
```
*Wait until you see:* `Application startup complete.`

### Terminal 2: VISUALS (Frontend)
Run this from the **frontend folder**:
```powershell
cd frontend
npm run dev
```
*Wait until you see:* `Local: http://localhost:5173/`

---

## 4. The Presentation Flow
1. **Open Browser**: Go to `http://localhost:5173`
2. **Show Dashboard**: Explain the "Live Status" and "Protected ATMs".
3. **Trigger Simulation**:
   - Click the **"🎮 Start Simulation (God Mode)"** button.
   - Wait 3-5 seconds.
   - **Point out:**
     - 🔴 **Red Alerts**: "Fraud Detected" in the feed.
     - 🟡 **Map Markers**: Pulsing circles appearing on the map.
     - 📉 **Predictive Analytics**: The system predicting *where* the money is going.
4. **End Demo**: Click "Stop Simulation".

---

## 5. Troubleshooting 🔧

### "Backend not reachable" / "DISCONNECTED"
- **Cause**: The backend server is not running or crashed.
- **Fix**: Check `Terminal 1`. If it stopped, restart it with the command in Section 3.
- **Note**: Ensure you activated the virtual environment (`.\venv\Scripts\activate`) before running.

### "Module not found" errors
- **Cause**: Dependencies missing or wrong python environment.
- **Fix**: Run `pip install -r requirements.txt` again inside the `venv`.

### Map tiles not loading
- **Cause**: No internet connection.
- **Fix**: The map relies on OpenStreetMap/CartoCDN. Ensure you are online.
