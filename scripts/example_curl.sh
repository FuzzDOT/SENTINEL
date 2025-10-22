#!/usr/bin/env bash
set -e
# List assets
curl -s localhost:8000/assets | jq .
# Train a model (example: SPY ETF)
curl -s -X POST localhost:8000/train -H "Content-Type: application/json" -d '{"category":"etfs","symbol":"SPY"}' | jq .
# Predict next 5 days
curl -s -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"category":"etfs","symbol":"SPY","days_ahead":5}' | jq .
# Backtest (proxy baseline)
curl -s -X POST localhost:8000/backtest -H "Content-Type: application/json" -d '{"category":"etfs","symbol":"SPY"}' | jq .
