#!/usr/bin/env python3
"""
Custom CTFd Theme: College CTF 2026
Adds custom branding, first blood notifications, and time-based scoring display

Installation:
1. Copy this folder to CTFd/themes/college_ctf/
2. In CTFd Admin → Config → Theme, select 'college_ctf'
3. Restart CTFd
"""

# This is a theme configuration file
# The actual theme files (HTML, CSS, JS) would go in the templates/ and static/ folders

THEME_CONFIG = {
    'name': 'College CTF 2026',
    'description': 'Custom theme for College CTF with first blood and time scoring',
    'version': '1.0.0',
    'author': 'CTF Team',
    
    # Colors
    'primary_color': '#1565c0',
    'secondary_color': '#d32f2f',
    'accent_color': '#2e7d32',
    
    # Features
    'show_first_blood': True,
    'show_critical_timer': True,
    'show_leaderboard_animation': True,
}

# Custom CSS to add to the theme
CUSTOM_CSS = """
/* First Blood Styling */
.first-blood-badge {
    background: linear-gradient(135deg, #d32f2f, #f44336);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Critical Timer Styling */
.critical-timer {
    background: linear-gradient(135deg, #e65100, #ff9800);
    color: white;
    padding: 15px 25px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(230, 81, 0, 0.3);
}

.critical-timer.warning {
    background: linear-gradient(135deg, #d32f2f, #f44336);
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* Score Animation */
.score-update {
    animation: scorePop 0.5s ease-out;
}

@keyframes scorePop {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); color: #2e7d32; }
    100% { transform: scale(1); }
}

/* Leaderboard Styling */
.leaderboard-entry.first-place {
    background: linear-gradient(135deg, #ffd700, #ffed4a);
    font-weight: bold;
}

.leaderboard-entry.second-place {
    background: linear-gradient(135deg, #c0c0c0, #e0e0e0);
}

.leaderboard-entry.third-place {
    background: linear-gradient(135deg, #cd7f32, #e8a87c);
}

/* College Branding */
.college-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 20px;
    text-align: center;
}

.college-logo {
    max-height: 80px;
    margin-bottom: 10px;
}
"""

# Custom JavaScript for real-time features
CUSTOM_JS = """
// First Blood Notification
function showFirstBloodNotification(challengeName, userName) {
    const notification = document.createElement('div');
    notification.className = 'first-blood-notification';
    notification.innerHTML = `
        <div class="first-blood-badge">🩸 FIRST BLOOD!</div>
        <div><strong>${userName}</strong> solved <strong>${challengeName}</strong> first!</div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Critical Timer
function updateCriticalTimer(endTime) {
    const timerElement = document.getElementById('critical-timer');
    if (!timerElement) return;
    
    const now = new Date();
    const end = new Date(endTime);
    const diff = end - now;
    
    if (diff <= 0) {
        timerElement.textContent = 'CTF ENDED!';
        timerElement.classList.add('warning');
        return;
    }
    
    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    
    timerElement.textContent = `${minutes}m ${seconds}s remaining`;
    
    // Warning when less than 30 minutes
    if (minutes < 30) {
        timerElement.classList.add('warning');
    }
}

// Score Animation
function animateScore(element, newScore) {
    element.textContent = newScore;
    element.classList.add('score-update');
    setTimeout(() => element.classList.remove('score-update'), 500);
}

// WebSocket for real-time updates (if CTFd supports it)
function connectWebSocket() {
    // Implementation depends on CTFd's WebSocket support
    console.log('WebSocket connection ready');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set up critical timer if on scoreboard page
    const timerElement = document.getElementById('critical-timer');
    if (timerElement) {
        const endTime = timerElement.dataset.endtime;
        if (endTime) {
            setInterval(() => updateCriticalTimer(endTime), 1000);
            updateCriticalTimer(endTime);
        }
    }
});
"""

def get_theme_files():
    """Get all theme files for installation"""
    return {
        'config': THEME_CONFIG,
        'css': CUSTOM_CSS,
        'js': CUSTOM_JS,
    }

if __name__ == '__main__':
    print("College CTF 2026 Theme")
    print("=" * 40)
    print(f"Name: {THEME_CONFIG['name']}")
    print(f"Version: {THEME_CONFIG['version']}")
    print(f"\nFeatures:")
    print(f"  • First Blood notifications: {THEME_CONFIG['show_first_blood']}")
    print(f"  • Critical timer: {THEME_CONFIG['show_critical_timer']}")
    print(f"  • Leaderboard animations: {THEME_CONFIG['show_leaderboard_animation']}")
