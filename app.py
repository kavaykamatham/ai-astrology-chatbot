import streamlit as st
import base64
import google.generativeai as genai
from datetime import datetime
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error("Please check your GEMINI_API_KEY in the .env file.")

# Set Streamlit page config
st.set_page_config(
    page_title="🔮 AI Astrology Chatbot",
    page_icon="🔮",
    layout="centered"
)



# Functions
def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    else:
        return "Unknown"

def generate_ai_response(prompt, context="", max_retries=3, delay=2):
    retry_count = 0
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            system_prompt = f"""You are a wise and mystical astrologer with deep knowledge of zodiac signs, birth charts, and cosmic influences.

            User Context: {context}

            Guidelines:
            - Provide warm, encouraging, and insightful responses
            - Use astrological knowledge and terminology naturally
            - Be specific to the user's zodiac sign when available
            - Keep responses engaging but not too long (2-3 paragraphs max)
            - Include emojis and mystical language appropriately

            User Question: {prompt}

            Respond as an expert astrologer would:
            """
            response = model.generate_content(system_prompt)
            if response.text:
                return response.text
            else:
                raise Exception("Empty response from Gemini")
        except Exception as e:
            print(f"Attempt {retry_count + 1} failed: {str(e)}")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(delay)
            else:
                return generate_fallback_response(prompt, context)

def generate_fallback_response(prompt, context):
    prompt_lower = prompt.lower()
    zodiac = "your sign"
    if "zodiac" in context:
        zodiac_line = [line for line in context.split('\n') if 'zodiac' in line.lower()]
        if zodiac_line:
            zodiac = zodiac_line[0].split(':')[-1].strip()

    if any(word in prompt_lower for word in ['zodiac', 'sign']):
        return f"✨ Your zodiac sign is {zodiac}! This celestial sign brings unique qualities and cosmic influences to your life. Each sign has its own characteristics that shape your personality and destiny."
    elif any(word in prompt_lower for word in ['love', 'relationship', 'romance']):
        return f"💕 In matters of love, {zodiac} individuals are guided by the stars. The cosmic energies suggest being open to authentic connections and trusting your heart's wisdom. Love flows naturally when you align with your true self."
    elif any(word in prompt_lower for word in ['career', 'job', 'work']):
        return f"💼 Career-wise, {zodiac} energy brings unique strengths to your professional journey. Trust your instincts in professional matters."
    elif any(word in prompt_lower for word in ['health', 'wellness']):
        return f"🌿 For {zodiac}, health and wellness are connected to maintaining cosmic balance. Regular self-care and mindfulness will support your natural vitality."
    else:
        return f"🔮 The cosmic energies surrounding {zodiac} suggest focusing on personal growth and positive intentions. Your path is illuminated by starlight! ✨"

def handle_conversation(user_input):
    if st.session_state.chat_stage == "greeting":
        st.session_state.chat_stage = "name"
        return "🌟 Welcome to the AI Astrology Realm! I'm your cosmic guide, ready to unveil the mysteries of your stars. What's your name, dear soul?"
    elif st.session_state.chat_stage == "name":
        st.session_state.user_data["name"] = user_input
        st.session_state.chat_stage = "birth_date"
        return f"Lovely to meet you, {user_input}! ✨ To read your cosmic blueprint, I need your birth date. Please share it in DD/MM/YYYY format."
    elif st.session_state.chat_stage == "birth_date":
        try:
            date_obj = datetime.strptime(user_input, "%d/%m/%Y")
            st.session_state.user_data["birth_date"] = date_obj
            st.session_state.user_data["zodiac"] = get_zodiac_sign(date_obj.month, date_obj.day)
            st.session_state.chat_stage = "birth_time"
            return "Perfect! 🌙 Now, what time were you born? (HH:MM format, or type 'unknown' if you're not sure)"
        except:
            return "I need the date in DD/MM/YYYY format (like 15/04/1990). Could you try again? 🌟"
    elif st.session_state.chat_stage == "birth_time":
        st.session_state.user_data["birth_time"] = user_input
        st.session_state.chat_stage = "birth_place"
        return "Wonderful! 🌍 Lastly, where were you born? (City, Country)"
    elif st.session_state.chat_stage == "birth_place":
        st.session_state.user_data["birth_place"] = user_input
        st.session_state.chat_stage = "reading"
        context = f"""
        Name: {st.session_state.user_data['name']}
        Birth Date: {st.session_state.user_data['birth_date'].strftime('%B %d, %Y')}
        Birth Time: {st.session_state.user_data['birth_time']}
        Birth Place: {st.session_state.user_data['birth_place']}
        Zodiac Sign: {st.session_state.user_data['zodiac']}
        """
        prompt = f"Please provide a comprehensive astrology reading for {st.session_state.user_data['name']} who is a {st.session_state.user_data['zodiac']}."
        reading = generate_ai_response(prompt, context)
        return f"{reading}\n\n🔮 Your cosmic profile is complete! Now you can ask me anything about love, career, health, future, or any other aspect of your life. The stars are ready to guide you!"
    else:  # Free chat mode
        context = f"""
        Name: {st.session_state.user_data['name']}
        Zodiac Sign: {st.session_state.user_data['zodiac']}
        Birth Date: {st.session_state.user_data['birth_date'].strftime('%B %d, %Y')}
        Birth Time: {st.session_state.user_data['birth_time']}
        Birth Place: {st.session_state.user_data['birth_place']}
        """
        return generate_ai_response(user_input, context)

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_stage = "greeting"
    st.session_state.user_data = {}

