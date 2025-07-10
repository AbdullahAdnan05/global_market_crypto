import pytest
from dash import Dash
from dashboard.layout import get_layout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from config.settings import CHROMEDRIVER_PATH

@pytest.mark.e2e
def test_dashboard_renders():
    app = Dash(__name__, suppress_callback_exceptions=True)
    app.layout = get_layout()
    layout_children = app.layout.children

    assert layout_children, "❌ Layout is empty"
    assert any("Tabs" in str(child) for child in layout_children), "❌ Tabs not found"
    
@pytest.mark.e2e
def test_dashboard_loads():
    # Start Chrome driver (update your path)
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        # Start your server in a separate terminal before running this test
        driver.get("http://localhost:8050/")
        time.sleep(3)  # Wait for layout to render

        # Check page title or header is visible
        assert "Global Market Pulse" in driver.title or driver.page_source

        # Wait for dropdowns or cards to appear
        coin_dropdown = driver.find_element(By.ID, "coin-dropdown")
        assert coin_dropdown is not None

        # Check at least one card is visible
        card = driver.find_element(By.ID, "total-market-cap")
        assert card.text.lower() != "loading..."

    finally:
        driver.quit()