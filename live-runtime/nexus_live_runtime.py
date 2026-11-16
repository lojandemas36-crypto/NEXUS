"""
NEXUS Live Runtime v5 — Modern UI refresh with CSS + card-based layout.
"""
import os, sys, sqlite3, time, threading, json, tempfile, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nexus.db import InMemoryDB
from nexus.orchestrator import Orchestrator
from nexus.workflow import Task, Workflow
from nexus.engine import NoEffect
from nexus_dashboard import server as dashboard_server
from nexus_dashboard.server import DashboardHTTPServer

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus_live.db")

MODERN_CSS = """
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #2d3748; line-height: 1.6; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
header { background: linear-gradient(135deg, #0a6e0a 0%, #0d8f0d 100%); color: white; padding: 30px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
header h1 { font-size: 2.5em; font-weight: 700; }
header p { opacity: 0.9; margin-top: 5px; }
nav { background: white; padding: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 30px; }
nav .container { display: flex; gap: 30px; }
nav a { color: #4a5568; text-decoration: none; font-weight: 500; transition: color 0.2s; }
nav a:hover, nav a.active { color: #0a6e0a; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
.stat-card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.stat-card h3 { font-size: 0.9em; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-card .number { font-size: 2.5em; font-weight: 700; color: #0a6e0a; margin-top: 10px; }
.workflow-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.workflow-card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; }
.workflow-card:hover { transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.12); }
.workflow-card h3 { font-size: 1.1em; margin-bottom: 10px; color: #2d3748; }
.workflow-card .status { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: 600; margin-top: 10px; }
.status-completed { background: #c6f6d5; color: #22543d; }
.status-unknown, .status-needs_review { background: #fefcbf; color: #744210; }
.status-failed { background: #fed7d7; color: #742a2a; }
.status-abandoned { background: #bee3f8; color: #2c5282; }
.capability-list { display: grid; gap: 20px; }
.capability-card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #0a6e0a; }
.capability-card h3 { color: #0a6e0a; margin-bottom: 10px; }
.tag { display: inline-block; background: #0a6e0a; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.75em; margin-right: 8px; }
.tag.phase-d { background: #3182ce; }
.tag.sealed { background: #718096; }
.tag.validated { background: #805ad5; }
table { width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
th { background: #0a6e0a; color: white; padding: 15px; text-align: left; font-weight: 600; }
td { padding: 15px; border-bottom: 1px solid #e2e8f0; }
tr:hover { background: #f7fafc; }
a { color: #0a6e0a; text-decoration: none; }
a:hover { text-decoration: underline; }
footer { text-align: center; padding: 30px; color: #718096; font-size: 0.9em; margin-top: 50px; }
</style>
"""

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

class LiveDB(InMemoryDB):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        init_db(db_path)
    
    def save(self, record):
        super().save(record)
        try:
            conn = sqlite3.connect(self.db_path)
            payload = {
                "workflow_id": record.get("workflow_id", ""),
                "run_id": record.get("run_id", ""),
                "task_id": record.get("task_id", ""),
                "state": record.get("state", ""),
                "reason": record.get("reason", ""),
                "attempts": record.get("attempts", 0),
                "time": record.get("time", time.time()),
                "event": record.get("event", ""),
            }
            conn.execute("INSERT INTO history (data) VALUES (?)", (json.dumps(payload),))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[LiveDB] SQLite write failed: {e}")

