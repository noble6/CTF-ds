"""
CTFd Plugin: First Blood Bonus
Awards bonus points to the first team/user to solve a challenge

Installation:
1. Copy this folder to CTFd/plugins/first_blood/
2. Restart CTFd
3. Configure bonus points in Admin → Plugins → First Blood
"""

from CTFd.models import db, Solves, Challenges, Users, Teams
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import BaseChallenge
from CTFd.utils import user as current_user
from CTFd.utils.decorators import admins_only
from flask import Blueprint, render_template, request, jsonify
import json

# Configuration
FIRST_BLOOD_PERCENTAGE = 10  # 10% bonus of challenge value
FIRST_BLOOD_MESSAGE = "🩸 First Blood!"

class FirstBloodConfig(db.Model):
    """Store first blood configuration"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

class FirstBloodSolve(db.Model):
    """Track first blood solves"""
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    solve_time = db.Column(db.DateTime, nullable=False)
    bonus_points = db.Column(db.Integer, nullable=False, default=0)

    challenge = db.relationship('Challenges', foreign_keys=[challenge_id])
    user = db.relationship('Users', foreign_keys=[user_id])
    team = db.relationship('Teams', foreign_keys=[team_id])

    def __init__(self, challenge_id, user_id, team_id, solve_time, bonus_points):
        self.challenge_id = challenge_id
        self.user_id = user_id
        self.team_id = team_id
        self.solve_time = solve_time
        self.bonus_points = bonus_points

first_bp = Blueprint('first_blood', __name__, template_folder='templates')

@first_bp.route('/admin/first_blood', methods=['GET'])
@admins_only
def admin_panel():
    """Admin panel for first blood configuration"""
    config = {}
    for item in FirstBloodConfig.query.all():
        config[item.key] = item.value
    
    bloods = FirstBloodSolve.query.order_by(FirstBloodSolve.solve_time.desc()).all()
    
    return render_template('first_blood_admin.html',
                         config=config,
                         bloods=bloods,
                         challenges=Challenges.query.all())

@first_bp.route('/admin/first_blood/config', methods=['POST'])
@admins_only
def update_config():
    """Update first blood configuration"""
    data = request.get_json()
    
    for key, value in data.items():
        config = FirstBloodConfig.query.filter_by(key=key).first()
        if config:
            config.value = str(value)
        else:
            config = FirstBloodConfig(key=key, value=str(value))
            db.session.add(config)
    
    db.session.commit()
    return jsonify({'success': True})

@first_bp.route('/api/v1/first_blood', methods=['GET'])
def get_first_bloods():
    """API endpoint to get first blood data"""
    bloods = FirstBloodSolve.query.order_by(FirstBloodSolve.solve_time).all()
    
    result = []
    for blood in bloods:
        result.append({
            'challenge_id': blood.challenge_id,
            'challenge_name': blood.challenge.name,
            'user_id': blood.user_id,
            'user_name': blood.user.name,
            'team_id': blood.team_id,
            'team_name': blood.team.name if blood.team else None,
            'solve_time': blood.solve_time.isoformat(),
            'bonus_points': blood.bonus_points
        })
    
    return jsonify({'first_bloods': result})

def check_first_blood(solve):
    """Check if a solve is first blood and award bonus"""
    # Check if challenge already has a solve
    existing = FirstBloodSolve.query.filter_by(
        challenge_id=solve.challenge_id
    ).first()
    
    if existing:
        return False  # Not first blood
    
    # Get bonus percentage from config
    config = FirstBloodConfig.query.filter_by(key='bonus_percentage').first()
    bonus_pct = int(config.value) if config else FIRST_BLOOD_PERCENTAGE
    
    # Calculate bonus points
    challenge = Challenges.query.get(solve.challenge_id)
    bonus_points = int(challenge.value * (bonus_pct / 100))
    
    # Record first blood
    blood = FirstBloodSolve(
        challenge_id=solve.challenge_id,
        user_id=solve.user_id,
        team_id=solve.team_id,
        solve_time=solve.date,
        bonus_points=bonus_points
    )
    db.session.add(blood)
    
    # Award bonus points to user/team
    user = Users.query.get(solve.user_id)
    if user:
        # Add bonus to user's score (via a custom field or additional solve)
        # This depends on CTFd's scoring implementation
        pass
    
    db.session.commit()
    
    return True

def load(app):
    """Load the plugin"""
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Set default config
        if not FirstBloodConfig.query.filter_by(key='bonus_percentage').first():
            config = FirstBloodConfig(key='bonus_percentage', value=str(FIRST_BLOOD_PERCENTAGE))
            db.session.add(config)
            db.session.commit()
    
    # Register blueprint
    app.register_blueprint(first_bp)
    
    # Register assets
    register_plugin_assets_directory(app, base_path='/plugins/first_blood/assets/')
    
    # Hook into solve process
    # Note: This requires modifying CTFd's solve handling or using signals
    print("[First Blood] Plugin loaded successfully!")
