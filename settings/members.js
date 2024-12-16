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
        window.location.href = '/login';
    });
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}
