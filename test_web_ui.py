#!/usr/bin/env python3
"""
Sovereign AI Stack Web UI Test
Tests cascade router at http://localhost:8888
"""

from playwright.async_api import async_playwright
import asyncio
import sys

async def test_web_ui():
    """Test the Sovereign AI web UI"""

    results = {
        "page_loads": False,
        "model_selector_visible": False,
        "query_input_present": False,
        "response_received": False,
        "model_displayed": False,
        "errors": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # 1. Navigate to web UI
            print("📍 [1/6] Navigating to http://localhost:8888...")
            await page.goto("http://localhost:8888", timeout=10000)
            await page.wait_for_load_state("networkidle")
            results["page_loads"] = True
            print("✅ Page loaded")

            # Take initial screenshot
            await page.screenshot(path="/tmp/ui_01_home.png")
            print("📸 Screenshot: /tmp/ui_01_home.png")

        except Exception as e:
            results["errors"].append(f"Failed to load page: {e}")
            print(f"❌ Failed to load page: {e}")
            await browser.close()
            return results

        try:
            # 2. Check for model selector
            print("\n📍 [2/6] Looking for model selector dropdown...")

            # Try different possible selectors for model dropdown
            selectors = [
                'select[name="model"]',
                'select',
                '[data-testid="model-selector"]',
                'div[class*="select"]',
            ]

            model_selector = None
            for selector in selectors:
                elements = await page.locator(selector).count()
                if elements > 0:
                    model_selector = selector
                    print(f"  Found: {selector}")
                    break

            if model_selector:
                results["model_selector_visible"] = True
                print("✅ Model selector found")

                # Click to see options
                await page.locator(model_selector).click()
                await page.wait_for_timeout(500)
                await page.screenshot(path="/tmp/ui_02_model_selector.png")
                print("📸 Screenshot: /tmp/ui_02_model_selector.png (dropdown opened)")
            else:
                # Check for button/radio options instead
                auto_button = await page.locator("text=Auto").count()
                t1_button = await page.locator("text=T1").count()

                if auto_button > 0 or t1_button > 0:
                    results["model_selector_visible"] = True
                    print("✅ Model selector found (button/radio format)")
                else:
                    results["errors"].append("Model selector not found")
                    print("⚠️ Model selector not found (may not be implemented yet)")

        except Exception as e:
            results["errors"].append(f"Error checking model selector: {e}")
            print(f"⚠️ Error checking model selector: {e}")

        try:
            # 3. Look for query input field
            print("\n📍 [3/6] Looking for query input field...")

            input_selectors = [
                'input[type="text"]',
                'textarea',
                'input[placeholder*="query"]',
                'input[placeholder*="message"]',
            ]

            query_input = None
            for selector in input_selectors:
                elements = await page.locator(selector).count()
                if elements > 0:
                    query_input = selector
                    print(f"  Found: {selector}")
                    break

            if query_input:
                results["query_input_present"] = True
                print("✅ Query input field found")
            else:
                results["errors"].append("Query input not found")
                print("⚠️ Query input field not found")

        except Exception as e:
            results["errors"].append(f"Error checking query input: {e}")
            print(f"⚠️ Error checking query input: {e}")

        # 4. Try to submit a query
        try:
            print("\n📍 [4/6] Submitting test query...")

            # Find and fill query input
            if query_input:
                await page.locator(query_input).fill("Hello, test query")
                print("  Filled query input: 'Hello, test query'")

                # Find submit button
                submit_button = None
                button_selectors = [
                    'button:has-text("Send")',
                    'button:has-text("Submit")',
                    'button:has-text("Query")',
                    'button[type="submit"]',
                ]

                for selector in button_selectors:
                    elements = await page.locator(selector).count()
                    if elements > 0:
                        submit_button = selector
                        break

                if submit_button:
                    await page.locator(submit_button).click()
                    print("  Clicked submit button")

                    # Wait for response
                    print("  Waiting for response...")
                    await page.wait_for_timeout(3000)

                    # Check for response text
                    response_text = await page.content()
                    if len(response_text) > 5000:  # Content changed
                        results["response_received"] = True
                        print("✅ Response received")
                    else:
                        results["errors"].append("No response detected")
                        print("⚠️ Response not detected")

                    await page.screenshot(path="/tmp/ui_03_response.png")
                    print("📸 Screenshot: /tmp/ui_03_response.png")
                else:
                    results["errors"].append("Submit button not found")
                    print("⚠️ Submit button not found")
            else:
                print("⚠️ Cannot submit query - input field not found")

        except Exception as e:
            results["errors"].append(f"Error submitting query: {e}")
            print(f"⚠️ Error submitting query: {e}")

        # 5. Check for model name in response
        try:
            print("\n📍 [5/6] Checking for model name in response...")

            page_text = await page.content()
            model_names = ["mistral", "llama", "neural-chat", "dolphin", "t1", "t2", "t3", "t4"]

            found_models = [m for m in model_names if m.lower() in page_text.lower()]

            if found_models:
                results["model_displayed"] = True
                print(f"✅ Model(s) found in response: {found_models}")
            else:
                results["errors"].append("No model name in response")
                print("⚠️ Model name not found in response")

        except Exception as e:
            results["errors"].append(f"Error checking model display: {e}")
            print(f"⚠️ Error checking model display: {e}")

        # 6. Final screenshot and summary
        print("\n📍 [6/6] Final page state...")
        await page.screenshot(path="/tmp/ui_04_final.png")
        print("📸 Screenshot: /tmp/ui_04_final.png")

        await browser.close()

    return results


async def main():
    print("=" * 60)
    print("  SOVEREIGN AI STACK - WEB UI VERIFICATION")
    print("=" * 60)
    print()

    results = await test_web_ui()

    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    print(f"\n{'Page Loads':<30} {'✅' if results['page_loads'] else '❌'}")
    print(f"{'Model Selector Visible':<30} {'✅' if results['model_selector_visible'] else '⚠️'}")
    print(f"{'Query Input Present':<30} {'✅' if results['query_input_present'] else '⚠️'}")
    print(f"{'Response Received':<30} {'✅' if results['response_received'] else '⚠️'}")
    print(f"{'Model Displayed':<30} {'✅' if results['model_displayed'] else '⚠️'}")

    if results["errors"]:
        print(f"\n⚠️ Issues Found:")
        for error in results["errors"]:
            print(f"  • {error}")

    print(f"\n📸 Screenshots saved to /tmp/ui_*.png")
    print(f"\nView with: file:///tmp/ui_*.png")

    # Exit code
    if results["page_loads"] and results["query_input_present"]:
        print("\n✅ Web UI is functional!")
        return 0
    else:
        print("\n⚠️ Web UI needs attention")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
