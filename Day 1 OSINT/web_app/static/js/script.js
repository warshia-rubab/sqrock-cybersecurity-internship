// Professional JavaScript for OSINT Scanner
class OSINTScanner {
    constructor() {
        this.domainInput = document.getElementById('domainInput');
        this.scanButton = document.getElementById('scanButton');
        this.progressSection = document.getElementById('progressSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.progressBar = document.getElementById('progressBar');
        this.progressPercent = document.getElementById('progressPercent');
        this.progressStatus = document.getElementById('progressStatus');
        
        this.scanInterval = null;
        this.isScanning = false;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Scan button click
        this.scanButton.addEventListener('click', () => this.startScan());
        
        // Enter key on input
        this.domainInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.startScan();
            }
        });
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn));
        });
        
        // Download buttons
        document.getElementById('downloadJSON').addEventListener('click', () => this.downloadJSON());
        document.getElementById('downloadReport').addEventListener('click', () => this.downloadReport());
        
        // Retry button
        document.getElementById('retryButton').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
            this.startScan();
        });
    }
    
    async startScan() {
        const domain = this.domainInput.value.trim();
        
        if (!domain) {
            this.showError('Please enter a domain to scan');
            return;
        }
        
        if (this.isScanning) {
            return;
        }
        
        // Reset UI
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.progressSection.classList.remove('hidden');
        this.scanButton.disabled = true;
        this.scanButton.innerHTML = '<span class="button-text">Scanning...</span>';
        this.isScanning = true;
        
        // Update progress
        this.updateProgress(0, 'Initiating scan...');
        
        try {
            // Start scan
            const response = await fetch('/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ domain: domain })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            // Poll for status
            this.pollStatus();
            
        } catch (error) {
            this.showError('Failed to start scan: ' + error.message);
        }
    }
    
    async pollStatus() {
        let attempts = 0;
        const maxAttempts = 120; // 2 minutes timeout
        
        this.scanInterval = setInterval(async () => {
            attempts++;
            
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.error) {
                    this.showError(data.error);
                    this.stopScanning();
                    return;
                }
                
                // Update progress
                if (data.progress !== undefined) {
                    this.updateProgress(data.progress, this.getProgressMessage(data.progress));
                }
                
                // Check if scan is complete
                if (!data.running && data.results) {
                    this.handleResults(data.results);
                    this.stopScanning();
                    return;
                }
                
                // Check for error
                if (data.error) {
                    this.showError(data.error);
                    this.stopScanning();
                    return;
                }
                
                // Timeout check
                if (attempts >= maxAttempts) {
                    this.showError('Scan timed out. Please try again.');
                    this.stopScanning();
                }
                
            } catch (error) {
                this.showError('Error checking scan status: ' + error.message);
                this.stopScanning();
            }
        }, 1000);
    }
    
    updateProgress(percent, message) {
        const clampedPercent = Math.min(100, Math.max(0, percent));
        this.progressBar.style.width = clampedPercent + '%';
        this.progressPercent.textContent = clampedPercent + '%';
        this.progressStatus.textContent = message || 'Scanning...';
    }
    
    getProgressMessage(percent) {
        if (percent < 20) return 'Initializing OSINT scanner...';
        if (percent < 40) return 'Gathering WHOIS information...';
        if (percent < 60) return 'Enumerating DNS records...';
        if (percent < 80) return 'Analyzing security headers...';
        if (percent < 100) return 'Generating report...';
        return 'Scan complete!';
    }
    
    handleResults(results) {
        // Show results section
        this.resultsSection.classList.remove('hidden');
        this.progressSection.classList.add('hidden');
        
        // Update risk score
        const riskScore = document.getElementById('riskScore');
        const scoreNumber = riskScore.querySelector('.score-number');
        scoreNumber.textContent = results.risk_score || 0;
        
        // Set score color
        const score = results.risk_score || 0;
        const circle = riskScore;
        if (score > 70) {
            circle.style.borderColor = '#e74c3c';
        } else if (score > 40) {
            circle.style.borderColor = '#f39c12';
        } else {
            circle.style.borderColor = '#2ecc71';
        }
        
        // Update stats
        document.getElementById('statIP').textContent = results.ip || '-';
        document.getElementById('statLocation').textContent = 
            results.city && results.country ? `${results.city}, ${results.country}` : '-';
        document.getElementById('statRegistrar').textContent = 
            results.whois?.registrar || '-';
        
        const headersCount = results.security_headers ? 
            Object.values(results.security_headers).filter(h => h === '✅ Set').length : 0;
        document.getElementById('statHeaders').textContent = 
            `${headersCount}/${Object.keys(results.security_headers || {}).length || 0}`;
        
        // Populate WHOIS table
        this.populateTable('whoisTable', results.whois || {});
        
        // Populate DNS table
        this.populateDNSTable(results.dns_records || {});
        
        // Populate Security Headers table
        this.populateTable('securityTable', results.security_headers || {});
        
        // Store results for download
        this.currentResults = results;
    }
    
    populateTable(tableId, data) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        tbody.innerHTML = '';
        
        for (const [key, value] of Object.entries(data)) {
            const tr = document.createElement('tr');
            const tdKey = document.createElement('td');
            const tdValue = document.createElement('td');
            
            tdKey.textContent = key.replace(/_/g, ' ').toUpperCase();
            
            if (Array.isArray(value)) {
                tdValue.textContent = value.join(', ');
            } else if (typeof value === 'object' && value !== null) {
                tdValue.textContent = JSON.stringify(value);
            } else {
                tdValue.textContent = value || 'N/A';
            }
            
            tr.appendChild(tdKey);
            tr.appendChild(tdValue);
            tbody.appendChild(tr);
        }
    }
    
    populateDNSTable(dnsData) {
        const tbody = document.querySelector('#dnsTable tbody');
        tbody.innerHTML = '';
        
        for (const [recordType, values] of Object.entries(dnsData)) {
            const tr = document.createElement('tr');
            const tdKey = document.createElement('td');
            const tdValue = document.createElement('td');
            
            tdKey.textContent = recordType;
            tdValue.textContent = Array.isArray(values) ? values.join(', ') : (values || 'No records found');
            
            tr.appendChild(tdKey);
            tr.appendChild(tdValue);
            tbody.appendChild(tr);
        }
    }
    
    switchTab(btn) {
        // Update button states
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update pane visibility
        const targetTab = btn.dataset.tab;
        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        document.getElementById(targetTab).classList.add('active');
    }
    
    async downloadJSON() {
        if (!this.currentResults) return;
        
        const json = JSON.stringify(this.currentResults, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `osint_report_${this.currentResults.domain || 'scan'}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    async downloadReport() {
        if (!this.currentResults || !this.currentResults.report_files) return;
        
        // Try to download the markdown report
        const files = this.currentResults.report_files;
        const reportFile = Array.isArray(files) ? files.find(f => f.endsWith('.md')) : null;
        
        if (reportFile) {
            const filename = reportFile.split('/').pop();
            window.location.href = `/download/reports/${filename}`;
        } else {
            // Fallback: download JSON
            this.downloadJSON();
        }
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.progressSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
    
    stopScanning() {
        this.isScanning = false;
        this.scanButton.disabled = false;
        this.scanButton.innerHTML = '<span class="button-text">Start Scan</span><span class="button-icon">→</span>';
        
        if (this.scanInterval) {
            clearInterval(this.scanInterval);
            this.scanInterval = null;
        }
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new OSINTScanner();
});
