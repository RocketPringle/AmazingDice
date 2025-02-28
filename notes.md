# Amazing Dice Game - Development Notes

## Current Features 
- Menu system with multiple levels
- Dice rolling animation
- Bot difficulty levels (-2 to +1 modifiers)
- Sign out animation

## To-Do List 
1. Authentication System
   - Sign up functionality
   - Password requirements (12 chars, capital, lowercase, special char)
   - Login system
   - Guest mode

2. Stats System
   - File management for storing stats
   - Stats display interface
   - Track wins/losses

3. Match System
   - Person vs Person
     - Player authentication/guest mode
     - First roll mechanism
     - 3 rolls per player
     - Draw handling
     - Score tracking
   
   - Person vs Bot
     - Difficulty modifiers implementation
     - Score calculation with modifiers
     - Draw handling
     - Score tracking

4. UI Enhancements
   - ASCII art trophy for winners
   - Score display formatting
   - Menu styling improvements

## Ideas for Future Features 💡
- Online multiplayer
- Tournament mode
- Custom dice sizes
- Achievement system
- High score leaderboard

## Bug Tracking 🐛
*Add bugs and issues here as they're discovered*

## Notes on Implementation 
- Bot difficulties:
  - Easy: score - 2
  - Medium: score - 1
  - Hard: no modifier
  - Expert: score + 1
- Each match consists of 3 rolls per player
- Draws trigger additional rolls 