def get_db_stats(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT data FROM history ORDER BY id").fetchall()
    conn.close()
    
    records = [json.loads(r["data"]) for r in rows]
    workflows = set(r.get("workflow_id") for r in records if r.get("workflow_id"))
    
    stats = {"total": len(workflows), "completed": 0, "unknown": 0, "failed": 0, "abandoned": 0}
    for wf in workflows:
        wf_records = [r for r in records if r.get("workflow_id") == wf]
        states = [r.get("state", "") for r in wf_records]
        if "completed" in states:
            stats["completed"] += 1
        elif "unknown" in states or "needs_review" in states:
            stats["unknown"] += 1
        elif "failed" in states:
            stats["failed"] += 1
        elif "abandoned" in states:
            stats["abandoned"] += 1
    
    return stats, records

def render_home(stats, records):
    workflows = {}
    for r in records:
        wf_id = r.get("workflow_id", "")
        if wf_id:
            if wf_id not in workflows:
                workflows[wf_id] = []
            workflows[wf_id].append(r)
    
    cards = ""
    for wf_id, wf_records in workflows.items():
        states = [r.get("state", "") for r in wf_records]
        status = "unknown"
        if "completed" in states: status = "completed"
        elif "failed" in states: status = "failed"
        elif "abandoned" in states: status = "abandoned"
        
        cards += f"""
        <div class="workflow-card" onclick="window.location='/workflows/{wf_id}'">
            <h3>{wf_id}</h3>
            <p>{len(wf_records)} records</p>
            <span class="status status-{status}">{status}</span>
        </div>
        """
    
    return f"""<!DOCTYPE html>
<html><head><title>NEXUS Dashboard</title>{MODERN_CSS}</head><body>
<header><div class="container"><h1>NEXUS Dashboard</h1><p>Live Workflow Orchestrator</p></div></header>
<nav><div class="container">
<a href="/" class="active">Home</a>
<a href="/workflows">Workflows</a>
<a href="/unknowns">Unknowns / orphans</a>
<a href="/healthz">Health</a>
<a href="/capabilities">Capabilities</a>
</div></nav>
<div class="container">
<div class="stats">
<div class="stat-card"><h3>Total Workflows</h3><div class="number">{stats['total']}</div></div>
<div class="stat-card"><h3>Completed</h3><div class="number" style="color:#38a169">{stats['completed']}</div></div>
<div class="stat-card"><h3>Needs Review</h3><div class="number" style="color:#d69e2e">{stats['unknown']}</div></div>
<div class="stat-card"><h3>Failed</h3><div class="number" style="color:#e53e3e">{stats['failed']}</div></div>
</div>
<h2 style="margin-bottom:20px">Recent Workflows</h2>
<div class="workflow-grid">{cards}</div>
</div>
<footer>NEXUS v1.1 — Sealed 2026-11-13 — Signed by Lojan Demas</footer>
</body></html>"""

def run_demo(db_path):
    db = LiveDB(db_path)
    orch = Orchestrator(db, poll_interval=0.01)
    
    orch.register_action("greet", lambda d: "Hello, " + d.get("name", "World") + "!", side_effects="none", cancellable="no")
    wf1 = Workflow("w_demo_1", "r1", [Task(id="t1", name="greet", action="greet", input={"name": "Lojan"})])
    r1 = orch.run(wf1)
    print("1. Completed:", r1.status, "->", r1.output("t1"))
    
    orch.register_action("uncertain", lambda d: None, side_effects="none", cancellable="no")
    wf2 = Workflow("w_demo_2", "r1", [Task(id="t2", name="uncertain", action="uncertain", input={})])
    r2 = orch.run(wf2)
    print("2. Needs review:", r2.status)
    
    orch.decide("t2", "abandon")
    print("3. Decided: t2 -> abandon")
    
    call_count = [0]
    def flaky(d):
        call_count[0] += 1
        if call_count[0] < 3:
            raise NoEffect()
        return "success after retry"
    orch.register_action("flaky", flaky, side_effects="none", cancellable="no")
    wf4 = Workflow("w_demo_4", "r1", [Task(id="t4", name="flaky", action="flaky", input={})])
    r4 = orch.run(wf4)
    print("4. Retried:", r4.status, "->", r4.output("t4"), "(attempts:", call_count[0], ")")
    
    def fail_hard(d):
        raise RuntimeError("simulated handler failure")
    orch.register_action("fail_hard", fail_hard, side_effects="none", cancellable="no")
    wf5 = Workflow("w_demo_5", "r1", [Task(id="t5", name="fail_hard", action="fail_hard", input={})])
    r5 = orch.run(wf5)
    print("5. Error:", r5.status)
    
    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    conn.close()
    print(f"\nDemo data seeded: {count} rows in history table.")

class ModernDashboardServer(DashboardHTTPServer):
    def do_GET(self):
        if self.path == "/" or self.path == "/home":
            stats, records = get_db_stats(self.server.database_path)
            html = render_home(stats, records)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            super().do_GET()


# Presentation overrides for the local read-only dashboard. Route dispatch,
# SQLite access mode, escaping helpers, and response security remain in the
# sealed dashboard module.
def _polished_page(title, body):
    safe_title = dashboard_server._esc(title)
    css = """
    :root{color-scheme:light;--primary:#0a6e0a;--secondary:#1a202c;--accent:#3182ce;--bg:#f7fafc;--surface:#fff;--text:#1a202c;--muted:#5d6878;--border:#e2e8f0;--green:#16803c;--green-bg:#e7f5ec;--amber:#805300;--amber-bg:#fff4cf;--red:#a61b16;--red-bg:#fde8e7;--blue:#175b91;--blue-bg:#e5f2fc}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;transition:background-color .15s,color .15s}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,input:focus-visible,label:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
    .shell{width:min(1200px,calc(100% - 40px));margin:auto}.masthead{background:var(--secondary);color:white;border-bottom:4px solid var(--primary)}.topbar{min-height:76px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}.brand{color:white;font-size:1.2rem;font-weight:850;letter-spacing:.12em}.brand small{display:block;color:#cbd5e0;font-size:.7rem;font-weight:500;letter-spacing:0}.nav-links{display:flex;align-items:center;gap:8px;margin-left:auto}.nav-links a{color:#e2e8f0;padding:9px 12px;border-radius:8px}.nav-links a:hover{background:#ffffff18;color:white;text-decoration:none}.theme-control{display:inline-flex;align-items:center;gap:7px;color:#e2e8f0;font-size:.88rem;cursor:pointer}.theme-control input{accent-color:#69c275;width:17px;height:17px}.nav-toggle,.nav-toggle-label{display:none}
    main.shell{padding:34px 0 52px}h1{font-size:clamp(1.8rem,4vw,2.35rem);line-height:1.2;letter-spacing:-.035em;margin:0 0 18px}h2{font-size:1.3rem;margin:28px 0 12px}p{margin:.65rem 0}.muted{color:var(--muted)}
    table{display:block;width:100%;overflow-x:auto;border-collapse:collapse;background:var(--surface);border:1px solid var(--border);border-radius:14px;box-shadow:0 8px 26px #1a202c0b;margin:14px 0 24px}thead{background:#edf4ee}th,td{padding:13px 15px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border)}th{font-size:.78rem;letter-spacing:.07em;text-transform:uppercase;color:#354254}tbody tr:last-child td{border:0}tbody tr:hover{background:#3182ce0c}code{font:.9em ui-monospace,Consolas,monospace;overflow-wrap:anywhere}
    .badge,.status-badge{display:inline-flex;align-items:center;border:1px solid transparent;border-radius:999px;padding:4px 10px;font-size:.78rem;font-weight:750}.badge{color:var(--amber);background:var(--amber-bg);border-color:#e7c86c}.status-completed{color:var(--green);background:var(--green-bg)}.status-unknown,.status-needs_review,.status-started_no_terminal{color:var(--amber);background:var(--amber-bg)}.status-failed{color:var(--red);background:var(--red-bg)}.status-abandoned,.status-cancelled,.status-running{color:var(--blue);background:var(--blue-bg)}
    .safety{border-left:4px solid #c58a1b;background:var(--amber-bg);padding:12px 16px;margin:10px 0;border-radius:0 10px 10px 0}.safety p{margin:5px 0}.stat-grid,.capability-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:20px 0 30px}.stat-card,.capability-card{background:var(--surface);border:1px solid var(--border);border-radius:15px;padding:20px;box-shadow:0 8px 26px #1a202c09;transition:transform .15s,box-shadow .15s}.stat-card:hover,.capability-card:hover{transform:translateY(-2px);box-shadow:0 12px 30px #1a202c15}.stat-card .label{color:var(--muted);font-size:.78rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase}.stat-card .value{display:block;font-size:2rem;font-weight:850;color:var(--primary);margin-top:8px}.stat-card.review .value{color:var(--amber)}.stat-card.failed .value{color:var(--red)}.capability-card{border-top:3px solid var(--primary)}.capability-card h2{margin:0 0 8px;font-size:1.1rem}.button{display:inline-flex;background:var(--primary);color:white;padding:9px 14px;border-radius:9px;font-weight:700}.button:hover{background:#085908;color:white;text-decoration:none}.empty-state{padding:24px;border:1px dashed #aab7c5;border-radius:12px;background:var(--surface);color:var(--muted)}footer{border-top:1px solid var(--border);background:var(--surface);color:var(--muted);padding:22px 0;font-size:.86rem}footer .shell{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
    body:has(#theme-toggle:checked){color-scheme:dark;--bg:#111820;--surface:#1b2632;--text:#edf2f7;--muted:#b2bfcc;--border:#344353;--green-bg:#163d2a;--amber-bg:#493914;--red-bg:#4a2424;--blue-bg:#183b56}body:has(#theme-toggle:checked) thead{background:#253443}body:has(#theme-toggle:checked) th{color:#e2e8f0}
    @media(max-width:1024px){.stat-grid,.capability-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:720px){.shell{width:calc(100% - 28px)}.topbar{padding:12px 0;gap:12px}.nav-toggle-label{display:inline-flex;margin-left:auto;padding:7px 10px;border:1px solid #ffffff55;border-radius:8px;color:white;cursor:pointer}.nav-toggle{display:block;position:absolute;opacity:0;width:1px;height:1px}.nav-toggle:focus-visible+.nav-toggle-label{outline:3px solid var(--accent);outline-offset:3px}.nav-links{display:none;order:3;width:100%;margin:0;flex-direction:column;align-items:stretch}.nav-toggle:checked~.nav-links{display:flex}.nav-links a{padding:10px}.theme-control{order:2}main.shell{padding-top:24px}table{font-size:.9rem}}@media(max-width:420px){.stat-grid,.capability-grid{grid-template-columns:1fr}.brand{font-size:1.05rem}th,td{padding:10px}}@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
    """
    document = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="theme-color" content="#1a202c">'
        f'<title>{safe_title} — NEXUS</title><style>{css}</style></head><body>'
        '<header class="masthead"><div class="shell topbar">'
        '<a class="brand" href="/">NEXUS <small>Local workflow review</small></a>'
        '<input class="nav-toggle" type="checkbox" id="nav-toggle" aria-label="Toggle navigation">'
        '<label class="nav-toggle-label" for="nav-toggle">Menu</label>'
        '<nav class="nav-links" aria-label="Main navigation"><a href="/">Overview</a>'
        '<a href="/workflows">Workflows</a><a href="/unknowns">Needs review</a>'
        '<a href="/capabilities">Capabilities</a></nav>'
        '<label class="theme-control" for="theme-toggle"><input id="theme-toggle" type="checkbox"> Dark mode</label>'
        '</div></header><main class="shell"><h1>' + safe_title + '</h1>' + body + '</main>'
        '<footer><div class="shell"><span>NEXUS v1.1 · Local dashboard</span>'
        '<span>Workflow state and history</span></div></footer></body></html>')
    return document.encode("utf-8")


