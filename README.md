# Travel Agency Bot

A fully functional Telegram bot for a travel agency built with Python, aiogram 3, and SQLite.

## Features

### User Features
- **Language Selection**: RU/UZ support.
- **Tour Selection Wizard**: Step-by-step FSM to find the perfect trip (Destination, Dates, Budget, People, Preferences).
- **Tour Catalog**: Browse available tours with images and descriptions.
- **Requests Management**: View status of your applications, cancel them, or proceed to payment.
- **Fake Payment Gateway**: Simulation of payment flow for checking bookings.
- **Contacts & FAQ**: Information sections.

### Admin Features
- **Statistics**: View counts of users, tours, requests, and payments.
- **Broadcast**: Send messages to all users using `/broadcast`.

## Installation

1.  Clone the repository.
2.  Create virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure `.env`:
    ```ini
    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    ADMIN_IDS=12345678,87654321
    ```
5.  Run the bot:
    ```bash
    python -m bot.main
    ```

## Project Structure

- `bot/main.py`: Entry point.
- `bot/app.py`: Application assembler.
- `bot/db/`: Database connection and repositories.
- `bot/handlers/`:
    - `selection_fsm.py`: Logic for "Find a Tour" wizard.
    - `tours_catalog.py`: Displays tours with photos.
    - `admin.py`: Admin panel commands.
    - `payments.py`: Fake payment logic.
- `bot/keyboards/`: Reply and Inline keyboards.
- `bot/texts/`: Localization logic.

## Adding New Content

- **Tours**: Add them to the `tours` table in SQLite or update `seed_tours` in `init_db.py`.
- **Translations**: Update `MESSAGES` dict in `bot/texts/localization.py`.

## Requirements

- Python 3.9+
- aiogram 3.x
- aiosqlite
- python-dotenv