# Main title
st.title("🔮 AI Astrology Chatbot")
st.markdown("*✨ Powered by Google Gemini AI • Discover your cosmic destiny ✨*")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize conversation
if len(st.session_state.messages) == 0:
    initial_message = handle_conversation("")
    st.session_state.messages.append({"role": "assistant", "content": initial_message})
    with st.chat_message("assistant"):
        st.markdown(initial_message)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Consulting the cosmic energies..."):
            response = handle_conversation(prompt)
            st.markdown(response)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun()
    
    
    st.markdown("### 👤 Your Astrology Profile")
    if "user_data" in st.session_state and "name" in st.session_state.user_data:
        user_data = st.session_state.user_data
        st.markdown(f"**Name:** {user_data.get('name', 'Not set')}")
        st.markdown(f"**Zodiac:** {user_data.get('zodiac', 'Not set')}")
        if 'birth_date' in user_data and user_data['birth_date']:
            birth_date = user_data['birth_date']
            st.markdown(f"**Birth Date:** {birth_date.strftime('%B %d, %Y')}")
        else:
            st.markdown("**Birth Date:** Not set")
        st.markdown(f"**Birth Time:** {user_data.get('birth_time', 'Not set')}")
        st.markdown(f"**Birth Place:** {user_data.get('birth_place', 'Not set')}")
    else:
        st.markdown("*Complete the chat to see your profile here* ✨")

        st.markdown("---")
    st.markdown("### 🌟 About This Chatbot")
    st.markdown("🤖 **AI-Powered:** Uses Google Gemini AI for intelligent responses")
    st.markdown("🔮 **Personalized:** Tailored readings based on your birth details")
    st.markdown("💬 **Interactive:** Ask any astrology question in natural language")
    
    st.markdown("---")
    
    st.markdown("### ✨ What You Can Ask")
    st.markdown("💕 **Love & Relationships**")
    st.markdown("💼 **Career & Work**")
    st.markdown("🌿 **Health & Wellness**")
    st.markdown("🔮 **Future Predictions**")
    st.markdown("💰 **Money & Finance**")
    
    st.markdown("---")
    
    # Download conversation transcript
    if 'messages' in st.session_state and len(st.session_state.messages) > 0:
        transcript = "\n".join([f"[{msg['role'].upper()}] {msg['content']}" for msg in st.session_state.messages])
        b64 = base64.b64encode(transcript.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="astrology_chat_transcript.txt">📥 Download Chat Transcript</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    # Debug mode
    if st.checkbox("🔧 Debug Mode"):
        st.markdown("### Debug Info")
        st.markdown(f"**Chat Stage:** {st.session_state.chat_stage}")
        if os.getenv("GEMINI_API_KEY"):
            st.markdown("✅ **API Status:** Connected")
        else:
            st.markdown("❌ **API Status:** Missing")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")

# Footer

st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "🌟 Remember: The stars guide, but you shape your destiny 🌟"
    "</div>", 
    unsafe_allow_html=True
)
