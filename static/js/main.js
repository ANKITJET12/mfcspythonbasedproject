// CipherMesh Web Application JavaScript

let currentMode = 'encrypt';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Mode selector buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const mode = btn.dataset.mode;
            switchMode(mode);
        });
    });

    // Process button
    document.getElementById('process-btn').addEventListener('click', handleProcess);

    // Copy button
    document.getElementById('copy-btn').addEventListener('click', handleCopy);
}

function switchMode(mode) {
    currentMode = mode;
    
    // Update active button
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.mode === mode) {
            btn.classList.add('active');
        }
    });

    // Update labels and placeholders
    const inputLabel = document.getElementById('input-label');
    const textInput = document.getElementById('text-input');
    const processBtn = document.querySelector('.btn-text');

    if (mode === 'encrypt') {
        inputLabel.textContent = 'Enter Plaintext';
        textInput.placeholder = 'Enter your text to encrypt...';
        processBtn.textContent = 'Initiate Encryption';
    } else {
        inputLabel.textContent = 'Enter Ciphertext';
        textInput.placeholder = 'Enter your ciphertext to decrypt...';
        processBtn.textContent = 'Initiate Decryption';
    }

    // Clear previous results
    hideResults();
    textInput.value = '';
}

function handleProcess() {
    const textInput = document.getElementById('text-input');
    const text = textInput.value.trim();

    if (!text) {
        showError('Please enter some text to process.');
        return;
    }

    const processBtn = document.getElementById('process-btn');
    const btnText = processBtn.querySelector('.btn-text');
    const btnLoader = processBtn.querySelector('.btn-loader');
    
    // Show loading state
    processBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';

    hideResults();

    // Make API call
    const endpoint = currentMode === 'encrypt' ? '/api/encrypt' : '/api/decrypt';
    
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            [currentMode === 'encrypt' ? 'plaintext' : 'ciphertext']: text
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showResults(data);
        } else {
            showError(data.error || 'An error occurred during processing.');
        }
    })
    .catch(error => {
        showError('Network error: ' + error.message);
    })
    .finally(() => {
        // Hide loading state
        processBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    });
}

function showResults(data) {
    const resultSection = document.getElementById('result-section');
    const resultContent = document.getElementById('result-content');
    const detailsSection = document.getElementById('details-section');
    const detailsContent = document.getElementById('details-content');

    // Show result
    const resultKey = currentMode === 'encrypt' ? 'result' : 'result';
    resultContent.textContent = data[resultKey];
    resultSection.style.display = 'block';

    // Show details
    if (data.details && data.details.layers) {
        detailsContent.innerHTML = '';
        data.details.layers.forEach((layer, index) => {
            const layerBox = createLayerBox(layer, index);
            detailsContent.appendChild(layerBox);
        });
        detailsSection.style.display = 'block';
    }

    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function createLayerBox(layer, index) {
    const layerBox = document.createElement('div');
    layerBox.className = 'layer-box';

    const header = document.createElement('div');
    header.className = 'layer-header';
    header.innerHTML = `<span>${index + 1}.</span> ${layer.name}`;
    layerBox.appendChild(header);

    const info = document.createElement('div');
    info.className = 'layer-info';
    info.innerHTML = `
        <div><strong>Input:</strong> <code>${escapeHtml(layer.input)}</code></div>
        <div><strong>Output:</strong> <code class="output-text">${escapeHtml(layer.output)}</code></div>
        ${layer.formula ? `<div><strong>Formula:</strong> ${layer.formula}</div>` : ''}
    `;
    layerBox.appendChild(info);

    // Add steps for Layer 1 and Layer 2
    if (layer.steps && layer.steps.length > 0) {
        const stepsContainer = document.createElement('div');
        stepsContainer.className = 'layer-steps';
        
        // Limit display to first 50 steps to prevent overwhelming UI
        const displaySteps = layer.steps.slice(0, 50);
        displaySteps.forEach(step => {
            const stepItem = createStepItem(step, layer.name);
            stepsContainer.appendChild(stepItem);
        });
        
        if (layer.steps.length > 50) {
            const moreInfo = document.createElement('div');
            moreInfo.style.color = 'var(--text-gray)';
            moreInfo.style.fontSize = '0.85rem';
            moreInfo.style.marginTop = '0.5rem';
            moreInfo.textContent = `... and ${layer.steps.length - 50} more steps`;
            stepsContainer.appendChild(moreInfo);
        }
        
        layerBox.appendChild(stepsContainer);
    }

    // Add blocks for Layer 3
    if (layer.blocks && layer.blocks.length > 0) {
        const blocksContainer = document.createElement('div');
        blocksContainer.style.marginTop = '1rem';
        blocksContainer.style.display = 'flex';
        blocksContainer.style.flexWrap = 'wrap';
        blocksContainer.style.gap = '0.5rem';
        
        layer.blocks.forEach(block => {
            const blockItem = document.createElement('div');
            blockItem.className = 'block-item';
            blockItem.innerHTML = `
                <span class="block-original">${escapeHtml(block.original)}</span>
                <span class="block-arrow">→</span>
                <span class="block-transformed">${escapeHtml(block.transformed)}</span>
            `;
            blocksContainer.appendChild(blockItem);
        });
        
        layerBox.appendChild(blocksContainer);
    }

    return layerBox;
}

function createStepItem(step, layerName) {
    const stepItem = document.createElement('div');
    stepItem.className = 'step-item';

    if (layerName.includes('Layer 1')) {
        stepItem.innerHTML = `
            <strong>Input:</strong> '<span style="color: var(--text-white)">${escapeHtml(step.input)}</span>' 
            (${step.rule}) | 
            <strong>Shift:</strong> ${step.shift} | 
            <strong>Output:</strong> '<span style="color: var(--red-bright)">${escapeHtml(step.output)}</span>'
        `;
    } else if (layerName.includes('Layer 2')) {
        stepItem.innerHTML = `
            <strong>Input:</strong> '<span style="color: var(--text-white)">${escapeHtml(step.input)}</span>' 
            (ASCII: ${step.input_ascii}) | 
            <strong>Formula:</strong> ${step.formula} | 
            <strong>Output:</strong> '<span style="color: var(--red-bright)">${escapeHtml(step.output)}</span>' 
            (ASCII: ${step.output_ascii})
        `;
    }

    return stepItem;
}

function showError(message) {
    const resultSection = document.getElementById('result-section');
    const resultContent = document.getElementById('result-content');
    
    resultContent.innerHTML = `<div class="error-message">${escapeHtml(message)}</div>`;
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('details-section').style.display = 'none';
}

function handleCopy() {
    const resultContent = document.getElementById('result-content');
    const text = resultContent.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copy-btn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.color = 'var(--red-bright)';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.color = 'var(--red-primary)';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
