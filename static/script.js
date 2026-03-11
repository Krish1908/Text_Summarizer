// Minimal JavaScript for Text Summarizer
// Just enough for dynamic functionality without complexity

class TextSummarizer {
    constructor() {
        this.config = this.loadConfig();
        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.populateModels();
        this.updateUI();
    }

    setupElements() {
        this.elements = {
            inputText: document.getElementById('inputText'),
            summarizeBtn: document.getElementById('summarizeBtn'),
            clearBtn: document.getElementById('clearBtn'),
            settingsBtn: document.getElementById('settingsBtn'),
            closeSettings: document.getElementById('closeSettings'),
            configPanel: document.getElementById('configPanel'),
            saveConfig: document.getElementById('saveConfig'),
            modelSelect: document.getElementById('modelSelect'),
            temperature: document.getElementById('temperature'),
            tempValue: document.getElementById('tempValue'),
            summaryType: document.getElementById('summaryType'),
            languageSelect: document.getElementById('languageSelect'),
            summaryOutput: document.getElementById('summaryOutput'),
            processingIndicator: document.getElementById('processingIndicator'),
            summaryStats: document.getElementById('summaryStats'),
            processingTime: document.getElementById('processingTime'),
            reductionRatio: document.getElementById('reductionRatio'),
            summaryWords: document.getElementById('summaryWords'),
            charCount: document.getElementById('charCount'),
            wordCount: document.getElementById('wordCount'),
            copyBtn: document.getElementById('copyBtn'),
            downloadBtn: document.getElementById('downloadBtn'),
            pasteBtn: document.getElementById('pasteBtn'),
            fileBtn: document.getElementById('fileBtn'),
            sampleBtn: document.getElementById('sampleBtn'),
            errorMessage: document.getElementById('errorMessage'),
            fileInput: document.getElementById('fileInput')
        };
    }

    setupEventListeners() {
        // Text input for stats
        this.elements.inputText.addEventListener('input', () => this.updateStats());
        
        // Buttons
        this.elements.summarizeBtn.addEventListener('click', () => this.summarizeText());
        this.elements.clearBtn.addEventListener('click', () => this.clearText());
        this.elements.settingsBtn.addEventListener('click', () => this.toggleSettings());
        this.elements.closeSettings.addEventListener('click', () => this.toggleSettings());
        this.elements.saveConfig.addEventListener('click', () => this.saveConfig());
        
        // Controls
        this.elements.temperature.addEventListener('input', (e) => {
            this.elements.tempValue.textContent = e.target.value;
        });
        
        this.elements.copyBtn.addEventListener('click', () => this.copySummary());
        this.elements.downloadBtn.addEventListener('click', () => this.downloadSummary());
        this.elements.pasteBtn.addEventListener('click', () => this.pasteFromClipboard());
        this.elements.fileBtn.addEventListener('click', () => this.uploadFile());
        this.elements.sampleBtn.addEventListener('click', () => this.loadSampleText());
        
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
        });
    }

    async populateModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            this.elements.modelSelect.innerHTML = '';
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.value;
                option.textContent = model.label;
                this.elements.modelSelect.appendChild(option);
            });
            
            // Set default model
            this.elements.modelSelect.value = this.config.model || 'llama-3.1-8b-instant';
        } catch (error) {
            console.error('Failed to load models:', error);
        }
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

        this.showProcessing(true);
        this.hideError();

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    summary_type: this.elements.summaryType.value,
                    language: this.elements.languageSelect.value,
                    model: this.elements.modelSelect.value,
                    temperature: parseFloat(this.elements.temperature.value)
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
            this.showError('Error generating summary. Please try again.');
        } finally {
            this.showProcessing(false);
        }
    }

    displaySummary(summary, stats) {
        this.elements.summaryOutput.textContent = summary;
        this.elements.summaryStats.style.display = 'flex';
        
        this.elements.processingTime.textContent = '0s'; // Simplified
        this.elements.reductionRatio.textContent = stats.reduction_percentage;
        this.elements.summaryWords.textContent = stats.summary_words;
    }

    clearText() {
        this.elements.inputText.value = '';
        this.elements.summaryOutput.textContent = '';
        this.elements.summaryStats.style.display = 'none';
        this.updateStats();
        this.hideError();
    }

    toggleSettings() {
        const isVisible = this.elements.configPanel.style.display === 'block';
        this.elements.configPanel.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            this.loadConfigToForm();
        }
    }

    loadConfigToForm() {
        this.elements.modelSelect.value = this.config.model || 'llama-3.1-8b-instant';
        this.elements.temperature.value = this.config.temperature || 0;
        this.elements.tempValue.textContent = this.config.temperature || 0;
        this.elements.summaryType.value = this.config.summaryType || 'concise';
        this.elements.languageSelect.value = this.config.language || 'auto';
    }

    saveConfig() {
        this.config = {
            model: this.elements.modelSelect.value,
            temperature: parseFloat(this.elements.temperature.value),
            summaryType: this.elements.summaryType.value,
            language: this.elements.languageSelect.value
        };
        
        localStorage.setItem('textSummarizerConfig', JSON.stringify(this.config));
        this.hideError();
        this.showSuccess('Configuration saved!');
    }

    loadConfig() {
        const saved = localStorage.getItem('textSummarizerConfig');
        return saved ? JSON.parse(saved) : {
            model: 'llama-3.1-8b-instant',
            temperature: 0,
            summaryType: 'concise',
            language: 'auto'
        };
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

    loadSampleText() {
        const sampleText = `Artificial intelligence (AI) is a rapidly evolving field of technology that involves the development of computer systems capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding. AI has the potential to revolutionize various industries, from healthcare and finance to transportation and entertainment.

One of the most significant breakthroughs in AI has been the development of machine learning algorithms, particularly deep learning. These algorithms enable computers to learn from vast amounts of data without being explicitly programmed. This has led to remarkable achievements in image recognition, natural language processing, and game playing, among other areas.

However, the rapid advancement of AI also raises important ethical and societal questions. Issues such as job displacement, privacy concerns, algorithmic bias, and the potential for autonomous weapons have sparked intense debate among researchers, policymakers, and the general public. As AI continues to develop, it will be crucial to establish appropriate regulations and guidelines to ensure that the technology is used responsibly and for the benefit of humanity.

Despite these challenges, the potential benefits of AI are immense. In healthcare, AI could help doctors diagnose diseases more accurately and develop personalized treatment plans. In education, AI-powered tutors could provide customized learning experiences for students. In environmental science, AI could help us better understand and address climate change. The possibilities are endless, and the future of AI is both exciting and uncertain.`;

        this.elements.inputText.value = sampleText;
        this.updateStats();
        this.showSuccess('Sample text loaded!');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TextSummarizer();
});