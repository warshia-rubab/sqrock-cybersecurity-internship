class Terminal {
    constructor() {
        this.input = document.getElementById('commandInput');
        this.output = document.getElementById('output');
        this.isProcessing = false;
        this.initEventListeners();
    }

    initEventListeners() {
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand(this.input.value.trim());
            }
        });

        document.querySelectorAll('.cmd-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                this.input.value = category;
                this.executeCommand(category);
            });
        });
    }

    async executeCommand(cmd) {
        if (this.isProcessing) return;
        if (!cmd) return;

        this.isProcessing = true;
        this.input.disabled = true;
        this.input.value = '';

        // Show command in terminal
        this.printLine(`<span class="user">root@sqrock</span>:<span class="path">~/day4</span>$ <span class="command">./vishing-generator ${cmd}</span>`);

        // Process command
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: cmd })
            });

            const data = await response.json();

            if (data.error) {
                this.printLine(`<span class="output-text error">❌ Error: ${data.error}</span>`);
            } else if (cmd === 'smishing') {
                this.displaySmishing(data);
            } else {
                this.displayScript(data);
            }

        } catch (error) {
            this.printLine(`<span class="output-text error">❌ Error: ${error.message}</span>`);
        }

        // Show ready prompt
        this.printLine(`<span class="user">root@sqrock</span>:<span class="path">~/day4</span>$ <span class="command blink">_</span>`);
        
        this.isProcessing = false;
        this.input.disabled = false;
        this.input.focus();

        // Auto scroll
        this.output.scrollTop = this.output.scrollHeight;
    }

    displayScript(data) {
        const category = data.category.replace('_', ' ').toUpperCase();
        this.printLine(`<span class="output-text info">📋 Generating ${category} Script...</span>`);
        this.printLine(`<span class="output-text">👤 Caller: ${data.caller_name} from ${data.company}</span>`);
        this.printLine(`<span class="output-text">🎯 Target: ${data.target}</span>`);
        
        // Script output
        const scriptHtml = data.script.split('\n').map(line => {
            if (line.includes('RED FLAGS') || line.includes('PROPER RESPONSE')) {
                return `<span class="label">${line}</span>`;
            }
            return line;
        }).join('<br>');
        
        this.printLine(`<div class="script-output">${scriptHtml}</div>`);
        
        // Psychological triggers
        this.printLine(`<span class="output-text warning">🧠 Psychological Triggers: ${data.psychological_triggers.join(', ')}</span>`);
        
        // Red flags
        this.printLine(`<span class="output-text error">🚨 Red Flags:</span>`);
        data.red_flags.forEach(flag => {
            this.printLine(`  <span class="output-text error">⚠️ ${flag}</span>`);
        });
    }

    displaySmishing(data) {
        this.printLine(`<span class="output-text info">📱 Generating Smishing Message...</span>`);
        this.printLine(`<span class="output-text">📋 ${data.description}</span>`);
        this.printLine(`<span class="output-text warning">📩 Message: ${data.message}</span>`);
        this.printLine(`<span class="output-text warning">🧠 Triggers: ${data.psychological_triggers.join(', ')}</span>`);
        this.printLine(`<span class="output-text error">🚨 Red Flags:</span>`);
        data.red_flags.forEach(flag => {
            this.printLine(`  <span class="output-text error">⚠️ ${flag}</span>`);
        });
    }

    printLine(html) {
        const p = document.createElement('p');
        p.innerHTML = html;
        this.output.appendChild(p);
        this.output.scrollTop = this.output.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Terminal();
});
