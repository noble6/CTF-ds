"""
CTFd Plugin: Time-Based Scoring
Implements dynamic scoring based on solve timing:
- First Blood Bonus: Extra points for first solver
- Critical Bonus: Extra points for solving near the end of CTF
- Time Decay: Points decrease as more time passes

Installation:
1. Copy this folder to CTFd/plugins/time_scoring/
2. Restart CTFd
3. Configure in Admin → Plugins → Time Scoring
"""

from CTFd.models import db, Solves, Challenges, Users, Teams
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils import user as current_user
from CTFd.utils.decorators import admins_only
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import json

# Default configuration
DEFAULT_CONFIG = {
    'first_blood_bonus': '10',        # 10% bonus for first blood
    'critical_window_minutes': '30',   # Last 30 minutes
    'critical_bonus': '5',            # 5% bonus for critical solves
    'time_decay_enabled': 'false',     # Whether points decay over time
    'decay_rate': '1',                # 1% decay per hour
    'min_points_percentage': '50',    # Minimum 50% of original points
}

class TimeScoringConfig(db.Model):
    """Store time-based scoring configuration"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

class CriticalSolve(db.Model):
    """Track critical timing solves"""
    id = db.Column(db.Integer, primary_key=True)
    solve_id = db.Column(db.Integer, db.ForeignKey('solves.id'), nullable=False)
    bonus_type = db.Column(db.String(32), nullable=False)  # 'first_blood' or 'critical'
    bonus_points = db.Column(db.Integer, nullable=False)
    awarded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    solve = db.relationship('Solves', foreign_keys=[solve_id])

    def __init__(self, solve_id, bonus_type, bonus_points):
        self.solve_id = solve_id
        self.bonus_type = bonus_type
        self.bonus_points = bonus_points

time_bp = Blueprint('time_scoring', __name__, template_folder='templates')

@time_bp.route('/admin/time_scoring', methods=['GET'])
@admins_only
def admin_panel():
    """Admin panel for time-based scoring configuration"""
    config = {}
    for item in TimeScoringConfig.query.all():
        config[item.key] = item.value
    
    # Fill defaults
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    
    # Get recent bonus awards
    recent_bonuses = CriticalSolve.query.order_by(
        CriticalSolve.awarded_at.desc()
    ).limit(50).all()
    
    return render_template('time_scoring_admin.html',
                         config=config,
                         recent_bonuses=recent_bonuses)

@time_bp.route('/admin/time_scoring/config', methods=['POST'])
@admins_only
def update_config():
    """Update time-based scoring configuration"""
    data = request.get_json()
    
    for key, value in data.items():
        config = TimeScoringConfig.query.filter_by(key=key).first()
        if config:
            config.value = str(value)
        else:
            config = TimeScoringConfig(key=key, value=str(value))
            db.session.add(config)
    
    db.session.commit()
    return jsonify({'success': True})

@time_bp.route('/api/v1/scoring/config', methods=['GET'])
def get_scoring_config():
    """API endpoint to get scoring configuration"""
    config = {}
    for item in TimeScoringConfig.query.all():
        config[item.key] = item.value
    
    # Fill defaults
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    
    return jsonify(config)

def get_config_value(key):
    """Get a configuration value with default"""
    config = TimeScoringConfig.query.filter_by(key=key).first()
    if config:
        return config.value
    return DEFAULT_CONFIG.get(key)

def calculate_time_bonus(solve, challenge, ctf_start, ctf_end):
    """Calculate time-based bonus for a solve"""
    bonus_points = 0
    bonus_type = None
    
    # Get configuration
    first_blood_pct = int(get_config_value('first_blood_bonus'))
    critical_window = int(get_config_value('critical_window_minutes'))
    critical_pct = int(get_config_value('critical_bonus'))
    
    # Check for first blood
    existing_solves = Solves.query.filter_by(
        challenge_id=challenge.id
    ).filter(Solves.id != solve.id).count()
    
    if existing_solves == 0:
        # First blood!
        bonus_points = int(challenge.value * (first_blood_pct / 100))
        bonus_type = 'first_blood'
    
    # Check for critical timing
    if ctf_end and solve.date:
        time_until_end = ctf_end - solve.date
        if time_until_end <= timedelta(minutes=critical_window):
            # Critical solve!
            if bonus_type is None:
                bonus_points = int(challenge.value * (critical_pct / 100))
                bonus_type = 'critical'
            else:
                # Both first blood and critical
                bonus_points += int(challenge.value * (critical_pct / 100))
                bonus_type = 'first_blood_critical'
    
    return bonus_points, bonus_type

def calculate_dynamic_points(challenge, solve_time, ctf_start, ctf_end):
    """Calculate dynamic points based on time elapsed"""
    if get_config_value('time_decay_enabled') != 'true':
        return challenge.value
    
    decay_rate = float(get_config_value('decay_rate'))
    min_pct = float(get_config_value('min_points_percentage'))
    
    # Calculate time elapsed as percentage of total CTF duration
    total_duration = (ctf_end - ctf_start).total_seconds()
    elapsed = (solve_time - ctf_start).total_seconds()
    
    if total_duration <= 0:
        return challenge.value
    
    hours_elapsed = elapsed / 3600
    decay = hours_elapsed * decay_rate
    
    # Calculate points with decay
    points = challenge.value * (1 - (decay / 100))
    min_points = challenge.value * (min_pct / 100)
    
    return max(int(points), int(min_points))

def load(app):
    """Load the plugin"""
    with app.app_context():
        db.create_all()
        
        # Set default config
        for key, value in DEFAULT_CONFIG.items():
            if not TimeScoringConfig.query.filter_by(key=key).first():
                config = TimeScoringConfig(key=key, value=value)
                db.session.add(config)
        
        db.session.commit()
    
    # Register blueprint
    app.register_blueprint(time_bp)
    
    # Register assets
    register_plugin_assets_directory(app, base_path='/plugins/time_scoring/assets/')
    
    print("[Time Scoring] Plugin loaded successfully!")
