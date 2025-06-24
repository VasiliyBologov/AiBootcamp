# Product Requirements Document (PRD)

## Product: Customer Support Chat Web Page (Frontend)

**Goal:**  
Enable users to chat with customer support agents via a web-based interface.

---

## 1. Overview

A single-page web interface for customer support chat. The chat window must be centered on the page for any screen size, using HTML, Bootstrap 5, and Fetch API for backend communication.

---

## 2. Functional Requirements

- **Chat Window**
  - Fixed width and height (responsive for mobile, tablet, desktop).
  - Always centered (both vertically and horizontally).
  - Scrollable message area for conversation.
  - Input field for typing messages.
  - Send button to send messages.
  - Messages appear as bubbles (user on right, support on left).
  - System messages in the center.
  - Loader/indicator when sending or waiting for reply.

- **API Interaction**
  - Fetch existing conversation on load (`GET /api/chat`).
  - Send message (`POST /api/chat/message`, payload: `{ message: "..." }`).
  - Poll for new messages (optional: every 2-3 seconds).
  - Handle network or server errors gracefully.

---

## 3. Non-Functional Requirements

- Uses **Bootstrap** for layout and styles.
- No frameworks (like React/Vue/Angular).
- Only **vanilla JS** with Fetch API.
- Responsive design.
- Supports all modern browsers.

---

## 4. User Stories

- **As a user**, I want to open the page and see the chat window in the center.
- **As a user**, I want to see past chat messages immediately.
- **As a user**, I want to type a message and send it by pressing the send button or Enter.
- **As a user**, I want to see my messages and support replies distinctly.
- **As a user**, I want to see when my message is being sent or waiting for a reply.
- **As a user**, I want a smooth experience on any device.

---

## 5. Acceptance Criteria

- Chat window is always centered on the page.
- User can send and receive messages.
- Existing chat history loads on open.
- Page adapts for mobile and desktop.
- Error states are shown if server is unavailable.

---

## 6. Example HTML + Bootstrap + JS Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Customer Support Chat</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Bootstrap 5 CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body, html { height: 100%; }
    .chat-center {
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #f8f9fa;
    }
    .chat-window {
      width: 100%;
      max-width: 400px;
      height: 600px;
      background: #fff;
      border-radius: 1rem;
      box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
    }
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
    }
    .message {
      margin-bottom: 0.5rem;
      max-width: 80%;
      word-break: break-word;
    }
    .message.user {
      align-self: flex-end;
      background: #d1e7dd;
      border-radius: 1rem 1rem 0 1rem;
      padding: 0.5rem 1rem;
    }
    .message.support {
      align-self: flex-start;
      background: #e2e3e5;
      border-radius: 1rem 1rem 1rem 0;
      padding: 0.5rem 1rem;
    }
    .message.system {
      align-self: center;
      background: transparent;
      color: #888;
      font-size: 0.85rem;
      margin: 0.5rem 0;
    }
    .chat-input-area {
      display: flex;
      border-top: 1px solid #eee;
      padding: 0.5rem;
      background: #f8f9fa;
    }
    .chat-input-area input {
      flex: 1;
      border: none;
      border-radius: 1rem;
      padding: 0.5rem 1rem;
      margin-right: 0.5rem;
    }
    .chat-input-area button {
      border-radius: 1rem;
    }
    .loading {
      text-align: center;
      color: #888;
    }
  </style>
</head>
<body>
  <div class="chat-center">
    <div class="chat-window d-flex flex-column">
      <div class="chat-messages" id="chatMessages">
        <div class="loading" id="chatLoading">Loading...</div>
      </div>
      <div class="chat-input-area">
        <input type="text" id="chatInput" placeholder="Type your message..." autocomplete="off"/>
        <button class="btn btn-primary" id="sendBtn">Send</button>
      </div>
    </div>
  </div>
  <script>
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatLoading = document.getElementById('chatLoading');

    // Fetch chat history
    function loadMessages() {
      fetch('/api/chat')
        .then(res => res.json())
        .then(data => {
          chatMessages.innerHTML = '';
          data.messages.forEach(msg => addMessage(msg));
          chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(() => chatMessages.innerHTML = '<div class="message system">Failed to load chat</div>');
    }

    // Add message bubble
    function addMessage(msg) {
      const div = document.createElement('div');
      div.className = 'message ' + (msg.role || 'system');
      div.innerText = msg.text;
      chatMessages.appendChild(div);
    }

    // Send message
    function sendMessage() {
      const text = chatInput.value.trim();
      if (!text) return;
      addMessage({role: 'user', text});
      chatInput.value = '';
      chatInput.disabled = true;
      sendBtn.disabled = true;
      // Loader
      const loader = document.createElement('div');
      loader.className = 'message system';
      loader.innerText = 'Sending...';
      chatMessages.appendChild(loader);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      fetch('/api/chat/message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      })
      .then(res => res.json())
      .then(data => {
        loader.remove();
        if (data.reply) {
          addMessage({role: 'support', text: data.reply});
        }
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch(() => {
        loader.innerText = 'Failed to send message';
        chatInput.disabled = false;
        sendBtn.disabled = false;
      });
    }

    sendBtn.onclick = sendMessage;
    chatInput.onkeydown = e => { if (e.key === 'Enter') sendMessage(); };

    // Optional: Poll for new messages every 3 seconds
    setInterval(loadMessages, 3000);

    // Initial load
    loadMessages();
  </script>
</body>
</html>
