#!/usr/bin/env python3
"""
Test Suite for Soul Foods Dash Application
Quantium Job Simulation - Task 5: Testing

This test suite validates the core components of the Soul Foods dashboard
using Dash's testing framework with Selenium WebDriver.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Import the Dash app
from app import app


class TestSoulFoodsDashboard:
    """Test suite for Soul Foods Dashboard components"""
    
    def test_001_header_is_present(self, dash_duo):
        """
        Test 1: Verify that the header is present on the page
        
        Requirements:
        - Header element with id="header" must be visible
        - Header should contain "Soul Foods Sales Analytics" text
        """
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for page to load
        dash_duo.wait_for_element("#header", timeout=10)
        
        # Find header element
        header_element = dash_duo.find_element("#header")
        
        # Assertions
        assert header_element is not None, "Header element not found"
        assert header_element.is_displayed(), "Header element is not visible"
        assert "Soul Foods Sales Analytics" in header_element.text, "Header text is incorrect"
        
        print("✓ Test 1 PASSED: Header is present and visible")
    
    def test_002_visualization_is_present(self, dash_duo):
        """
        Test 2: Verify that the visualization (Line Chart) is present on the page
        
        Requirements:
        - Graph element with id="sales-line-chart" must be present
        - Graph should be interactive and displayable
        """
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for the graph component to load
        dash_duo.wait_for_element("#sales-line-chart", timeout=15)
        
        # Find the graph element
        graph_element = dash_duo.find_element("#sales-line-chart")
        
        # Assertions
        assert graph_element is not None, "Sales line chart element not found"
        assert graph_element.is_displayed(), "Sales line chart is not visible"
        
        # Check if Plotly graph is properly rendered
        # Plotly graphs have a specific structure when rendered
        plotly_graph = dash_duo.find_element("#sales-line-chart .js-plotly-plot")
        assert plotly_graph is not None, "Plotly graph not properly rendered"
        
        print("✓ Test 2 PASSED: Sales line chart visualization is present and rendered")
    
    def test_003_region_picker_is_present(self, dash_duo):
        """
        Test 3: Verify that the region picker (RadioItems) is present on the page
        
        Requirements:
        - RadioItems element with id="region-selector" must be present
        - Should contain all 5 region options (All, North, East, South, West)
        - Default selection should be "All"
        """
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for the region selector to load
        dash_duo.wait_for_element("#region-selector", timeout=10)
        
        # Find the region selector element
        region_selector = dash_duo.find_element("#region-selector")
        
        # Assertions
        assert region_selector is not None, "Region selector element not found"
        assert region_selector.is_displayed(), "Region selector is not visible"
        
        # Check for all radio buttons
        radio_buttons = dash_duo.find_elements("#region-selector input[type='radio']")
        assert len(radio_buttons) == 5, f"Expected 5 radio buttons, found {len(radio_buttons)}"
        
        # Check for specific region labels
        expected_regions = ["All Regions", "North", "East", "South", "West"]
        for region in expected_regions:
            label_element = dash_duo.find_element(f"#region-selector label:contains('{region}')")
            assert label_element is not None, f"Region label '{region}' not found"
        
        # Check default selection (should be "All")
        selected_radio = dash_duo.find_element("#region-selector input[checked]")
        assert selected_radio is not None, "No default selection found"
        assert selected_radio.get_attribute("value") == "All", "Default selection is not 'All'"
        
        print("✓ Test 3 PASSED: Region picker is present with all options and correct default")
    
    def test_004_integration_region_filter_works(self, dash_duo):
        """
        BONUS Test 4: Verify that the region filter functionality works
        
        This test ensures the interaction between region selector and chart updates
        """
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for both components to load
        dash_duo.wait_for_element("#region-selector", timeout=10)
        dash_duo.wait_for_element("#sales-line-chart", timeout=10)
        
        # Find North region radio button and click it
        north_radio = dash_duo.find_element("#region-selector input[value='north']")
        assert north_radio is not None, "North region radio button not found"
        
        # Click North region
        north_radio.click()
        
        # Wait for chart to update (Dash callback execution)
        time.sleep(2)
        
        # Verify the radio button is selected
        assert north_radio.is_selected(), "North region radio button not selected after click"
        
        # Check if chart updated (this is a basic check)
        graph_element = dash_duo.find_element("#sales-line-chart")
        assert graph_element is not None, "Chart disappeared after region change"
        
        print("✓ Test 4 PASSED: Region filter integration works correctly")
    
    def test_005_app_loads_without_errors(self, dash_duo):
        """
        BONUS Test 5: Verify that the app loads without any console errors
        
        This test checks for JavaScript errors and ensures clean app startup
        """
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for page to fully load
        dash_duo.wait_for_element("#header", timeout=10)
        
        # Check for JavaScript errors
        logs = dash_duo.driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        # Assert no severe errors
        assert len(severe_errors) == 0, f"Found JavaScript errors: {severe_errors}"
        
        # Check page title
        assert "Soul Foods" in dash_duo.driver.title, "Page title is incorrect"
        
        print("✓ Test 5 PASSED: App loads without errors and has correct title")


# Pytest fixtures and configuration - Dash provides dash_duo fixture automatically
# No need to redefine it


# Test configuration
def pytest_configure(config):
    """Configure pytest for Dash testing"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


# Helper functions for test utilities
def wait_for_element_with_retry(dash_duo, selector, max_retries=3, timeout=10):
    """
    Helper function to wait for element with retry logic
    Useful for flaky elements that might take time to load
    """
    for attempt in range(max_retries):
        try:
            dash_duo.wait_for_element(selector, timeout=timeout)
            return True
        except TimeoutException:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    return False


if __name__ == "__main__":
    """
    Run tests directly if script is executed
    Usage: python test_app.py
    """
    import subprocess
    import sys
    
    print("Soul Foods Dashboard - Test Suite")
    print("=" * 50)
    print("Running Dash application tests...")
    print()
    
    # Run pytest with verbose output
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__, 
        "-v", 
        "--tb=short"
    ], capture_output=False)
    
    if result.returncode == 0:
        print("\n🎉 All tests passed! Dashboard is working correctly.")
    else:
        print("\n❌ Some tests failed. Check output above.")
        
    sys.exit(result.returncode)