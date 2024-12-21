function sendPremiumMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    const token = localStorage.getItem('id_token');
    const access_token = localStorage.getItem('access_token');

    console.log('Message:', message);
    console.log('Token:', token);
    console.log('Access Token:', access_token);
    
    if (!message || !token) {
        console.log('Missing message or token');
        return;}

    addMessage('user', message);
    input.value = '';

    fetch('/api/v1/content-o-members', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            'X-Access-Token': access_token

        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.data.content);
    })
    .then(data => {
        // Extract just the content/message to display
        const messageToShow = typeof data.data === 'string' ? data.data : data.data.response_data;
        addMessage('bot', messageToShow);
    })
    .catch(error => {
        console.error('Error:', error);
        //window.location.href = '/login';
    });
}

// Add at the beginning of the file
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('message-input');
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendPremiumMessage();
        }
    });
});


function addMessage(type, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    console.log(marked('# Hello, world!'));


    // Convertir Markdown a HTML usando marked.js
    const htmlContent = marked(content);

    // Insertar el HTML en el mensaje
    messageDiv.innerHTML = htmlContent;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function logout() {
    localStorage.removeItem('id_token');
    localStorage.removeItem('access_token');
    window.location.href = '/';
}
