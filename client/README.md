# Customer Support Chat Web Page

A simple, responsive web-based interface for customer support chat built with HTML, CSS, and vanilla JavaScript.

## Features

- Single-page web application
- Responsive design for mobile, tablet, and desktop
- Bootstrap 5 for styling
- Real-time chat with support agents
- Message history loading
- Visual indicators for message status
- Network status monitoring
- No frameworks, only vanilla JavaScript

## Implementation Details

This application is built following the requirements specified in the PRD:

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS with Fetch API
- **API Endpoints**:
  - `GET /api/chat` - Fetch conversation history
  - `POST /api/chat/message` - Send new message

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Custom styling beyond Bootstrap
- `app.js` - JavaScript for chat functionality

## Getting Started

1. Ensure the backend API server is running
2. Open `index.html` in a modern web browser

## Browser Compatibility

This application supports all modern browsers including:
- Chrome
- Firefox
- Safari
- Edge

## Responsive Design

The chat interface adapts to different screen sizes:
- On mobile devices, the chat window takes almost the full screen
- On larger screens, the chat window is centered with fixed dimensions

## Additional Features

- Network status indicator
- Typing animation when waiting for support response
- Error handling for API failures
- Message polling for real-time updates
