class USBSimulator {
    constructor() {
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        this.isSimulating = false;
        this.initEventListeners();
    }
    
    initEventListeners() {
        document.querySelectorAll('.payload-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const payload = btn.dataset.payload;
                this.simulate(payload);
            });
        });
        document.getElementById('retryBtn').addEventListener('click', () => {
            this.errorSection.classList.add('hidden');
        });
    }
    
    async simulate(payloadType) {
        if (this.isSimulating) return;
        
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.isSimulating = true;
        
        // Disable buttons
        document.querySelectorAll('.payload-btn').forEach(b => b.disabled = true);
        
        try {
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ payload_type: payloadType })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.handleResults(data);
            
        } catch (error) {
            this.showError('Failed to simulate: ' + error.message);
        }
        
        this.isSimulating = false;
        document.querySelectorAll('.payload-btn').forEach(b => b.disabled = false);
    }
    
    handleResults(data) {
        this.resultsSection.classList.remove('hidden');
        
        // USB Info
        document.getElementById('usbName').textContent = data.usb_details?.usb_name || 'Unknown';
        document.getElementById('usbSize').textContent = data.usb_details?.usb_size || 'Unknown';
        document.getElementById('usbFormat').textContent = data.usb_details?.usb_format || 'Unknown';
        
        // Severity
        const severity = data.severity || 'LOW';
        const severityEl = document.getElementById('usbSeverity');
        severityEl.querySelector('.severity-value').textContent = severity;
        severityEl.querySelector('.severity-value').className = 'severity-value ' + severity.toLowerCase();
        
        // System Info
        const sysInfo = data.system_info || {};
        const systemGrid = document.getElementById('systemGrid');
        systemGrid.innerHTML = '';
        const sysItems = [
            { label: 'Hostname', value: sysInfo.hostname },
            { label: 'OS', value: sysInfo.os + ' ' + sysInfo.os_release },
            { label: 'Username', value: sysInfo.username },
            { label: 'IP Address', value: sysInfo.ip_address },
            { label: 'Architecture', value: sysInfo.architecture },
            { label: 'Python Version', value: sysInfo.python_version }
        ];
        sysItems.forEach(item => {
            if (item.value) {
                const div = document.createElement('div');
                div.className = 'system-item';
                div.innerHTML = `<span class="label">${item.label}</span><span class="value">${item.value}</span>`;
                systemGrid.appendChild(div);
            }
        });
        
        // Recon Data
        const recon = data.recon_data || {};
        const reconGrid = document.getElementById('reconGrid');
        reconGrid.innerHTML = '';
        if (recon.system) {
            const items = [
                { label: 'CPU', value: recon.system.cpu_count + ' cores' },
                { label: 'CPU Usage', value: recon.system.cpu_percent + '%' },
                { label: 'Memory', value: recon.system.memory_percent + '% used' },
                { label: 'Disk Used', value: recon.system.disk_usage }
            ];
            items.forEach(item => {
                if (item.value) {
                    const div = document.createElement('div');
                    div.className = 'recon-item';
                    div.innerHTML = `<span class="label">${item.label}</span><span class="value">${item.value}</span>`;
                    reconGrid.appendChild(div);
                }
            });
        }
        
        // Red Flags
        const flagsList = document.getElementById('flagsList');
        flagsList.innerHTML = '';
        (data.red_flags || ['No red flags']).forEach(flag => {
            const li = document.createElement('li');
            li.textContent = flag;
            flagsList.appendChild(li);
        });
        
        // Defense Tips
        const defenseList = document.getElementById('defenseList');
        defenseList.innerHTML = '';
        (data.defense_tips || ['No defense tips']).forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            defenseList.appendChild(li);
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
    new USBSimulator();
});
