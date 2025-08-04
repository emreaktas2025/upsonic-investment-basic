# 🚀 Upsonic Investment Report Generator - Basic Version

A simple command-line tool that generates professional investment reports using AI analysis and real-time stock data.

## ✨ Features

- **Real-time stock prices** from Yahoo Finance
- **AI-powered analysis** using OpenAI GPT models
- **Investment recommendations** (BUY/HOLD/SELL)
- **Risk assessment** (LOW/MEDIUM/HIGH)
- **Key strengths and risks** identification
- **Professional report formatting**
- **Export to text files**

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install upsonic python-dotenv yfinance ddgs
```

### 2. Set Up API Key

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## 🚀 Usage

### Basic Usage

```bash
python main.py AAPL
```

### With Different AI Model

```bash
python main.py TSLA --model openai/gpt-4
```

### Save Report to File

```bash
python main.py MSFT --output my_report.txt
```

## 📊 Example Output

```🚀 Upsonic Investment Report Generator
🔍 Analyzing MSFT...
📊 Current price: $420.55

📈 ANALYSIS COMPLETE!
🏢 Microsoft Corporation (MSFT)
💰 Price: $420.55
🎯 Target: $441.58
📊 Recommendation: BUY
⚠️  Risk: MEDIUM
🏭 Market Cap: $3.12T
📊 P/E: 34.2
📈 Growth: 12.3%

✅ KEY STRENGTHS:
   • Strong cloud computing growth
   • Diversified revenue streams
   • Market leadership in enterprise software

⚠️  KEY RISKS:
   • Competitive pressure in cloud services
   • Economic slowdown impact
   • Regulatory scrutiny

📝 ANALYSIS:
Microsoft shows strong fundamentals with robust cloud growth...
```

## 📁 Project Structure

```upsonic-investment-basic/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── .env                 # API key (create this)
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## 🔧 How It Works

1. **Fetches real-time data** from Yahoo Finance (price, market cap, P/E ratio)
2. **Uses AI agent** to search web for recent news and analysis
3. **Combines data** to generate comprehensive investment report
4. **Provides recommendation** based on financial metrics and market trends

## 📋 Requirements

- Python 3.8+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Internet connection

## ⚙️ Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `ticker` | Stock symbol (required) | `AAPL`, `MSFT`, `GOOGL` |
| `--model` | AI model to use | `openai/gpt-4o`, `openai/gpt-4` |
| `--output` | Save to file | `--output report.txt` |

## 🔍 Supported AI Models

- `openai/gpt-4o` (default, recommended)
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`

## 🐛 Troubleshooting

### API Key Error

```❌ OpenAI API key not found

```**Solution:** Create `.env` file with your API key

### Invalid Ticker

```❌ Invalid ticker or data unavailable
```**Solution:** Use valid stock symbols (AAPL, MSFT, GOOGL, etc.)

### Import Error

```ModuleNotFoundError: No module named 'yfinance'
```**Solution:** Install dependencies: `pip install -r requirements.txt`

## 📝 Sample Report File

When using `--output`, generates a structured text report:

```INVESTMENT ANALYSIS REPORT
==================================================
Generated: 2025-08-04 12:30:45
Ticker: MSFT

Company Name: Microsoft Corporation
Current Price: 420.55
Target Price: 441.58
Recommendation: BUY
Risk Level: MEDIUM
Market Cap: $3.12T
Pe Ratio: 34.2
Revenue Growth: 12.3%

Key Strengths:
  • Strong cloud computing growth
  • Diversified revenue streams

Key Risks:
  • Competitive pressure
  • Economic uncertainty

Analysis Summary:
Microsoft demonstrates strong fundamentals...

--------------------------------------------------
Generated using Upsonic AI Framework
```

## 💡 Tips

- Use popular tickers like AAPL, MSFT, GOOGL for best results
- Try different AI models to compare analysis perspectives
- Save reports for future reference and comparison
- Check that your API key has sufficient credits
# upsonic-investment-basic
