# 🔮 AI Astrology Chatbot

An intelligent, conversational astrology application powered by Google Gemini AI and built with Streamlit. This project demonstrates modern AI integration, robust error handling, and user-centric design for personalized astrological insights.

## ✨ Features

- 🤖 AI-Powered Conversations: Uses Google Gemini AI for intelligent, context-aware responses
- 🔮 Personalized Readings: Tailored astrological insights based on your birth details
- 💬 Natural Language Q&A: Ask any questions about love, career, health, future, and finances
- 📥 Download Transcripts: Save your conversation as a text file
- 🛡️ Robust Fallback: Continues working even when AI is temporarily unavailable
- 📱 Clean UI: Modern chat interface with cosmic-themed design

## 🧠 AI-Powered with Robust Fallback

This chatbot uses a **dual-method approach** for maximum reliability:

### Primary Method: Google Gemini AI
- Provides advanced, personalized astrology insights.
- Generates unique answers based on user birth details.

### Secondary Method: Rule-Based Fallback
- Ensures meaningful responses if Gemini AI API is unavailable (rate limits, outages).
- Uses traditional zodiac knowledge base for fallback answers.

This hybrid architecture guarantees relevant replies and professional-grade reliability.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free at [Google AI Studio](https://ai.google.dev/))

### Installation

1. Clone the repository
2. Install dependencies via `pip install -r requirements.txt`
3. Create a `.env` file with your Google Gemini API Key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the app with `streamlit run app.py`

## 🎯 How to Use

1. Enter Your Birth Details
- Provide your name, birth date, time, and place
- The chatbot guides you through each step conversationally

2. Get Your Astrology Reading
- Receive a personalized reading based on your zodiac sign
- Learn about your cosmic personality and traits

3. Ask Questions
- Inquire about love, career, health, future predictions, or finances
- Get AI-powered insights tailored to your astrological profile

4. Download & Share
- Save your conversation transcript from the sidebar
- Keep your cosmic insights for future reference

## 🛠️ Technology Stack

| Component | Technology | Implementation |
|-----------|------------|----------------|
| Frontend | Streamlit | Chat UI with custom CSS styling |
| AI Engine | Google Gemini API | Primary response generation |
| Fallback System | Python logic | Rule-based astrology responses |
| Data Processing | Python datetime | Zodiac calculation and validation |
| State Management | Streamlit session | User data and conversation history |
| Security | Environment variables | Secure API key management |

## 📊 Architecture Overview

Describes hybrid AI and fallback components to ensure professional-grade reliability.

# 🔧 Error Handling & Reliability

- API Failures: Automatic fallback to rule-based responses
- Rate Limiting: Exponential backoff and retry mechanism
- Input Validation: Clear error messages and retry prompts
- Network Issues: Graceful degradation with informative messages
- Debug Tools: Built-in troubleshooting capabilities

## 📁 Project Structure


ai-astrology-chatbot/
│
├── app.py # Main application with AI + fallback logic
├── requirements.txt # Python dependencies
├── .env # Environment variables (create this)
├── README.md # Project documentation
