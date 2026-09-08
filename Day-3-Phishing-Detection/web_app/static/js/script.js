class PhishShield {
    constructor() {
        this.urlInput = document.getElementById('urlInput');
        this.analyzeButton = document.getElementById('analyzeButton');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.gaugeScore = document.getElementById('gaugeScore');
        this.gaugeProgress = document.getElementById('gaugeProgress');
        this.riskLevelBadge = document.getElementById('riskLevelBadge');
        this.riskUrl = document.getElementById('riskUrl');
        this.indicatorsGrid = document.getElementById('indicatorsGrid');
        this.recommendationsList = document.getElementById('recommendationsList');
        this.breakdownBars = document.getElementById('breakdownBars');
        
        // Stats
        this.totalScans = 0;
        this.threatsFound = 0;
        this.safeUrls = 0;
        this.totalScore = 0;
        
        this.isAnalyzing = false;
        this.currentResults = null;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.analyzeButton.addEventListener('click', () => this.analyze());
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.analyze();
        });
        document.getElementById('retryButton').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
            this.analyze();
        });
        
        // Quick test buttons
        document.querySelectorAll('.tag-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.urlInput.value = btn.dataset.url;
                this.analyze();
            });
        });
    }
    
    updateStats(score, isThreat) {
        this.totalScans++;
        if (isThreat) this.threatsFound++;
        else this.safeUrls++;
        this.totalScore += score;
        
        document.getElementById('totalScans').textContent = this.totalScans;
        document.getElementById('threatsFound').textContent = this.threatsFound;
        document.getElementById('safeUrls').textContent = this.safeUrls;
        document.getElementById('avgScore').textContent = Math.round(this.totalScore / this.totalScans);
    }
    
    async analyze() {
        let url = this.urlInput.value.trim();
        if (!url) {
            this.showError('Please enter a valid URL');
            return;
        }
        
        // Add https:// if no protocol
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        
        if (this.isAnalyzing) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.analyzeButton.disabled = true;
        this.analyzeButton.innerHTML = '<span class="btn-text">Analyzing...</span><span class="btn-icon">⏳</span>';
        this.isAnalyzing = true;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.handleResults(data);
            this.updateStats(data.risk_score || 0, data.risk_level !== 'LOW');
            
        } catch (error) {
            this.showError('Failed to analyze: ' + error.message);
        }
        
        this.analyzeButton.disabled = false;
        this.analyzeButton.innerHTML = '<span class="btn-text">Analyze</span><span class="btn-icon">→</span>';
        this.isAnalyzing = false;
    }
    
    handleResults(results) {
        this.resultsSection.classList.remove('hidden');
        this.currentResults = results;
        
        const score = results.risk_score || 0;
        const level = results.risk_level || 'LOW';
        const url = results.url || '-';
        
        // Update gauge
        this.gaugeScore.textContent = score;
        const rotation = (score / 100) * 270 - 135;
        this.gaugeProgress.style.transform = `rotate(${rotation}deg)`;
        
        // Update risk level badge
        this.riskLevelBadge.className = 'risk-level-badge ' + level;
        this.riskLevelBadge.querySelector('.level-text').textContent = level;
        this.riskUrl.textContent = url;
        
        // Update indicators
        this.displayIndicators(results.indicators || {});
        
        // Update recommendations
        this.displayRecommendations(results.recommendations || []);
        
        // Update breakdown
        this.displayBreakdown(results.details?.score_breakdown || {});
    }
    
    displayIndicators(indicators) {
        this.indicatorsGrid.innerHTML = '';
        
        const indicatorMap = {
            'uses_https': { label: 'HTTPS Secure', good: true },
            'has_suspicious_keywords': { label: 'Suspicious Keywords', good: false },
            'has_urgent_keywords': { label: 'Urgent Language', good: false },
            'brand_impersonation': { label: 'Brand Impersonation', good: false },
            'suspicious_tld': { label: 'Suspicious TLD', good: false },
            'has_at_symbol': { label: 'Contains @ Symbol', good: false },
            'many_subdomains': { label: 'Multiple Subdomains', good: false },
            'excessive_length': { label: 'Excessive Length', good: false },
            'uses_ip_address': { label: 'Uses IP Address', good: false },
            'has_redirect_param': { label: 'Redirect Parameter', good: false },
            'domain_age_suspicious': { label: 'New Domain (< 30 days)', good: false },
            'has_unicode': { label: 'Unicode Characters', good: false }
        };
        
        let hasIndicators = false;
        for (const [key, info] of Object.entries(indicatorMap)) {
            const value = indicators[key];
            if (value === undefined || value === null) continue;
            hasIndicators = true;
            
            const isDanger = typeof value === 'boolean' ? !info.good && value : false;
            const statusText = typeof value === 'boolean' ? (value ? '⚠️ Detected' : '✅ Safe') : String(value);
            
            const div = document.createElement('div');
            div.className = 'indicator-item';
            div.innerHTML = `
                <span class="indicator-name">${info.label}</span>
                <span class="indicator-status ${typeof value === 'boolean' ? (value ? 'danger' : 'success') : ''}">${statusText}</span>
            `;
            this.indicatorsGrid.appendChild(div);
        }
        
        if (!hasIndicators) {
            this.indicatorsGrid.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#4a5a6a;padding:20px;">No indicators detected</div>';
        }
    }
    
    displayRecommendations(recommendations) {
        this.recommendationsList.innerHTML = '';
        
        if (recommendations.length === 0) {
            const li = document.createElement('li');
            li.textContent = '✅ No recommendations - URL appears safe';
            this.recommendationsList.appendChild(li);
            return;
        }
        
        recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            this.recommendationsList.appendChild(li);
        });
    }
    
    displayBreakdown(breakdown) {
        this.breakdownBars.innerHTML = '';
        
        const colors = {
            'HTTPS': 'danger',
            'Keywords': 'warning',
            'Brand Impersonation': 'danger',
            'URL Structure': 'warning',
            'Domain': 'info',
            'Other': 'info'
        };
        
        let hasData = false;
        for (const [label, value] of Object.entries(breakdown)) {
            if (value > 0) {
                hasData = true;
                const div = document.createElement('div');
                div.className = 'breakdown-item';
                div.innerHTML = `
                    <span class="breakdown-label">${label}</span>
                    <div class="breakdown-track">
                        <div class="breakdown-fill ${colors[label] || 'info'}" style="width: ${Math.min(value, 100)}%"></div>
                    </div>
                    <span class="breakdown-value">+${value}</span>
                `;
                this.breakdownBars.appendChild(div);
            }
        }
        
        if (!hasData) {
            this.breakdownBars.innerHTML = '<div style="text-align:center;color:#4a5a6a;padding:10px;">No risk factors detected</div>';
        }
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PhishShield();
});
