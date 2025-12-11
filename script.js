document.addEventListener('DOMContentLoaded', () => {
    // API KEY CONFIGURATION
    // WARNING: Exposing API keys in client-side code is not recommended for production.
    // This is for demonstration purposes only as requested.
    const GEMINI_API_KEY = "AIzaSyCUi7cEhlg_VDnKAd9yQuZgn1b7VebB4RA";
    const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-preview-02-05:generateContent?key=${GEMINI_API_KEY}`;

    // --- UI Interactions ---

    // Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile Menu Toggle (Basic)
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        // Simple toggle for demo; in production would add class to show/hide
        // For now, let's just log or do a simple alert if we don't have CSS for it
        // Actually, let's add a class and style it if we had time, but for now focus on chatbot
        console.log('Mobile menu toggled');
    });

    // Smooth Scroll for Anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- Chatbot Logic ---
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Toggle Chat
    chatToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            setTimeout(() => chatInput.focus(), 300);
        }
    });

    chatClose.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Send Message
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Add User Message
        addMessage(text, 'user');
        chatInput.value = '';

        // Show Loading State (Basic)
        const loadingId = addMessage('Thinking...', 'bot', true);

        try {
            const response = await fetchGeminiResponse(text);
            // Remove loading and add response
            removeMessage(loadingId);
            addMessage(response, 'bot');
        } catch (error) {
            console.error(error);
            removeMessage(loadingId);
            addMessage("Sorry, I'm having trouble connecting to the mountains right now. Please try again later.", 'bot');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(text, sender, isLoading = false) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        if (isLoading) div.id = 'loading-msg';

        const textDiv = document.createElement('div');
        textDiv.className = 'text';
        textDiv.textContent = text;

        div.appendChild(textDiv);
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div.id; // Return ID if needed
    }

    function removeMessage(id) {
        const el = document.getElementById('loading-msg'); // Simple ID selector for the loading one
        if (el) el.remove();
    }

    // Gemini API Call
    async function fetchGeminiResponse(userMessage) {
        // System prompt context
        const context = `
            You are the helpful AI assistant for Yodelin Broth Company & Beer Garden in Leavenworth, WA. 
            We are a stylish, rustic joint offering bone broth, burgers, salads, and craft beer with mountain views.
            Location: 633 Front St #1346, Leavenworth, WA.
            Hours: Mon-Thu 11am-9pm, Fri-Sun 11am-10pm.
            We do takeout (ToastTab) and have a beer garden.
            We specialize in Bone Broth (healing, 24hr simmer) and Craft Beer interactions (inventory varies).
            Tone: Friendly, rustic, helpful, slightly hipster/outdoorsy but professional.
            Keep answers concise (under 50 words usually).
            User asked: ${userMessage}
        `;

        const payload = {
            contents: [{
                parts: [{
                    text: context
                }]
            }]
        };

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        // Extract text from Gemini response structure
        // Usually: candidates[0].content.parts[0].text
        const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "I didn't catch that.";
        return reply;
    }
});