def _status_badge(value):
    allowed = {"completed", "unknown", "needs_review", "failed", "abandoned", "cancelled",
               "running", "started_no_terminal", "never_run", "interrupted", "skipped", "reused"}
    label = value if isinstance(value, str) and value in allowed else "unknown"
    return f'<span class="status-badge status-{label}">{dashboard_server._esc(label.replace("_", " "))}</span>'


def _render_overview_polished(records):
    ids = sorted({wid for rec in records if (wid := dashboard_server._workflow_id(rec)) is not None})
    states = {wid: dashboard_server._workflow_state(records, wid) for wid in ids}
    review_count = len(dashboard_server._unknown_records(records))
    completed = sum(state == "completed" for state in states.values())
    failed = sum(state == "failed" for state in states.values())
    body = ('<p class="muted">Read-only workflow activity. Review items remain unresolved until a person acts.</p>'
        '<section class="stat-grid" aria-label="Workflow totals">'
        f'<article class="stat-card"><span class="label">Total workflows</span><strong class="value">{len(ids)}</strong></article>'
        f'<article class="stat-card"><span class="label">Completed</span><strong class="value">{completed}</strong></article>'
        f'<article class="stat-card review"><span class="label">Needs review</span><strong class="value">{review_count}</strong></article>'
        f'<article class="stat-card failed"><span class="label">Failed</span><strong class="value">{failed}</strong></article></section>'
        '<p><a class="button" href="/workflows">Browse workflows</a></p>')
    if review_count:
        body += '<h2>Needs review</h2>' + dashboard_server._render_safety_table(
            dashboard_server._unknown_records(records), records)
    else:
        body += '<h2>Needs review</h2><p class="empty-state">No unresolved safety records are present.</p>'
    return dashboard_server._page("Overview", body)


