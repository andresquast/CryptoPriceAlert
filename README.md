# Crypto Price Monitor

A desktop application for real-time cryptocurrency price monitoring and alerts using CoinGecko API.

## Features

- Real-time price tracking
- Interactive price charts
- Configurable price alerts with desktop notifications
- Historical price data visualization

## Installation

```bash
# Clone repository
git clone [your-repo-url]
cd crypto_monitor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create `.env` file in root directory
2. Add your CoinGecko API key:

```
COINGECKO_API_KEY=your_api_key_here
```

## Usage

```bash
python3 -m app.main
```

## Project Structure

```
crypto_monitor/
├── app/
│   ├── api/           # API integration
│   ├── utils/         # Helper functions
│   └── main.py        # Desktop application
├── data/              # Price history storage
└── config.py          # Configuration settings
```

## Requirements

- Python 3.8+
- PyQt5
- Requests
- Matplotlib
