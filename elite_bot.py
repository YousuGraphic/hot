import asyncio
import json
import logging
import os
import random
import re
import time
import httpx
from datetime import datetime
from typing import Dict, List, Optional, Union
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from playwright.async_api import async_playwright
# تأكد من تثبيت متصفح chromium
async def ensure_browser_installed():
    import os
    if not os.path.exists("/usr/bin/chromium"):
        os.system("playwright install chromium")
# 1. نظام التسجيل الاحترافي
class EliteLogger:
    def __init__(self):
        self.logger = logging.getLogger("TikTokEliteReporter")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(handler)
        self.logger.addHandler(logging.FileHandler("elite_bot.log"))
        
    def log(self, message: str, level: str = "info"):
        log_method = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical
        }.get(level, self.logger.info)
        
        enhanced_msg = f"🏆 [EliteSystem] {message}"
        log_method(enhanced_msg)

# 2. نظام إدارة الحسابات المتقدم
class AccountManager:
    def __init__(self):
        self.accounts: Dict[str, dict] = {}
        self.logger = EliteLogger()
        
    def add_account(self, cookies: dict, proxy: Optional[str] = None) -> str:
        """إضافة حساب جديد مع كوكيز"""
        session_id = f"SESS_{int(time.time())}_{random.randint(1000,9999)}"
        self.accounts[session_id] = {
            "cookies": cookies,
            "proxy": proxy,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "usage_count": 0
        }
        self.logger.log(f"تم إضافة حساب جديد (ID: {session_id})")
        return session_id
        
    def get_session_config(self, session_id: str) -> dict:
        """الحصول على إعدادات جلسة للحساب"""
        account = self.accounts.get(session_id)
        if not account:
            raise ValueError(f"الجلسة غير موجودة: {session_id}")
            
        # تحديث عدد الاستخدامات
        self.accounts[session_id]["usage_count"] += 1
        self.accounts[session_id]["last_used"] = datetime.utcnow().isoformat()
        
        return {
            "session_id": session_id,
            "cookies": account["cookies"],
            "proxy": account["proxy"],
            "status": account["status"]
        }
    
    def rotate_account(self) -> str:
        """تناوب الحسابات لتحقيق التوازن"""
        if not self.accounts:
            raise Exception("لا توجد حسابات نشطة")
        
        # ترتيب الحسابات حسب الأقل استخدامًا
        sorted_accounts = sorted(self.accounts.items(), key=lambda x: x[1]["usage_count"])
        return sorted_accounts[0][0]

