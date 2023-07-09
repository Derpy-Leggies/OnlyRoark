const socket = io({autoConnect: false});
const loginForm = document.querySelector('#loginform');
const chatForm = document.querySelector('#chatform');
const chatRoom = document.querySelector('#chatroom');

let username = '';

loginForm.onsubmit = (event) => {
    event.preventDefault();
    username = loginForm.querySelector('#username').value;
    socket.connect();

    socket.on('connect', () => { socket.emit('user_joined', username); });
}

chatForm.onsubmit = (event) => {
    event.preventDefault();
    const message = chatForm.querySelector('#message');
    socket.emit('new_message', message.value);
    message.value = '';
}

socket.on('user_joined', (data) => {
    if (data.username === username) {
        loginForm.style.display = 'none';
        chatForm.style.display = 'flex';
        chatRoom.style.display = 'flex';
    } else {
        const message = document.createElement('p');
        message.innerHTML = `<span class="server">Server</span>: ${data.username} joined`;
        chatRoom.appendChild(message);
    }
});

socket.on('chat_message', (data) => {
    const message = document.createElement('p');
    message.innerHTML = `<span class="username">${data.username}</span>: ${data.message}`;
    chatRoom.appendChild(message);

    chatRoom.scrollTop = chatRoom.scrollHeight;
});
