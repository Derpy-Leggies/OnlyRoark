const messages = document.querySelector('.messages');
const chatRoom = document.querySelector('main');
const chatForm = document.querySelector('#chatform');
const message = chatForm.querySelector('#message');

getMessages(scroll);

chatRoom.onscroll = () => {
    if (chatRoom.scrollTop === 0) {
        scroll += 50;
        getMessages(scroll);
        console.log(scroll);
    }
}

chatForm.onsubmit = (event) => {
    event.preventDefault();

    if (message.value || document.querySelector('#file').files[0]) {
        const form = new FormData();
        form.append('message', message.value);
        for(let i = 0; i < document.querySelector('#file').files.length; i++) {
            form.append('file[]', document.querySelector('#file').files[i]);
        }

        console.log(form);

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
