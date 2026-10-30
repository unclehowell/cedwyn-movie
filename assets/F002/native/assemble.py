#!/usr/bin/env python3
"""Assemble Door 2 native-language cut: python3 assemble.py en|es [--standin] [--out /tmp/x.webm]
Video: shared shots cut from clips/F002.v6.webm at plan.v6_windows (captions/cards included); talking shots = oh_<lang>/sNN.mp4
(1274x722 -> 1280x720), each trimmed to plan.shots[].<lang>.shot_s. --standin uses the Welsh renders (pipeline test only, never publish).
Audio: only this language's lines (adj.wav, lead 0.4 s) at each talking shot's start + ambience bed (F003v1 amb_field looped,
amb_geese over shots 9-10), loudnorm -18 LUFS. Subtitles: <lang> default + the other two languages, timed to this cut.
Output VP9 crf 33 + Opus 96k, must be < 25 MB. Work files in /tmp/f002asm_<lang>. — Sion's Tab agent"""
import json, sys, os, pathlib, subprocess, shutil
W = pathlib.Path(__file__).resolve().parent; MOVIE = W.parent
lang = sys.argv[1]; standin = '--standin' in sys.argv
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else str(W / f'F002.v7.{lang}.webm')
plan = json.load(open(W / 'plan.json')); T = pathlib.Path(f'/tmp/f002asm_{lang}'); shutil.rmtree(T, ignore_errors=True); T.mkdir()
V6 = pathlib.Path('/tmp/cedwyn_f002/F002.v6.webm')
if not V6.exists():
    V6.parent.mkdir(exist_ok=True)
    subprocess.run(['curl', '-sL', '--max-time', '300', '-o', str(V6), 'https://raw.githubusercontent.com/unclehowell/cedwyn-movie/main/clips/F002.v6.webm'], check=True)
STANDIN = {2: 'S2v5/oh/iL1.mp4', 3: 'S2v5/oh/iL2.mp4', 6: 'S2v5/oh/iL3.mp4', 7: 'S2v5/oh/iL4.mp4', 8: 'S2v5/oh/iL5.mp4', 10: 'S2v5/oh/iL6.mp4',
           11: 'F002v4/oh/oh11.mp4', 13: 'F002v6/oh/s13.mp4', 14: 'F002v6/oh/s14.mp4', 16: 'F002v6/oh/s16.mp4', 17: 'F002v6/oh/s17.mp4'}
def ff(*a): subprocess.run(['timeout', '-k', '5', '600', 'ffmpeg', '-v', 'error', '-y', *a], check=True)
talk = {s['shot']: s for s in plan['shots']}
VF = 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=25,format=yuv420p,setsar=1'
CAP1 = {'en': 'Spoken in English; they spoke Brittonic, the ancestor of Welsh', 'es': 'Hablado en español; ellos hablaban britónico, el antepasado del galés'}
def shot1(seg, d):
    """shot 1 for en/es: the raw i2v (S2v5/i2v/aS02.mp4) slowed to the window, with the date card redrawn in this language
    (the v6 card names Welsh as the spoken language)."""
    src = MOVIE / 'S2v5/i2v/aS02.mp4'; k = d / 5.042
    for nm, txt in (('t1', 'c. 200 BC'), ('t2', 'Llandough hill, above the River Ely · Bryn Llandochau'), ('t3', CAP1[lang])):
        open(T / f'{nm}.txt', 'w').write(txt)
    PF = '/home/user/.fonts/PlayfairDisplay.ttf'; SS = '/home/user/.local/share/fonts/SourceSerif4.ttf'
    al = "alpha='if(lt(t,0.6),0,min(1,(t-0.6)/0.8))'"
    vf = (f"setpts={k:.4f}*PTS,{VF},"
          f"drawtext=fontfile={PF}:textfile={T}/t1.txt:fontsize=58:fontcolor=0xE8C873:x=70:y=500:shadowcolor=black@0.6:shadowx=2:shadowy=2:{al},"
          f"drawtext=fontfile={SS}:textfile={T}/t2.txt:fontsize=26:fontcolor=white:x=72:y=580:shadowcolor=black@0.6:shadowx=1:shadowy=1:{al},"
          f"drawtext=fontfile={SS}:textfile={T}/t3.txt:fontsize=19:fontcolor=0xDDDDDD:x=72:y=622:shadowcolor=black@0.6:shadowx=1:shadowy=1:{al}")
    ff('-i', str(src), '-t', f'{d}', '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', str(seg))
