# Multi-language lip-sync — research, plan, rule (30 Oct 2026, worker c52025d8)

Owner ask, WhatsApp 02:39 GMT 30 Oct (m:5a76d0ad), verbatim: "Surely you can make 3 variations of the webm in the 3 different languages so lipsync always matches the spoken language. I'm sure there's been innovations in ai for doing this recently. Research a bit first. Plan a big. Then attempt it."

## What exists (video-to-video: keep the shot, redraw only the mouth to new audio)
All reachable through our fal vendor proxy (VENDOR_CAPABILITY.md, fal registered). Prices are the model pages' own, read 30 Oct 2026.

| Tool | fal id | Price | Clip limits | Notes / source |
|---|---|---|---|---|
| Kling LipSync (audio-to-video) | fal-ai/kling-video/lipsync/audio-to-video | $0.014 per 5 s increment (page text; one snippet reads per second, to confirm on our receipt) | video 2–10 s, 720p/1080p, ≤100 MB; audio 2–60 s, ≤5 MB | language-agnostic (phoneme-free audio model). https://fal.ai/models/fal-ai/kling-video/lipsync/audio-to-video |
| sync. lipsync-2 | fal-ai/sync-lipsync/v2 | $3.00 / min ($0.05/s) | long clips | zero-shot, keeps speaker style; strongest published quality. https://fal.ai/models/fal-ai/sync-lipsync/v2 |
| sync. lipsync-2-pro | fal-ai/sync-lipsync/v2/pro | $5.00 / min ($0.083/s) | long clips | finer teeth/beard detail. https://fal.ai/models/fal-ai/sync-lipsync/v2/pro |
| LatentSync | fal-ai/latentsync | $0.20 per video up to 40 s, then $0.005/s | | diffusion lip-sync, open model. https://fal.ai/models/fal-ai/latentsync |
| MuseTalk | fal-ai/musetalk | per compute second | | real-time, lower fidelity. https://fal.ai/models/fal-ai/musetalk |
| sync lipsync 1.9 | fal-ai/sync-lipsync | $0.70 / min | | older generation |
| HeyGen / Rask-style "video translate" | not on our proxy | subscription | | they also re-translate and clone the voice; we already have our own cy/en/es lines and voices, so we only need the mouth step |
| OmniHuman 2.0 per language | bytedance/omnihuman/v2 | ≈ $0.105/s | ≤ ~30 s audio | full re-render from the still: best match to our cy shots but 3× the cost; fallback only |
| Wav2Lip / Piper | — | — | — | REJECTED by the owner 27 Oct. Never. |

All of these drive the mouth from the audio waveform, not from text, so Welsh is not a special case for them; the quality risk is the dub's timing, not the language.

## Verdict
- PRIMARY: Kling LipSync — cheapest by far, 720p native, fits our ≤10 s talking shots (longer shots split at a pause into ≤10 s pieces and re-joined).
- FALLBACK: sync. lipsync-2 ($0.05/s) when a Kling result smears the mouth or drifts; lipsync-2-pro for close-ups that need it. OmniHuman per language only if both fail on a shot.

## Plan and cost per scene (≈ 95 s of talking per ~2 min scene)
- cy video: OmniHuman as now (≈ $10 per scene incl. stills/i2v).
- en + es videos: Kling on every talking shot per language ≈ 2 × 95 s → about $0.27–$2.70 per scene depending on how Kling is billed (to be confirmed on the first receipts); with lipsync-2 instead ≈ $9.50.
- Order: Door 2 now (being re-voiced anyway) → Door 1 inside its all-motion redo → every future door by default.
- Verification per shot per language: audio-proof on the track, then 3 frames per shot checked against the line (open mouth on vowels, closed on silence).

## Manifest shape (for the player)
Each `filled` entry keeps `clip` (the Welsh video, back-compat) and gains
`"video": {"cy": "clips/F00N.webm", "en": "clips/F00N.en.webm", "es": "clips/F00N.es.webm"}`.
Each language file carries ONLY its own audio track. A missing language key means: play `clip` with the separate `audio[lang]` track (old behaviour).
