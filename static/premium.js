function sendPremiumMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    const token = localStorage.getItem('token');
    
    if (!message || !token) return;

    addMessage('user', message);
    input.value = '';

    fetch('/api/v1/content-o-members', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.data.content);
    })
    .catch(error => {
        console.error('Error:', error);
        //window.location.href = '/login';
    });
}

function addMessage(type, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}
