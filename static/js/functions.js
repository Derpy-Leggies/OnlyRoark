function makeMessage(data) {
    let content;

    const message = document.createElement('div');
    message.classList.add('message');
    message.dataset.id = data.message.id;

    const info = document.createElement('div');
    info.classList.add('info');

    const username = document.createElement('span');
    username.innerText = data.message.username;
    info.prepend(username);

    const timestamp = document.createElement('span');
    timestamp.innerText = data.message.created_at;
    info.append(timestamp);

    const attachments = document.createElement('div');
    attachments.classList.add('attachments');

    if (data['attachment']) {
        for (let i = 0; i < data['attachment'].length; i++) {
            let attachment = data['attachment'][i];

            const img = document.createElement('img');
            img.src = `/uploads/${attachment['file_name']}?r=thumbnail`;
            img.onload = () => { img.classList.add('loaded') }
            img.classList.add('content');

            attachments.append(img);
        }
    }

    content = document.createElement('p');
    content.innerText = data.message.message;
    content.classList.add('content');

    message.append(info);
    message.append(content);
    message.append(attachments);

    return message;
}


function getMessages(offset) {
    fetch(`/message?offset=${offset}`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                let message = makeMessage(data[i]);
                messages.prepend(message);
            }
        })
        .catch(error => { console.error('Error:', error) });
}
