class TargetProfile {
    constructor() {
        this.usernameInput = document.getElementById('usernameInput');
        this.searchButton = document.getElementById('searchButton');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        this.isSearching = false;
        this.currentResults = null;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.searchButton.addEventListener('click', () => this.search());
        this.usernameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.search();
        });
        document.getElementById('retryButton').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
            this.search();
        });
        
        // Quick test buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.usernameInput.value = btn.dataset.username;
                this.search();
            });
        });
    }
    
    async search() {
        const username = this.usernameInput.value.trim();
        if (!username) {
            this.showError('Please enter a GitHub username');
            return;
        }
        if (this.isSearching) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.searchButton.disabled = true;
        this.searchButton.textContent = 'Searching...';
        this.isSearching = true;
        
        try {
            const response = await fetch('/build-profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.handleResults(data);
            
        } catch (error) {
            this.showError('Failed to build profile: ' + error.message);
        }
        
        this.searchButton.disabled = false;
        this.searchButton.textContent = 'Analyze';
        this.isSearching = false;
    }
    
    handleResults(data) {
        this.resultsSection.classList.remove('hidden');
        this.currentResults = data;
        
        const user = data.github_data?.user || {};
        const assessment = data.social_engineering_assessment || {};
        
        // Profile header
        document.getElementById('profileName').textContent = user.name || data.target;
        document.getElementById('profileBio').textContent = user.bio || 'No bio available';
        document.getElementById('statRepos').textContent = `📁 ${user.public_repos || 0}`;
        document.getElementById('statFollowers').textContent = `👥 ${user.followers || 0}`;
        document.getElementById('statFollowing').textContent = `📌 ${user.following || 0}`;
        
        // Risk badge
        const riskScore = assessment.risk_score || 0;
        document.getElementById('riskScore').textContent = riskScore;
        const riskColor = riskScore > 60 ? '#ff4444' : riskScore > 30 ? '#ffaa00' : '#00ff88';
        document.getElementById('riskScore').style.color = riskColor;
        document.querySelector('.risk-badge').style.borderColor = riskColor + '33';
        
        // Stats
        document.getElementById('exposureLevel').textContent = assessment.exposure_level || 'UNKNOWN';
        document.getElementById('infoExposed').textContent = assessment.personal_info_exposed?.length || 0;
        document.getElementById('techStackCount').textContent = assessment.technical_stack?.length || 0;
        document.getElementById('threatVectors').textContent = data.threat_vectors?.length || 0;
        
        // Personal Info
        this.populateList('personalInfoList', assessment.personal_info_exposed || []);
        
        // Tech Stack
        this.populateList('techStackList', assessment.technical_stack || []);
        
        // Collaborators
        this.populateList('collaboratorsList', assessment.collaborators || []);
        
        // Threat Vectors
        const threatList = document.getElementById('threatVectorsList');
        threatList.innerHTML = '';
        (data.threat_vectors || []).forEach(vector => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${vector.vector}</strong> <span class="severity-${vector.severity.toLowerCase()}">(${vector.severity})</span>`;
            threatList.appendChild(li);
        });
        
        // Recommendations
        this.populateList('recommendationsList', data.recommendations || []);
        
        // Attacker Perspective
        const attackerData = data.attacker_perspective || {};
        const attackerView = attackerData.attacker_view || [];
        const attackList = document.getElementById('attackerViewList');
        attackList.innerHTML = '';
        attackerView.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            attackList.appendChild(li);
        });
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    populateList(listId, items) {
        const list = document.getElementById(listId);
        list.innerHTML = '';
        if (!items || items.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'No data available';
            li.style.color = '#4a6a8a';
            list.appendChild(li);
            return;
        }
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            list.appendChild(li);
        });
    }
    
    showError(message) {
        this.errorSection.classList.remove('hidden');
        this.resultsSection.classList.add('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new TargetProfile();
});
