// ============ Dashboard Script ============

let userLocation = null;

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');
    
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    document.getElementById('username').textContent = username;
    loadPredictionHistory();
    requestUserLocation();
});

// Request user's location for doctor recommendations
function requestUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                console.log('Location obtained:', userLocation);
                const locationStatus = document.getElementById('location-status');
                if (locationStatus) {
                    locationStatus.innerHTML = '✓ Location enabled for doctor recommendations';
                }
            },
            (error) => {
                console.log('Location error:', error.message);
                const locationStatus = document.getElementById('location-status');
                if (locationStatus) {
                    locationStatus.innerHTML = '⚠️ Enable location to find doctors near you';
                }
                userLocation = null;
            }
        );
    }
}

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'history') {
        loadPredictionHistory();
    }
}

// Logout
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.clear();
        window.location.href = '/';
    }
}

// Prediction Form Submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = localStorage.getItem('access_token');
    
    const predictionData = {
        age: parseFloat(document.getElementById('age').value),
        sex: parseFloat(document.getElementById('sex')?.value || 0),
        cp: parseFloat(document.getElementById('cp')?.value || 0),
        systolic: parseFloat(document.getElementById('systolic').value),
        diastolic: parseFloat(document.getElementById('diastolic').value),
        cholesterol: parseFloat(document.getElementById('cholesterol').value),
        fbs: parseFloat(document.getElementById('fbs')?.value || 0),
        restecg: parseFloat(document.getElementById('restecg')?.value || 0),
        heart_rate: parseFloat(document.getElementById('heart_rate').value),
        exang: parseFloat(document.getElementById('exang')?.value || 0),
        oldpeak: parseFloat(document.getElementById('oldpeak')?.value || 0.3),
        slope: parseFloat(document.getElementById('slope')?.value || 1),
        ca: parseFloat(document.getElementById('ca')?.value || 0),
        thal: parseFloat(document.getElementById('thal')?.value || 3),
        glucose: parseFloat(document.getElementById('glucose').value),
        location: userLocation
    };
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(predictionData)
        });
        
        if (!response.ok) {
            throw new Error('Prediction failed');
        }
        
        const data = await response.json();
        displayPredictionResult(data);
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Display Prediction Result with conditional doctor recommendations
function displayPredictionResult(data) {
    const resultContainer = document.getElementById('result-container');
    const resultCard = document.getElementById('result-card');
    
    const prediction = data.prediction;
    const probability = (data.probability * 100).toFixed(1);
    const feedback = data.feedback;
    
    let statusClass = prediction === 1 ? 'danger' : 'healthy';
    let statusEmoji = prediction === 1 ? '⚠️' : '✅';
    
    let doctorSection = '';
    if (feedback.severity === 'HIGH' && feedback.doctors && feedback.doctors.length > 0) {
        doctorSection = `
            <div class="result-item">
                <strong>🏥 RECOMMENDED DOCTORS NEAR YOU:</strong>
                <p class="doctor-note">${feedback.doctor_note}</p>
                <div class="doctors-list">
                    ${feedback.doctors.map(doctor => `
                        <div class="doctor-card">
                            <div class="name">${doctor.name}</div>
                            <div class="specialty">${doctor.specialty}</div>
                            <div class="rating">⭐ ${doctor.rating} • ${doctor.distance}</div>
                            ${doctor.phone ? `<div class="phone">📱 ${doctor.phone}</div>` : ''}
                            ${doctor.address ? `<div class="address">📍 ${doctor.address}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    } else if (feedback.doctor_note) {
        doctorSection = `
            <div class="result-item info-message">
                <strong>${feedback.doctor_note}</strong>
            </div>
        `;
    }
    
    let html = `
        <div class="result-status ${statusClass}">
            ${statusEmoji} ${feedback.status}
        </div>
        
        <div class="result-item">
            <strong>Confidence Level:</strong> ${probability}%
        </div>
        
        <div class="result-item">
            <strong>📋 Health Tips:</strong>
            <ul class="tips-list">
                ${feedback.tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
        
        <div class="result-item">
            <strong>⚕️ Recommended Action:</strong>
            <p>${feedback.action}</p>
        </div>
        
        ${doctorSection}
    `;
    
    resultCard.innerHTML = html;
    resultContainer.style.display = 'block';
    loadPredictionHistory();
}

// Load Prediction History
async function loadPredictionHistory() {
    const token = localStorage.getItem('access_token');
    const historyList = document.getElementById('history-list');
    
    try {
        const response = await fetch('/api/prediction-history', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const predictions = await response.json();
        
        if (predictions.length === 0) {
            historyList.innerHTML = '<p>No predictions yet. Make your first prediction!</p>';
            return;
        }
        
        let html = '';
        predictions.forEach(pred => {
            const date = new Date(pred.created_at).toLocaleDateString();
            const time = new Date(pred.created_at).toLocaleTimeString();
            const status = pred.prediction === 1 ? 'High BP' : 'Normal';
            const itemClass = pred.prediction === 1 ? 'high' : 'normal';
            const probability = (pred.probability * 100).toFixed(1);
            
            html += `
                <div class="history-item ${itemClass}">
                    <div class="history-item-content">
                        <div class="history-item-prediction">${status}</div>
                        <div class="history-item-date">${date} at ${time}</div>
                        <small>Confidence: ${probability}%</small>
                    </div>
                </div>
            `;
        });
        
        historyList.innerHTML = html;
    } catch (error) {
        historyList.innerHTML = `<p>Error loading history: ${error.message}</p>`;
    }
}
