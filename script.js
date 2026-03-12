// Text Summarizer JavaScript
// Modern, clean implementation inspired by Tender_frontend design

class TextSummarizer {
    constructor() {
        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.updateUI();
        this.setupScrollAnimation();
    }

    setupElements() {
        this.elements = {
            // Navigation
            navLinks: document.querySelectorAll('.nav-link'),
            navMenu: document.getElementById('navMenu'),
            hamburgerBtn: document.getElementById('hamburgerBtn'),
            header: document.querySelector('.header'),
            
            // Configuration
            summaryType: document.getElementById('summaryType'),
            
            // Input
            inputText: document.getElementById('inputText'),
            charCount: document.getElementById('charCount'),
            wordCount: document.getElementById('wordCount'),
            pasteBtn: document.getElementById('pasteBtn'),
            fileBtn: document.getElementById('fileBtn'),
            clearBtn: document.getElementById('clearBtn'),
            fileInput: document.getElementById('fileInput'),
            
            // Action
            summarizeBtn: document.getElementById('summarizeBtn'),
            processingIndicator: document.getElementById('processingIndicator'),
            
            // Output
            summaryOutput: document.getElementById('summaryOutput'),
            summaryStats: document.getElementById('summaryStats'),
            reductionRatio: document.getElementById('reductionRatio'),
            summaryWords: document.getElementById('summaryWords'),
            copyBtn: document.getElementById('copyBtn'),
            downloadBtn: document.getElementById('downloadBtn'),
            
            // Messages
            errorMessage: document.getElementById('errorMessage'),
        };
    }

