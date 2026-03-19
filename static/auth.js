// ============ Authentication Script ============

function toggleForms() {
    document.getElementById('login-form').classList.toggle('active');
    document.getElementById('register-form').classList.toggle('active');
    clearMessages();
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('auth-message');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
}

function clearMessages() {
    const messageDiv = document.getElementById('auth-message');
    messageDiv.className = 'message';
    messageDiv.textContent = '';
}

// Login Form Submission
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token to localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('username', data.username);
            
            showMessage('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } else {
            showMessage(data.message || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
});

// Register Form Submission
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    
    if (password !== confirm) {
        showMessage('Passwords do not match', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Registration successful! Redirecting to login...', 'success');
            setTimeout(() => {
                document.getElementById('register-form').reset();
                toggleForms();
                showMessage('Please sign in with your new account', 'success');
            }, 1500);
        } else {
            showMessage(data.message || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
});
