const messages = document.querySelector('.messages');
const chatRoom = document.querySelector('.chatroom');
const chatForm = document.querySelector('#chatform');
const message = chatForm.querySelector('#message');


function makeMessage(data) {
    const message = document.createElement('div');
    message.classList.add('message');
    message.dataset.id = data.id;

    const info = document.createElement('span');
    info.innerText = data.username + ' | ' + data.created_at;
    info.classList.add('info');

    let content;
    if (data.type === 'text') {
        content = document.createElement('p');
        content.innerText = data.content;
        content.classList.add('content');
    } else if (data.type === 'image') {
        content = document.createElement('img');
        content.src = "/static/uploads/" + data.content;
        content.classList.add('content');
    } else {
        content = document.createElement('p');
        content.innerText = 'Could not load message content';
        content.classList.add('content');
    }

    message.append(info);
    message.append(content);

    return message;
}


function getMessages() {
    messages.innerHTML = '';

    fetch('/message')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let message = makeMessage(data[i]);
            messages.prepend(message);
        }
    })
    .catch(error => { console.error('Error:', error) });
}

getMessages();

chatForm.onsubmit = (event) => {
    event.preventDefault();

    if (message.value || document.querySelector('#file').files[0]) {
        const form = new FormData();
        form.append('message', message.value);
        form.append('file', document.querySelector('#file').files[0]);

        fetch('/message', {
            method: 'POST',
            body: form
        })
        .catch(error => { console.error('Error:', error) });

        message.value = '';
        document.querySelector('#file').value = '';
    }
}


socket.on('new_message', (data) => {
    let message = makeMessage(data);
    messages.append(message);
    chatRoom.scrollTop = chatRoom.scrollHeight;
});
