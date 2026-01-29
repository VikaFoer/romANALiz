const statusEl = document.getElementById('status');
const statusText = statusEl?.querySelector('.status-text');
const form = document.getElementById('event-form');
const feedback = document.getElementById('form-feedback');
const submitBtn = document.getElementById('submit-btn');

async function checkHealth() {
  if (!statusEl || !statusText) return;
  try {
    const r = await fetch('/health');
    const ok = r.ok;
    statusEl.classList.toggle('ok', ok);
    statusEl.classList.toggle('err', !ok);
    statusText.textContent = ok ? 'онлайн' : 'помилка';
  } catch {
    statusEl.classList.remove('ok');
    statusEl.classList.add('err');
    statusText.textContent = 'офлайн';
  }
}

function showFeedback(message, isError) {
  if (!feedback) return;
  feedback.hidden = false;
  feedback.textContent = message;
  feedback.classList.toggle('success', !isError);
  feedback.classList.toggle('error', isError);
}

function hideFeedback() {
  if (feedback) {
    feedback.hidden = true;
    feedback.textContent = '';
  }
}

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  hideFeedback();
  if (submitBtn) submitBtn.disabled = true;

  const id = form.querySelector('#evt-id')?.value?.trim() || 'unknown';
  const value = parseFloat(form.querySelector('#evt-value')?.value || '0');
  const rawPayload = form.querySelector('#evt-payload')?.value?.trim();

  let payload = null;
  if (rawPayload) {
    try {
      payload = JSON.parse(rawPayload);
    } catch {
      showFeedback('Невалідний JSON у Payload.', true);
      if (submitBtn) submitBtn.disabled = false;
      return;
    }
  }

  try {
    const res = await fetch('/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, value, payload }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      showFeedback(`Подію «${data.id || id}» додано в чергу.`, false);
    } else {
      showFeedback(data.detail || `Помилка ${res.status}`, true);
    }
  } catch (err) {
    showFeedback('Мережева помилка: ' + (err.message || 'невідомо'), true);
  } finally {
    if (submitBtn) submitBtn.disabled = false;
  }
});

// use form.elements for form fields
const idInput = form?.querySelector('#evt-id');
const valueInput = form?.querySelector('#evt-value');
const payloadInput = form?.querySelector('#evt-payload');

checkHealth();
setInterval(checkHealth, 30_000);
