"""PEOPLE backend.

Minimal FastAPI app used by the PEOPLE PWA prototype.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


APP_NAME = "PEOPLE"
APP_VERSION = "0.1.0"


app = FastAPI(
    title=APP_NAME,
    description="Personal digital website per person/device",
    version=APP_VERSION,
)


INDEX_HTML = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>PEOPLE</title>
    <style>
      :root { color-scheme: dark; }
      body {
        margin: 0;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        background: #000;
        color: #fff;
      }
      header {
        padding: 16px;
        border-bottom: 1px solid #222;
      }
      h1 { margin: 0; font-size: 20px; letter-spacing: 0.5px; }
      main { padding: 16px; max-width: 520px; }
      .card {
        border: 1px solid #222;
        border-radius: 12px;
        padding: 12px;
        background: #0b0b0b;
      }
      .row { display: flex; gap: 10px; align-items: center; }
      .grow { flex: 1; }
      .id {
        font-variant-numeric: tabular-nums;
        letter-spacing: 2px;
        font-size: 18px;
      }
      button {
        background: #111;
        color: #fff;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;
      }
      button:active { background: #1b1b1b; }
      .keypad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
      textarea {
        width: 100%;
        background: #000;
        color: #fff;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        min-height: 90px;
        resize: vertical;
      }
      .muted { color: #aaa; font-size: 12px; }
      .pill {
        display: inline-block;
        border: 1px solid #222;
        background: #000;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        color: #bbb;
      }
    </style>
  </head>
  <body>
    <header>
      <h1>PEOPLE</h1>
      <div class=\"muted\">One personal digital website per device.</div>
    </header>
    <main>
      <section class=\"card\">
        <div class=\"row\">
          <div class=\"grow\">
            <div class=\"muted\">Your 10-digit ID</div>
            <div id=\"peopleId\" class=\"id\">----------</div>
          </div>
          <span class=\"pill\" id=\"status\">offline</span>
        </div>
      </section>

      <div style=\"height: 14px\"></div>

      <section class=\"card\">
        <div class=\"muted\">Digital call pad</div>
        <div style=\"height: 10px\"></div>
        <div class=\"keypad\" id=\"keypad\"></div>
        <div style=\"height: 10px\"></div>
        <div class=\"row\">
          <button id=\"backspace\" type=\"button\">⌫</button>
          <button id=\"clear\" type=\"button\">Clear</button>
          <button id=\"newId\" type=\"button\">New ID</button>
        </div>
      </section>

      <div style=\"height: 14px\"></div>

      <section class=\"card\">
        <div class=\"muted\">Only text message ❤️</div>
        <div style=\"height: 10px\"></div>
        <textarea id=\"message\" placeholder=\"Type a message…\"></textarea>
      </section>

      <script>
        const idEl = document.getElementById('peopleId');
        const statusEl = document.getElementById('status');
        const keypadEl = document.getElementById('keypad');

        function random10() {
          const n = Math.floor(Math.random() * 1e10);
          return String(n).padStart(10, '0');
        }

        function loadId() {
          let id = localStorage.getItem('people_id');
          if (!id || !/^\\d{10}$/.test(id)) {
            id = random10();
            localStorage.setItem('people_id', id);
          }
          idEl.textContent = id;
        }

        function setStatus(online) {
          statusEl.textContent = online ? 'online' : 'offline';
          statusEl.style.color = online ? '#7CFC90' : '#bbb';
          statusEl.style.borderColor = online ? '#134d20' : '#222';
        }

        function appendDigit(d) {
          const current = idEl.textContent.replace(/[^0-9]/g, '');
          const next = (current + d).slice(0, 10);
          idEl.textContent = next.padEnd(10, '-');
          if (/^\\d{10}$/.test(next)) localStorage.setItem('people_id', next);
        }

        function backspace() {
          const current = idEl.textContent.replace(/[^0-9]/g, '');
          const next = current.slice(0, -1);
          idEl.textContent = next.padEnd(10, '-');
          if (/^\\d{10}$/.test(next)) localStorage.setItem('people_id', next);
        }

        function clearId() {
          idEl.textContent = '----------';
          localStorage.removeItem('people_id');
        }

        for (const d of ['1','2','3','4','5','6','7','8','9','0']) {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.textContent = d;
          btn.addEventListener('click', () => appendDigit(d));
          keypadEl.appendChild(btn);
        }

        document.getElementById('backspace').addEventListener('click', backspace);
        document.getElementById('clear').addEventListener('click', clearId);
        document.getElementById('newId').addEventListener('click', () => {
          const id = random10();
          localStorage.setItem('people_id', id);
          loadId();
        });

        window.addEventListener('online', () => setStatus(true));
        window.addEventListener('offline', () => setStatus(false));

        loadId();
        setStatus(navigator.onLine);
      </script>
    </main>
  </body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

