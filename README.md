# Cedwyn — the film

*A tab.bot production.*

This repository is **file storage only** for the Cedwyn film: it is not a website and nothing here is built or published as pages.
The film's page lives in the Cedwyn site's movie theme, which plays these files inline.

## What is here

| path | what |
|---|---|
| `PROMPT.md` | the production prompt. Edit it to steer the production: the daily scene run reads it first, every day, before it touches a scene. |
| `frames.json` | the frame map: every planned ~2-minute frame (scene) with its number, dates, chronology events, evidence ids, setting, cast, title and logline. |
| `manifest.json` | which frames are filled: clip, audio tracks and subtitles per frame, length, date made, and anything left out (to be cited in a later frame's revision). |
| `scripts/Fnnn.json` | full dialogue scripts (English, Welsh, Spanish; Welsh and Spanish are machine translations awaiting review). |
| `subs/Fnnn.<lang>.vtt` | WebVTT subtitles in cy / en / es. |
| `clips/Fnnn.webm` | the frame: 1280×720 VP9 video with three Opus audio tracks (cy, en, es), under 25 MB. |
| `audio/Fnnn.<lang>.webm` | each language track on its own (Opus), for the page's audio toggle. |
| `bible/` | the consistency bible: cast reference portraits, set references, voices, palette and the per-scene recipe. |

## Rules for every frame

The story is told by characters talking about what is happening on paper and around Llandough. The script is the chronology: every dated event is placed in a frame,
and anything a clip leaves out is recorded in `manifest.json` and cited in a later frame. Records are presented as ingredients with their evidence ids; where a court
ruled, the court's view comes first.

Commits are made by the daily scene run and end with "— Sion's Tab agent".
