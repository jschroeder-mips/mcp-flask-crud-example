/**
 * 🚀 FUTURAMA QUOTES API - CLIENT-SIDE JAVASCRIPT
 * Year 3000 Interactive Experience
 * 
 * Built with vanilla JavaScript and modern ES6+ features
 * Good news everyone! This code is from the future!
 */

// === GLOBAL STATE ===
const FuturamaApp = {
    quotes: [],
    currentQuote: null,
    isLoading: false,
    apiBaseUrl: '/api/quotes'
};

// === DOM ELEMENTS ===
const elements = {
    quoteCount: document.getElementById('quote-count'),
    characterCount: document.getElementById('character-count'),
    episodeCount: document.getElementById('episode-count'),
    toastContainer: document.getElementById('toast-container'),
    navbarBurger: document.querySelector('.navbar-burger'),
    navbarMenu: document.querySelector('.navbar-menu')
};

// === UTILITY FUNCTIONS ===

/**
 * Show a toast notification with Futurama styling
 * @param {string} message - The message to display
 * @param {string} type - success, error, warning, or info
 * @param {number} duration - How long to show the toast (ms)
 */
function showToast(message, type = 'info', duration = 4000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type} fade-in`;
    
    const icon = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    }[type];
    
    toast.innerHTML = `
        <div class="is-flex is-align-items-center">
            <span class="icon mr-2">
                <i class="${icon}"></i>
            </span>
            <span>${message}</span>
        </div>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    // Auto-remove toast
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            if (toast.parentNode) {
                elements.toastContainer.removeChild(toast);
            }
        }, 300);
    }, duration);
}

/**
 * Show loading overlay
 */
function showLoading() {
    if (document.querySelector('.loading-overlay')) return;
    
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="has-text-centered">
            <div class="loading-spinner mb-4"></div>
            <p class="has-text-white futurama-title">
                Loading quotes from the year 3000...
            </p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    FuturamaApp.isLoading = true;
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.remove();
    }
    FuturamaApp.isLoading = false;
}

/**
 * Format date to readable string
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Sanitize HTML to prevent XSS
 * @param {string} str - String to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeHtml(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

// === API FUNCTIONS ===

/**
 * Make API request with error handling
 * @param {string} url - API endpoint
 * @param {object} options - Request options
 * @returns {Promise} Response data
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await axios({
            url,
            method: options.method || 'GET',
            data: options.data,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        
        if (error.response) {
            // Server responded with error
            const errorMsg = error.response.data?.error || error.response.data?.message || 'Server error occurred';
            throw new Error(errorMsg);
        } else if (error.request) {
            // Network error
            throw new Error('Network error - please check your connection');
        } else {
            // Other error
            throw new Error('An unexpected error occurred');
        }
    }
}

/**
 * Fetch all quotes from API
 */
