# ASSETS — index of the reusable production assets (30 Oct 2026)

Everything below is our own AI-made material (invented faces, sets and voices) unless marked. Paths are repo paths.
Not here on purpose: real family likenesses and private photos, public figures' photos, API keys.

## Doors and versions
| Door | Latest (v0.0.1) | Earlier cuts | Script / shot list | Subtitles |
|---|---|---|---|---|
| 1 Place-names before the deeds | clips/F001.v2.webm | v0.0.1-0.0.1 clips/F001.webm | scripts/F001.json | subs/F001.{cy,en,es}.vtt |
| 2 The hill before the records | clips/F002.v6.webm (cy), .en.webm, .es.webm | v0.0.1-0.0.1 F002.v1, -0.0.2 F002, -0.0.3 F002.v5, -0.0.4 F002.v5.1 | scripts/F002.json (19 shots) | subs/F002.v6.* |
| 3 Graves above the Ely (c. 650) | rendered, NOT released (clips/F004.webm) — held for the all-motion redo and a re-voice | — | scripts/F004.json | subs/F004.* |
Former Scene 3 (clips/F003.webm, audio/F003.*) is now the second half of Door 2 (kept as history). Scripts for later
doors: scripts/F005–F009.json (+ VTT drafts). Full moment list: bible/SCENE-LIST.md and frames.json.

## Faces (cast) — assets/CAST.json has who plays whom per era, with voices
- bible/cast/A_MARY … J_ELENA.jpg — the repertory company (reference portraits).
- Era variants: A_MARY_ironage, B_JOHN_ironage (c. 200 BC), A_MARY_1974 (+ _gptedit), B_JOHN_1890s.
- New era cast: K_FARMER_AD200, L_WIFE_AD200 (c. AD 200; different faces from the Iron Age pair).
- Door 3 people: assets/F004/stills/p_monk.jpg, p_woman.jpg.

## Sets — assets/SETS.json
- bible/sets/s01–s13.jpg reference plates (farmhouse, kitchen, church, village, inn, office, court, archive, hill,
  prehistory, 1974–88 house, after demolition, Patagonia); s10_ironage.jpg (Iron Age homestead plate).
- Per-door shot stills (3/4-profile talking stills and image-to-video sources):
  assets/F001/stills (6), assets/F002/stills (Iron Age iL1–6, AD 200 rL1/2/4/5, wide sST2),
  assets/F002/stills_v4 (s02–s11, image-to-video sources),
  assets/F004/stills (13).
- Title and end cards: assets/gfx/card1.png, card2.png, end.png.

## Voices — bible/VOICES.json (ids, model eleven_v4, settings, design prompts, QC scores)
- Samples per actor per language: bible/voices/<ACTOR>_<cy|en|es>.mp3.
- Per-line dialogue: assets/F002/lines (AD 200 talking shots s13/s14/s16/s17 in cy/en/es, v1.0.2 voices),
  assets/F004/lines (L3–L7 cy/en/es).
- Door 3 voice tests: assets/F004/voices (K_BROTHER_*, L_ELIN_*).
- Provider: ElevenLabs (text-to-speech eleven_v4; voices designed with text-to-voice). Welsh fallback: Gemini TTS
  (prebuilt voice Kore), only if a Welsh line fails transcribe-back. No keys are stored here.

## SFX and ambience
- assets/sfx/F004/amb_hill.mp3 (22 s), amb_proc.mp3 (16 s), amb_dusk.mp3 (18 s), amb_spade.mp3 (6 s): beds made for
  Door 3 on 30 Oct 2026 and mixed under its dialogue. The generator was not recorded in the work folder; treat as our
  own generated audio, not a licensed library, and re-check before reuse elsewhere.
- Doors 1–2 carry no separate SFX files: their sound is the dialogue tracks (audio/) plus whatever the rendered video
  carries. Add any new SFX under assets/sfx/<door>/ with its source and licence.

## Models and methods
- bible/MODELS.md (recipes and prices), bible/LIPSYNC-MULTILANG.md (per-language mouths), RESUME.md (start here).

## Not committed, and where it lives
- Raw per-shot renders (OmniHuman and Kling outputs for Door 2, about 120 MB): kept on the production agent's box only.
  Each shot can be re-cut from the published clip using the shot list's start/seconds.
- Real family photographs and likenesses (private) and public figures' photos (licence not cleared): not published.
- Former Scene 3 stills (old AD 200 faces) and the superseded AD 200 stills: not committed (do not reuse).
- Render request logs and spend logs: kept on the agent box (they hold no prompts).