# 3. نظام الإبلاغ المتكامل (وظائف حقيقية)
class TikTokReporter:
    # قائمة الانتهاكات كما في تيك توك تمامًا
    VIOLATION_TYPES = [
        "معلومات كاذبة",
        "محتوى غير لائق",
        "تحرش",
        "انتحال شخصية",
        "مشكلة في حقوق الملكية",
        "إيذاء الحيوانات",
        "إرهاب",
        "عنف",
        "كره",
        "انتحار وإيذاء النفس",
        "تمييز",
        "محتوى خطير",
        "محتوى غير مناسب للأطفال",
        "احتيال ونصب",
        "انتهاك خصوصيتي",
        "قاصر في خطر",
        "مضايقات",
        "إساءة استخدام مواد"
    ]
    
    def __init__(self):
        self.logger = EliteLogger()
        self.playwright = None
        self.browser = None
        self.session = httpx.AsyncClient()
        
    async def start_browser(self):
        """تشغيل متصفح للجلسة"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        
    async def close_browser(self):
        """إغلاق المتصفح"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        await self.session.aclose()
    
    async def report_video(self, session_config: dict, video_url: str, violation_type: str) -> dict:
        """تنفيذ الإبلاغ على فيديو معين"""
        if violation_type not in self.VIOLATION_TYPES:
            raise ValueError(f"نوع الانتهاك غير صحيح: {violation_type}")
            
        if not self.browser:
            await self.start_browser()
            
        context = await self.browser.new_context(
            storage_state={"cookies": [session_config["cookies"]]},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        page = await context.new_page()
        result = {"status": "error", "code": "UNKNOWN_ERROR"}
        
        try:
            # الانتقال إلى رابط الفيديو
            await page.goto(video_url, timeout=60000)
            await page.wait_for_selector('div[data-e2e="video-detail"]', timeout=30000)
            
            # فتح قائمة الإبلاغ
            await page.click('button[aria-label="More"]')
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await page.click('text=الإبلاغ')
            
            # انتظار ظهور قائمة الانتهاكات
            await page.wait_for_selector('div.reason-item', timeout=5000)
            
            # اختيار نوع الانتهاك
            violation_elements = await page.query_selector_all('div.reason-item')
            for element in violation_elements:
                text = await element.inner_text()
                if violation_type in text:
                    await element.click()
                    break
            
            # تقديم التقرير
            await asyncio.sleep(random.uniform(1.0, 1.5))
            submit_button = await page.query_selector('button:has-text("تقديم")')
            if submit_button:
                await submit_button.click()
                
                # انتظار تأكيد الإبلاغ
                await asyncio.sleep(random.uniform(1.5, 2.5))
                success_element = await page.query_selector('text=شكرًا على ملاحظاتك')
                
                if success_element:
                    self.logger.log(f"تم الإبلاغ بنجاح على: {video_url}")
                    result = {"status": "success", "code": "REPORT_ACCEPTED"}
                else:
                    self.logger.log(f"فشل الإبلاغ على: {video_url}", "error")
                    result = {"status": "error", "code": "REPORT_FAILED"}
            else:
                self.logger.log("لم يتم العثور على زر التقديم", "error")
                
        except Exception as e:
            self.logger.log(f"خطأ أثناء الإبلاغ: {str(e)}", "error")
            result = {"status": "error", "code": "RUNTIME_ERROR"}
            
        finally:
            await context.close()
            return result
    
    async def get_user_videos(self, username: str, max_videos: int = 50) -> List[str]:
        """الحصول على فيديوهات المستخدم الحقيقية"""
        try:
            response = await self.session.get(
                f"https://www.tiktok.com/@{username}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
            )
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
            
            if not script_tag:
                return []
            
            data = json.loads(script_tag.string)
            user_data = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {})
            video_list = user_data.get("itemList", [])
            
            return [f"https://www.tiktok.com/@{username}/video/{item['id']}" for item in video_list[:max_videos]]
        
        except Exception as e:
            self.logger.log(f"خطأ في جلب الفيديوهات: {str(e)}", "error")
            return []
                
    async def report_latest_20_videos(self, session_id: str, username: str, violation_type: str, account_manager: AccountManager) -> dict:
        """الإبلاغ عن آخر 20 فيديو حقيقي"""
        self.logger.log(f"بدء الإبلاغ عن آخر 20 فيديو لـ: @{username}")
        video_urls = await self.get_user_videos(username, 20)
        
        if not video_urls:
            return {"status": "error", "message": "لم يتم العثور على فيديوهات"}
        
        results = []
        for i, url in enumerate(video_urls):
            # تناوب الحسابات كل 5 تقارير
            if i % 5 == 0:
                session_id = account_manager.rotate_account()
            
            session_config = account_manager.get_session_config(session_id)
            result = await self.report_video(session_config, url, violation_type)
            results.append(result)
            
            # فاصل زمني عشوائي
            delay = random.uniform(10.0, 20.0) if i < 15 else random.uniform(20.0, 30.0)
            await asyncio.sleep(delay)
            
        success_count = sum(1 for r in results if r.get("status") == "success")
        return {
            "total_videos": len(video_urls),
            "success_count": success_count,
            "success_rate": (success_count / len(video_urls)) * 100,
            "details": results
        }
        
    async def scan_and_report_violations(self, session_id: str, username: str, account_manager: AccountManager) -> dict:
        """فحص الحساب والإبلاغ عن المنشورات المخالفة"""
        self.logger.log(f"بدء فحص الحساب: @{username}")
        video_urls = await self.get_user_videos(username, 50)
        
        if not video_urls:
            return {"status": "error", "message": "لم يتم العثور على فيديوهات"}
        
        # تحليل الفيديوهات لاكتشاف المخالفات
        violating_urls = []
        for url in video_urls:
            if await self.detect_violation(url):
                violating_urls.append(url)
        
        results = []
        for i, url in enumerate(violating_urls):
            # تناوب الحسابات كل 3 تقارير
            if i % 3 == 0:
                session_id = account_manager.rotate_account()
            
            session_config = account_manager.get_session_config(session_id)
            violation_type = await self.detect_violation_type(url)
            result = await self.report_video(session_config, url, violation_type)
            results.append(result)
            
            # فاصل زمني متزايد
            delay = 15.0 + (i * 2.0)
            await asyncio.sleep(delay)
            
        success_count = sum(1 for r in results if r.get("status") == "success")
        return {
            "total_videos": len(video_urls),
            "violating_videos": len(violating_urls),
            "reported_count": len(results),
            "success_count": success_count,
            "details": results
        }
        
    async def detect_violation(self, video_url: str) -> bool:
        """الكشف الحقيقي عن المخالفات"""
        try:
            response = await self.session.get(video_url)
            if response.status_code != 200:
                return False
                
            # تحليل المحتوى للكشف عن مخالفات
            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.find('meta', property='og:description')['content'] if soup.find('meta', property='og:description') else ""
            title = soup.find('title').text if soup.find('title') else ""
            
            # كلمات دالة للكشف عن مخالفات
            violation_keywords = [
                "نودز", "سكس", "إباحي", "عري", "محتوى خطير", "تحرش", 
                "كراهية", "تمييز", "انتحار", "عنف", "مخدرات", "احتيال"
            ]
            
            content = f"{title} {description}".lower()
            return any(keyword in content for keyword in violation_keywords)
            
        except Exception:
            return False
        
    async def detect_violation_type(self, video_url: str) -> str:
        """تحديد نوع المخالفة بناءً على المحتوى"""
        try:
            response = await self.session.get(video_url)
            if response.status_code != 200:
                return random.choice(self.VIOLATION_TYPES)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.find('meta', property='og:description')['content'] if soup.find('meta', property='og:description') else ""
            
            # تحديد نوع الانتهاك بناءً على المحتوى
            if any(kw in description.lower() for kw in ["نودز", "سكس", "إباحي", "عري"]):
                return "محتوى غير لائق"
            elif any(kw in description.lower() for kw in ["تحرش", "اغتصاب"]):
                return "تحرش"
            elif any(kw in description.lower() for kw in ["كراهية", "تمييز"]):
                return "كره"
            elif any(kw in description.lower() for kw in ["انتحار", "إيذاء النفس"]):
                return "انتحار وإيذاء النفس"
            elif any(kw in description.lower() for kw in ["عنف", "قتل", "ضرب"]):
                return "عنف"
            else:
                return "محتوى غير مناسب للأطفال"
                
        except Exception:
            return random.choice(self.VIOLATION_TYPES)

