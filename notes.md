# Amazing Dice Game - Development Notes

## To-Do List 
1. Authentication System ✔
   - Sign up functionality ✔
   - Password requirements (12 chars, capital, lowercase, special char) ✔
   - Login system ✔
   - Guest mode ✔

2. Stats System ✔
   - File management for storing stats ✔
   - Stats display interface ✔
   - Track wins/losses ✔

3. Match System
   - Person vs Person 
     - Player authentication/guest mode
     - First roll mechanism
     - 3 rolls per player ✔
     - Draw handling ✔
     - Score tracking ✔
     - Make online queue?
   
   - Person vs Bot ✔
     - Difficulty modifiers implementation ✔
     - Score calculation with modifiers ✔
     - Draw handling ✔
     - Score tracking ✔

4. UI Enhancements
   - ASCII art trophy for winners ✔
   - Score display formatting ✔
   - Menu styling improvements ✔
   - Actual gui/maybe website or web app 

## Ideas for Future Features 
- P2W would be hilarious
- SHOP !!!!
- Online multiplayer
- Tournament mode
- Custom dice sizes (class/upgrade thing)
- Achievement system
- High score leaderboard
- Classes that change dice stats + luck? (some bonuses from specific numbers? some get more points for lower, maybe take away opponents score? idk i want this to actualy be interesting not just pure rng and nothing else)
- Upgrades using currencies
- Cool rolling animations etc

## Bug Tracking 
*Add bugs and issues here as they're discovered*

## Notes on Implementation 
- Bot difficulties: ✔
  - Easy: score - 2  ✔
  - Medium: score - 1 ✔
  - Hard: no modifier ✔
  - Expert: score + 1 ✔
- Each match consists of 3 rolls per player ✔
- And five rounds ✔
- Draws trigger additional rolls  ✔

monday:
remove scrolls on guis and work on converting all terminal stuff left over to guis, plus mroe gui design