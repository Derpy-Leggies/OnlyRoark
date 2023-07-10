const chatRoom = document.querySelector('.messages');
const chatForm = document.querySelector('#chatform');
const message = chatForm.querySelector('#message');


function makeMessage(data) {
    const message = document.createElement('div');
    message.classList.add('message');
    message.dataset.id = data.id;

    const img = document.createElement('img');
    img.src = "/static/images/pfp.jpg";

    const info = document.createElement('span');
    info.innerText = data.username + ' | ' + data.created_at;

    const content = document.createElement('p');
    content.innerText = data.content;

    message.prepend(img);
    message.prepend(info);
    message.prepend(content);

    return message;
}


function getMessages() {
    chatRoom.innerHTML = '';

    fetch('/message')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            const message = makeMessage(data[i]);
            chatRoom.append(message);
            console.log(data[i]);
        }
    })
    .catch(error => { console.error('Error:', error) });
}
getMessages();


chatForm.onsubmit = (event) => {
    event.preventDefault();

    if (message.value) {
        const form = new FormData();
        form.append('message', message.value);

        fetch('/message', {
            method: 'POST',
            body: form
        })
        // .then(response => response.json())
        // .then(data => { console.log(data) })
        .catch(error => { console.error('Error:', error) });

        message.value = '';
    }
}


socket.on('new_message', (data) => {
    const message = makeMessage(data);
    chatRoom.prepend(message);
    chatRoom.scrollTop = chatRoom.innerHeight;
});
