import { useState, useEffect, useCallback } from 'react'
import './index.css'

type HealthStatus = 'checking' | 'ok' | 'err'
type Feedback = { type: 'success' | 'error'; message: string } | null

async function checkHealth(): Promise<boolean> {
  try {
    const r = await fetch('/health')
    return r.ok
  } catch {
    return false
  }
}

export default function App() {
  const [status, setStatus] = useState<HealthStatus>('checking')
  const [id, setId] = useState('evt-001')
  const [value, setValue] = useState(50)
  const [payload, setPayload] = useState('')
  const [loading, setLoading] = useState(false)
  const [feedback, setFeedback] = useState<Feedback>(null)

  const refreshHealth = useCallback(async () => {
    const ok = await checkHealth()
    setStatus(ok ? 'ok' : 'err')
  }, [])

  useEffect(() => {
    refreshHealth()
    const t = setInterval(refreshHealth, 30_000)
    return () => clearInterval(t)
  }, [refreshHealth])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setFeedback(null)
    setLoading(true)
    let parsed: object | null = null
    if (payload.trim()) {
      try {
        parsed = JSON.parse(payload) as object
      } catch {
        setFeedback({ type: 'error', message: 'Невалідний JSON у Payload.' })
        setLoading(false)
        return
      }
    }
    try {
      const res = await fetch('/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, value, payload: parsed }),
      })
      const data = (await res.json().catch(() => ({}))) as { id?: string; detail?: string }
      if (res.ok) {
        setFeedback({ type: 'success', message: `Подію «${data.id ?? id}» додано в чергу.` })
      } else {
        setFeedback({ type: 'error', message: data.detail ?? `Помилка ${res.status}` })
      }
    } catch (err) {
      setFeedback({
        type: 'error',
        message: 'Мережева помилка: ' + (err instanceof Error ? err.message : 'невідомо'),
      })
    } finally {
      setLoading(false)
    }
  }

  const statusText = status === 'checking' ? 'перевірка…' : status === 'ok' ? 'онлайн' : 'офлайн'

  return (
    <>
      <div className="bg" aria-hidden="true" />
      <header className="header">
        <div className="logo">
          <span className="logoIcon">◈</span>
          <h1>Air-bot</h1>
          <span className="tagline">Maximum-Detail & Efficiency</span>
        </div>
        <div className={`status ${status}`}>
          <span className="statusDot" />
          <span>{statusText}</span>
        </div>
      </header>

      <main className="main">
        <section className="card cardHero">
          <h2>Надіслати подію</h2>
          <p className="muted">
            Подія потрапляє в чергу, обробляється детекторами і скорингом.
          </p>
          <form className="form" onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="evt-id">ID події</label>
              <input
                id="evt-id"
                value={id}
                onChange={(e) => setId(e.target.value)}
                placeholder="evt-001"
              />
            </div>
            <div className="field">
              <label htmlFor="evt-value">Value (0–100)</label>
              <input
                id="evt-value"
                type="number"
                min={0}
                max={100}
                step={0.01}
                value={value}
                onChange={(e) => setValue(Number(e.target.value))}
                placeholder="50"
              />
            </div>
            <div className="field">
              <label htmlFor="evt-payload">Payload (JSON, опційно)</label>
              <textarea
                id="evt-payload"
                value={payload}
                onChange={(e) => setPayload(e.target.value)}
                rows={3}
                placeholder='{"source": "web"}'
              />
            </div>
            <button type="submit" className="btn btnPrimary" disabled={loading}>
              {loading ? 'Відправка…' : 'Надіслати'}
            </button>
          </form>
          {feedback && (
            <div className={`formFeedback ${feedback.type}`} role="alert">
              {feedback.message}
            </div>
          )}
        </section>

        <section className="card cardLinks">
          <h3>API</h3>
          <ul className="links">
            <li>
              <a href="/health">GET /health</a> — стан сервісу
            </li>
            <li>
              <a href="/docs">GET /docs</a> — Swagger UI
            </li>
            <li>
              <code>POST /events</code> — надіслати подію
            </li>
          </ul>
        </section>
      </main>

      <footer className="footer">
        <span>Air-bot v0.1.0</span>
      </footer>
    </>
  )
}
