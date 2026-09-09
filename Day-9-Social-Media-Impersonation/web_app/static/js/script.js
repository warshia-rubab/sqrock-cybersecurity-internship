class FakeProfileDetector {
    constructor() {
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.isAnalyzing = false;
        this.initEventListeners();
    }
    
    initEventListeners() {
        document.querySelectorAll('.profile-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const index = parseInt(btn.dataset.index);
                this.detectProfile(index);
            });
        });
        
        document.getElementById('impersonationBtn').addEventListener('click', () => {
            this.detectImpersonation();
        });
        
        document.getElementById('retryBtn').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
        });
    }
    
    async detectProfile(index) {
        if (this.isAnalyzing) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.isAnalyzing = true;
        
        document.querySelectorAll('.profile-btn').forEach(b => b.disabled = true);
        
        try {
            const response = await fetch('/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ profile_index: index })
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
        
        this.isAnalyzing = false;
        document.querySelectorAll('.profile-btn').forEach(b => b.disabled = false);
    }
    
    async detectImpersonation() {
        if (this.isAnalyzing) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.isAnalyzing = true;
        
        document.querySelectorAll('.profile-btn').forEach(b => b.disabled = true);
        
        try {
            const response = await fetch('/detect-impersonation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ profile1_index: 0, profile2_index: 1 })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.showImpersonationResults(data);
            
        } catch (error) {
            this.showError('Failed to analyze: ' + error.message);
        }
        
        this.isAnalyzing = false;
        document.querySelectorAll('.profile-btn').forEach(b => b.disabled = false);
    }
    
    handleResults(data) {
        this.resultsSection.classList.remove('hidden');
        
        // Profile Summary
        document.getElementById('profileIcon').textContent = data.fake_score > 50 ? '🤖' : '👤';
        document.getElementById('profileName').textContent = data.name || 'Unknown';
        document.getElementById('profileUsername').textContent = '@' + (data.username || 'unknown');
        
        const heuristics = data.heuristics || {};
        document.getElementById('metricAge').textContent = '📅 ' + (heuristics.account_age?.age_days || 0) + ' days';
        document.getElementById('metricFollowers').textContent = '👥 ' + (heuristics.follower_ratio?.followers || 0);
        document.getElementById('metricFollowing').textContent = '📌 ' + (heuristics.follower_ratio?.following || 0);
        document.getElementById('metricPosts').textContent = '📝 ' + (heuristics.post_count?.post_count || 0);
        
        // Risk Badge
        const score = data.fake_score || 0;
        const riskEl = document.getElementById('fakeScore');
        riskEl.textContent = score;
        riskEl.className = 'risk-value ' + (score > 70 ? 'critical' : score > 50 ? 'high' : score > 25 ? 'medium' : 'low');
        
        // Heuristics
        const grid = document.getElementById('heuristicsGrid');
        grid.innerHTML = '';
        const heuristicMap = {
            'account_age': { label: 'Account Age', value: (h) => h.age_days + ' days' },
            'follower_ratio': { label: 'Follower Ratio', value: (h) => h.ratio + ':1' },
            'profile_pic': { label: 'Profile Picture', value: (h) => h.has_pic ? '✅ Yes' : '❌ No' },
            'post_count': { label: 'Post Count', value: (h) => h.post_count + ' posts' },
            'bio_quality': { label: 'Bio Quality', value: (h) => h.is_default ? '⚠️ Default' : '✅ Good' },
            'verification': { label: 'Verification', value: (h) => h.verified ? '✅ Verified' : '❌ Not Verified' },
            'username_pattern': { label: 'Username Pattern', value: (h) => h.suspicious ? '⚠️ Suspicious' : '✅ Normal' }
        };
        
        for (const [key, info] of Object.entries(heuristicMap)) {
            const h = heuristics[key] || {};
            const div = document.createElement('div');
            div.className = 'heuristic-item';
            const isDanger = h.suspicious || h.is_default || h.is_numeric || h.has_bot_pattern;
            const isWarning = !h.verified && h.verified !== undefined;
            div.style.borderLeftColor = isDanger ? '#ef4444' : isWarning ? '#fbbf24' : '#34d399';
            div.innerHTML = `
                <span class="label">${info.label}</span>
                <span class="value">${info.value(h)}</span>
                <span class="status ${isDanger ? 'danger' : isWarning ? 'warning' : 'safe'}">
                    ${isDanger ? '⚠️ Suspicious' : isWarning ? '⚠️ Caution' : '✅ Safe'}
                </span>
            `;
            grid.appendChild(div);
        }
        
        // Bot Signals
        const signalsList = document.getElementById('signalsList');
        signalsList.innerHTML = '';
        const signals = data.bot_signals || [];
        if (signals.length === 0) {
            signalsList.innerHTML = '<li style="color: #34d399;">✅ No bot signals detected</li>';
        } else {
            signals.forEach(signal => {
                const li = document.createElement('li');
                li.textContent = '🤖 ' + signal;
                signalsList.appendChild(li);
            });
        }
        
        // Issues
        const issuesList = document.getElementById('issuesList');
        issuesList.innerHTML = '';
        (data.issues || ['No issues found']).forEach(issue => {
            const li = document.createElement('li');
            li.textContent = issue;
            issuesList.appendChild(li);
        });
        
        // Recommendations
        const recList = document.getElementById('recommendationsList');
        recList.innerHTML = '';
        (data.recommendations || ['No recommendations']).forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });
        
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    showImpersonationResults(data) {
        this.resultsSection.classList.remove('hidden');
        
        document.getElementById('profileIcon').textContent = data.is_impersonation ? '🚨' : '✅';
        document.getElementById('profileName').textContent = 'Impersonation Detection';
        document.getElementById('profileUsername').textContent = data.profile1 + ' vs ' + data.profile2;
        
        document.getElementById('metricAge').textContent = '📊 Similarity: ' + data.similarity_score + '%';
        document.getElementById('metricFollowers').textContent = '📌 Risk: ' + data.risk_level;
        document.getElementById('metricFollowing').textContent = '🔍 ' + (data.matching_factors?.length || 0) + ' factors';
        document.getElementById('metricPosts').textContent = data.is_impersonation ? '🚨 IMPERSONATION' : '✅ Legitimate';
        
        const score = data.similarity_score || 0;
        const riskEl = document.getElementById('fakeScore');
        riskEl.textContent = score;
        riskEl.className = 'risk-value ' + (score > 70 ? 'critical' : score > 50 ? 'high' : score > 30 ? 'medium' : 'low');
        
        // Show matching factors as signals
        const signalsList = document.getElementById('signalsList');
        signalsList.innerHTML = '';
        if (data.matching_factors && data.matching_factors.length > 0) {
            data.matching_factors.forEach(factor => {
                const li = document.createElement('li');
                li.textContent = '🔍 ' + factor;
                signalsList.appendChild(li);
            });
        } else {
            signalsList.innerHTML = '<li>✅ No matching factors found</li>';
        }
        
        // Clear issues and recommendations
        document.getElementById('issuesList').innerHTML = '<li>' + (data.is_impersonation ? '🚨 Possible impersonation detected!' : '✅ No impersonation detected') + '</li>';
        document.getElementById('recommendationsList').innerHTML = '<li>✅ Verify both accounts through official channels</li>';
        
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new FakeProfileDetector();
});
