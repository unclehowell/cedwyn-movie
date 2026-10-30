# RESUME — how to pick up the Cedwyn documentary (30 Oct 2026)

This repository is the film's storage: clips, audio, subtitles, scripts, the cast/voice/set bible and the manifest the
documentary page reads at run time (https://cedwyn.bucklerfamily.estate/documentary/). Anything an agent needs to make
the next scene is here or listed in ASSETS.md with where it lives.

## 1. Where things are
- `manifest.json` — one entry per released door (`filled`): clip, per-language `video`, `audio`, `subs`, `downloads`,
  `version`, and `cuts` (earlier cuts). The page opens a door when its entry is here. Bump `version` (x.y.z) on every edit.
- `frames.json` — all doors in date order (moment, cast, set, captions, evidence). Over 400 KB: edit with care.
- `scripts/FNNN.json` — per-scene script = the shot list (shot, start, seconds, animate, direction, lines cy/en/es, captions).
- `subs/`, `audio/`, `clips/`, `stills/`, `thumbs/`, `downloads/` — published media.
- `bible/` — the consistency bible: `BIBLE.md` (rules), `CAST_DRAFT.md`, `cast/` (portraits), `sets/` (plates),
  `voices/` (voice samples), `VOICES.json` (voice ids + settings), `MODELS.md` (models, recipes, prices),
  `LIPSYNC-MULTILANG.md` (per-language mouths), `RERENDER-QUEUE.md` (what is next), `SCENE-LIST.md` (all moments).
- `assets/` — per-door production inputs: talking stills, i2v source stills, per-line dialogue audio, ambience, title cards;
  `assets/CAST.json` (who plays whom, per era, with voices) and `assets/SETS.json` (sets and plates). Index: ASSETS.md.
- Page code (player, versions, download): repository unclehowell/cedwyn, branch `cedwyn-movie`, folder `public/`
  (movie.js, documentary.js, download.js, paywall.js, movie.css, index.html). The live site mirrors it into branch `site`,
  folder `documentary/`; a site build can overwrite that mirror, so re-copy after builds (the agent box has a
  `player_reapply.py` for this). Pushes to `cedwyn-movie` do not start a site build.

## 2. Versions and pricing (rule from 30 Oct 2026)
All documentary versions are FREE until the producer names a version as paid quality.
- No dubbing (30 Oct 2026 05:00Z): `0.0.1` of each door is its native-language release, three separately performed
  videos (cy, en, es). Until a door has them, its entry's `version` names the cut that plays (Door 2 `0.0.1-0.0.5`,
  Door 1 `0.0.1-0.0.2`, the dubbed cuts) and `next_version: {"version": "0.0.1", "status": "coming"}` reserves 0.0.1.
- When a new cut replaces the playing one, move the old one into that entry's `cuts` list as
  `{"version": "0.0.1-0.0.N", "clip", "audio", "subs", "video"?, "made", "note"}` with the next N (oldest = `0.0.1-0.0.1`).
- A newly opened door, performed natively in all three languages, gets `0.0.1`. `pricing.all_free` stays `true`.
- The page (page 1.6.0: documentary.js 1.6.0, movie.js 1.5.0) plays every door with no licence or checkout and shows
  each door's versions as hashtag chips under the scene (default cut marked free and selected; `next_version` shown as
  "coming", not playable). A card-size control above the scenes sets small / medium / large for every card.
  Do not create or change payment links or products.

## 3. Making the next scene (the recipe that produced Door 2 v0.0.1)
1. Take the next item in `bible/RERENDER-QUEUE.md` (redos first), then the next unfilled door in `frames.json` order.
2. Script from the door's `moment`: one dated moment, who was there, what was most likely said. No narrator and no
   fourth wall from scene 3 on; characters speak only to each other; side events as on-screen captions. Welsh spoken
   before about 1970 (en/es subtitles; Spanish is Rioplatense), English after, with Welsh accents.
3. Stills: edits of the bible plates and portraits (gpt-image-2.5 edit), speakers in 3/4 profile looking at each other,
   never at the camera. A new era means a new cast (new faces) and new voices.
4. Voices: ElevenLabs `eleven_v4` with `language_code` cy/en/es and the actor's voice id from `bible/VOICES.json`
   (settings there). Transcribe each line back and require a word match of at least 0.8. Voice gender must match the
   on-screen speaker in every track (median pitch: male about 85–160 Hz, female about 180–260 Hz). The voice account is
   full, so rotate existing voices; never reuse one voice for two eras in the same scene.
5. Talking shots: ByteDance OmniHuman 2.0 (fal `bytedance/omnihuman/v2`, about $0.105 per output second), one render per
   language, only where a character speaks on camera. Everything else moves too: Kling 2.5 turbo image-to-video. No stills,
   no slideshows. Archive scans are never animated.
6. English and Spanish videos: NO DUBBING and no mouth re-sync (30 Oct 2026). Each language is its own performance:
   native voice lines and its own OmniHuman 2.0 render of every on-camera talking shot; non-speaking shots are shared.
   Plan and cost per door: `bible/LIPSYNC-MULTILANG.md` (top) and `bible/RERENDER-QUEUE.md` JOB 1.
7. NEVER the Wav2Lip / Piper talking-portrait route (rejected by the producer).
8. Mix with ffmpeg; 720p VP9 webm, about 2 minutes, under 25 MB; cy/en/es VTT subtitles; one video per language.
9. Upload large files in parts through the `fetch-media` workflow (parts mode: blobs on a short-lived `inbox-*` branch,
   joined on main with a sha256 check). Then add the manifest entry (with `version` 0.0.1), build the downloadable
   variants (3 audio x 4 subtitle states), and check the door on a phone-width browser in cy, en and es.

## 4. Budget
Spend only what the render budget has left for the day (the producer's rule: quality first, minimal spend; retakes only
when a shot is visibly wrong). If nothing is left, prepare everything up to the paid render and stop.

## 5. Public-text rules
Never name the producer in public text. Do not use the banned public words (base64 JSON list:
`WyJzYXlzIiwgImNsYWltcyIsICJhY2NvcmRpbmcgdG8iLCAiaGVhcnNheSIsICJ1bnZlcmlmaWVkIiwgImFsbGVnZWQiLCAiZnJhdWQiLCAic3RvbGVuIl0=`);
write "not checked" instead. No heraldry. No likeness of real family members. Never commit API keys, tokens or
passwords: model and voice calls go through the agent's own key proxy. Commits: no force-push; small commits.
