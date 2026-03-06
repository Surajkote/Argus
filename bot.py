import time
import sys
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def join_google_meet(meet_url, bot_name="Notetaker Bot"):
    print("Launching bot in Anonymous mode...")
    
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=False, 
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        # Standard ephemeral context (no saved logins)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            permissions=['camera', 'microphone']
        )
        
        page = context.new_page()
        
        try:
            print(f"Navigating to {meet_url}...")
            page.goto(meet_url)
            
            # Let the UI settle
            time.sleep(4)
            
            print("Looking for the name input field...")
            # We use multiple selectors to catch different versions of the Meet UI
            name_input = page.locator('input[aria-label="Your name"], input[placeholder="Your name"], input[type="text"]')
            
            if name_input.count() > 0:
                name_input.first.fill(bot_name)
                print(f"Entered name: {bot_name}")
            else:
                print("⚠️ COULD NOT FIND NAME INPUT!")
                print("Google might be demanding a login, or the UI changed.")
                page.screenshot(path="debug_screen.png")
                print("📸 Saved a screenshot to 'debug_screen.png' so you can see what the bot sees.")
                
            time.sleep(2)
            
            print("Attempting to click Join...")
            join_button = page.locator('button:has-text("Ask to join"), button:has-text("Join now"), button:has-text("Join")')
            
            if join_button.count() > 0:
                join_button.first.click()
                print("✅ Successfully clicked join! Waiting for host to admit...")
            else:
                print("⚠️ COULD NOT FIND JOIN BUTTON!")
                page.screenshot(path="debug_screen.png")
            
            print("\n" + "="*50)
            print("BOT IS ACTIVE. Press Ctrl+C in this terminal to kill it.")
            print("="*50 + "\n")
            
            # Infinite loop to keep the bot alive until you manually kill it
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            # THIS IS THE FIX FOR THE LINGERING BOT
            print("\n🛑 Shutdown signal received (Ctrl+C). Exiting gracefully...")
            
            # Try to actually click the red "Leave Call" button if we are in the meeting
            try:
                leave_button = page.locator('button[aria-label="Leave call"]')
                if leave_button.count() > 0:
                    leave_button.first.click()
                    print("Clicked the 'Leave call' button.")
                    time.sleep(1)
            except Exception:
                pass # If the button isn't there, just move on
                
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            page.screenshot(path="error_screen.png")
            
        finally:
            print("Sweeping up processes and closing the browser...")
            context.close()
            browser.close()
            sys.exit(0) # Forces python to quit immediately

if __name__ == "__main__":
    # ---> PASTE YOUR GOOGLE MEET LINK HERE <---
    MEETING_LINK = "https://meet.google.com/crv-zjrb-svz" 
    
    join_google_meet(MEETING_LINK)