def _render_workflows_polished(records):
    ids = sorted({wid for rec in records if (wid := dashboard_server._workflow_id(rec)) is not None})
    body = '<div class="table-wrap"><table><thead><tr><th>Workflow</th><th>Latest state</th><th>Runs</th><th>Last event</th></tr></thead><tbody>'
    for wid in ids:
        rows = [rec for rec in records if dashboard_server._workflow_id(rec) == wid]
        runs = {rid for rec in rows if (rid := dashboard_server._run_id(rec)) is not None}
        latest = rows[-1] if rows else {}
        state = dashboard_server._workflow_state(records, wid)
        safety_kind = next((dashboard_server._safety_kind(rec) for rec in rows if dashboard_server._safety_kind(rec)), None)
        state_html = dashboard_server._badge(safety_kind) if safety_kind else _status_badge(state)
        href = dashboard_server._esc(dashboard_server.quote(wid, safe=""))
        body += (f'<tr><td><a href="/workflow/{href}"><code>{dashboard_server._esc(wid)}</code></a></td>'
                 f'<td>{state_html}</td><td>{len(runs)}</td><td>{dashboard_server._time(latest)}</td></tr>')
    if not ids:
        body += '<tr><td colspan="4">No workflow history is available.</td></tr>'
    return dashboard_server._page("Workflows", body + '</tbody></table></div>')


