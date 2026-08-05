#!/usr/bin/env python3
"""
Browser Testing Setup Script
Installs Chrome browser and chromedriver for Dash testing
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_chrome_installed():
    """Check if Chrome is already installed"""
    chrome_commands = [
        "google-chrome --version",
        "chromium --version", 
        "chromium-browser --version"
    ]
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✓ Chrome found: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError:
            continue
    
    return False

def install_chrome_ubuntu():
    """Install Chrome on Ubuntu/Debian systems"""
    commands = [
        "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
        "sudo sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google-chrome.list'",
        "sudo apt-get update",
        "sudo apt-get install -y google-chrome-stable"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Installing Chrome: {cmd.split()[0]}"):
            return False
    
    return True

def install_chrome_alternatives():
    """Install Chromium as alternative"""
    alternatives = [
        "sudo apt-get install -y chromium-browser",
        "sudo apt-get install -y chromium"
    ]
    
    for cmd in alternatives:
        if run_command(cmd, f"Installing Chromium: {cmd.split()[-1]}"):
            return True
    
    return False

def setup_webdriver():
    """Setup webdriver using webdriver-manager"""
    print("⏳ Setting up webdriver...")
    
    # Create a test script to download chromedriver
    test_script = '''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    # Setup Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Install and setup chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Test basic functionality
    driver.get("data:text/html,<h1>Test</h1>")
    title = driver.title
    driver.quit()
    
    print("✓ WebDriver setup successful")
    
except Exception as e:
    print(f"❌ WebDriver setup failed: {e}")
    exit(1)
'''
    
    # Write and execute test script
    with open("/tmp/test_webdriver.py", "w") as f:
        f.write(test_script)
    
    try:
        subprocess.run([sys.executable, "/tmp/test_webdriver.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    finally:
        # Clean up
        if os.path.exists("/tmp/test_webdriver.py"):
            os.remove("/tmp/test_webdriver.py")

def main():
    """Main setup function"""
    print("🚀 Soul Foods Dashboard - Browser Testing Setup")
    print("=" * 60)
    
    # Check if Chrome is already installed
    if check_chrome_installed():
        print("✓ Chrome browser is already available")
    else:
        print("⚠️  Chrome browser not found. Installing...")
        
        # Try to install Chrome
        if not install_chrome_ubuntu():
            print("⚠️  Chrome installation failed, trying Chromium...")
            if not install_chrome_alternatives():
                print("❌ Failed to install any Chrome browser")
                print("Please install Chrome manually:")
                print("  - Download from https://www.google.com/chrome/")
                print("  - Or install chromium: sudo apt-get install chromium-browser")
                return False
    
    # Setup webdriver
    if not setup_webdriver():
        print("❌ WebDriver setup failed")
        return False
    
    print("\n🎉 Browser testing setup complete!")
    print("You can now run browser tests with:")
    print("  pytest test_app.py -v")
    print("  or")
    print("  pytest test_app.py -v --headless")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)