const form = document.getElementById('downloadForm');
const urlInput = document.getElementById('urlInput');
const modeSelect = document.getElementById('modeSelect');
const qualitySelect = document.getElementById('qualitySelect');
const downloadBtn = document.getElementById('downloadBtn');

const statusArea = document.getElementById('statusArea');
const statusText = document.getElementById('statusText');
const progressArea = document.getElementById('progressArea');
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');
const progressEta = document.getElementById('progressEta');
const historyArea = document.getElementById('historyArea');
const historyList = document.getElementById('historyList');

function setStatus(message, kind = 'info') {
  statusText.textContent = message;
  statusText.dataset.kind = kind;
}

function setProgress(pct, etaText = '–') {
  progressFill.style.width = `${pct}%`;
  progressPercent.textContent = `${Math.floor(pct)}%`;
  progressEta.textContent = etaText;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
  
    const url = (urlInput.value || '').trim();
    if (!url) {
      setStatus('Please paste a valid URL.', 'error');
      urlInput.focus();
      return;
    }
    const mode = modeSelect.value;
    const quality = qualitySelect.value;
  
    setStatus('Starting download…');
    downloadBtn.disabled = true;
    progressArea.classList.remove('hidden');
    setProgress(0, '–');
  
    let taskId = null;
    try {
      const res = await fetch('/api/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, mode, quality })
      });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        setStatus(data.message || 'Failed to start.', 'error');
        downloadBtn.disabled = false;
        return;
      }
      taskId = data.task_id;
    } catch (err) {
      setStatus('Network error. Check server.', 'error');
      downloadBtn.disabled = false;
      return;
    }
  
    // Poll every 800ms
    const pollMs = 800;
    const timer = setInterval(async () => {
      try {
        const r = await fetch(`/api/progress?task_id=${encodeURIComponent(taskId)}`);
        const j = await r.json();
        if (!r.ok || !j.ok) return;
  
        const p = j.progress || {};
        const pct = typeof p.percent === 'number' ? p.percent : 0;
        const eta = p.eta != null ? `${p.eta}s` : '–';
        setProgress(pct, eta);
  
        if (p.status === 'error') {
          clearInterval(timer);
          setStatus(p.error || 'Download failed.', 'error');
          downloadBtn.disabled = false;
        } else if (p.done || p.status === 'complete') {
          clearInterval(timer);
          setProgress(100, 'done');
          setStatus('Download complete.', 'success');
          historyArea.classList.remove('hidden');
          const li = document.createElement('li');
          li.innerHTML = `<span>${url}</span><a href="#" class="dl-link">Open</a>`;
          historyList.prepend(li);
          downloadBtn.disabled = false;
        } else {
          setStatus(p.status || 'Working…');
        }
      } catch (e) {
        // transient errors ignored
      }
    }, pollMs);
  });