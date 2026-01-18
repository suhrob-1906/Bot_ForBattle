# Travel Agency Bot

A fully functional Telegram bot for a travel agency built with Python, aiogram 3, and SQLite.

## Features

### User Features
- **Language Selection**: RU/UZ support.
- **Tour Selection Wizard**: Step-by-step FSM to find the perfect trip.
- **Flight Tickets**: Search and book flight tickets (Origin -> Destination -> Dates).
- **Tour Catalog**: Browse available tours with images and sharing.
- **Requests Management**: View status of your applications and flight history.
- **Fake Payment Gateway**: Simulation of payment flow.

### Admin Features
- **Statistics**: View counts of users, tours, requests, and payments via `/admin`.
- **Broadcast**: Send messages to all users using `/broadcast`.

## Local Installation

1.  Clone the repository.
2.  Create virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Linux/Mac
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure `.env`:
    Create a file named `.env` and add:
    ```ini
    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    ADMIN_IDS=12345678,87654321
    ```
5.  Run the bot:
    ```bash
    python -m bot.main
    ```

## Deployment Guide

### Option 1: VPS (Ubuntu/Debian)

1.  **Prepare Server**:
    ```bash
    sudo apt update && sudo apt install python3-pip python3-venv git
    ```
2.  **Clone & Setup**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
    cd YOUR_REPO
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Environment**:
    Create `.env` file with `nano .env` and paste your tokens.
4.  **Run with Systemd (Keep alive)**:
    Create file `/etc/systemd/system/bot.service`:
    ```ini
    [Unit]
    Description=Telegram Bot
    After=network.target

    [Service]
    User=root
    WorkingDirectory=/root/YOUR_REPO
    ExecStart=/root/YOUR_REPO/venv/bin/python -m bot.main
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    Start: `sudo systemctl enable --now bot`

### Option 2: Render / Railway / Heroku

1.  **Build Command**: `pip install -r requirements.txt`
2.  **Start Command**: `python -m bot.main`
3.  **Environment Variables**:
    Go to "Settings" -> "Environment Variables" and add:
    *   Key: `BOT_TOKEN`, Value: `your_token_from_botfather`
    *   Key: `ADMIN_IDS`, Value: `12345,67890`

## Troubleshooting "Invalid Token"

If you see `Token validation failed` or `Unauthorized`:
1.  **Check .env**: Ensure there are no spaces around the `=` sign (e.g. `BOT_TOKEN = 123` is WRONG).
2.  **Correct Token**: Copy the token again from **@BotFather**.
3.  **Environment**: If deploying to cloud, make sure you pasted the token into the "Environment Variables" section of the dashboard, not in a file (unless you uploaded .env).
4.  **Old Process**: If you reset the token, restart the bot completely.

## Project Structure

- `bot/main.py`: Entry point.
- `bot/handlers/`:
    - `selection_fsm.py`: Logic for "Find a Tour".
    - `tickets.py`: Flight booking logic.
    - `tours_catalog.py`: Catalog & Inline mode.
- `bot/texts/localization.py`: Multi-language support (RU/UZ).
