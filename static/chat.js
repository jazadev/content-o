function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;

    addMessage('user', message);
    input.value = '';

    fetch('/api/v1/content-o-courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.data.content);
    })
    .catch(error => console.error('Error:', error));
}

function addMessage(type, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
