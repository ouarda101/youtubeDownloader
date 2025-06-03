const videoUrlInput = document.getElementById('videoUrl');
const downloadButton = document.getElementById('downloadBtn');
const messageDisplay = document.getElementById('messageDisplay');
const loadingSpinner = document.getElementById('loadingSpinner');


function showMessage(msg, type) {
    messageDisplay.textContent = msg;
    messageDisplay.className = `message ${type}`; 
    messageDisplay.classList.remove('hidden');
}


function hideMessage() {
    messageDisplay.classList.add('hidden');
    messageDisplay.textContent = '';
}


downloadButton.addEventListener('click', async () => {
    const url = videoUrlInput.value.trim();

    if (!url) {
        showMessage('Please enter a YouTube video URL.', 'error');
        return;
    }

    hideMessage(); 
    loadingSpinner.style.display = 'block';  
    downloadButton.disabled = true; 

    try {
        
        const response = await fetch('http://127.0.0.1:5000/download', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json(); 

        if (response.ok) { 
            showMessage(data.message, 'success');
        } else {
            showMessage(`Error: ${data.error || 'Something went wrong on the server.'}`, 'error');
        }
    } catch (error) {
        console.error('Fetch error:', error);
        showMessage('Could not connect to the server. Is it running?', 'error');
    } finally {
        loadingSpinner.style.display = 'none'; 
        downloadButton.disabled = false; 
    }
});