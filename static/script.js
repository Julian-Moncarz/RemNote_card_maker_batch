// Global variables
let selectedFiles = [];
let isProcessing = false;
let defaultPrompt = '';

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const selectedFilesSection = document.getElementById('selectedFiles');
const fileList = document.getElementById('fileList');
const processBtn = document.getElementById('processBtn');
const clearBtn = document.getElementById('clearBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const flashcardsEditor = document.getElementById('flashcardsEditor');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newBatchBtn = document.getElementById('newBatchBtn');
const selectAllBtn = document.getElementById('selectAllBtn');
const fileCount = document.getElementById('fileCount');
const toastContainer = document.getElementById('toastContainer');

// Advanced settings elements
const advancedToggle = document.getElementById('advancedToggle');
const advancedContent = document.getElementById('advancedContent');
const toggleIcon = document.getElementById('toggleIcon');
const promptEditor = document.getElementById('promptEditor');
const resetPromptBtn = document.getElementById('resetPromptBtn');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Store the default prompt
    defaultPrompt = promptEditor.value;
    
    initializeEventListeners();
    updateUI();
    
    console.log('🚀 FlashCard Generator initialized');
    console.log('📝 Default prompt loaded:', defaultPrompt.substring(0, 100) + '...');
});

function initializeEventListeners() {
    console.log('🔧 Setting up event listeners');
    
    // File input events
    fileInput.addEventListener('change', handleFileSelect);
    browseBtn.addEventListener('click', () => fileInput.click());
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Button events
    processBtn.addEventListener('click', processFiles);
    clearBtn.addEventListener('click', clearFiles);
    copyBtn.addEventListener('click', copyToClipboard);
    downloadBtn.addEventListener('click', downloadFlashcards);
    newBatchBtn.addEventListener('click', startNewBatch);
    selectAllBtn.addEventListener('click', selectAllText);
    
    // Advanced settings events
    advancedToggle.addEventListener('click', toggleAdvancedSettings);
    resetPromptBtn.addEventListener('click', resetPromptToDefault);
    
    // Prompt editor events
    promptEditor.addEventListener('input', function() {
        console.log('📝 Prompt modified by user');
    });
    
    // Prevent default drag behaviors on the document
    document.addEventListener('dragover', e => e.preventDefault());
    document.addEventListener('drop', e => e.preventDefault());
    
    console.log('✅ Event listeners set up successfully');
}

// File handling functions
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    console.log(`📁 File input selected: ${files.length} files`);
    addFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    console.log(`🎯 Files dropped: ${files.length} files`);
    addFiles(files);
}

function addFiles(files) {
    console.log(`📄 Adding ${files.length} files to selection`);
    
    const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png'];
    const validFiles = files.filter(file => {
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        const isValid = allowedExtensions.includes(extension);
        if (!isValid) {
            console.warn(`❌ Invalid file rejected: ${file.name} (${file.type})`);
            showToast('Invalid file', `${file.name} is not a supported file type.`, 'error');
        } else {
            console.log(`✅ Valid file accepted: ${file.name} (${formatFileSize(file.size)})`);
        }
        return isValid;
    });
    
    // Avoid duplicates
    const newFiles = validFiles.filter(file => 
        !selectedFiles.some(existing => existing.name === file.name && existing.size === file.size)
    );
    
    if (newFiles.length < validFiles.length) {
        const duplicates = validFiles.length - newFiles.length;
        console.log(`🔄 Skipped ${duplicates} duplicate files`);
        showToast('Duplicates skipped', `${duplicates} duplicate files were skipped.`, 'info');
    }
    
    selectedFiles.push(...newFiles);
    console.log(`📊 Total files selected: ${selectedFiles.length}`);
    updateUI();
}

function removeFile(index) {
    const removedFile = selectedFiles[index];
    selectedFiles.splice(index, 1);
    console.log(`🗑️ Removed file: ${removedFile.name}`);
    updateUI();
}

function clearFiles() {
    const fileCount = selectedFiles.length;
    selectedFiles = [];
    console.log(`🧹 Cleared ${fileCount} files`);
    updateUI();
}

// UI update functions
function updateUI() {
    const hasFiles = selectedFiles.length > 0;
    
    // Toggle sections
    selectedFilesSection.style.display = hasFiles ? 'block' : 'none';
    uploadArea.style.display = hasFiles ? 'none' : 'block';
    
    // Update buttons
    processBtn.disabled = !hasFiles || isProcessing;
    clearBtn.disabled = !hasFiles || isProcessing;
    
    // Update file list
    renderFileList();
    
    console.log(`🔄 UI updated: ${selectedFiles.length} files, processing: ${isProcessing}`);
}

function renderFileList() {
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        
        const fileIcon = document.createElement('i');
        fileIcon.className = getFileIcon(file.name);
        
        const fileName = document.createElement('span');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('span');
        fileSize.className = 'file-size';
        fileSize.textContent = formatFileSize(file.size);
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-file';
        removeBtn.innerHTML = '<i class="fas fa-times"></i>';
        removeBtn.onclick = () => removeFile(index);
        
        fileInfo.appendChild(fileIcon);
        fileInfo.appendChild(fileName);
        fileInfo.appendChild(fileSize);
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeBtn);
        fileList.appendChild(fileItem);
    });
}

