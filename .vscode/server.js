const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const vonage = require('@vonage/server-sdk');

const app = express();
app.use(bodyParser.json());

const VONAGE_API_KEY = 'e5aee254';
const VONAGE_API_SECRET = 'B8G1rsKCtQSkwq42';

const nexmo = new vonage({
    apiKey: VONAGE_API_KEY,
    apiSecret: VONAGE_API_SECRET,
});

app.post('/send-sms', (req, res) => {
    const { message, phoneNumber } = req.body;

    exec(`python3 encryption.py encrypt "${message}"`, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }

        const encryptedMessage = stdout.trim();
        nexmo.message.sendSms('+254799868379', phoneNumber, encryptedMessage, (err, responseData) => {
            if (err) {
                res.status(500).json({ error: err });
            } else {
                if (responseData.messages[0]['status'] === "0") {
                    res.status(200).json({ message: 'Message sent successfully.' });
                } else {
                    res.status(500).json({ error: responseData.messages[0]['error-text'] });
                }
            }
        });
    });
});

app.post('/decrypt-message', (req, res) => {
    const { encryptedMessage, key } = req.body;

    exec(`python3 encryption.py decrypt "${encryptedMessage}" "${key}"`, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }

        const message = stdout.trim();
        res.status(200).json({ message });
    });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
