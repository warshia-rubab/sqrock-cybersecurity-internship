class PhishingEngine {
    constructor() {
        this.targetSelect = document.getElementById('targetSelect');
        this.templateSelect = document.getElementById('templateSelect');
        this.generateBtn = document.getElementById('generateBtn');
        this.emailContent = document.getElementById('emailContent');
        this.flagsContent = document.getElementById('flagsContent');
        
        this.isGenerating = false;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.generateBtn.addEventListener('click', () => this.generate());
    }
    
    async generate() {
        if (this.isGenerating) return;
        
        const targetIndex = parseInt(this.targetSelect.value);
        const templateType = this.templateSelect.value;
        
        this.isGenerating = true;
        this.generateBtn.disabled = true;
        this.generateBtn.textContent = 'Generating...';
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target_index: targetIndex,
                    template_type: templateType
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            if (templateType === 'all') {
                this.displayAllTemplates(data);
            } else {
                this.displayTemplate(data);
            }
            
        } catch (error) {
            this.showError('Failed to generate template: ' + error.message);
        }
        
        this.isGenerating = false;
        this.generateBtn.disabled = false;
        this.generateBtn.textContent = 'Generate Email';
    }
    
    displayTemplate(data) {
        const template = data.template;
        const target = data.target;
        
        // Build email HTML
        let html = `
            <div class="email-sender">From: ${template.sender.name} &lt;${template.sender.email}&gt;</div>
            <div class="email-sender">To: ${target.name} &lt;${target.email}&gt;</div>
            <div class="email-subject">${template.subject}</div>
            <span class="email-urgency ${template.urgency.toLowerCase()}">${template.urgency} URGENCY</span>
            <div class="email-body">${template.body.replace(/\n/g, '<br>')}</div>
        `;
        
        this.emailContent.innerHTML = html;
        
        // Display red flags
        this.displayFlags(template.red_flags || []);
        
        // Scroll to email
        document.querySelector('.email-preview').scrollIntoView({ behavior: 'smooth' });
    }
    
    displayAllTemplates(data) {
        const templates = data.templates || [];
        const target = data.target || {};
        
        let html = '';
        templates.forEach((template, index) => {
            html += `
                <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 16px 0; ${index > 0 ? 'margin-top: 16px;' : ''}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-weight: 600; color: #60a5fa;">${template.template_type.replace('_', ' ').toUpperCase()}</span>
                        <span class="email-urgency ${template.urgency.toLowerCase()}">${template.urgency}</span>
                    </div>
                    <div class="email-sender">From: ${template.sender.name} &lt;${template.sender.email}&gt;</div>
                    <div class="email-subject" style="font-size: 15px;">${template.subject}</div>
                    <div class="email-body" style="font-size: 13px; max-height: 100px; overflow: hidden;">${template.body.replace(/\n/g, '<br>').substring(0, 300)}...</div>
                </div>
            `;
        });
        
        this.emailContent.innerHTML = html;
        
        // Display combined red flags
        const allFlags = templates.reduce((acc, t) => [...acc, ...(t.red_flags || [])], []);
        this.displayFlags([...new Set(allFlags)]);
    }
    
    displayFlags(flags) {
        if (!flags || flags.length === 0) {
            this.flagsContent.innerHTML = '<p class="flags-empty">No specific red flags identified</p>';
            return;
        }
        
        let html = '<ul>';
        flags.forEach(flag => {
            html += `<li>${flag}</li>`;
        });
        html += '</ul>';
        this.flagsContent.innerHTML = html;
    }
    
    showError(message) {
        this.emailContent.innerHTML = `
            <div style="text-align: center; padding: 40px 0; color: #ff6b6b;">
                <span style="font-size: 48px; display: block; margin-bottom: 12px;">❌</span>
                <p style="font-size: 16px;">${message}</p>
            </div>
        `;
        this.flagsContent.innerHTML = '<p class="flags-empty">Error generating email</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PhishingEngine();
});
