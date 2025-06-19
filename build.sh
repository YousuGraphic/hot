#!/bin/bash

# تثبيت المتطلبات الأساسية للنظام
sudo apt-get update
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libxshmfence1

# تثبيت متطلبات بايثون
pip install --upgrade pip
pip install -r requirements.txt

# تثبيت متصفح Chromium
python -m playwright install chromium
python -m playwright install-deps
