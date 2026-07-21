from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/usr/bin/chromium",
        headless=False
    )

    page = browser.new_page(
        viewport={"width": 1600, "height": 1200}
    )

    page.goto("https://jp.investing.com/charts/live-charts")

    page.wait_for_timeout(8000)

    print(page.locator("body").inner_text)

    input("Enterで終了")
