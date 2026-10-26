# CEDWYN — consistency bible (v1.0.0, 25 Oct 2026)

*A tab.bot production.* Everything a daily scene run needs so that the last frame shows the same people, voices, buildings and landscapes as the first.
Files: `bible/cast/`, `bible/sets/`, `bible/voices/`, `bible/VOICES.json`, `bible/test/` (the test clip).

## 1. The repertory company

A small company of ten actors plays the people of Llandough in every age — the Williams line, the village voices, the officials. One fixed reference portrait per actor;
an age or costume change is always an **edit of that portrait**, never a new face. Real family members are played by these actors with **no attempt at likeness** until the
family supplies photographs and approves. The present-day researcher is never named: he is "the Grandson". No heraldry anywhere (crests, arms, shields, emblems on chairs or seals).

| id | role | plays | reference | voice (ElevenLabs, eleven_v4, cy/en/es) |
|---|---|---|---|---|
| A_MARY | the Williams woman | Mary (Nancy) Williams (b. 1913) and the earlier Williams women (Amy Williams 1860s); the roundhouse mother in the prologue | `cast/A_MARY.jpg` | `uZ2F64pQ4awvfM38w9V9` |
| B_JOHN | the Williams man | the John Williamses (1841–1949); Iron-Age elder, villa steward, monk in the prologue | `cast/B_JOHN.jpg` | `ft0WkOZmCF3NFIbyp280` |
| C_FRED | the in-law | Frederick Buckler (1908–1967) | `cast/C_FRED.jpg` | `XZLLk8LKa4NX4HsuCPiS` |
| D_BILLY | the son / the Grandson | William (Billy) Buckler as boy and man; in the 2020s "the Grandson" (never named) | `cast/D_BILLY.jpg` | `bi1ppGIASFluT4PbdRza` |
| E_AGENT | the Man from the Estate | offices only: Bute estate agent, company agents, solicitors, overseers, Land Registry and council officers | `cast/E_AGENT.jpg` | `2Jm4mkkEDFemeO085c56` |
| F_GWEN | the village voice (fictional) | Gwen, who reads the papers aloud in every era | `cast/F_GWEN.jpg` | `UmQyXL5FYPCIbuUQZKqK` |
| G_DAI | the landlord (fictional) | Dai, innkeeper/carter, Gwen's sparring partner | `cast/G_DAI.jpg` | `bjneJtpl97NGdlhAINbN` |
| H_CLERK | the Court | clerks, magistrates and judges; lines quote judgments verbatim | `cast/H_CLERK.jpg` | `nzPzKJE9RrymxViKMFhm` |
| I_NIA | the Archivist (fictional) | Nia, who reads each document with the Grandson | `cast/I_NIA.jpg` | `XEKRPEMYQPpow8lb1XZN` |
| J_ELENA | the Patagonian (fictional) | Elena, guide at Puerto Madryn (Argentina frames) | `cast/J_ELENA.jpg` | `VJAA1A5gQklMXZjm0smO` |

Era edits made so far: `A_MARY_1974.jpg` (aged ~60, nano-banana-pro edit — canonical for 1960s–80s), `B_JOHN_1890s.jpg` (gpt-image edit). Make each new era once,
check it against the reference, save it as `cast/<ID>_<era>.jpg`, and reuse it for every later scene of that era.

## 2. Voices

One designed voice per actor, used for all three languages so the timbre never changes (`VOICES.json`): model **eleven_v4** with `language_code` cy / en / es,
settings stability 0.5, similarity 0.8, style 0, speaker boost on. Welsh fallback for a line that fails transcribe-back: Gemini 3.8 Flash TTS (voice Kore), accepting a timbre change.
Every line is transcribed back (OpenAI gpt-4o-transcribe) and must match the script at ≥ 0.8; years are spelled out in words.

## 3. Sets and eras

| id | set | reference |
|---|---|---|
| s01 | Great House Farm / Tŷ Mawr farmhouse exterior and yard (c.1850–1974) | `sets/s01.jpg` |
| s02 | the farmhouse kitchen (inglenook, flagstones, dresser) | `sets/s02.jpg` |
| s03 | St Dochdwy's church and churchyard, Llandough | `sets/s03.jpg` |
| s04 | Llandough village street and green | `sets/s04.jpg` |
| s05 | the village inn (taproom) | `sets/s05.jpg` |
| s06 | a Cardiff office (Bute estate office / solicitors / company office, by era) | `sets/s06.jpg` |
| s07 | a courtroom (magistrates, county court, High Court, Court of Appeal, by era) | `sets/s07.jpg` |
| s08 | the archive reading room (modern records office) and the Grandson's desk | `sets/s08.jpg` |
| s09 | Llandough hill landscape over the Ely, Leckwith woods and Cardiff Bay | `sets/s09.jpg` |
| s10 | prologue: the hill in prehistory/Roman/early-medieval times (roundhouse, villa, monastery) | `sets/s10.jpg` |
| s11 | the farmhouse 1974–88: aged, threatened, development around | `sets/s11.jpg` |
| s12 | the site after demolition (1988–2026): housing estate, verge, green | `sets/s12.jpg` |
| s13 | Puerto Madryn coast, Patagonia (Argentina) | `sets/s13.jpg` |

