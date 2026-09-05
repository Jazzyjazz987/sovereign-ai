#!/usr/bin/env python3
"""Test FastAPI web UI with Playwright"""
import asyncio
from playwright.async_api import async_playwright

async def test_fastapi_ui():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to API docs
        print("📱 Navigating to http://localhost:5000/docs")
        await page.goto("http://localhost:5000/docs")

        # Wait for page to load
        await page.wait_for_load_state("networkidle")

        # Check if Swagger UI loaded
        title = await page.title()
        print(f"✅ Page title: {title}")

        # Take screenshot
        await page.screenshot(path="/tmp/fastapi_docs.png")
        print("📸 Screenshot saved to /tmp/fastapi_docs.png")

        # Verify key elements are present
        try:
            # Check for Swagger UI elements
            swagger_title = await page.locator("text=Swagger UI").first.is_visible(timeout=5000)
            print(f"✅ Swagger UI visible: {swagger_title}")
        except:
            print("⚠️  Swagger UI not found, checking for OpenAPI")

        # Get page content summary
        body_text = await page.text_content("body")
        if "mistral" in body_text.lower() or "openapi" in body_text.lower():
            print("✅ API documentation loaded")

        # List some endpoints visible in docs
        try:
            endpoints = await page.locator("text=/\/query|\/health|\/models/").all_text_contents()
            if endpoints:
                print(f"✅ Found endpoints: {len(endpoints)} visible")
        except:
            pass

        await browser.close()
        print("🎉 Test complete!")

if __name__ == "__main__":
    asyncio.run(test_fastapi_ui())