def _render_workflow_polished(records, workflow_id):
    rows = [rec for rec in records if dashboard_server._workflow_id(rec) == workflow_id]
    if not rows:
        return dashboard_server._page("Workflow not found", '<p class="empty-state">No history exists for this workflow.</p>')
    runs = sorted({rid for rec in rows if (rid := dashboard_server._run_id(rec)) is not None})
    safety = [rec for rec in rows if dashboard_server._safety_kind(rec) is not None]
    kind = next((dashboard_server._safety_kind(rec) for rec in rows if dashboard_server._safety_kind(rec)), None)
    state_html = dashboard_server._badge(kind) if kind else _status_badge(dashboard_server._workflow_state(records, workflow_id))
    body = (f'<p>Workflow: <code>{dashboard_server._esc(workflow_id)}</code>; latest state: '
            f'<strong>{state_html}</strong>; runs: {len(runs)}.</p>')
    if safety:
        body += '<h2>Safety review required</h2>' + dashboard_server._render_safety_table(safety, records)
    body += '<h2>Runs</h2><ul>'
    for run_id in runs:
        wf_href = dashboard_server._esc(dashboard_server.quote(workflow_id, safe=""))
        run_href = dashboard_server._esc(dashboard_server.quote(run_id, safe=""))
        body += f'<li><a href="/runs/{wf_href}?run={run_href}"><code>{dashboard_server._esc(run_id)}</code></a></li>'
    if not runs:
        body += '<li>No run identifier is recorded.</li>'
    return dashboard_server._page("Workflow", body + '</ul>')


