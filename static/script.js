async function encryptMessage() {
    const message = document.getElementById('message').value;
    const phoneNumber = document.getElementById('phone_number').value;

    const response = await fetch('/encrypted_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message, phone_number: phoneNumber })
    });

    const result = await response.json();
    document.getElementById('encrypted-message').textContent = result.encrypted_message;
}

async function decryptMessage() {
    const encryptedMessage = document.getElementById('encrypted_message').value;
    const key = document.getElementById('key').value;

    const response = await fetch('/decrypted_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ encrypted_message: encryptedMessage, key })
    });

    const result = await response.json();
    document.getElementById('decrypted-message').textContent = result.message;
}
