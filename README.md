# Travel Bot

A strictly structured Telegram bot for travel bookings.

## Setup

1.  **Clone & Install**:
    ```bash
    git clone ...
    cd tg_botForBattle
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Environment**:
    Create `.env`:
    ```ini
    BOT_TOKEN=123...
    ```

3.  **Run**:
    ```bash
    python -m bot.main
    ```

## Architecture

*   `bot/main.py`: Entry point.
*   `bot/app.py`: Dispatcher and Router setup.
*   `bot/db/`: 
    *   `init_db.py`: Schema creation (users, bookings).
    *   `repositories/`: Data access layers.
*   `bot/handlers/`:
    *   `start.py`: Registration and Language.
    *   `booking.py`: Booking FSM and History.
*   `bot/texts/localization.py`: All texts (RU/UZ). NO emojis.

## Deployment

Deploy on any VPS using Systemd or Docker. Ensure the `bot.service` runs `python -m bot.main` in the virtual environment.
