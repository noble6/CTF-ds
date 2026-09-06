# Scoring System Guide

## Overview

Your CTF uses a multi-layered scoring system that rewards both skill and timing.

## Scoring Components

### 1. Base Points
Each challenge has a fixed point value:
- **Easy**: 100-200 points
- **Medium**: 300-400 points  
- **Hard**: 500-800 points

### 2. First Blood Bonus 🩸

The first team/user to solve a challenge receives a **10% bonus**.

| Challenge Value | First Blood Bonus | Total for First Solver |
|----------------|-------------------|------------------------|
| 100 pts | +10 pts | 110 pts |
| 200 pts | +20 pts | 220 pts |
| 400 pts | +40 pts | 440 pts |
| 800 pts | +80 pts | 880 pts |

### 3. Critical Bonus ⏰

Solving a challenge in the **last 30 minutes** of the CTF awards a **5% bonus**.

| Challenge Value | Critical Bonus |
|----------------|----------------|
| 100 pts | +5 pts |
| 200 pts | +10 pts |
| 400 pts | +20 pts |
| 800 pts | +40 pts |

### 4. Hint Costs 💡

Viewing hints costs points from your score:

| Difficulty | Hint 1 | Hint 2 | Hint 3 |
|------------|--------|--------|--------|
| Easy | Free | -10 to -20 pts | -25 to -40 pts |
| Medium | Free | -25 to -40 pts | -50 to -80 pts |
| Hard | Free | -50 to -80 pts | -100 to -160 pts |

## Scoring Examples

### Example 1: First Blood on Hard Challenge
```
Challenge: SSRF Master (600 pts)
Solve time: 1 hour into CTF
First blood: Yes (+10% = +60 pts)
Critical: No
Hint used: Hint 1 (free)

Final score: 600 + 60 = 660 points
```

### Example 2: Late Solve with Hints
```
Challenge: Padding Oracle (700 pts)
Solve time: 5 hours 45 min into 6-hour CTF (last 15 min)
First blood: No
Critical: Yes (+5% = +35 pts)
Hints used: Hint 1 (-70 pts), Hint 2 (-140 pts)

Final score: 700 + 35 - 70 - 140 = 525 points
```

### Example 3: Easy Challenge with Hints
```
Challenge: SQL Rookie (200 pts)
Solve time: 2 hours into CTF
First blood: No
Critical: No
Hints used: Hint 1 (free), Hint 2 (-20 pts), Hint 3 (-40 pts)

Final score: 200 - 20 - 40 = 140 points
```

## Configuration

All scoring parameters can be adjusted in the admin panels:

### First Blood Configuration
- **Admin → Plugins → First Blood**
- Adjust bonus percentage (default: 10%)
- View first blood history

### Time Scoring Configuration
- **Admin → Plugins → Time Scoring**
- First blood bonus percentage
- Critical window duration (default: 30 minutes)
- Critical bonus percentage (default: 5%)
- Time decay settings (optional)

### Hint Configuration
- Edit `scripts/hint_config.py` before import
- Or modify hints in **Admin → Challenges → [Challenge] → Hints**

## Scoreboard Display

The scoreboard shows:
- **Rank**: Current position
- **Team/User**: Name
- **Score**: Total points
- **Solves**: Number of challenges solved
- **First Bloods**: Number of first bloods (🩸)

## Event Timeline

```
CTF Start                                              CTF End
    |                                                      |
    |  [Normal Scoring]                                    |
    |  - Base points                                       |
    |  - First blood bonus                                 |
    |                                                      |
    |                                    [Critical Window] |
    |                                    - Last 30 minutes |
    |                                    - +5% bonus       |
    |                                                      |
    +------------------------------------------------------+
```

## Tips for Participants

1. **Try challenges early** - First blood gives significant bonus
2. **Be strategic with hints** - They cost points!
3. **Watch the clock** - Critical bonus is small but helps
4. **Focus on what you know** - Easy challenges are quick points

## Admin Tips

1. **Freeze scoreboard** 30 min before end (optional)
2. **Announce first bloods** to create excitement
3. **Monitor hint usage** - Adjust costs if needed
4. **Keep critical window short** - 30 min creates urgency without chaos

## Troubleshooting

### First Blood not awarded
- Check if First Blood plugin is loaded
- Verify in Admin → Plugins → First Blood

### Critical bonus not working
- Ensure CTF end time is set in CTFd config
- Check Admin → Plugins → Time Scoring settings

### Hints not showing cost
- Verify hints were imported with `import_challenges.py`
- Check hint configuration in Admin → Challenges

## API Endpoints

For custom integrations:

```
GET /api/v1/first_blood          - Get all first bloods
GET /api/v1/scoring/config       - Get scoring configuration
GET /api/v1/scoreboard           - Get current scoreboard
```
