import requests
import ollama
import time

# --- CONFIGURATION ---
VEXA_API_KEY = "klZgy9QxOwMRwhZ2FaGEackoAHhQcMjfT3Nr9Gvq" # Replace with your real key from vexa.ai dashboard
MEETING_ID = "kai-bcjm-dyq" # ONLY the meeting ID, not the full URL

def send_bot_to_meeting(meeting_id):
    """Tells Vexa to send a bot to the meeting."""
    print(f"🤖 Sending bot to Google Meet: {meeting_id}")
    
    # Corrected Endpoint and Headers based on Vexa Docs
    api_url = "https://api.cloud.vexa.ai/bots"
    headers = {
        "X-API-Key": VEXA_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Corrected Payload structure
    payload = {
        "platform": "google_meet",
        "native_meeting_id": meeting_id
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status() # This will raise an error if the request fails (e.g. 401 Unauthorized)
        
        print("✅ Bot successfully requested!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to join.")
        if e.response is not None:
            print(f"Error details: {e.response.text}")
        else:
            print(f"Connection Error: {e}")
        return None

def summarize_transcript(transcript_text):
    """Uses your local Ollama model to summarize the text."""
    print("🧠 Generating summary using local Ollama...")
    
    try:
        # Assuming you have a small model like 'phi3' or 'llama3' pulled via Ollama
        response = ollama.chat(model='llama3.2:1b', messages=[
            {
                'role': 'system',
                'content': 'You are an expert meeting assistant. Summarize the following meeting transcript into key bullet points and action items.'
            },
            {
                'role': 'user',
                'content': transcript_text
            }
        ])
        return response['message']['content']
    except Exception as e:
         print(f"❌ Ollama Error: Is the Ollama app running? Did you pull the model? Error: {e}")
         return None

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Request the bot to join
    bot_response = send_bot_to_meeting(MEETING_ID)
    
    if bot_response:
        print("\n⏳ Bot is joining the meeting. Please wait a few seconds and check your Google Meet tab.")
        print("You will need to 'Admit' the bot if you are the host.")
        
        # NOTE: For phase 1, we are just verifying the bot joins.
        dummy_transcript = "Alice: Hi guys, let's build a meetbot. Bob: Sounds good, let's use Vexa AI for the bot and Ollama for the summary."
        
        # 2. Summarize (Testing local Ollama setup)
        summary = summarize_transcript(dummy_transcript)
        if summary:
            print("\n📝 --- TEST MEETING SUMMARY ---")
            print(summary)