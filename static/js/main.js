/**
 * Traffic Violation Detection App - Main JavaScript
 * Handles file uploads, form interactions, and UI enhancements
 */

// Global variables
let uploadProgress = null;
let isProcessing = false;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    addAnimations();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('🚦 Traffic Violation Detection App Initialized');
    
    // Check if we're on the home page
    if (document.getElementById('uploadForm')) {
        setupFileUpload();
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add loading states
    addLoadingStates();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // File input change handler
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelection);
    }
    
    // Form submission handler
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmission);
    }
    
    // Window resize handler
    window.addEventListener('resize', handleWindowResize);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

/**
 * Setup file upload functionality
 */
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.querySelector('.card-body');
    
    if (!fileInput || !uploadArea) return;
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection();
        }
    });
}

/**
 * Handle file selection
 */
function handleFileSelection() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    // Validate file
    if (!validateFile(file)) {
        showAlert('Invalid file type or size. Please select a valid image or video file.', 'danger');
        fileInput.value = '';
        return;
    }
    
    // Show file info
    showFileInfo(file);
    
    // Enable upload button
    const uploadBtn = document.getElementById('uploadBtn');
    if (uploadBtn) {
        uploadBtn.disabled = false;
        uploadBtn.classList.remove('btn-secondary');
        uploadBtn.classList.add('btn-primary');
    }
}

/**
 * Validate uploaded file
 */
function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'video/mp4', 'video/avi', 'video/mov', 'video/mkv'];
    const maxSize = 100 * 1024 * 1024; // 100MB
    
    if (!allowedTypes.includes(file.type)) {
        return false;
    }
    
    if (file.size > maxSize) {
        return false;
    }
    
    return true;
}

/**
 * Show file information
 */
function showFileInfo(file) {
    const fileSize = formatFileSize(file.size);
    const fileType = file.type.startsWith('image/') ? 'Image' : 'Video';
    
    // Create or update file info display
    let fileInfo = document.getElementById('fileInfo');
    if (!fileInfo) {
        fileInfo = document.createElement('div');
        fileInfo.id = 'fileInfo';
        fileInfo.className = 'alert alert-info mt-3';
        document.getElementById('fileInput').parentNode.appendChild(fileInfo);
    }
    
    fileInfo.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-file-earmark me-2"></i>
            <div>
                <strong>${file.name}</strong>
                <div class="small text-muted">${fileType} • ${fileSize}</div>
            </div>
        </div>
    `;
}

/**
 * Handle form submission
 */
async function handleFormSubmission(e) {
    e.preventDefault();
    
    if (isProcessing) return;
    
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const processingStatus = document.getElementById('processingStatus');
    const resultsSection = document.getElementById('resultsSection');
    
    if (!fileInput.files[0]) {
        showAlert('Please select a file to upload', 'warning');
        return;
    }
    
    formData.append('file', fileInput.files[0]);
    
    // Set processing state
    isProcessing = true;
    processingStatus.style.display = 'block';
    resultsSection.style.display = 'none';
    
    if (uploadBtn) {
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Processing...';
    }
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.results, result.filename);
            showAlert('File processed successfully!', 'success');
        } else {
            showAlert('Error: ' + result.error, 'danger');
        }
    } catch (error) {
        showAlert('Upload failed: ' + error.message, 'danger');
    } finally {
        // Reset processing state
        isProcessing = false;
        processingStatus.style.display = 'none';
        
        if (uploadBtn) {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = '<i class="bi bi-upload me-2"></i>Upload and Analyze';
        }
    }
}

/**
 * Display detection results
 */
function displayResults(results, filename) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    if (!resultsSection || !resultsContent) return;
    
    if (results.length === 0) {
        resultsContent.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-check-circle text-success fs-1"></i>
                <h5 class="mt-3">No Violations Detected</h5>
                <p class="text-muted">Great! No traffic violations were found in the uploaded file.</p>
            </div>
        `;
    } else {
        let html = '<div class="row">';
        
        results.forEach((result, index) => {
            html += `
                <div class="col-md-6 col-lg-4 mb-3">
                    <div class="card border-0 shadow-sm fade-in">
                        <div class="card-body">
                            <h6 class="card-title text-capitalize">
                                ${result.violation_type.replace('_', ' ')}
                            </h6>
                            <p class="card-text">
                                <span class="badge bg-primary">Confidence: ${(result.confidence * 100).toFixed(1)}%</span>
                            </p>
                            ${result.result_image ? `
                                <img src="/static/results/${result.result_image}" 
                                     class="img-fluid rounded" 
                                     alt="Detection result"
                                     style="max-height: 200px; object-fit: cover;">
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        html += `
            <div class="text-center mt-3">
                <a href="/results/${filename}" class="btn btn-primary">
                    <i class="bi bi-eye me-2"></i>View Detailed Results
                </a>
            </div>
        `;
        
        resultsContent.innerHTML = html;
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

/**
 * Create alert container
 */
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add loading states
 */
function addLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit' && !this.disabled) {
                this.classList.add('loading');
            }
        });
    });
}

/**
 * Add animations
 */
function addAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
}

/**
 * Handle window resize
 */
function handleWindowResize() {
    // Update any responsive elements
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (window.innerWidth < 768) {
            card.classList.add('mobile-optimized');
        } else {
            card.classList.remove('mobile-optimized');
        }
    });
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(e) {
    // Ctrl/Cmd + U for upload
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.click();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
}

/**
 * Utility function to debounce events
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility function to throttle events
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global access
window.TrafficViolationApp = {
    showAlert,
    displayResults,
    formatFileSize
};

