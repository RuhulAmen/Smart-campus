// ============================================
// BACKEND API INTEGRATION
// ============================================

const API_BASE_URL = 'http://localhost:5000/api';

// API Helper
async function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
    };

    // Add token if available
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers,
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication Functions
async function login(email, password) {
    try {
        const result = await apiRequest('/auth/login', 'POST', { email, password });
        if (result.token) {
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));
            showToast('✅ Login successful!', 'success');
            return result;
        }
        return null;
    } catch (error) {
        showToast(error.message, 'error');
        return null;
    }
}

async function signup(userData) {
    try {
        const result = await apiRequest('/auth/signup', 'POST', userData);
        if (result.token) {
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));
            showToast('✅ Account created successfully!', 'success');
            return result;
        }
        return null;
    } catch (error) {
        showToast(error.message, 'error');
        return null;
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    showToast('Logged out successfully', 'info');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 500);
}

function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function isLoggedIn() {
    return !!localStorage.getItem('token');
}

// Facility Functions
async function getFacilities() {
    try {
        const result = await apiRequest('/facilities');
        return result.facilities || [];
    } catch (error) {
        console.error('Error fetching facilities:', error);
        return [];
    }
}

// Announcement Functions
async function getAnnouncements() {
    try {
        const result = await apiRequest('/announcements');
        return result.announcements || [];
    } catch (error) {
        console.error('Error fetching announcements:', error);
        return [];
    }
}

async function getRecentAnnouncements(limit = 5) {
    try {
        const result = await apiRequest(`/announcements/recent?limit=${limit}`);
        return result.announcements || [];
    } catch (error) {
        console.error('Error fetching recent announcements:', error);
        return [];
    }
}

// Issue Functions
async function reportIssue(issueData) {
    try {
        const result = await apiRequest('/issues', 'POST', issueData);
        showToast('✅ Issue reported successfully!', 'success');
        return result;
    } catch (error) {
        showToast(error.message, 'error');
        return null;
    }
}

// Dashboard Functions
async function getDashboardStats() {
    try {
        const result = await apiRequest('/dashboard/stats');
        return result.stats || null;
    } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        return null;
    }
}

// Toast Notification System
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toasts if too many
    const existingToasts = document.querySelectorAll('.toast');
    if (existingToasts.length >= 3) {
        existingToasts[0].remove();
    }

    // Create container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };

    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;

    container.appendChild(toast);

    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'slideInRight 0.4s ease reverse';
            setTimeout(() => toast.remove(), 400);
        }
    }, duration);
}

// Update Navigation
function updateNavigation() {
    const user = getCurrentUser();
    const nav = document.querySelector('header nav ul');
    if (!nav) return;

    if (user) {
        nav.innerHTML = `
            <li><a href="index.html">Home</a></li>
            <li><a href="facilities.html">Facilities</a></li>
            <li><a href="announcements.html">Announcements</a></li>
            <li><a href="dashboard.html">Dashboard</a></li>
            <li><a href="#" onclick="logout()">Logout</a></li>
        `;
    } else {
        nav.innerHTML = `
            <li><a href="index.html">Home</a></li>
            <li><a href="facilities.html">Facilities</a></li>
            <li><a href="announcements.html">Announcements</a></li>
            <li><a href="login.html">Login</a></li>
            <li><a href="signup.html">Sign Up</a></li>
        `;
    }
}

// Form Validation
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

// Make functions globally available
window.login = login;
window.signup = signup;
window.logout = logout;
window.getCurrentUser = getCurrentUser;
window.isLoggedIn = isLoggedIn;
window.getFacilities = getFacilities;
window.getAnnouncements = getAnnouncements;
window.getRecentAnnouncements = getRecentAnnouncements;
window.reportIssue = reportIssue;
window.getDashboardStats = getDashboardStats;
window.showToast = showToast;
window.updateNavigation = updateNavigation;
window.validateEmail = validateEmail;
window.validatePassword = validatePassword;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    updateNavigation();
});
// Remove existing toasts if too many