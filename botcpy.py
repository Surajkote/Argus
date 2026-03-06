import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def join_google_meet(meet_url):
    print("Launching browser with persistent profile...")
    
    with Stealth().use_sync(sync_playwright()) as p:
        
        # NEW: We use launch_persistent_context to save login cookies
        # It will create a folder called "chrome_profile" in your meetbot directory
        context = p.chromium.launch_persistent_context(
            user_data_dir="./chrome_profile",
            headless=False, 
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--disable-blink-features=AutomationControlled"
            ],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            permissions=['camera', 'microphone']
        )
        
        # In persistent context, a page is created automatically
        page = context.pages[0] 
        
        print(f"Navigating to {meet_url}...")
        page.goto(meet_url)
        
        try:
            # We removed the "Guest Name" logic because logged-in users don't need it.
            # Give the page a moment to load the buttons
            time.sleep(5)
            
            print("Attempting to join the meeting...")
            join_button = page.locator('button:has-text("Ask to join"), button:has-text("Join now")').first
            join_button.wait_for(state="visible", timeout=15000)
            join_button.click()
            
            print("Successfully clicked join! Waiting in the meeting...")
            
            # Keep the bot alive
            time.sleep(3600) 
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Keep the browser open to see what is blocking the bot...")
            time.sleep(60)
            
        finally:
            print("Closing the bot...")
            context.close()

if __name__ == "__main__":
    # ---> PASTE YOUR GOOGLE MEET LINK HERE <---
    MEETING_LINK = "https://meet.google.com/crv-zjrb-svz" 
    
    join_google_meet(MEETING_LINK)