def _render_runs_polished(records, workflow_id, run_id):
    rows = [rec for rec in records if dashboard_server._workflow_id(rec) == workflow_id
            and (run_id is None or dashboard_server._run_id(rec) == run_id)]
    if not rows:
        return dashboard_server._page("Runs", '<p class="empty-state">No matching run history exists.</p>')
    body = f'<p>Workflow: <code>{dashboard_server._esc(workflow_id)}</code></p>'
    safety = [rec for rec in rows if dashboard_server._safety_kind(rec) is not None]
    if safety:
        body += '<h2>Safety review required</h2>' + dashboard_server._render_safety_table(safety, records)
    body += '<div class="table-wrap"><table><thead><tr><th>Time</th><th>Event</th><th>Task</th><th>Status</th><th>Attempt</th></tr></thead><tbody>'
    for rec in rows:
        event = rec.get("event") if isinstance(rec.get("event"), str) else "unknown event"
        status = dashboard_server._enum(rec.get("status"), dashboard_server._KNOWN_STATES, "")
        status_html = dashboard_server._badge("unknown") if dashboard_server._safety_kind(rec) == "unknown" else _status_badge(status or "unknown")
        body += (f'<tr><td>{dashboard_server._time(rec)}</td><td>{dashboard_server._esc(event)}</td>'
            f'<td><code>{dashboard_server._esc(rec.get("task_id", ""))}</code></td>'
            f'<td>{status_html}</td><td>{dashboard_server._esc(rec.get("attempts", ""))}</td></tr>')
    return dashboard_server._page("Run history", body + '</tbody></table></div>')


def _render_capabilities():
    items = [
        ("Workflow orchestration", "Run tasks in dependency order and inspect recorded runs."),
        ("Uncertain outcomes", "Unknown and orphaned activity stays visible with a reason for review."),
        ("Human decisions", "Record a decision through the orchestrator decision API; this page is informational."),
        ("Bounded NoEffect retry", "The runtime supports controlled retries for NoEffect outcomes."),
        ("Read-only dashboard", "Dashboard requests use SQLite read-only connections."),
        ("Local model validation", "The release was validated locally with Ollama and qwen3.5:2b."),
    ]
    body = '<p class="muted">NEXUS makes workflow progress inspectable while keeping unresolved outcomes visible.</p><div class="capability-grid">'
    for title, description in items:
        body += f'<article class="capability-card"><h2>{dashboard_server._esc(title)}</h2><p>{dashboard_server._esc(description)}</p></article>'
    return dashboard_server._page("Capabilities", body + '</div>')


dashboard_server._page = _polished_page
dashboard_server._render_overview = _render_overview_polished
dashboard_server._render_workflows = _render_workflows_polished
dashboard_server._render_workflow = _render_workflow_polished
dashboard_server._render_runs = _render_runs_polished
_original_dashboard_dispatch = dashboard_server.DashboardHandler._dispatch

def _dispatch_with_capabilities(self, send_body):
    parsed = dashboard_server.urlsplit(self.path)
    if parsed.path == "/capabilities":
        self._send(200, _render_capabilities(), "text/html; charset=utf-8", send_body)
        return
    return _original_dashboard_dispatch(self, send_body)

dashboard_server.DashboardHandler._dispatch = _dispatch_with_capabilities

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--db", default=DB_PATH)
    ap.add_argument("--seed", action="store_true")
    args = ap.parse_args()
    
    if args.seed:
        run_demo(args.db)
    
    print(f"Starting NEXUS live runtime on 127.0.0.1:{args.port}")
    print(f"Database: {args.db}")
    print("Press Ctrl+C to stop.")
    
    server = ModernDashboardServer(("127.0.0.1", args.port), database_path=args.db)
    server.daemon_threads = True
    server.serve_forever()

