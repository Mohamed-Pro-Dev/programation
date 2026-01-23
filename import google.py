import google.generativeai as genai
import os

# Configure API key
api_key = os.getenv("AIzaSyBTmdZN1cgGD8blW4leTnil9mGKafqi2Ys")
if not api_key:
    raise ValueError("AIzaSyBTmdZN1cgGD8blW4leTnil9mGKafqi2Ys environment variable is not set")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

def chatbot():
    """Simple AI chatbot using Google Generative AI"""
    print("AI Chatbot (type 'quit' to exit)")
    print("-" * 40)
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Send message to AI
        response = model.generate_content(user_input)
        print(f"Bot: {response.text}\n")

if __name__ == "__main__":
    chatbot()