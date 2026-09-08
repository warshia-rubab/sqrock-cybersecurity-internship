class EmailHarvester {
    constructor() {
        this.urlInput = document.getElementById('urlInput');
        this.harvestButton = document.getElementById('harvestButton');
        this.progressSection = document.getElementById('progressSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.progressBar = document.getElementById('progressBar');
        this.progressPercent = document.getElementById('progressPercent');
        this.progressStatus = document.getElementById('progressStatus');
        this.emailList = document.getElementById('emailList');
        
        this.harvestInterval = null;
        this.isHarvesting = false;
        this.currentResults = null;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.harvestButton.addEventListener('click', () => this.startHarvest());
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.startHarvest();
        });
        document.getElementById('downloadJSON').addEventListener('click', () => this.downloadJSON());
        document.getElementById('downloadReport').addEventListener('click', () => this.downloadReport());
        document.getElementById('retryButton').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
            this.startHarvest();
        });
    }
    
    async startHarvest() {
        const url = this.urlInput.value.trim();
        if (!url) {
            this.showError('Please enter a valid URL');
            return;
        }
        if (this.isHarvesting) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.progressSection.classList.remove('hidden');
        this.harvestButton.disabled = true;
        this.harvestButton.innerHTML = '<span>⏳ Harvesting...</span>';
        this.isHarvesting = true;
        this.updateProgress(0, '🚀 Initializing...');
        
        try {
            const response = await fetch('/harvest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            if (data.error) {
                this.showError(data.error);
                return;
            }
            this.pollStatus();
        } catch (error) {
            this.showError('Failed to start: ' + error.message);
        }
    }
    
    async pollStatus() {
        let attempts = 0;
        const maxAttempts = 120;
        
        this.harvestInterval = setInterval(async () => {
            attempts++;
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.error) {
                    this.showError(data.error);
                    this.stopHarvesting();
                    return;
                }
                
                if (data.progress !== undefined) {
                    this.updateProgress(data.progress, this.getProgressMessage(data.progress));
                }
                
                if (!data.running && data.results) {
                    this.handleResults(data.results);
                    this.stopHarvesting();
                    return;
                }
                
                if (data.error) {
                    this.showError(data.error);
                    this.stopHarvesting();
                    return;
                }
                
                if (attempts >= maxAttempts) {
                    this.showError('⏰ Harvest timed out. Please try again.');
                    this.stopHarvesting();
                }
            } catch (error) {
                this.showError('Error: ' + error.message);
                this.stopHarvesting();
            }
        }, 1000);
    }
    
    updateProgress(percent, message) {
        const clamped = Math.min(100, Math.max(0, percent));
        this.progressBar.style.width = clamped + '%';
        this.progressPercent.textContent = clamped + '%';
        this.progressStatus.textContent = message || '⏳ Working...';
    }
    
    getProgressMessage(percent) {
        if (percent < 20) return '🚀 Initializing harvester...';
        if (percent < 40) return '🌐 Connecting to website...';
        if (percent < 60) return '📧 Extracting emails...';
        if (percent < 80) return '📊 Analyzing patterns...';
        if (percent < 100) return '📄 Generating report...';
        return '✅ Complete!';
    }
    
    handleResults(results) {
        this.resultsSection.classList.remove('hidden');
        this.progressSection.classList.add('hidden');
        this.currentResults = results;
        
        document.getElementById('statEmails').textContent = results.total_emails || 0;
        document.getElementById('statDomains').textContent = 
            results.analysis?.unique_domains?.length || 0;
        document.getElementById('statPatterns').textContent = 
            Object.keys(results.analysis?.username_patterns || {}).length || 0;
        
        this.displayEmails(results.emails || []);
    }
    
    displayEmails(emails) {
        this.emailList.innerHTML = '';
        if (emails.length === 0) {
            this.emailList.innerHTML = '<p style="color: #4a3a5a; text-align: center; padding: 20px; font-style: italic;">No emails found on this page.</p>';
            return;
        }
        const ul = document.createElement('ul');
        emails.forEach(email => {
            const li = document.createElement('li');
            li.textContent = email;
            ul.appendChild(li);
        });
        this.emailList.appendChild(ul);
    }
    
    async downloadJSON() {
        if (!this.currentResults) return;
        const json = JSON.stringify(this.currentResults, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `emails_${this.currentResults.url.replace(/https?:\/\//, '').replace(/\//g, '_')}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    async downloadReport() {
        if (!this.currentResults || !this.currentResults.report_path) return;
        const filename = this.currentResults.report_path.split('/').pop();
        window.location.href = `/download/reports/${filename}`;
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.progressSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
    
    stopHarvesting() {
        this.isHarvesting = false;
        this.harvestButton.disabled = false;
        this.harvestButton.innerHTML = '<span>🔍 Harvest</span>';
        if (this.harvestInterval) {
            clearInterval(this.harvestInterval);
            this.harvestInterval = null;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new EmailHarvester();
});
