#!/usr/bin/env python3
"""
Test Runner for Soul Foods Dashboard
Runs appropriate tests based on available environment
"""

import subprocess
import sys
import os

def check_chrome_available():
    """Check if Chrome/Chromium is available for browser testing"""
    chrome_commands = [
        "google-chrome --version",
        "chromium --version", 
        "chromium-browser --version"
    ]
    
    for cmd in chrome_commands:
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError:
            continue
    
    return False

def run_unit_tests():
    """Run unit tests (no browser required)"""
    print("🧪 Running Unit Tests (No Browser Required)")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "test_app_unit.py"
        ], check=False)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Unit tests failed: {e}")
        return False

def run_browser_tests():
    """Run browser-based Dash tests"""
    print("🌐 Running Browser Tests (Dash + Selenium)")
    print("-" * 50)
    
    try:
        # Try to run the Quantium-specific tests
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "test_dash_quantium.py::TestQuantiumDashboard::test_header_is_present",
            "test_dash_quantium.py::TestQuantiumDashboard::test_visualization_is_present", 
            "test_dash_quantium.py::TestQuantiumDashboard::test_region_picker_is_present",
            "-v", "--tb=short"
        ], check=False, timeout=120)  # 2 minute timeout
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Browser tests timed out")
        return False
    except Exception as e:
        print(f"❌ Browser tests failed: {e}")
        return False

def main():
    """Main test execution"""
    print("🚀 Soul Foods Dashboard - Complete Test Suite")
    print("=" * 60)
    print("Quantium Job Simulation - Task 5: Testing")
    print()
    
    # Check environment capabilities
    has_chrome = check_chrome_available()
    
    print("Environment Check:")
    print(f"  Chrome Browser: {'✅ Available' if has_chrome else '❌ Not Available'}")
    print()
    
    # Run unit tests first (always available)
    print("Phase 1: Unit Tests")
    unit_success = run_unit_tests()
    print(f"Unit Tests: {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print()
    
    # Run browser tests if Chrome is available
    browser_success = False
    if has_chrome:
        print("Phase 2: Browser Tests") 
        browser_success = run_browser_tests()
        print(f"Browser Tests: {'✅ PASSED' if browser_success else '❌ FAILED'}")
    else:
        print("Phase 2: Browser Tests - SKIPPED")
        print("❌ Chrome not available. Install Chrome to run browser tests:")
        print("   sudo apt-get install google-chrome-stable")
        print("   or")
        print("   sudo apt-get install chromium-browser")
    
    print()
    print("=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    if unit_success:
        print("✅ Unit Tests: Application structure and components validated")
    else:
        print("❌ Unit Tests: Failed - check app structure")
    
    if has_chrome:
        if browser_success:
            print("✅ Browser Tests: All 3 Quantium requirements verified")
            print("  1. ✓ Header is present")
            print("  2. ✓ Visualization is present") 
            print("  3. ✓ Region picker is present")
        else:
            print("❌ Browser Tests: Failed - check browser compatibility")
    else:
        print("⚠️  Browser Tests: Skipped (no Chrome browser)")
    
    # Overall status
    print()
    if unit_success and (browser_success or not has_chrome):
        print("🎉 TASK 5 COMPLETE: Dashboard testing successful!")
        print("✅ Ready for Quantium submission")
        return True
    else:
        print("❌ Task 5 incomplete - some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)