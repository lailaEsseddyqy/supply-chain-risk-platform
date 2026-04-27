# Supply Chain Risk Intelligence Platform

An end-to-end data engineering and machine learning architecture designed to predict and mitigate supplier disruptions in real-time.

## The Business Problem

In global manufacturing, a single delayed component can halt an entire assembly line, costing millions. Traditionally, supply chain analysts manage this risk manually using static spreadsheets and reactive phone calls. 

This project aims to modernize that approach. I built an automated pipeline that ingests real-time signals, evaluates supplier health, and not only predicts the likelihood of a disruption but explains *why* it might happen.

## How It Works

The platform is built around a modern Data Lakehouse architecture (Medallion pattern) and integrates both predictive ML and generative AI:

1. **Streaming & Ingestion:** Instead of relying on static CSVs, the system simulates real-time ERP data and news alerts using Apache Kafka. 
2. **Distributed Processing:** PySpark cleans and transforms the incoming streams, moving data from Bronze (raw) to Silver (cleaned) and Gold (aggregated KPIs) layers.
3. **Predictive Scoring & Explainability:** A Random Forest model calculates a risk score for each supplier. Because "black box" models are rarely trusted in enterprise settings, I implemented SHAP to provide a mathematical explanation for every high-risk alert.
4. **Local GenAI (RAG):** Supply chain managers can ask questions in natural language (e.g., "What are the current risks in Turkey?"). The system uses LangChain, FAISS, and a local Mistral 7B model (via Ollama) to answer based strictly on the ingested data, ensuring zero data leakage to public APIs.
5. **Analytics:** DuckDB serves as a highly efficient, in-process analytical engine to power the final Power BI dashboard.

## System Architecture

```text
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Data Sources   │ ───► │  Data Pipeline  │ ───► │  Intelligence   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
  - ERP Simulator          - Apache Kafka           - Random Forest
  - News/Weather APIs      - PySpark                - SHAP Explainer
                           - Medallion Arch.        - LangChain & FAISS
                           (Bronze/Silver/Gold)     - Local Mistral 7B
                           