# 4. البوت الرئيسي للتليجرام (وظائف حقيقية)
class TelegramBot:
    def __init__(self, token: str, account_manager: AccountManager, reporter: TikTokReporter):
        self.token = token
        self.account_manager = account_manager
        self.reporter = reporter
        self.logger = EliteLogger()
        self.user_sessions: Dict[str, dict] = {}
        self.session = httpx.AsyncClient()
        
    async def send_message(self, chat_id: str, text: str, buttons: list = None):
        """إرسال رسالة حقيقية عبر بوت التليجرام"""
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        if buttons:
            payload["reply_markup"] = {
                "inline_keyboard": buttons
            }
        
        try:
            response = await self.session.post(url, json=payload)
            return response.json()
        except Exception as e:
            self.logger.log(f"خطأ في إرسال الرسالة: {str(e)}", "error")
            return None
    
    async def handle_update(self, update: dict):
        """معالجة تحديثات التليجرام الحقيقية"""
        try:
            message = update.get("message", {})
            chat_id = str(message["chat"]["id"])
            text = message.get("text", "").strip()
            
            if text.startswith("/"):
                command = text[1:].split(" ")[0].lower()
                data = text[len(command)+2:] if len(text) > len(command)+2 else ""
                
                if command == "start":
                    await self.handle_start(chat_id)
                elif command == "add_account":
                    await self.handle_add_account(chat_id, data)
                elif command == "report_video":
                    await self.handle_report_video(chat_id, data)
                elif command == "report_last20":
                    await self.handle_report_last20(chat_id, data)
                elif command == "scan_and_report":
                    await self.handle_scan_and_report(chat_id, data)
                else:
                    await self.send_message(chat_id, "❌ أمر غير معروف")
        except Exception as e:
            self.logger.log(f"خطأ في معالجة التحديث: {str(e)}", "error")
    
    async def handle_start(self, chat_id: str):
        """بدء التشغيل"""
        self.user_sessions[chat_id] = {"state": "main"}
        await self.send_message(
            chat_id,
            "🚀 *مرحبًا بك في بوت الإبلاغ الفائز!*\nأقوى نظام إبلاغ على تيك توك",
            buttons=self.main_menu_buttons()
        )
    
    async def handle_add_account(self, chat_id: str, data: str):
        """إضافة حساب جديد"""
        try:
            cookies = json.loads(data)
            session_id = self.account_manager.add_account(cookies)
            await self.send_message(
                chat_id,
                f"✅ تم إضافة الحساب بنجاح!\nID: `{session_id}`",
                buttons=self.main_menu_buttons()
            )
        except Exception as e:
            self.logger.log(f"فشل إضافة حساب: {str(e)}", "error")
            await self.send_message(
                chat_id,
                "❌ فشل إضافة الحساب. تأكد من صيغة ملف الكوكيز",
                buttons=self.main_menu_buttons()
            )
    
    async def handle_report_video(self, chat_id: str, data: str):
        """الإبلاغ عن فيديو"""
        if not data:
            await self.send_message(chat_id, "❌ يرجى إرسال رابط الفيديو")
            return
            
        video_url = data.strip()
        if not re.match(r'https?://(www\.)?tiktok\.com/.+', video_url):
            await self.send_message(chat_id, "❌ رابط غير صالح. يجب أن يكون رابط تيك توك")
            return
        
        try:
            session_id = self.account_manager.rotate_account()
            session_config = self.account_manager.get_session_config(session_id)
            result = await self.reporter.report_video(
                session_config, 
                video_url, 
                random.choice(self.reporter.VIOLATION_TYPES)
            
            if result["status"] == "success":
                await self.send_message(chat_id, "🎉 تم الإبلاغ بنجاح!", buttons=self.main_menu_buttons())
            else:
                await self.send_message(chat_id, "❌ فشل الإبلاغ. حاول لاحقًا", buttons=self.main_menu_buttons())
        except Exception as e:
            self.logger.log(f"خطأ في الإبلاغ: {str(e)}", "error")
            await self.send_message(chat_id, f"🔥 خطأ فني: {str(e)}", buttons=self.main_menu_buttons())
    
    async def handle_report_last20(self, chat_id: str, data: str):
        """الإبلاغ عن آخر 20 فيديو"""
        username = data.strip().replace("@", "")
        if not username:
            await self.send_message(chat_id, "❌ يرجى إرسال اسم المستخدم")
            return
        
        try:
            session_id = self.account_manager.rotate_account()
            result = await self.reporter.report_latest_20_videos(
                session_id,
                username,
                random.choice(self.reporter.VIOLATION_TYPES),
                self.account_manager
            )
            
            await self.send_message(
                chat_id,
                f"📊 نتائج الإبلاغ عن @{username}:\n"
                f"• عدد الفيديوهات: {result['total_videos']}\n"
                f"• نجاح الإبلاغ: {result['success_count']} ({result['success_rate']:.2f}%)",
                buttons=self.main_menu_buttons()
            )
        except Exception as e:
            self.logger.log(f"خطأ في الإبلاغ الشامل: {str(e)}", "error")
            await self.send_message(chat_id, f"🔥 خطأ فني: {str(e)}", buttons=self.main_menu_buttons())
    
    async def handle_scan_and_report(self, chat_id: str, data: str):
        """فحص وابلاغ"""
        username = data.strip().replace("@", "")
        if not username:
            await self.send_message(chat_id, "❌ يرجى إرسال اسم المستخدم")
            return
        
        try:
            session_id = self.account_manager.rotate_account()
            result = await self.reporter.scan_and_report_violations(
                session_id,
                username,
                self.account_manager
            )
            
            await self.send_message(
                chat_id,
                f"🔍 نتائج فحص @{username}:\n"
                f"• عدد الفيديوهات: {result['total_videos']}\n"
                f"• فيديوهات مخالفة: {result['violating_videos']}\n"
                f"• تم الإبلاغ عن: {result['reported_count']}\n"
                f"• نجاح الإبلاغ: {result['success_count']}",
                buttons=self.main_menu_buttons()
            )
        except Exception as e:
            self.logger.log(f"خطأ في الفحص والإبلاغ: {str(e)}", "error")
            await self.send_message(chat_id, f"🔥 خطأ فني: {str(e)}", buttons=self.main_menu_buttons())
    
    def main_menu_buttons(self) -> List[List[Dict]]:
        """إنشاء قائمة الأزرار الرئيسية"""
        return [
            [{"text": "➕ إضافة حساب", "callback_data": "add_account"}],
            [{"text": "🎬 إبلاغ فيديو", "callback_data": "report_video"}],
            [{"text": "📦 الإبلاغ عن 20 منشور", "callback_data": "report_last20"}],
            [{"text": "🔍 فحص وابلاغ", "callback_data": "scan_and_report"}]
        ]

# 5. الخادم الرئيسي (وظائف حقيقية)
class EliteServer:
    def __init__(self):
        self.logger = EliteLogger()
        self.account_manager = AccountManager()
        self.reporter = TikTokReporter()
        self.bot = TelegramBot(
            os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN"),
            self.account_manager,
            self.reporter
        )
        self.webhook_url = None
        
    async def startup(self):
        """تهيئة النظام"""
        self.logger.log("🚀 تهيئة النظام الفائز...")
        await self.reporter.start_browser()
        
        # إضافة حسابات افتراضية للاختبار
        if not self.account_manager.accounts:
            self.logger.log("🔧 إضافة حسابات افتراضية للاختبار...")
            self.account_manager.add_account(
                {"name": "sessionid", "value": "test_session_123", "domain": ".tiktok.com"},
                "http://proxy1.example.com:8080"
            )
            self.account_manager.add_account(
                {"name": "sessionid", "value": "test_session_456", "domain": ".tiktok.com"},
                "socks5://proxy2.example.com:1080"
            )
        
        self.logger.log("✅ تم تهيئة النظام بنجاح")
    
    async def shutdown(self):
        """إيقاف النظام"""
        self.logger.log("🛑 إيقاف النظام...")
        await self.reporter.close_browser()
        self.logger.log("✅ تم إيقاف النظام بنجاح")
    
    async def setup_webhook(self, url: str):
        """إعداد ويبهوك التليجرام"""
        self.webhook_url = url
        api_url = f"https://api.telegram.org/bot{self.bot.token}/setWebhook"
        payload = {"url": url}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload)
            result = response.json()
            
            if result.get("ok"):
                self.logger.log(f"✅ تم إعداد الويب هوك: {url}")
            else:
                self.logger.log(f"❌ فشل إعداد الويب هوك: {result.get('description')}", "error")
    
    async def handle_webhook(self, request: dict) -> dict:
        """معالجة طلبات الويب هوك"""
        await self.bot.handle_update(request)
        return {"status": "ok"}

# 6. التهيئة والتشغيل (وظائف حقيقية)
async def main():
    # تكوين السجلات
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # إنشاء الخادم
    server = EliteServer()
    await server.startup()
    
    # إعداد ويبهوك
    render_url = os.getenv("RENDER_EXTERNAL_URL", "https://your-service.onrender.com")
    await server.setup_webhook(f"{render_url}/webhook")
    
    # البقاء نشطًا
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف النظام بشكل آمن")
    except Exception as e:
        print(f"🔥 خطأ غير متوقع: {str(e)}")
