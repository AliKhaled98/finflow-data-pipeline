# 💹 FinFlow: Automated USD/EGP Market Monitor

**An End-to-End Medallion Data Pipeline for Currency Volatility Analysis.**

## 📌 Project Overview
In volatile economic environments, the gap between official bank rates and parallel market rates is a critical indicator of economic stability. This project automates the collection, transformation, and analysis of **USD/EGP** exchange rates using a structured **Medallion Architecture**.

The pipeline is designed to detect "High Volatility" events—situations where the market spread exceeds a **0.1% threshold**—and generates actionable alerts for financial risk management.



## 🏗️ Technical Architecture (Medallion Pattern)
The system is built using **Python** and **Pandas**, utilizing **Parquet** for schema-enforced, efficient data storage.

* **Bronze Layer (Ingestion):**
    * `ingest_api.py`: Fetches official rates from the AlphaVantage API.
    * `scrape_market.py`: Scrapes real-time market rates using `yfinance` to simulate parallel market activity.
* **Silver Layer (Transformation):**
    * `refine_silver.py`: Standardizes schemas, handles floating-point precision errors, and merges datasets to calculate raw variance.
* **Gold Layer (Analytics):**
    * `gold_volatility_alert.py`: Calculates **Spread % KPI** and flags volatility based on business risk thresholds.

## 🚀 Orchestration & Automation
I implemented a custom **Pipeline Orchestrator** (`run_pipeline.py`) using the Python `subprocess` module to manage the end-to-end workflow.

**Key Orchestration Features:**
* **Dependency Management**: Ensures steps execute in the strict logical order (Bronze → Silver → Gold).
* **Fail-Fast Logic**: The pipeline utilizes `check=True` to halt execution immediately if any stage returns an error, preventing downstream data corruption.
* **Performance Tracking**: Logs execution time for each stage to monitor pipeline efficiency.

## 📊 How to Run
```bash
# Clone the repository
git clone [https://github.com/AliKhaled98/finflow-data-pipeline.git](https://github.com/AliKhaled98/finflow-data-pipeline.git)

# Install dependencies (pandas, pyarrow, yfinance)
pip install pandas pyarrow yfinance

# Execute the full pipeline with one command
python run_pipeline.py