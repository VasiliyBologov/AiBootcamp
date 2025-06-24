// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatLoading = document.getElementById('chatLoading');

// API endpoints
const API_ENDPOINTS = {
  GET_CHAT: '/api/chat',
  SEND_MESSAGE: '/api/chat/message'
};

// Chat state
let isWaitingForResponse = false;

/**
 * Fetch chat history from the server
 */
function loadMessages() {
  // Don't fetch again if we're waiting for a response
  if (isWaitingForResponse) return;

  fetch(API_ENDPOINTS.GET_CHAT)
    .then(handleResponse)
    .then(data => {
      // Clear loading indicator if it exists
      if (chatLoading) {
        chatMessages.innerHTML = '';
      }

      // Display messages
      if (data.messages && Array.isArray(data.messages)) {
        data.messages.forEach(msg => addMessage(msg));
        scrollToBottom();
      }
    })
    .catch(error => {
      console.error('Error loading messages:', error);
      chatMessages.innerHTML = '<div class="message system">Failed to load chat history. Please refresh the page.</div>';
    });
}

/**
 * Handle API response and check for errors
 */
function handleResponse(response) {
  if (!response.ok) {
    throw new Error(`Network response was not ok: ${response.status}`);
  }
  return response.json();
}

/**
 * Add a message to the chat window
 */
function addMessage(msg) {
  const div = document.createElement('div');
  div.className = 'message ' + (msg.role || 'system');
  div.textContent = msg.text;
  chatMessages.appendChild(div);
}

/**
 * Send a message to the server
 */
function sendMessage() {
  const text = chatInput.value.trim();
  if (!text || isWaitingForResponse) return;

  // Add user message to chat
  addMessage({role: 'user', text});

  // Clear input and disable while sending
  chatInput.value = '';
  chatInput.disabled = true;
  sendBtn.disabled = true;
  isWaitingForResponse = true;

  // Show typing indicator
  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'message system typing-indicator';
  typingIndicator.innerHTML = '<span></span><span></span><span></span>';
  chatMessages.appendChild(typingIndicator);
  scrollToBottom();

  // Send message to server
  fetch(API_ENDPOINTS.SEND_MESSAGE, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: text})
  })
  .then(handleResponse)
  .then(data => {
    // Remove typing indicator
    typingIndicator.remove();

    // Add support response if available
    if (data.reply) {
      addMessage({role: 'support', text: data.reply});
    }

    // Re-enable input
    chatInput.disabled = false;
    sendBtn.disabled = false;
    chatInput.focus();
    scrollToBottom();
    isWaitingForResponse = false;
  })
  .catch(error => {
    console.error('Error sending message:', error);
    typingIndicator.remove();
    addMessage({role: 'system', text: 'Failed to send message. Please try again.'});
    chatInput.disabled = false;
    sendBtn.disabled = false;
    isWaitingForResponse = false;
  });
}

/**
 * Scroll chat to the bottom
 */
function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', e => { 
  if (e.key === 'Enter') sendMessage(); 
});

// Poll for new messages every 3 seconds
setInterval(loadMessages, 3000);

// Initial load
loadMessages();

// Add connection status handling
window.addEventListener('online', () => {
  document.querySelector('.status-indicator').classList.remove('offline');
  document.querySelector('.status-indicator').classList.add('online');
  addMessage({role: 'system', text: 'You are back online.'});
  loadMessages(); // Refresh messages when coming back online
});

window.addEventListener('offline', () => {
  document.querySelector('.status-indicator').classList.remove('online');
  document.querySelector('.status-indicator').classList.add('offline');
  addMessage({role: 'system', text: 'You are currently offline. Messages cannot be sent or received.'});
});
