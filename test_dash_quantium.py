#!/usr/bin/env python3
"""
Quantium Soul Foods Dashboard Test Suite
Task 5: Test Your Dash Application

This test suite validates the three required components:
1. Header is present
2. Visualization is present  
3. Region picker is present

Using pytest and dash.testing framework with Selenium WebDriver
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import the Dash app
from app import app


class TestQuantiumDashboard:
    """
    Test suite for Quantium requirements
    Tests the three mandatory components of the Soul Foods dashboard
    """
    
    def test_header_is_present(self, dash_duo):
        """
        TEST 1: Verify that the header is present on the page
        
        Quantium Requirements:
        - Header element must be visible
        - Should contain application title
        """
        # Start the Dash server
        dash_duo.start_server(app)
        
        # Wait for the header element to load
        try:
            dash_duo.wait_for_element("#header", timeout=10)
            header = dash_duo.find_element("#header")
            
            # Verify header is present and visible
            assert header is not None, "Header element with id='header' not found"
            assert header.is_displayed(), "Header element is not visible"
            
            # Verify header contains expected text
            header_text = header.text
            assert "Soul Foods" in header_text, f"Header should contain 'Soul Foods', got: {header_text}"
            
            print("✅ TEST 1 PASSED: Header is present and contains correct text")
            
        except TimeoutException:
            pytest.fail("Header element not found within timeout period")
        except Exception as e:
            pytest.fail(f"Header test failed: {str(e)}")
    
    def test_visualization_is_present(self, dash_duo):
        """
        TEST 2: Verify that the visualization (line chart) is present on the page
        
        Quantium Requirements:
        - Graph component must be present
        - Should be a Plotly chart that renders correctly
        """
        # Start the Dash server
        dash_duo.start_server(app)
        
        # Wait for the chart to load
        try:
            dash_duo.wait_for_element("#sales-line-chart", timeout=15)
            chart = dash_duo.find_element("#sales-line-chart")
            
            # Verify chart is present and visible
            assert chart is not None, "Chart element with id='sales-line-chart' not found"
            assert chart.is_displayed(), "Chart element is not visible"
            
            # Wait for Plotly to render the chart
            time.sleep(2)
            
            # Check for Plotly-specific elements that indicate proper rendering
            try:
                plotly_plot = dash_duo.find_element("#sales-line-chart .plotly")
                assert plotly_plot is not None, "Plotly chart not properly rendered"
            except NoSuchElementException:
                # Alternative check - look for SVG which Plotly creates
                svg_element = dash_duo.find_element("#sales-line-chart svg")
                assert svg_element is not None, "Chart SVG not found - chart may not be rendering"
            
            print("✅ TEST 2 PASSED: Visualization is present and rendering correctly")
            
        except TimeoutException:
            pytest.fail("Chart element not found within timeout period")
        except Exception as e:
            pytest.fail(f"Visualization test failed: {str(e)}")
    
    def test_region_picker_is_present(self, dash_duo):
        """
        TEST 3: Verify that the region picker (radio buttons) is present on the page
        
        Quantium Requirements:
        - RadioItems component must be present
        - Should have all required region options
        - Should have proper default selection
        """
        # Start the Dash server
        dash_duo.start_server(app)
        
        # Wait for the region selector to load
        try:
            dash_duo.wait_for_element("#region-selector", timeout=10)
            region_selector = dash_duo.find_element("#region-selector")
            
            # Verify region selector is present and visible
            assert region_selector is not None, "Region selector with id='region-selector' not found"
            assert region_selector.is_displayed(), "Region selector is not visible"
            
            # Find all radio buttons within the selector
            radio_buttons = dash_duo.find_elements("#region-selector input[type='radio']")
            assert len(radio_buttons) >= 5, f"Expected at least 5 radio buttons, found {len(radio_buttons)}"
            
            # Verify required region options exist
            expected_values = ['All', 'north', 'east', 'south', 'west']
            found_values = []
            
            for radio in radio_buttons:
                value = radio.get_attribute('value')
                if value:
                    found_values.append(value)
            
            for expected_value in expected_values:
                assert expected_value in found_values, f"Region option '{expected_value}' not found. Available: {found_values}"
            
            # Check that one radio button is selected by default (should be 'All')
            selected_radios = [r for r in radio_buttons if r.is_selected()]
            assert len(selected_radios) == 1, f"Expected exactly 1 selected radio button, found {len(selected_radios)}"
            
            default_selection = selected_radios[0].get_attribute('value')
            assert default_selection == 'All', f"Default selection should be 'All', but is '{default_selection}'"
            
            print("✅ TEST 3 PASSED: Region picker is present with all options and correct default")
            
        except TimeoutException:
            pytest.fail("Region selector element not found within timeout period")
        except Exception as e:
            pytest.fail(f"Region picker test failed: {str(e)}")


# Configuration and helper functions
@pytest.fixture(scope="session")
def chrome_options():
    """Configure Chrome options for testing"""
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    return options

@pytest.fixture(scope="session")
def webdriver_manager():
    """Setup webdriver using webdriver-manager"""
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    
    # Automatically download and setup chromedriver
    service = Service(ChromeDriverManager().install())
    return service


def test_app_loads_successfully(dash_duo):
    """
    BONUS TEST: Verify the app loads without errors
    
    This ensures the basic functionality works before running specific tests
    """
    try:
        dash_duo.start_server(app)
        
        # Wait for any element to load (page should be responsive)
        dash_duo.wait_for_element("body", timeout=10)
        
        # Check page title
        title = dash_duo.driver.title
        assert "Soul Foods" in title or "Quantium" in title, f"Page title should contain app name, got: {title}"
        
        print("✅ BONUS TEST PASSED: App loads successfully without errors")
        
    except Exception as e:
        pytest.fail(f"App loading test failed: {str(e)}")


# Test runner for direct execution
if __name__ == "__main__":
    """
    Direct test execution
    Usage: python test_dash_quantium.py
    """
    print("🧪 Quantium Soul Foods Dashboard - Test Suite")
    print("=" * 60)
    print("Running required tests for Task 5...")
    print()
    print("Tests to run:")
    print("1. ✓ Header is present") 
    print("2. ✓ Visualization is present")
    print("3. ✓ Region picker is present")
    print()
    print("Starting pytest execution...")
    print("=" * 60)
    
    # Run pytest on this file
    import subprocess
    import sys
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__, 
        "-v", 
        "--tb=short",
        "-x"  # Stop on first failure
    ])
    
    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("🎉 ALL QUANTIUM TESTS PASSED!")
        print("✅ Dashboard meets all requirements for Task 5")
    else:
        print("❌ Some tests failed - check output above")
    
    sys.exit(result.returncode)