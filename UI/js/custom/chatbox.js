// Floating Chatbox Injection and Logic
(function() {
    // Inject chatbox HTML
    var chatboxHTML = `
    <div id="floating-chatbox" style="display: flex; flex-direction: column; position: fixed; bottom: 24px; right: 24px; width: 340px; max-width: 90vw; z-index: 9999; font-family: Roboto, Arial, sans-serif;">
        <div id="chatbox-header" style="background: #007bff; color: #fff; padding: 10px 16px; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: bold; display: flex; align-items: center; justify-content: space-between;">
            <span>Agent Chat</span>
            <span>
                <span id="chatbox-minimize" title="Minimize" style="margin-right: 12px; cursor: pointer; font-size: 18px;">&#8211;</span>
                <span id="chatbox-close" title="Close" style="cursor:pointer; font-size: 20px;">&times;</span>
            </span>
        </div>
        <div id="chatbox-body" style="background: #fff; height: 320px; overflow-y: auto; border: 1px solid #007bff; border-top: none; padding: 12px; display: flex; flex-direction: column; gap: 8px;"></div>
        <div id="chatbox-input-area" style="background: #f8f9fa; border: 1px solid #007bff; border-top: none; border-radius: 0 0 8px 8px; padding: 8px; display: flex; gap: 8px;">
            <input id="chatbox-input" type="text" placeholder="Type a command..." style="flex:1; padding: 6px 8px; border-radius: 4px; border: 1px solid #ccc; outline: none;" />
            <button id="chatbox-send" style="background: #007bff; color: #fff; border: none; border-radius: 4px; padding: 6px 16px; cursor: pointer;">Send</button>
        </div>
    </div>
    `;
    if (!document.getElementById('floating-chatbox')) {
        var div = document.createElement('div');
        div.innerHTML = chatboxHTML;
        document.body.appendChild(div.firstElementChild);
    }

    // Chat history from localStorage
    var chatHistory = JSON.parse(localStorage.getItem('chatbox-history') || '[]');
    var chatboxBody = document.getElementById('chatbox-body');
    function renderHistory() {
        chatboxBody.innerHTML = '';
        chatHistory.forEach(function(msg) {
            var bubble = document.createElement('div');
            bubble.style.maxWidth = '80%';
            bubble.style.marginBottom = '4px';
            bubble.style.padding = '8px 12px';
            bubble.style.borderRadius = '16px';
            bubble.style.whiteSpace = 'pre-wrap';
            if (msg.role === 'user') {
                bubble.style.alignSelf = 'flex-end';
                bubble.style.background = '#e9f5ff';
                bubble.style.color = '#222';
            } else {
                bubble.style.alignSelf = 'flex-start';
                bubble.style.background = '#f1f1f1';
                bubble.style.color = '#333';
            }
            bubble.textContent = msg.content;
            chatboxBody.appendChild(bubble);
        });
        chatboxBody.scrollTop = chatboxBody.scrollHeight;
    }
    renderHistory();

    // Send message
    function sendMessage() {
        var input = document.getElementById('chatbox-input');
        var text = input.value.trim();
        if (!text) return;
        chatHistory.push({role: 'user', content: text});
        localStorage.setItem('chatbox-history', JSON.stringify(chatHistory));
        renderHistory();
        input.value = '';
        // Show loading
        var loadingMsg = {role: 'agent', content: '...'};
        chatHistory.push(loadingMsg);
        renderHistory();
        // Send to backend
        fetch('http://127.0.0.1:5000/agent', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: text})
        })
        .then(r => r.json())
        .then(data => {
            chatHistory.pop(); // remove loading
            chatHistory.push({role: 'agent', content: data.response});
            localStorage.setItem('chatbox-history', JSON.stringify(chatHistory));
            renderHistory();
            // Auto-refresh if product added or deleted
            if (typeof data.response === 'string' && (data.response.includes('Product') && (data.response.includes('added successfully') || data.response.includes('deleted')))) {
                setTimeout(function() { window.location.reload(); }, 800);
            }
        })
        .catch(() => {
            chatHistory.pop();
            chatHistory.push({role: 'agent', content: '❌ Error contacting agent.'});
            localStorage.setItem('chatbox-history', JSON.stringify(chatHistory));
            renderHistory();
        });
    }
    document.getElementById('chatbox-send').onclick = sendMessage;
    document.getElementById('chatbox-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    // Close button
    document.getElementById('chatbox-close').onclick = function(e) {
        document.getElementById('floating-chatbox').style.display = 'none';
        e.stopPropagation();
    };
    // Minimize/maximize button
    var minimized = false;
    document.getElementById('chatbox-minimize').onclick = function(e) {
        minimized = !minimized;
        var body = document.getElementById('chatbox-body');
        var inputArea = document.getElementById('chatbox-input-area');
        if (minimized) {
            body.style.display = 'none';
            inputArea.style.display = 'none';
            this.innerHTML = '&#x25A1;'; // maximize icon
            this.title = 'Maximize';
        } else {
            body.style.display = 'flex';
            inputArea.style.display = 'flex';
            this.innerHTML = '&#8211;'; // minimize icon
            this.title = 'Minimize';
        }
        e.stopPropagation();
    };
    // Prevent header click from toggling minimize
    document.getElementById('chatbox-header').onclick = function(e) {
        if (e.target.id === 'chatbox-minimize' || e.target.id === 'chatbox-close') return;
    };
})(); 