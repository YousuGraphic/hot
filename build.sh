#!/bin/bash

# تثبيت المتطلبات النظامية
sudo apt-get update
sudo apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3.9-venv \
    g++ \
    libnss3 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgbm1

# إنشاء بيئة افتراضية جديدة
python3.9 -m venv venv
source venv/bin/activate

# تثبيت الأدوات الأساسية
pip install --upgrade pip setuptools wheel

# تثبيت greenlet بإصدار متوافق أولاً
pip install greenlet==2.0.2 --no-cache-dir --force-reinstall

# تثبيت المتطلبات الأخرى
pip install -r requirements.txt

# تثبيت playwright
python -m pip install playwright==1.32.1
python -m playwright install chromium
python -m playwright install-deps
