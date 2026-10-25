# CEDWYN MOVIE — daily scene run (RUNNER v1.0.0, 25 Oct 2026)

One run per day makes ONE frame (scene) of the Cedwyn film, about 2 minutes (90–150 s), 720p webm, and opens its door on
cedwyn.bucklerfamily.estate/movie/. Paths below are under /home/user/tab/work/cedwyn-movie/ unless they start with `repo:`
(= github.com/unclehowell/cedwyn-movie, storage only). Tools: `tools/cedwyn_movie.py` (model calls, scripts, translation, VTT, GitHub
commit/upload, HubSpot), `tools/build_chronology.py`, `BIBLE.md` (cast, voices, sets, recipe), `bible/MODELS.md` (model ids, costs).

Rules for every run: editorial rules in memory/sion-cedwyn-editorial.md and memory/sion-cedwyn-wales-argentina.md (records as ingredients;
court's view first; no findings or accusations about named private individuals; public bodies may be criticised); never name the producer
(he is "the Grandson" on screen); banned public words: says, claims, according to, hearsay, unverified, alleged, fraud, stolen; no heraldry;
commits end "— Sion's Tab agent"; never mark a HubSpot task SENT and never create a Gmail draft for CEDWYN MOVIE tasks; zero spend beyond the
renders (≈ $4–5/scene; never upgrade a plan); wrap shell in `timeout -k 5 120` (renders `timeout -k 5 600`); disk: stop if under 1.5 GB free,
delete raw renders after muxing. Send Sion nothing yourself; your report goes to the root.

## 0. Start
- `tab_list_tasks`: if another "CEDWYN MOVIE RUN" is running, stop.
- `df -h /home/user` ≥ 1.5 GB free, else report and stop.

## 1. Read the producer's prompt FIRST
- Fetch `repo:PROMPT.md` (raw, cache-busted). Record its git sha in the run log. Everything under "Current steer" overrides this runner
  (style, pacing, cast, priorities). If it asks for a change of plan (e.g. "slow down the 1980s", "more scenes at the church"), apply it to the
  frames that are not yet filled, and say what you changed in the report.

## 2. Re-check the chronology against Cedwyn (every day)
- `python3 tools/build_chronology.py` (sources: work/chronology/chronology.json — refresh it from the live /wayback/chronology/ data if
  newer —, the evidence register, 1000 Cuts, the HyperFrames reel cites; findings that have become Cedwyn pages leave `excluded[]`).
  Read `CHANGES.json` (added / removed / changed ids).
- New or changed events:
  - dated inside a frame already filled → append to `repo:manifest.json` `left_out_register` with reason "found after the frame was made",
    and add it to the NEXT unfilled frame's `revision_citations` so its script cites it in a short "on paper, later" beat (Sion: "If something
    is left out of a video clip cite the event later in a revision to a later event in the script").
  - dated inside an unfilled frame → add its id to that frame's `events` (scripts not yet written pick it up; a written script is rewritten).
  - a big new run of events (> 3 beats) → split the affected unfilled frame into two; renumber only unfilled frames, at most once a week, and
    update their HubSpot subjects. Filled frames keep their numbers forever.
- Removed events: never silently drop — mark in the frame and the register why (merged / corrected / moved).
- Every event must sit in exactly one frame (assert it); save `FRAMES.json` with a bumped patch version.

## 3. Take the next unfilled frame N
- N = the lowest frame with no `repo:manifest.json` `filled[]` entry.
- Script: if `scripts/FNNN.json` is missing, write it: `python3 tools/cedwyn_movie.py script N` (Opus writes en with every event cited and
  the banned-word check; cy/es machine translations). Then read the HubSpot task for frame N (`HUBSPOT.json` ids; batch tasks for 11+) and merge
  accepted hive edits (latest semver in its CHANGELOG; facts first, then wording). Note the version used.
- Keep scripts 10 frames ahead: write the script for frame N+10 and create its HubSpot task in the hive format
  "[TURN: ChatGPT v0.1.0] CEDWYN MOVIE · Frame NNN: <logline>" (body ≤ 6 KB: status block, logline, events, evidence, English script;
  regex the id from a 201 body_head; never blind-retry a create — search subjects first). Record the id in `HUBSPOT.json`.

## 4. Produce (take the day; quality first) — BIBLE.md §5 in detail
1. Stills for every shot (16:9) as edits of `bible/cast/*` and `bible/sets/*` (+ era edits saved back to the bible once, reused after).
   Look at each still beside its reference; redo any that drifts (face, building, era, heraldry).
2. TTS: every line in en, cy, es with the actor's voice (`bible/VOICES.json`, eleven_v4); transcribe-back ≥ 0.8.
3. OmniHuman 2.0 (`bytedance/omnihuman/v2`) for 2–4 talking close-ups (English lip-sync; cy/es dubbed). Use it "occasionally" as the producer asked:
   most lines play over stills, document props, reactions and landscapes.
4. Optional ambient i2v (Kling 2.5 turbo / Seedance) for 1–2 landscape shots.
5. HyperFrames assembly at 1280×720 (work/hf-series kit; `npx hyperframes render`, `HFW=1` under pressure): date card, shots, document overlays
   with the real quoted words and evidence ids, end card "Cedwyn · A tab.bot production". Timeline from the real TTS durations.
6. ffmpeg: `clips/FNNN.webm` = VP9 crf 32–34 + 3 Opus tracks (cym, eng default, spa) + WebVTT tracks; `audio/FNNN.<lang>.webm` (Opus) per
   language; `subs/FNNN.<lang>.vtt` from the real timings; `stills/FNNN.jpg` poster. < 25 MB each, else raise crf, else split FNNN-a/-b.
7. QC (all must pass): duration 90–150 s; −16 to −20 LUFS and no unscripted silence > 1.5 s (`node /home/user/tab/audio-proof.mjs inspect`);
   three frames checked against the portraits; every event id of the frame cited on screen or in dialogue; banned-word grep on the three
   VTTs; nothing invented about named real people.
8. Anything the clip leaves out (a shot that failed, an event cut for time) → `left_out` on the manifest entry with its id and reason, and into the
   next frame's `revision_citations`.

## 5. Upload and open the door
- `spec = upload_media({...clips/audio...}, msg)` then `wait_media(spec)` (parts branch → fetch-media workflow → main). Small files (VTTs,
  poster, scripts, frames.json) with `commit_files(MOVIE, 'main', {...}, msg)`.
- Add the entry to `repo:manifest.json`: `{"n": N, "clip": "clips/FNNN.webm", "audio": {"cy": "audio/FNNN.cy.webm", "en": …, "es": …},
  "subs": {"cy": "subs/FNNN.cy.vtt", …}, "poster": "stills/FNNN.jpg", "seconds": S, "made": "<UTC>", "script_version": "v…",
  "prompt_sha": "…", "left_out": [...]}` and commit. The page reads the manifest live: the door opens with no Cedwyn build.
- Check: fetch the clip's raw URL (Range request 206) and load cedwyn.bucklerfamily.estate/movie/ at 390 px with headless Chromium: door N open, plays,
  subtitles toggle, audio toggle switches language.
- HubSpot: append a CHANGELOG line to the frame's task ("rendered from vX.Y.Z, clip FNNN, S s") — keep the custom status, never SENT.
- Weekly (Mondays): if the page itself changed (theme files), commit to branch `cedwyn-movie` of unclehowell/cedwyn only when no other worker is
  committing to that repo; the theme is already registered in themes.json (do not touch other themes or shared files).

## 6. Report (to the root, 4 lines)
Door N open (title, dates, length) with the page link; what the producer's prompt changed; chronology changes today (added / moved / left out → cited in
frame M); spend estimate and anything only Sion can supply. The root tells Sion in one short bubble.

## Schedule (proposed; the root creates it)
Daily at 06:00 Europe/London: spawn ONE worker (kind "video", goal starting "CEDWYN MOVIE RUN", references BIBLE.md, RUNNER.md, FRAMES.json,
bible/MODELS.md) that follows this file. The door is open by the 08:00 morning brief. About 60–120 minutes per run.