function getFileIcon(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    switch (extension) {
        case 'pdf':
            return 'fas fa-file-pdf file-icon';
        case 'jpg':
        case 'jpeg':
        case 'png':
            return 'fas fa-file-image file-icon';
        default:
            return 'fas fa-file file-icon';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Processing functions
async function processFiles() {
    if (selectedFiles.length === 0 || isProcessing) return;
    
    console.log('🚀 Starting file processing...');
    console.log(`📁 Files to process: ${selectedFiles.length}`);
    console.log(`📝 Using custom prompt: ${promptEditor.value !== defaultPrompt ? 'Yes' : 'No'}`);
    
    isProcessing = true;
    showProgress();
    
    const formData = new FormData();
    selectedFiles.forEach((file, index) => {
        formData.append('files', file);
        console.log(`📄 Added file ${index + 1}: ${file.name} (${formatFileSize(file.size)})`);
    });
    
    // Add the custom prompt to the form data
    const currentPrompt = promptEditor.value.trim();
    if (currentPrompt && currentPrompt !== defaultPrompt) {
        formData.append('prompt', currentPrompt);
        console.log('📝 Custom prompt included in request');
    } else {
        console.log('📝 Using default prompt');
    }
    
    try {
        updateProgress(10, 'Uploading files...');
        console.log('📤 Uploading files to server...');
        
        const response = await fetch('/process_files', {
            method: 'POST',
            body: formData
        });
        
        console.log(`📡 Server response status: ${response.status}`);
        
        updateProgress(50, 'Processing with AI...');
        console.log('🤖 Server processing files with AI...');
        
        const result = await response.json();
        console.log('📥 Received response from server:', {
            success: result.success,
            processed_files: result.processed_files,
            total_files: result.total_files
        });
        
        if (result.success) {
            updateProgress(100, 'Complete!');
            console.log('✅ Processing completed successfully!');
            setTimeout(() => {
                showResults(result);
            }, 500);
        } else {
            throw new Error(result.error || 'Processing failed');
        }
        
    } catch (error) {
        console.error('❌ Error processing files:', error);
        console.error('🔍 Error details:', {
            message: error.message,
            stack: error.stack
        });
        hideProgress();
        showToast('Processing failed', error.message, 'error');
    } finally {
        isProcessing = false;
        updateUI();
        console.log('🏁 File processing session ended');
    }
}

function showProgress() {
    console.log('⏳ Showing progress section');
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    selectedFilesSection.style.display = 'none';
}

function updateProgress(percentage, message) {
    progressFill.style.width = percentage + '%';
    progressText.textContent = message;
    console.log(`📊 Progress: ${percentage}% - ${message}`);
}

function hideProgress() {
    console.log('❌ Hiding progress section');
    progressSection.style.display = 'none';
    selectedFilesSection.style.display = selectedFiles.length > 0 ? 'block' : 'none';
    uploadArea.style.display = selectedFiles.length === 0 ? 'block' : 'none';
}

function showResults(result) {
    console.log('📋 Displaying results to user');
    console.log(`📊 Results summary: ${result.processed_files}/${result.total_files} files processed`);
    
    progressSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    flashcardsEditor.value = result.flashcards;
    fileCount.textContent = `${result.processed_files} of ${result.total_files} files processed`;
    
    console.log(`📝 Flashcards length: ${result.flashcards.length} characters`);
    showToast('Success!', result.message, 'success');
}

// Results functions
function copyToClipboard() {
    flashcardsEditor.select();
    document.execCommand('copy');
    console.log('📋 Flashcards copied to clipboard');
    showToast('Copied!', 'Flashcards copied to clipboard.', 'success');
}

function downloadFlashcards() {
    const blob = new Blob([flashcardsEditor.value], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flashcards.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log('💾 Flashcards downloaded as file');
    showToast('Downloaded!', 'Flashcards saved to downloads.', 'success');
}

function selectAllText() {
    flashcardsEditor.select();
    flashcardsEditor.setSelectionRange(0, 99999); // For mobile devices
    console.log('📝 All text selected in editor');
}

function startNewBatch() {
    console.log('🔄 Starting new batch - clearing all data');
    clearFiles();
    resultsSection.style.display = 'none';
    progressSection.style.display = 'none';
    flashcardsEditor.value = '';
    fileCount.textContent = '';
    updateUI();
    console.log('✨ New batch started - UI reset');
}

// Advanced settings functions
function toggleAdvancedSettings() {
    const isExpanded = advancedContent.classList.contains('expanded');
    
    if (isExpanded) {
        advancedContent.classList.remove('expanded');
        toggleIcon.classList.remove('rotated');
        console.log('🔽 Advanced settings collapsed');
    } else {
        advancedContent.classList.add('expanded');
        toggleIcon.classList.add('rotated');
        console.log('🔼 Advanced settings expanded');
    }
}

function resetPromptToDefault() {
    promptEditor.value = defaultPrompt;
    showToast('Prompt reset', 'AI prompt has been reset to default.', 'success');
    console.log('🔄 Prompt reset to default');
}

// Toast notification system
function showToast(title, message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = getToastIcon(type);
    
    toast.innerHTML = `
        <i class="${icon}"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => {
                toastContainer.removeChild(toast);
            }, 300);
        }
    }, 5000);
}

function getToastIcon(type) {
    switch (type) {
        case 'success':
            return 'fas fa-check-circle';
        case 'error':
            return 'fas fa-exclamation-circle';
        case 'warning':
            return 'fas fa-exclamation-triangle';
        default:
            return 'fas fa-info-circle';
    }
}
