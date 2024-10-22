import asyncio
import sys
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from backend.browser import Browser
from backend.gui import BrowserGUI

async def test_basic_navigation(browser, gui):
    print("Testing basic navigation...")
    try:
        await gui.navigate_async("https://www.example.com")
        await asyncio.sleep(5)  # Increased wait time
        print("Basic navigation test completed.")
    except Exception as e:
        print(f"Basic navigation test failed: {str(e)}")
        traceback.print_exc()

async def test_navigation_buttons(browser, gui):
    print("Testing navigation buttons...")
    try:
        await gui.navigate_async("https://www.python.org")
        await asyncio.sleep(5)
        await gui.navigate_async("https://www.github.com")
        await asyncio.sleep(5)
        gui.back_button.click()
        await asyncio.sleep(5)
        gui.forward_button.click()
        await asyncio.sleep(5)
        gui.refresh_button.click()
        await asyncio.sleep(5)
        print("Navigation buttons test completed.")
    except Exception as e:
        print(f"Navigation buttons test failed: {str(e)}")

async def test_search(browser, gui):
    print("Testing search functionality...")
    try:
        await browser.search("Python programming")
        await asyncio.sleep(5)
        print("Search functionality test completed.")
    except Exception as e:
        print(f"Search functionality test failed: {str(e)}")

async def test_bookmarks(browser, gui):
    print("Testing bookmark functionality...")
    try:
        await gui.navigate_async("https://www.python.org")
        await asyncio.sleep(5)
        await browser.add_bookmark("Python Official Site")
        bookmarks = browser.get_bookmarks()
        print("Current bookmarks:", bookmarks)
        print("Bookmark functionality test completed.")
    except Exception as e:
        print(f"Bookmark functionality test failed: {str(e)}")

async def test_history(browser, gui):
    print("Testing history functionality...")
    try:
        await gui.navigate_async("https://www.github.com")
        await asyncio.sleep(5)
        await browser.go_back()
        await asyncio.sleep(5)
        print("History functionality test completed.")
    except Exception as e:
        print(f"History functionality test failed: {str(e)}")

async def test_error_handling(browser, gui):
    print("Testing error handling...")
    try:
        await gui.navigate_async("https://www.thisisnotarealwebsite123.com")
        await asyncio.sleep(5)
        print("Error handling test completed.")
    except Exception as e:
        print(f"Error handling test failed: {str(e)}")

async def run_tests(browser, gui):
    tests = [
        test_basic_navigation,
        test_navigation_buttons,
        test_search,
        test_bookmarks,
        test_history,
        test_error_handling
    ]
    
    for test in tests:
        try:
            print(f"Starting test: {test.__name__}")
            await test(browser, gui)
            await asyncio.sleep(2)  # Add a small delay between tests
            print(f"Completed test: {test.__name__}")
        except Exception as e:
            print(f"Test {test.__name__} failed: {str(e)}")
            traceback.print_exc()
    
    print("All tests completed. Please check browser.log for detailed logs.")
    QApplication.instance().quit()

def start_tests(browser, gui):
    print("Starting tests...")
    asyncio.ensure_future(run_tests(browser, gui))

if __name__ == "__main__":
    print("Test script started")
    app = QApplication(sys.argv)
    browser = Browser()
    gui = BrowserGUI(browser)
    browser.set_gui(gui)
    
    # Start the browser
    gui.show()
    
    # Create a QTimer to start the tests
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: start_tests(browser, gui))
    timer.start(1000)
    
    # Run the event loop
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        print("Test script ended")