async function fetchQuotes() {
    try {
        showLoading();
        const data = await apiRequest(FuturamaApp.apiBaseUrl);
        
        FuturamaApp.quotes = data.quotes || [];
        updateDashboardStats();
        renderQuotes();
        
        showToast(`Loaded ${FuturamaApp.quotes.length} quotes from the future! 🚀`, 'success');
    } catch (error) {
        showToast(`Error loading quotes: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Create a new quote
 * @param {object} quoteData - Quote information
 */
async function createQuote(quoteData) {
    try {
        showLoading();
        const data = await apiRequest(FuturamaApp.apiBaseUrl, {
            method: 'POST',
            data: quoteData
        });
        
        FuturamaApp.quotes.push(data.quote);
        updateDashboardStats();
        renderQuotes();
        
        showToast(`Quote by ${data.quote.character} added successfully! ✨`, 'success');
        closeModal('add-quote-modal');
        document.getElementById('add-quote-form').reset();
    } catch (error) {
        showToast(`Error creating quote: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Update an existing quote
 * @param {number} quoteId - Quote ID
 * @param {object} quoteData - Updated quote information
 */
async function updateQuote(quoteId, quoteData) {
    try {
        showLoading();
        const data = await apiRequest(`${FuturamaApp.apiBaseUrl}/${quoteId}`, {
            method: 'PUT',
            data: quoteData
        });
        
        const index = FuturamaApp.quotes.findIndex(q => q.id === quoteId);
        if (index !== -1) {
            FuturamaApp.quotes[index] = data.quote;
        }
        
        renderQuotes();
        showToast(`Quote updated successfully! ✏️`, 'success');
        closeModal('edit-quote-modal');
    } catch (error) {
        showToast(`Error updating quote: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Delete a quote
 * @param {number} quoteId - Quote ID to delete
 */
async function deleteQuote(quoteId) {
    if (!confirm('Are you sure you want to delete this quote? Even Bender would think twice!')) {
        return;
    }
    
    try {
        showLoading();
        await apiRequest(`${FuturamaApp.apiBaseUrl}/${quoteId}`, {
            method: 'DELETE'
        });
        
        FuturamaApp.quotes = FuturamaApp.quotes.filter(q => q.id !== quoteId);
        updateDashboardStats();
        renderQuotes();
        
        showToast('Quote deleted successfully! 🗑️', 'success');
    } catch (error) {
        showToast(`Error deleting quote: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// === UI FUNCTIONS ===

/**
 * Update dashboard statistics
 */
function updateDashboardStats() {
    const uniqueCharacters = new Set(FuturamaApp.quotes.map(q => q.character)).size;
    const uniqueEpisodes = new Set(FuturamaApp.quotes.map(q => q.episode)).size;
    
    if (elements.quoteCount) elements.quoteCount.textContent = FuturamaApp.quotes.length;
    if (elements.characterCount) elements.characterCount.textContent = uniqueCharacters;
    if (elements.episodeCount) elements.episodeCount.textContent = uniqueEpisodes;
}

/**
 * Render quotes in the UI
 */
function renderQuotes() {
    const container = document.getElementById('quotes-container');
    if (!container) return;
    
    if (FuturamaApp.quotes.length === 0) {
        container.innerHTML = `
            <div class="has-text-centered py-6">
                <i class="fas fa-robot fa-3x futurama-orange mb-4"></i>
                <h3 class="title is-4 has-text-white">No quotes found!</h3>
                <p class="has-text-light">Looks like even Bender is speechless. Add some quotes to get started!</p>
                <button class="button is-primary mt-4" onclick="showAddQuoteModal()">
                    <span class="icon"><i class="fas fa-plus"></i></span>
                    <span>Add Your First Quote</span>
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = FuturamaApp.quotes.map(quote => `
        <div class="column is-12-mobile is-6-tablet is-4-desktop">
            <div class="quote-card p-5 fade-in">
                <div class="quote-text mb-4">
                    "${sanitizeHtml(quote.text)}"
                </div>
                
                <div class="quote-character mb-2">
                    <i class="fas fa-user-robot mr-2"></i>
                    ${sanitizeHtml(quote.character)}
                </div>
                
                <div class="quote-meta">
                    <div class="is-flex is-justify-content-space-between is-align-items-center mb-3">
                        <div>
                            <small>
                                <i class="fas fa-tv mr-1"></i>
                                ${sanitizeHtml(quote.episode)}
                                ${quote.season ? `(Season ${quote.season})` : ''}
                            </small>
                            ${quote.year ? `<br><small><i class="fas fa-calendar mr-1"></i>${quote.year}</small>` : ''}
                        </div>
                    </div>
                    
                    <div class="buttons is-centered">
                        <button class="button is-small is-warning" onclick="editQuote(${quote.id})">
                            <span class="icon"><i class="fas fa-edit"></i></span>
                            <span>Edit</span>
                        </button>
                        <button class="button is-small is-danger" onclick="deleteQuote(${quote.id})">
                            <span class="icon"><i class="fas fa-trash"></i></span>
                            <span>Delete</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Show modal
 * @param {string} modalId - Modal ID to show
 */
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('is-active');
    }
}

/**
 * Close modal
 * @param {string} modalId - Modal ID to close
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('is-active');
    }
}

/**
 * Show add quote modal
 */
function showAddQuoteModal() {
    showModal('add-quote-modal');
    document.getElementById('quote-text-input').focus();
}

/**
 * Show edit quote modal with quote data
 * @param {number} quoteId - Quote ID to edit
 */
function editQuote(quoteId) {
    const quote = FuturamaApp.quotes.find(q => q.id === quoteId);
    if (!quote) return;
    
    FuturamaApp.currentQuote = quote;
    
    // Populate edit form
    document.getElementById('edit-quote-text').value = quote.text;
    document.getElementById('edit-quote-character').value = quote.character;
    document.getElementById('edit-quote-episode').value = quote.episode;
    document.getElementById('edit-quote-season').value = quote.season || '';
    document.getElementById('edit-quote-year').value = quote.year || '';
    
    showModal('edit-quote-modal');
    document.getElementById('edit-quote-text').focus();
}

// === EVENT HANDLERS ===

/**
 * Handle add quote form submission
 */
function handleAddQuoteSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const quoteData = {
        text: formData.get('text').trim(),
        character: formData.get('character').trim(),
        episode: formData.get('episode').trim(),
        season: formData.get('season') ? parseInt(formData.get('season')) : null,
        year: formData.get('year') ? parseInt(formData.get('year')) : null
    };
    
    // Validation
    if (!quoteData.text || !quoteData.character || !quoteData.episode) {
        showToast('Please fill in all required fields! 📋', 'warning');
        return;
    }
    
    createQuote(quoteData);
}

/**
 * Handle edit quote form submission
 */
function handleEditQuoteSubmit(event) {
    event.preventDefault();
    
    if (!FuturamaApp.currentQuote) return;
    
    const formData = new FormData(event.target);
    const quoteData = {
        text: formData.get('text').trim(),
        character: formData.get('character').trim(),
        episode: formData.get('episode').trim(),
        season: formData.get('season') ? parseInt(formData.get('season')) : null,
        year: formData.get('year') ? parseInt(formData.get('year')) : null
    };
    
    // Validation
    if (!quoteData.text || !quoteData.character || !quoteData.episode) {
        showToast('Please fill in all required fields! 📋', 'warning');
        return;
    }
    
    updateQuote(FuturamaApp.currentQuote.id, quoteData);
}

// === INITIALIZATION ===

/**
 * Initialize the application
 */
function initApp() {
    console.log('🚀 Initializing Futurama Quotes App - Year 3000!');
    
    // Mobile menu toggle
    if (elements.navbarBurger && elements.navbarMenu) {
        elements.navbarBurger.addEventListener('click', () => {
            elements.navbarBurger.classList.toggle('is-active');
            elements.navbarMenu.classList.toggle('is-active');
        });
    }
    
    // Close modals when clicking background
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal-background')) {
            const modal = event.target.closest('.modal');
            if (modal) {
                modal.classList.remove('is-active');
            }
        }
    });
    
    // Close modals with escape key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            const activeModal = document.querySelector('.modal.is-active');
            if (activeModal) {
                activeModal.classList.remove('is-active');
            }
        }
    });
    
    // Load quotes on page load
    fetchQuotes();
    
    showToast('Welcome to the year 3000! Good news everyone! 🤖', 'success');
}

// === GLOBAL FUNCTIONS (accessible from HTML) ===
window.showAddQuoteModal = showAddQuoteModal;
window.editQuote = editQuote;
window.deleteQuote = deleteQuote;
window.showModal = showModal;
window.closeModal = closeModal;
window.handleAddQuoteSubmit = handleAddQuoteSubmit;
window.handleEditQuoteSubmit = handleEditQuoteSubmit;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);
