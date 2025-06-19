#!/bin/bash

# تحديث النظام الأساسي
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-dev python3.10-venv g++

# إنشاء بيئة افتراضية جديدة
python3.10 -m venv venv
source venv/bin/activate

# تثبيت الأدوات الأساسية
pip install --upgrade pip setuptools wheel

# تثبيت greenlet بشكل منفصل أولاً
pip install --force-reinstall --no-cache-dir greenlet==3.0.3

# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت playwright والمتصفح
python -m pip install playwright==1.42.0
python -m playwright install chromium
python -m playwright install-deps
