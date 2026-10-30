#!/usr/bin/env python3
"""F002 native-language talking shots (Door 2, JOB 1): one OmniHuman 2.0 render per talking shot per language.
Usage: TAB_TASK_ID=<task> python3 render.py en|es [--cap 9.6] [--day-limit 10] [--only 2,3] [--dry]
- Sequential (fal renders run one at a time). Skips shots already rendered (oh_<lang>/sNN.mp4).
- Spend guard: our own ledger (every work/cedwyn-movie/**/spend*.jsonl) for the current UTC day plus this shot's
  estimate must stay <= --day-limit, and this run's spend <= --cap. The live-state render meter does NOT see these
  direct vendor-door renders (it read $0 / 0 renders on 30 Oct while the ledger held $26.34), so this guard is the meter.
- Inputs are public raw GitHub URLs of unclehowell/cedwyn-movie (stills + adj.wav), so fal can fetch them.
— Sion's Tab agent"""
import json, os, sys, time, glob, datetime, pathlib, subprocess, requests
W = pathlib.Path(__file__).resolve().parent
MOVIE = W.parent
VC = json.load(open('/home/user/tab/.vendor-capability.json')); B = VC['base_url']
H = {'Authorization': 'Bearer ' + VC['token'], 'x-tab-task': os.environ.get('TAB_TASK_ID', ''), 'content-type': 'application/json'}
RAW = 'https://raw.githubusercontent.com/unclehowell/cedwyn-movie/main/'
MODEL = 'bytedance/omnihuman/v2'; RATE = 0.105
args = sys.argv[1:]; lang = args[0]; assert lang in ('en', 'es')
def opt(name, default):
    return type(default)(args[args.index(name) + 1]) if name in args else default
cap = opt('--cap', 9.6); day_limit = opt('--day-limit', 10.0); dry = '--dry' in args
only = [int(x) for x in opt('--only', '').split(',') if x]
plan = json.load(open(W / 'plan.json'))
out_dir = W / f'oh_{lang}'; out_dir.mkdir(exist_ok=True)
SPEND = W / 'spend.jsonl'; REQ = W / 'fal_requests.jsonl'
def day_spent():
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d'); tot = 0.0
    for f in glob.glob(str(MOVIE / '**' / 'spend*.jsonl'), recursive=True):
        for l in open(f):
            try: r = json.loads(l)
            except Exception: continue
            t = r.get('at') or r.get('t')
            if t and datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d') == today: tot += float(r.get('usd') or 0)
    return tot
def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True, timeout=30).stdout)
run_spent = 0.0
for sh in plan['shots']:
    n = sh['shot']
    if only and n not in only: continue
    dst = out_dir / f's{n:02d}.mp4'
    if dst.exists() and dst.stat().st_size > 10000: print('have', dst.name); continue
    L = sh[lang]; est = round(-(-L['shot_s'] // 1) * RATE, 3)  # billed per output second; round up
    ds = day_spent()
    if ds + est > day_limit or run_spent + est > cap:
        print(f'STOP before shot {n}: day {ds:.2f} + {est} > {day_limit} or run {run_spent:.2f} + {est} > {cap}'); break
    body = {'image_url': RAW + sh['still'], 'audio_url': RAW + L['audio'], 'prompt': sh['prompt']}
    for u in (body['image_url'], body['audio_url']):
        assert requests.head(u, timeout=30).status_code == 200, 'not on raw yet: ' + u
    if dry: print('DRY', n, est, body['audio_url']); continue
    r = requests.post(f'{B}/fal-queue/{MODEL}', headers=H, json=body, timeout=120); r.raise_for_status(); j = r.json()
    rid = j['request_id']; st_url = f'{B}/fal-queue/bytedance/omnihuman/requests/{rid}/status'; res_url = f'{B}/fal-queue/bytedance/omnihuman/requests/{rid}'
    open(REQ, 'a').write(json.dumps({'tag': f'F002native:{lang}:s{n:02d}', 'model': MODEL, 'request_id': rid, 'at': time.time()}) + '\n')
    t0 = time.time(); status = None
    while time.time() - t0 < 1500:
        time.sleep(15)
        try: status = requests.get(st_url, headers=H, timeout=60).json().get('status')
        except Exception as e: print('status err', e); continue
        if status in ('COMPLETED', 'FAILED', 'ERROR'): break
    if status != 'COMPLETED': print('shot', n, 'status', status, 'request', rid, '(not billed if it failed; check before retrying)'); break
    res = requests.get(res_url, headers=H, timeout=120).json(); url = res['video']['url']
    subprocess.run(['curl', '-sL', '--max-time', '300', '-o', str(dst), url], check=True)
    secs = dur(dst); usd = round(max(1, round(secs)) * RATE, 3); run_spent += usd
    open(SPEND, 'a').write(json.dumps({'item': f'F002native omnihuman {lang} s{n:02d}', 'usd': usd, 'at': time.time(), 'seconds': secs, 'request_id': rid}) + '\n')
    print('rendered', n, round(secs, 2), 's', usd, 'USD', round(time.time() - t0), 's wall')
print('run spend', round(run_spent, 3), 'day spend', round(day_spent(), 2))
