class PasswordSecurity {
    constructor() {
        this.usernameInput = document.getElementById('usernameInput');
        this.passwordInput = document.getElementById('passwordInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        this.isAnalyzing = false;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.analyzeBtn.addEventListener('click', () => this.analyze());
        this.passwordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.analyze();
        });
        document.getElementById('retryBtn').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
            this.analyze();
        });
        
        // Suggestion buttons
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.usernameInput.value = btn.dataset.username;
                this.passwordInput.value = btn.dataset.password;
                this.analyze();
            });
        });
    }
    
    async analyze() {
        const username = this.usernameInput.value.trim();
        const password = this.passwordInput.value.trim();
        
        if (!username || !password) {
            this.showError('Please enter both username and password');
            return;
        }
        if (this.isAnalyzing) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.analyzeBtn.disabled = true;
        this.analyzeBtn.textContent = 'Analyzing...';
        this.isAnalyzing = true;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.handleResults(data);
            
        } catch (error) {
            this.showError('Failed to analyze: ' + error.message);
        }
        
        this.analyzeBtn.disabled = false;
        this.analyzeBtn.textContent = 'Analyze';
        this.isAnalyzing = false;
    }
    
    handleResults(data) {
        this.resultsSection.classList.remove('hidden');
        
        const strength = data.password_analysis || {};
        const brute = data.brute_force_simulation || {};
        
        // Strength
        const badge = document.getElementById('strengthBadge');
        const bar = document.getElementById('strengthBar');
        const score = strength.score_percentage || 0;
        
        badge.textContent = strength.strength?.toUpperCase() || 'UNKNOWN';
        badge.className = 'strength-badge ' + (strength.strength || 'weak');
        bar.style.width = score + '%';
        bar.className = 'strength-fill ' + (strength.strength || 'weak');
        
        document.getElementById('pwdLength').textContent = strength.length || 0;
        document.getElementById('pwdScore').textContent = (strength.score || 0) + '/10';
        
        // Stats
        document.getElementById('attemptsCount').textContent = brute.attempts || 0;
        document.getElementById('foundStatus').textContent = brute.found ? '✅ Yes' : '❌ No';
        document.getElementById('timeTaken').textContent = (brute.time_taken || 0) + 's';
        document.getElementById('rateLimitStatus').textContent = brute.rate_limited ? '⚠️ Triggered' : '✅ Off';
        
        // Issues
        const issuesList = document.getElementById('issuesList');
        issuesList.innerHTML = '';
        (strength.issues || ['No issues found']).forEach(issue => {
            const li = document.createElement('li');
            li.textContent = issue;
            issuesList.appendChild(li);
        });
        
        // Recommendations
        const recList = document.getElementById('recommendationsList');
        recList.innerHTML = '';
        (data.security_recommendations || ['No recommendations']).forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PasswordSecurity();
});
