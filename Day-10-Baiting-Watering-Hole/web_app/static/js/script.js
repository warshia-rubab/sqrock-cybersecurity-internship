class ThreatIntelligence {
    constructor() {
        this.isLoading = false;
        this.initEventListeners();
        this.loadLogs();
        this.loadStats();
    }
    
    initEventListeners() {
        // Bait buttons
        document.querySelectorAll('.bait-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const type = btn.dataset.type;
                this.generateBait(type);
            });
        });
        
        // Waterhole buttons
        document.querySelectorAll('.waterhole-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.target;
                this.simulateWaterhole(target);
            });
        });
        
        // Copy button
        document.getElementById('copyBaitBtn').addEventListener('click', () => {
            const url = document.getElementById('baitUrl').textContent;
            navigator.clipboard.writeText(window.location.origin + url);
            alert('Link copied to clipboard!');
        });
        
        // Refresh logs
        document.getElementById('refreshLogsBtn').addEventListener('click', () => {
            this.loadLogs();
            this.loadStats();
        });
    }
    
    async generateBait(type) {
        if (this.isLoading) return;
        this.isLoading = true;
        
        try {
            const response = await fetch('/generate-bait', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bait_type: type })
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            document.getElementById('baitResult').classList.remove('hidden');
            document.getElementById('baitIcon').textContent = data.icon || '🎁';
            document.getElementById('baitName').textContent = data.name || 'Free Gift';
            document.getElementById('baitDesc').textContent = data.description || 'Fake giveaway';
            document.getElementById('baitId').textContent = 'ID: ' + (data.id || 'unknown');
            document.getElementById('baitUrl').textContent = data.url || '/bait/unknown';
            
            document.getElementById('baitResult').scrollIntoView({ behavior: 'smooth' });
            
            // Update stats
            this.loadStats();
            
        } catch (error) {
            alert('Failed to generate bait: ' + error.message);
        }
        
        this.isLoading = false;
    }
    
    async simulateWaterhole(target) {
        if (this.isLoading) return;
        this.isLoading = true;
        
        try {
            const response = await fetch('/waterhole', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_type: target })
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            document.getElementById('waterholeResult').classList.remove('hidden');
            document.getElementById('whTarget').textContent = data.details?.name || target;
            document.getElementById('whDesc').textContent = data.details?.description || '';
            
            const risk = document.getElementById('whRisk');
            risk.textContent = data.details?.risk || 'MEDIUM';
            risk.className = 'wh-risk ' + (data.details?.risk || 'medium').toLowerCase();
            
            // Red Flags
            const flagsList = document.getElementById('whFlags');
            flagsList.innerHTML = '';
            (data.red_flags || []).forEach(flag => {
                const li = document.createElement('li');
                li.textContent = flag;
                flagsList.appendChild(li);
            });
            
            // Defense Tips
            const tipsList = document.getElementById('whTips');
            tipsList.innerHTML = '';
            (data.defense_tips || []).forEach(tip => {
                const li = document.createElement('li');
                li.textContent = tip;
                tipsList.appendChild(li);
            });
            
            document.getElementById('waterholeResult').scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            alert('Failed to simulate watering hole: ' + error.message);
        }
        
        this.isLoading = false;
    }
    
    async loadLogs() {
        try {
            const response = await fetch('/logs');
            const data = await response.json();
            
            if (data.error) {
                console.error('Error loading logs:', data.error);
                return;
            }
            
            const container = document.getElementById('logsContainer');
            const logs = data.logs || [];
            
            if (logs.length === 0) {
                container.innerHTML = '<p class="logs-empty">No attacks logged yet. Generate a bait link to start.</p>';
                return;
            }
            
            container.innerHTML = '';
            logs.slice().reverse().forEach(log => {
                const div = document.createElement('div');
                div.className = 'log-entry';
                
                const severityClass = log.severity?.toLowerCase() === 'critical' ? 'severity-critical' : 
                                     log.severity?.toLowerCase() === 'high' ? 'severity-high' : '';
                
                div.innerHTML = `
                    <span class="time">${new Date(log.timestamp).toLocaleTimeString()}</span>
                    <span class="ip">${log.ip || 'Unknown'}</span>
                    <span class="bait">${log.bait_name || 'Unknown'}</span>
                    <span class="${severityClass}">${log.severity || 'LOW'}</span>
                    <span style="color: #4a5a7a; font-size: 11px;">${log.location || 'Unknown'}</span>
                `;
                container.appendChild(div);
            });
            
        } catch (error) {
            console.error('Failed to load logs:', error);
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch('/logs');
            const data = await response.json();
            
            if (data.error || !data.summary) return;
            
            const summary = data.summary;
            document.getElementById('totalAttacks').textContent = summary.total_attacks || 0;
            document.getElementById('uniqueIPs').textContent = summary.unique_ips || 0;
            document.getElementById('criticalAttacks').textContent = (summary.severity_counts?.CRITICAL || 0) + 
                                                                     (summary.severity_counts?.HIGH || 0);
            
            // Get bait links count
            const baitResponse = await fetch('/bait-links');
            const baitData = await baitResponse.json();
            document.getElementById('baitLinks').textContent = baitData.links?.length || 0;
            
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ThreatIntelligence();
});
