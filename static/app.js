function append(role, text, retrieved = []) {
    const box = document.getElementById('messages');
    const d = document.createElement('div');
    d.className = 'msg ' + role;
    d.textContent = text;
    box.appendChild(d);

    if (retrieved.length) {
        const r = document.createElement('div');
        r.className = 'retrieved';
        r.textContent = 'Retrieved: ' +
            retrieved.map(x => `[ #${x.rank} ${x.doc} s=${x.score.toFixed(3)} ]`).join('  ');
        box.appendChild(r);
    }

    box.scrollTop = box.scrollHeight;
}

async function sendQuery() {
    const q = document.getElementById('query').value.trim();
    if (!q) return;

    append('user', q);
    document.getElementById('query').value = '';

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: q })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Server error');

        append('assistant', data.answer, data.retrieved);

    } catch (e) {
        append('assistant', 'Error: ' + e.message);
    }
}

document.getElementById('send').addEventListener('click', sendQuery);
document.getElementById('query').addEventListener('keydown', e => {
    if (e.key === 'Enter') sendQuery();
});