segs = []; t = 0.0; cues = []; placed = []
for n, a, b in plan['v6_windows']:
    seg = T / f'seg{n:02d}.mp4'
    if n in talk:
        L = talk[n][lang]; d = L['shot_s']
        src = (MOVIE / STANDIN[n]) if standin else (W / f'oh_{lang}' / f's{n:02d}.mp4')
        assert src.exists(), f'missing render {src}'
        ff('-stream_loop', '-1', '-i', str(src), '-t', f'{d}', '-an', '-vf', VF, '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', str(seg))
        placed.append((t, W / lang / f's{n:02d}.adj.wav'))
        lead = 0.4
        for lg in ('cy', 'en', 'es'):
            txt = {'en': talk[n]['en']['text'], 'es': talk[n]['es']['text']}.get(lg) or talk[n].get('cy_text', '')
            cues.append((lg, t + lead, t + min(d, lead + L['speech_s'] + 0.3), txt))
    elif n == 1 and lang != 'cy':
        d = round(b - a, 3); shot1(seg, d)
    else:
        d = round(b - a, 3)
        ff('-ss', f'{a}', '-i', str(V6), '-t', f'{d}', '-an', '-vf', VF, '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', str(seg))
    segs.append(seg); t += d
total = t
open(T / 'list.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
ff('-f', 'concat', '-safe', '0', '-i', str(T / 'list.txt'), '-c', 'copy', str(T / 'video.mp4'))
# audio
inputs = []; filt = []
for i, (st, wav) in enumerate(placed):
    inputs += ['-i', str(wav)]; filt.append(f'[{i}]adelay={int(st * 1000)}:all=1,apad[d{i}]')
k = len(placed)
inputs += ['-stream_loop', '-1', '-i', str(MOVIE / 'F003v1/audio/amb_field.mp3')]
filt.append(f'[{k}]atrim=0:{total},loudnorm=I=-29:TP=-8:LRA=7,afade=t=in:d=1.5,afade=t=out:st={total - 2}:d=2[bed]')
win = {n: (a, b) for n, a, b in plan['v6_windows']}
# geese over shots 9-10 (start of shot 9 in THIS cut)
t9 = 0.0
for n, a, b in plan['v6_windows']:
    if n == 9: break
    t9 += talk[n][lang]['shot_s'] if n in talk else (b - a)
inputs += ['-i', str(MOVIE / 'F003v1/audio/amb_geese.mp3')]
filt.append(f'[{k + 1}]volume=0.35,afade=t=in:d=1,afade=t=out:st=10:d=3,adelay={int(t9 * 1000)}:all=1,apad[gs]')
filt.append(''.join(f'[d{i}]' for i in range(k)) + f'[bed][gs]amix=inputs={k + 2}:normalize=0:duration=longest,atrim=0:{total},loudnorm=I=-18:TP=-1.5:LRA=11[aout]')
ff(*inputs, '-filter_complex', ';'.join(filt), '-map', '[aout]', '-ar', '48000', '-ac', '2', str(T / 'audio.wav'))
def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}'
for lg in ('cy', 'en', 'es'):
    with open(T / f'{lg}.vtt', 'w') as f:
        f.write('WEBVTT\n\n')
        for j, (l2, a, b, txt) in enumerate([c for c in cues if c[0] == lg]):
            f.write(f'{j + 1}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')
LN = {'cy': 'wel', 'en': 'eng', 'es': 'spa'}; order = [lang] + [x for x in ('cy', 'en', 'es') if x != lang]
sub_in = []; maps = []; meta = []
for i, lg in enumerate(order):
    sub_in += ['-i', str(T / f'{lg}.vtt')]; maps += ['-map', f'{i + 2}:0']
    meta += [f'-metadata:s:s:{i}', f'language={LN[lg]}', f'-disposition:s:{i}', 'default' if i == 0 else '0']
ff('-i', str(T / 'video.mp4'), '-i', str(T / 'audio.wav'), *sub_in, '-map', '0:v', '-map', '1:a', *maps,
   '-c:v', 'libvpx-vp9', '-crf', '34', '-b:v', '1250k', '-maxrate', '1600k', '-bufsize', '3000k', '-row-mt', '1', '-cpu-used', '4', '-deadline', 'good',
   '-c:a', 'libopus', '-b:a', '96k', '-metadata:s:a:0', f'language={LN[lang]}', '-c:s', 'webvtt', *meta, out)
for lg in ('cy', 'en', 'es'): shutil.copy(T / f'{lg}.vtt', pathlib.Path(out).with_suffix('').as_posix() + f'.subs.{lg}.vtt')
sz = os.path.getsize(out); print(json.dumps({'out': out, 'seconds': round(total, 2), 'MB': round(sz / 1e6, 2), 'under_25MB': sz < 25 * 1024 * 1024}))