Rule: **every era of a set is an edit of its establishing reference** (s11, the farmhouse c. 1980, is an edit of s01 — same building, same viewpoint, aged, housing behind).
Next improvement: condition s01/s02/s11 on the real archive photographs of Tŷ Mawr held in the Cedwyn media register (measured survey 1974, press photographs 1974–88) so the
farmhouse matches the real building; until then the farmhouse is an evocation, not a likeness.

Eras: prologue (s10, the hill before the records) → 1824–1915 Bute years (s01 c.1900, s02, s03, s04, s05, s06 19th c.) → 1916–1968 (s01/s02 mid-century, s06 20th c.) →
1969–1988 (s11 threatened farmhouse, s07 courts, s06 company offices) → 1988 onwards (s12 the site after demolition) → 2026 (s08 archive, s12, s04) → Argentina (s13).

## 4. Palette and lens

Muted Glamorgan greens, slate grey, lime-wash white, oak brown, warm tungsten interiors; gold (#d4b25a) only for titles and date cards. 35 mm lens look, natural light,
slight film grain, shallow depth of field for talking close-ups, slow push-ins on stills, no handheld shake. Date/era card at the start of each scene; "A tab.bot production" end card.
Documents appear as props on the table; the real quoted words are overlaid by HyperFrames with their evidence id — never invented legible text in a generated image.

## 5. Per-scene recipe (proved in pre-production)

1. Read `PROMPT.md` first, then the frame's script (en/cy/es), cast and set ids, and the frame's HubSpot task (latest version).
2. Stills, 16:9 (1920×1072 → 1280×720), 8–14 per scene, always edits of the bible references (people: nano-banana-pro/edit for age, gpt-image-2.5/edit for costume/scene; places: gpt-image-2.5/edit of `sets/sNN.jpg`). Look at each one against its reference. ≈ $1/scene. Keep ≤ 4–6 jobs in flight.
3. Dialogue audio: every line × 3 languages with the actor's voice (eleven_v4), transcribe-back QC, joined per language. ≈ $0.3–0.5/scene.
4. Talking shots: **OmniHuman 2.0** (`bytedance/omnihuman/v2` on fal; image + audio → talking video; $0.105 per output second; ~7–8 min per render; generated faces accepted) for 2–4 close-ups of 5–12 s, English lip-sync; cy/es are dubbed over them. Inputs must be https URLs (host audio through `fal-ai/ffmpeg-api/loudnorm`). Make the still 16:9 so the output is widescreen.
5. Ambient motion (optional): Kling 2.5 turbo or Seedance image-to-video for 5 s landscapes; otherwise slow push-ins in HyperFrames.
6. Assembly: HyperFrames (`npx hyperframes render`, the hf-series kit, `HFW=1` under memory/disk pressure) at 1280×720 — clips, stills, document overlays with their evidence ids, date card, end card. No burned-in subtitles.
7. Mux: VP9 crf 32–34 (raise to 36 near the limit), three Opus tracks (cym, eng default, spa) and the WebVTT tracks embedded; sidecar `subs/Fnnn.<lang>.vtt` from the real TTS timings; `audio/Fnnn.<lang>.webm` per language for the page; `stills/Fnnn.jpg` poster. Under 25 MB, else split into `Fnnn-a` / `Fnnn-b`.
8. QC: ffprobe (90–150 s), `audio-proof.mjs inspect` (−16 to −20 LUFS, no unscripted silence > 1.5 s), three frames compared with the portraits, transcribe-back per language, banned-word grep on all subtitles, every event id of the frame cited.
9. Cost ≈ $4–5 per scene (≈ $600–750 for 148 frames); machine time ≈ 25–40 min per scene.

## 6. Storage and upload

Large files are uploaded in parts: parts of ≤ 1.8 MB go to a short-lived `inbox-*` branch,
the repository's `fetch-media` workflow joins them on main, checks sha256 and the 25 MB limit, commits ("— Sion's Tab agent") and deletes the branch. Proved with the test clip on 25 Oct 2026.

## Chronology rule (Sion, 11:45 GMT 26 Oct 2026) — read before every script and render

- Tŷ Mawr is first named in the record we have found in the 1824 David Stewart survey of the Bute Glamorgan estates (EV-0211). In the family's account, Tŷ Mawr was acquired in 1667.
- Never present "the 1547 lease" or "the 1552 Bute deed" as Tŷ Mawr records. Bute estate and other third-party documents are never shown as records of Tŷ Mawr before 1824: on screen they are Bute (or third-party) papers whose application to Tŷ Mawr is under forensic examination, and the Bute freeholds are under forensic examination for validity.
- Outside narratives (websites, catalogue summaries, secondary books) are tested on screen, not repeated. Our film asserts and defends our evidence and our interpretation.
- Names have been played on (Cydwin, Cydfin, Cedfin, Ked Fen, Tŷ Mawr, Great House, Great House Farm; Llandough-juxta-Penarth CF64 vs Llandough near Cowbridge CF71): the register is the e-book "Enwau" on cedwyn.bucklerfamily.estate/ebooks/.
- F006 ("A thousand-year lease") is re-titled and must be rewritten to this rule before it is rendered; F005's hand-over line and F006's continuity are updated.
