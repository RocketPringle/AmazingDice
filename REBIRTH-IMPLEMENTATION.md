# Rebirth Mechanic – Implementation Guide

Rebirth = reset progress (coins, inventory) in exchange for **permanent** bonuses that persist across resets. Each rebirth makes the next run slightly stronger so you progress faster.

---

## 1. Data model

Add to each user in `userInfo.json`:

```json
"rebirthCount": 0
```

- **Persists:** `rebirthCount`, `hashedPassword`, `joinDate`, `achievements`, `achievementProgress`
- **Resets on rebirth:** `coins`, `inventory`, and optionally `stats` (your choice)

### In `amazingDice.py` – `addNewUser()`

Add the new field when creating a user (after `"inventory": []`):

```python
"inventory": [],
"rebirthCount": 0
```

### Safe reads for old saves

Anywhere you read rebirth data, default for users created before this feature:

```python
def getRebirthCount(username):
    data = loadUsers()
    return data['users'][username].get('rebirthCount', 0)
```

---

## 2. Rebirth logic (`amazingDice.py`)

### Constants (at top of file or near other constants)

```python
REBIRTH_COST = 50_000   # coins required to rebirth
REBIRTH_START_COINS = 500  # coins given after rebirth (optional, or 0)
```

### Check if player can rebirth

```python
def canRebirth(username):
    if username == 'Guest':
        return False
    return getCoins(username) >= REBIRTH_COST
```

### Perform rebirth

```python
def doRebirth(username):
    if username == 'Guest' or not canRebirth(username):
        return False
    data = loadUsers()
    u = data['users'][username]
    u['coins'] = REBIRTH_START_COINS
    u['inventory'] = []
    u['rebirthCount'] = u.get('rebirthCount', 0) + 1
    # Optional: reset stats too (wins/losses/etc.)
    # resetStats(u['stats'])
    saveUsers(data)
    return True
```

### Rebirth bonus (permanent multiplier)

Example: 10% more coin rewards per rebirth (1.1, 1.2, 1.3, …).

```python
def getRebirthRewardMultiplier(username):
    if username == 'Guest':
        return 1.0
    count = getRebirthCount(username)
    return 1.0 + (count * 0.10)  # 10% per rebirth
```

Optional: extra dice sides per rebirth.

```python
def getRebirthDiceBonus(username):
    if username == 'Guest':
        return 0
    return getRebirthCount(username)  # +1 side per rebirth, or use 2 * count
```

---

## 3. Apply the bonus in the game

### Rewards – `getWinReward()`

Multiply the final reward by the rebirth multiplier:

```python
def getWinReward(difficulty, username):
    # ... existing winMulti logic ...
    base = int(500 * mult)  # or 750, 1000, 1500 from your if/elif
    rebirth_mult = getRebirthRewardMultiplier(username)
    return int(base * rebirth_mult)
```

(You already have `mult` and the if/elif for difficulty; multiply the final `return` value by `rebirth_mult`.)

### Dice size – `getSize()`

If you added `getRebirthDiceBonus()`:

```python
def getSize(username):
    inventory = getInventory(username)
    base = 6
    # ... existing item loop ...
    return base + getRebirthDiceBonus(username)
```

---

## 4. GUI (`amazingDiceGUI.py`)

### Menu – Rebirth button

In `menu()`, add a Rebirth button (e.g. after Shop, before Settings):

```python
def rebirthPressed():
    menuWindow.destroy()
    rebirthWindow(username, settings)  # new window

rebirthButton = customtkinter.CTkButton(menuWindow, text='Rebirth', command=rebirthPressed)
rebirthButton.pack(pady=10)
```

Disable for guests:

```python
rebirthButton = customtkinter.CTkButton(
    menuWindow, text='Rebirth',
    command=rebirthPressed,
    state='disabled' if guestMode else 'normal'
)
```

### Rebirth window

New function that shows:

- Current rebirth count
- Current bonus (e.g. “Reward multiplier: 1.2x”)
- Cost (e.g. “Requires 50,000 coins”)
- Current coins
- Confirm / Back

Only allow Confirm when `ad.canRebirth(username)` is True. On confirm:

- Call `ad.doRebirth(username)`
- Show a short “Rebirth complete! You are now Rebirth 1.” message
- Close rebirth window and reopen menu (so coins and UI refresh)

Example layout:

```python
def rebirthWindow(username, guestMode, settings):
    rw = customtkinter.CTk()
    rw.geometry('400x350')
    rw.title('Amazing Dice - Rebirth')

    count = ad.getRebirthCount(username)
    coins = ad.getCoins(username)
    can_do = ad.canRebirth(username)
    mult = ad.getRebirthRewardMultiplier(username)

    customtkinter.CTkLabel(rw, text='Rebirth', font=('Arial Bold', 24)).pack(pady=15)
    customtkinter.CTkLabel(rw, text=f'Rebirths: {count}').pack(pady=5)
    customtkinter.CTkLabel(rw, text=f'Reward multiplier: {mult:.1f}x').pack(pady=5)
    customtkinter.CTkLabel(rw, text=f'Cost: {ad.REBIRTH_COST:,} coins').pack(pady=5)
    customtkinter.CTkLabel(rw, text=f'Your coins: {coins:,}').pack(pady=5)

    msg = customtkinter.CTkLabel(rw, text='')
    msg.pack(pady=10)

    def confirm():
        if ad.doRebirth(username):
            msg.configure(text=f'Rebirth complete! You are now Rebirth {count + 1}.', text_color='green')
            rw.after(1500, lambda: (rw.destroy(), menu(guestMode, username, settings)))
        else:
            msg.configure(text='Not enough coins or invalid.', text_color='red')

    customtkinter.CTkButton(rw, text='Rebirth' if can_do else 'Not enough coins', command=confirm, state='normal' if can_do else 'disabled').pack(pady=10)
    customtkinter.CTkButton(rw, text='Back', command=lambda: (rw.destroy(), menu(guestMode, username, settings))).pack(pady=10)

    rw.mainloop()
```

Use your actual constant name (e.g. `REBIRTH_COST` in `ad`) or pass the cost from the backend so the GUI stays in sync.

---

## 5. Optional: show rebirth in menu/stats

- In the menu header or coin line: `Rebirth 3 | Coins: 12,000`
- In stats screen: add a line `Rebirth count: 3` and `Current reward multiplier: 1.3x`

---

## 6. Balance suggestions

| Rebirth cost | Multiplier per rebirth | Feel |
|--------------|------------------------|------|
| 50,000       | 10%                    | Steady, many rebirths |
| 100,000      | 15%                    | Slower, stronger steps |
| 25,000       | 5%                     | Fast rebirths, smaller gains |

Start with one set (e.g. 50k + 10%), then tune. You can also cap the multiplier (e.g. max 2.0x) or add a small dice bonus per rebirth as above.

---

## 7. Checklist

- [ ] Add `rebirthCount` to new users in `addNewUser()`
- [ ] Add `getRebirthCount()`, `canRebirth()`, `doRebirth()`, `getRebirthRewardMultiplier()` in `amazingDice.py`
- [ ] Define `REBIRTH_COST` (and optionally `REBIRTH_START_COINS`)
- [ ] In `getWinReward()`, multiply final reward by `getRebirthRewardMultiplier(username)`
- [ ] Optionally add `getRebirthDiceBonus()` and use it in `getSize()`
- [ ] Add Rebirth button and `rebirthWindow()` in GUI; disable for guests
- [ ] Optionally show rebirth count and multiplier in menu and stats

If you want, the next step is to paste your current `getWinReward` and `addNewUser` and I can show the exact diffs for your project.