    setupEventListeners() {
        // Navigation
        window.addEventListener('scroll', () => this.handleScroll());
        this.elements.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.handleNavClick(e);
                // Close menu on link click
                this.elements.navMenu.classList.remove('open');
                this.elements.hamburgerBtn.classList.remove('open');
            });
        });

        // Hamburger toggle
        this.elements.hamburgerBtn.addEventListener('click', () => {
            this.elements.navMenu.classList.toggle('open');
            this.elements.hamburgerBtn.classList.toggle('open');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.header')) {
                this.elements.navMenu.classList.remove('open');
                this.elements.hamburgerBtn.classList.remove('open');
            }
        });

        // Text input for stats
        this.elements.inputText.addEventListener('input', () => this.updateStats());
        
        // Buttons
        this.elements.summarizeBtn.addEventListener('click', () => this.summarizeText());
        this.elements.clearBtn.addEventListener('click', () => this.clearText());
        this.elements.pasteBtn.addEventListener('click', () => this.pasteFromClipboard());
        this.elements.fileBtn.addEventListener('click', () => this.uploadFile());
        this.elements.copyBtn.addEventListener('click', () => this.copySummary());
        this.elements.downloadBtn.addEventListener('click', () => this.downloadSummary());
        
        // File input
        this.elements.fileInput.addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files[0]);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.summarizeText();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                this.clearText();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
                this.pasteFromClipboard();
            }
        });
    }

    updateStats() {
        const text = this.elements.inputText.value;
        const charCount = text.length;
        const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        
        this.elements.charCount.textContent = charCount;
        this.elements.wordCount.textContent = wordCount;
    }

    async summarizeText() {
        const text = this.elements.inputText.value.trim();
        if (!text) {
            this.showError('Please enter some text to summarize.');
            return;
        }

        const wordCount = text.split(/\s+/).filter(w => w.length > 0).length;
        if (wordCount > 3000) {
            this.showError(`Text too long (${wordCount} words). Please reduce to under 3000 words to stay within API limits.`);
            return;
        }

        this.showProcessing(true);
        this.hideError();

        let response;
        try {
            // Call FastAPI backend
            response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    summary_type: this.elements.summaryType.value
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                this.displaySummary(data.summary, data.stats);
                this.showSuccess('Summary generated successfully!');
            } else {
                throw new Error(data.error || 'Failed to generate summary');
            }

        } catch (error) {
            console.error('Error:', error);
            if (response && response.status === 429) {
                const data = await response.json().catch(() => ({}));
                this.showError(data.detail || 'Text too large. Please shorten your input and try again.');
            } else {
                this.showError('Error generating summary. Please check your connection and try again.');
            }
        } finally {
            this.showProcessing(false);
        }
    }

    generateMockSummary(text) {
        // Simple mock summary generation
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const summaryLength = Math.max(2, Math.floor(sentences.length / 3));
        
        let summary = '';
        for (let i = 0; i < Math.min(summaryLength, sentences.length); i++) {
            summary += sentences[i].trim() + '. ';
        }
        
        return summary.trim() + ' This is a simulated summary for demonstration purposes.';
    }

    displaySummary(summary, stats) {
    this.elements.summaryOutput.textContent = summary;
    this.elements.summaryStats.style.display = 'flex';
    
    this.elements.reductionRatio.textContent = stats.reduction_percentage + '%';
    this.elements.summaryWords.textContent = stats.summary_words;
}   

    clearText() {
        this.elements.inputText.value = '';
        this.elements.summaryOutput.textContent = '';
        this.elements.summaryStats.style.display = 'none';
        this.updateStats();
        this.hideError();
    }

    handleScroll() {
        if (window.scrollY > 50) {
            this.elements.header.classList.add('scrolled');
        } else {
            this.elements.header.classList.remove('scrolled');
        }
    }

    handleNavClick(e) {
        this.elements.navLinks.forEach(link => link.classList.remove('active'));
        e.target.classList.add('active');
    }

    showProcessing(show) {
        if (show) {
            this.elements.summarizeBtn.disabled = true;
            this.elements.summarizeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Processing...</span>';
            this.elements.processingIndicator.style.display = 'flex';
        } else {
            this.elements.summarizeBtn.disabled = false;
            this.elements.summarizeBtn.innerHTML = '<i class="fas fa-sparkles"></i><span>Generate Summary</span>';
            this.elements.processingIndicator.style.display = 'none';
        }
    }

    showError(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.errorMessage.style.display = 'block';
        this.elements.errorMessage.className = 'error-message';
    }

    showSuccess(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.errorMessage.style.display = 'block';
        this.elements.errorMessage.className = 'success-message';
        setTimeout(() => {
            this.elements.errorMessage.style.display = 'none';
        }, 3000);
    }

    hideError() {
        this.elements.errorMessage.style.display = 'none';
    }

    async copySummary() {
        const summary = this.elements.summaryOutput.textContent;
        if (!summary) {
            this.showError('No summary to copy!');
            return;
        }

        try {
            await navigator.clipboard.writeText(summary);
            this.showSuccess('Summary copied to clipboard!');
        } catch (err) {
            this.showError('Failed to copy. Please try manually.');
        }
    }

    downloadSummary() {
        const summary = this.elements.summaryOutput.textContent;
        if (!summary) {
            this.showError('No summary to download!');
            return;
        }

        const blob = new Blob([summary], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `summary-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showSuccess('Summary downloaded!');
    }

    async pasteFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            this.elements.inputText.value = text;
            this.updateStats();
            this.showSuccess('Text pasted from clipboard!');
        } catch (err) {
            this.showError('Failed to access clipboard. Please paste manually.');
        }
    }

    uploadFile() {
        this.elements.fileInput.click();
    }

    async handleFileUpload(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            this.elements.inputText.value = e.target.result;
            this.updateStats();
            this.showSuccess(`File loaded: ${file.name}`);
        };
        reader.readAsText(file);
    }


    setupScrollAnimation() {
        // Add smooth scroll behavior for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe sections for fade-in effect
        document.querySelectorAll('.features-grid .feature-card, .about-content, .hero-stats .stat-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    updateUI() {
        // Initialize UI state on load
        this.updateStats();
        this.elements.summaryStats.style.display = 'none';
        this.elements.processingIndicator.style.display = 'none';
        this.elements.errorMessage.style.display = 'none';
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TextSummarizer();
});