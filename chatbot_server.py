import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyBjHdAl1aUwWa3xVbH0vi_0tCjSZcoYWgQ"
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash")
# Store conversation history for context
conversation_history = []

# System prompt for the chatbot
SYSTEM_PROMPT = """أنت مساعد ذكي لثانوية عمر بن عبد العزيز (مدرسة مغربية متخصصة في التعليم الثانوي التأهيلي والأقسام التحضيرية).

معلومات عن المدرسة:
- الموقع: شارع علال بن عبدالله، وجدة، المغرب
- رقم الهاتف: 0536683189
- البريد الإلكتروني: info@lycee-omar.ma
- التخصصات: أقسام تحضيرية (علمي وأدبي)
- مواعيد التسجيل: من 1 يناير إلى 31 مايو يومياً من 8:00 إلى 17:00
- القيم: الشفافية والعدالة، الابتكار الرقمي، التعليم المخصص

إجابتك يجب أن تكون:
- مفيدة وودية
- موجهة بالعربية (باللهجة الفصحى)
- مختصرة وواضحة (بحد أقصى 3 فقرات)
- متعلقة بالمدرسة والتعليم
- إذا كان السؤال خارج التخصص، أعد توجيه المستخدم بلطف

تجنب:
- الإجابات الطويلة جداً
- المعلومات الحساسة الشخصية
- النصائح الطبية أو القانونية
"""

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'الرسالة فارغة'
            }), 400
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Build conversation context
        context = SYSTEM_PROMPT + "\n\nمحادثة سابقة:\n"
        for msg in conversation_history[-4:]:  # Keep last 4 messages for context
            role = "المستخدم" if msg['role'] == 'user' else "المساعد"
            context += f"{role}: {msg['content']}\n"
        
        # Generate response from AI
        response = model.generate_content(context)
        bot_response = response.text
        
        # Add bot response to history
        conversation_history.append({
            'role': 'assistant',
            'content': bot_response
        })
        
        # Limit history to last 10 messages to save memory
        if len(conversation_history) > 10:
            conversation_history.pop(0)
            conversation_history.pop(0)
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({
        'success': True,
        'message': 'تم إعادة تعيين المحادثة'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'الخادم يعمل بشكل صحيح'
    })

if __name__ == '__main__':
    print("🤖 خادم الذكاء الاصطناعي يعمل على http://localhost:5000")
    print("📝 افتح chatbot.html في متصفحك للدخول للمساعد الذكي")
    print("⚠️ تأكد من تثبيت المكتبات: pip install flask flask-cors google-generativeai python-dotenv")
    
    # Run the Flask server
    app.run(debug=True, port=5000, host='0.0.0.0')
