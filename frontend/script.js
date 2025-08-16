const form = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const fileDropArea = document.getElementById('file-drop-area');
const fileNameDisplay = document.getElementById('file-name');
const loader = document.getElementById('loader');
const resultContainer = document.getElementById('result-container');

// --- Drag and Drop Logic ---
fileDropArea.addEventListener('click', () => fileInput.click());

fileDropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    fileDropArea.classList.add('drag-over');
});

fileDropArea.addEventListener('dragleave', () => {
    fileDropArea.classList.remove('drag-over');
});

fileDropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    fileDropArea.classList.remove('drag-over');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        fileNameDisplay.textContent = files[0].name;
    }
});

fileInput.addEventListener('change', () => {
     if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    }
});

// --- Form Submission Logic ---
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    const fileFormat = form.elements['file_format'].value;

    if (!file) {
        alert("Please select a file first!");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_format', fileFormat);

    loader.style.display = 'block';
    resultContainer.innerHTML = '';

    try {
        const response = await fetch('/extract_from_doc', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Server responded with status: ${response.status}`);
        }
        
        if (data.error) {
             throw new Error(data.error);
        }

        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        displayError(error.message);
    } finally {
        loader.style.display = 'none';
    }
});

function displayResults(data) {
    let tableHTML = '<table class="result-table"><tbody>';
    
    for (const [key, value] of Object.entries(data)) {
        const cleanKey = key.replace(/_/g, ' ');
        const cleanValue = value ? String(value).replace(/</g, "&lt;").replace(/>/g, "&gt;") : "Not Found";
        
        tableHTML += `
            <tr>
                <th>${cleanKey}</th>
                <td><pre style="white-space: pre-wrap; margin: 0; font-family: inherit;">${cleanValue}</pre></td>
            </tr>
        `;
    }
    
    tableHTML += '</tbody></table>';
    resultContainer.innerHTML = tableHTML;
}

function displayError(errorMessage) {
    resultContainer.innerHTML = `<div class="error-message"><strong>Error:</strong> ${errorMessage}</div>`;
}