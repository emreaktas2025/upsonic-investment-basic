#!/usr/bin/env python3
"""
Upsonic Investment Report Generator - Enhanced Basic Version

A command-line tool that generates investment reports using Upsonic AI
framework with real-time financial data from Yahoo Finance.

Installation:
    pip install upsonic python-dotenv yfinance ddgs

Usage:
    python main.py AAPL
    python main.py TSLA --model openai/gpt-4
    python main.py MSFT --output report.txt
"""

import os
import argparse
import sys
import json
from datetime import datetime
from upsonic import Task, Agent
from upsonic.tools import Search
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()


def get_stock_data(ticker):
    """Fetch real-time stock data using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        market_cap = info.get('marketCap', 0)
        pe_ratio = info.get('trailingPE') or info.get('forwardPE', 0)
        target_price = info.get('targetMeanPrice', current_price * 1.05)
        company_name = info.get('longName') or info.get('shortName', f"{ticker} Corporation")
        
        # Format market cap
        if market_cap >= 1e12:
            market_cap_str = f"${market_cap / 1e12:.2f}T"
        elif market_cap >= 1e9:
            market_cap_str = f"${market_cap / 1e9:.2f}B"
        else:
            market_cap_str = "N/A"
        
        # Format revenue growth
        revenue_growth = info.get('revenueGrowth')
        revenue_growth_str = f"{revenue_growth * 100:.1f}%" if revenue_growth else "N/A"
        
        return {
            "company_name": company_name,
            "current_price": round(current_price, 2) if current_price else 0,
            "target_price": round(target_price, 2) if target_price else 0,
            "market_cap": market_cap_str,
            "pe_ratio": round(pe_ratio, 1) if pe_ratio else 0,
            "revenue_growth": revenue_growth_str,
            "sector": info.get('sector', 'N/A')
        }
    except Exception as e:
        print(f"⚠️  Could not fetch financial data: {e}")
        return None


def main():
    print("🚀 Upsonic Investment Report Generator")
    print("=" * 50)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate investment reports with real-time data")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL, MSFT)")
    parser.add_argument("--model", default="openai/gpt-4o", help="AI model to use")
    parser.add_argument("--output", help="Save report to file")
    
    args = parser.parse_args()
    ticker = args.ticker.upper()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found")
        print("💡 Create .env file with: OPENAI_API_KEY=your-key-here")
        return 1
    
    print(f"🔍 Analyzing {ticker}...")
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    
    # Get real financial data
    stock_data = get_stock_data(ticker)
    if not stock_data:
        print("❌ Invalid ticker or data unavailable")
        return 1
    
    print(f"📊 Current price: ${stock_data['current_price']}")
    
    # Create AI analysis task
    task_description = f"""
    You are a professional investment analyst analyzing {ticker}.
    
    REAL FINANCIAL DATA (use these exact numbers):
    - Company: {stock_data['company_name']}
    - Current Price: ${stock_data['current_price']}
    - Target Price: ${stock_data['target_price']}
    - Market Cap: {stock_data['market_cap']}
    - P/E Ratio: {stock_data['pe_ratio']}
    - Revenue Growth: {stock_data['revenue_growth']}
    - Sector: {stock_data['sector']}
    
    Use Search to find recent news, analyst opinions, and market trends.
    
    Return ONLY this JSON format:
    {{
        "ticker": "{ticker}",
        "company_name": "{stock_data['company_name']}",
        "current_price": {stock_data['current_price']},
        "target_price": {stock_data['target_price']},
        "recommendation": "BUY/HOLD/SELL",
        "risk_level": "LOW/MEDIUM/HIGH",
        "market_cap": "{stock_data['market_cap']}",
        "pe_ratio": {stock_data['pe_ratio']},
        "revenue_growth": "{stock_data['revenue_growth']}",
        "key_strengths": ["strength1", "strength2"],
        "key_risks": ["risk1", "risk2"],
        "analysis_summary": "Your analysis here"
    }}
    """
    
    # Create task and agent
    task = Task(
        name="InvestmentReport",
        description=task_description,
        tools=[Search],
        output_schema={
            "ticker": str, "company_name": str, "current_price": float,
            "target_price": float, "recommendation": str, "risk_level": str,
            "market_cap": str, "pe_ratio": float, "revenue_growth": str,
            "key_strengths": list, "key_risks": list, "analysis_summary": str
        }
    )
    
    agent = Agent(name="InvestmentAnalyst", model=args.model)
    
    try:
        # Execute analysis
        result = agent.do(task)
        
        print("\n📈 ANALYSIS COMPLETE!")
        print("=" * 40)
        
        # Handle different result types
        if isinstance(result, dict):
            report = result
        else:
            # Try to parse JSON from text
            report = parse_json(str(result))
            if not report:
                print("📋 RAW ANALYSIS:")
                print(result)
                if args.output:
                    save_text(result, args.output, ticker)
                return 0
        
        # Display report
        display_report(report)
        
        # Save if requested
        if args.output:
            save_report(report, args.output, ticker)
        
        print(f"\n⏰ Completed: {datetime.now().strftime('%H:%M:%S')}")
        return 0
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return 1


def parse_json(text):
    """Extract JSON from text response."""
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None


def display_report(data):
    """Display formatted investment report."""
    print(f"🏢 {data.get('company_name', 'N/A')} ({data.get('ticker', 'N/A')})")
    print(f"💰 Price: ${data.get('current_price', 0):.2f}")
    print(f"🎯 Target: ${data.get('target_price', 0):.2f}")
    print(f"📊 Recommendation: {data.get('recommendation', 'N/A')}")
    print(f"❌   Risk: {data.get('risk_level', 'N/A')}")
    print(f"🏭 Market Cap: {data.get('market_cap', 'N/A')}")
    print(f"📊 P/E: {data.get('pe_ratio', 0)}")
    print(f"📈 Growth: {data.get('revenue_growth', 'N/A')}")
    
    # Strengths
    strengths = data.get('key_strengths', [])
    if strengths:
        print("\n✅ KEY STRENGTHS:")
        for strength in strengths:
            print(f"   • {strength}")
    
    # Risks
    risks = data.get('key_risks', [])
    if risks:
        print("\n❌ KEY RISKS:")
        for risk in risks:
            print(f"   • {risk}")
    
    # Summary
    print(f"\n📝 ANALYSIS:")
    print("-" * 30)
    print(data.get('analysis_summary', 'No analysis available'))


def save_report(data, path, ticker):
    """Save structured report to file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("INVESTMENT ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Ticker: {ticker}\n\n")
            
            for key, value in data.items():
                formatted_key = key.replace('_', ' ').title()
                if isinstance(value, list):
                    f.write(f"{formatted_key}:\n")
                    for item in value:
                        f.write(f"  • {item}\n")
                    f.write("\n")
                else:
                    f.write(f"{formatted_key}: {value}\n")
            
            f.write("\n" + "-" * 50 + "\n")
            f.write("Generated using Upsonic AI Framework\n")
        
        print(f"💾 Saved to: {path}")
    except Exception as e:
        print(f"⚠️  Save failed: {e}")


def save_text(text, path, ticker):
    """Save text report to file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"INVESTMENT ANALYSIS - {ticker}\n")
            f.write("=" * 40 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(str(text))
        print(f"💾 Text saved to: {path}")
    except Exception as e:
        print(f"⚠️  Save failed: {e}")


if __name__ == "__main__":
    sys.exit(main())