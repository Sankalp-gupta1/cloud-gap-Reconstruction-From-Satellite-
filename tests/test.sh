#!/bin/bash
set -e

pytest /app/tests/test_outputs.py

mkdir -p /logs/verifier
echo "1.0" > /logs/verifier/reward.txt