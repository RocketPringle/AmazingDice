# GitHub Instructions for AmazingDice

## First Time Setup (Other Computer)
1. Open Cursor
2. Open terminal (View > Terminal)
3. Navigate to where you want the project (using `cd` command)
4. Clone the repository:
   ```
   git clone https://github.com/RocketPringle/AmazingDice.git
   ```

## Regular Usage

### When you want to SEND changes to GitHub:
1. Stage your changes:
   ```
   git add .
   ```
2. Commit your changes with a message:
   ```
   git commit -m "Describe what you changed"
   ```
3. Push to GitHub:
   ```
   git push
   ```

### When you want to GET changes from GitHub:
1. Pull the latest changes:
   ```
   git pull
   ```

## Tips
- Always `pull` before you start working to get the latest changes
- Always `push` when you're done working so your changes are available on other computers
- Write helpful commit messages that describe what you changed
- If you get stuck, you can always check the status of your repository with:
  ```
  git status
  ```

## Common Issues
- If you get conflicts (both computers edited the same file), Git will mark these in the file. You'll need to manually resolve them by choosing which changes to keep.
- If you forget to pull before making changes, you might need to merge changes. The easiest way is usually to pull first, then make your changes.

## Making Repository Private
1. Go to https://github.com/RocketPringle/AmazingDice/settings
2. Scroll down to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Make private"
5. Follow the confirmation steps 