# MPL (Manovikas Premier League)

A fun cricket simulation game built with Pygame that recreates the excitement of T20 cricket matches between friends. This project simulates a 5-over cricket match between two teams with real-time gameplay, detailed statistics, and a dynamic scoreboard.

## Features

- **Complete Match Simulation**: Simulates a full 5-over cricket match with two innings
- **Real-time Gameplay**: Ball-by-ball updates with automatic progression and manual control options
- **Detailed Scoreboard**:
  - Current score and run rate
  - Active batsmen stats
  - Current bowler figures
  - Over-by-over batting history
  - Required run rate in second innings
- **Team Management**:
  - Custom team creation with 11 players each
  - Automatic bowler rotation
  - Batting order management
- **Match Events**:
  - Regular scoring (1-6 runs)
  - Wickets with remaining lives system
  - Extras (wides and no-balls in the last over)
  - Batsmen rotation for odd runs and over completion
- **Final Scorecard**:
  - Complete batting scorecard with runs and balls faced
  - Detailed bowling figures
  - Match result summary

## How to Play

1. Press SPACE to manually trigger the next ball, or let the game auto-progress every second
2. Watch as batsmen score runs, bowlers take wickets, and the match unfolds
3. Press 'S' after the match to view the detailed final scorecard
4. Press 'M' to return to the main scoreboard view

## Technical Details

- Built with Python using Pygame
- Features a modular design with separate Team and Player classes
- Includes realistic cricket simulation logic
- Dynamic UI with team logos and color-coded events
- Handles all cricket-specific rules like:
  - Over completion and bowler changes
  - Batsmen rotation
  - Run chase calculations
  - Match completion conditions

## Requirements

- Python 3.x
- Pygame library

## Future Enhancements

- Add support for custom team creation through UI
- Implement player statistics and tournament modes
- Add sound effects and animations
- Include more cricket-specific events and scenarios
- Add support for saving match results and maintaining leaderboards

This project is perfect for cricket enthusiasts who want to simulate quick matches or for friends looking to organize their own mini cricket league simulations.
