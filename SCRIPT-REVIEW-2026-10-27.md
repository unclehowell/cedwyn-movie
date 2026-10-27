# SCRIPT REVIEW — 27 Oct 2026

Scope: FRAMES.json (148 frames), scripts F001–F012 (JSON + VTT), F002-v2 plan, sets, chronology PX events. Checked against the catalogue (305 items), CHRONOLOGY.json, case-file-v2, the family timeline and the owner rules of 25–27 Oct. Nothing was rendered.

**Result: 16 inaccuracies fixed** (5 high, 7 medium, 4 low), **5 open or noted items**, and rule breaches in every scripted frame (table 3).

## 1. Inaccuracies fixed
| scene / line | current text (before) | what the record shows (source) | fix | severity |
|---|---|---|---|---|
| F006 whole frame | 'A thousand-year lease': the third-party papers' early dates spoken as fact; the estate's papers presented as the title's start | EV-0002/EV-0003 are third-party papers under forensic examination (case-file-v2). Editorial ban on those dates in public text | Rewritten as "The family's account, and the papers in question": the 1667 family account (CH-0003), 1824 Stewart survey as the first record found so far (EV-0211), the papers named as under examination, no dates spoken | high |
| F006 Land Registry officer | An invented Land Registry officer speaking lines | No record of such words; a public body in a live dispute | Officer removed; Nia and the Grandson carry the scene on camera | high |
| F003 whole frame | Villa steward, villa woman, villa range shown | Owner depiction rule 27 Oct: no villa. CH-0174 (GGAT/BAR 188) does describe a villa, a known tension, see research/roman-F003.md | Rewritten 'Same hill, new neighbours': Romano-British farm family in Welsh, Nia hook, 3 archive talking shots | high |
| F004 title + lines | 'From villa to monastery'; monk's villa line; Nia's 'villa's hill' | Owner rule (no villa); PX-03 wording derived | Retitled 'Graves above the Ely'; villa lines removed | high |
| FRAMES F055, F129 | A living family member named; F055 described a private pregnancy photograph | Editorial rule: never name the family or children | Name removed; photo description neutral; the person not named or shown | high |
| F004 church c.650 | Stone church drawn c.650 | No stone-church evidence for that date in the catalogue; early churches of the period were most likely timber | Drawn as timber, marked interpretation | medium |
| F010 consecration | 'spring 1866' | Church consecrated 12 July 1866 (catalogue) | 12 July 1866 | medium |
| F005 Sutton | 'Sutton on the coast' | Geography rule: the hill and the Sutton reference are inland/down the Vale | 'Sutton, down the Vale' | medium |
| FRAMES F073 | No numbers for the 29 Apr 1988 eviction attempt | Five bailiffs and about fifteen police; chainsaw; withdrawal after four hours (ghf-19880429-1/-2, EV-0088, EV-0089) | Numbers added with source_note | medium |
| FRAMES F082 | Demolition date carried as 'Nov 1988' in one source | 6 Dec 1988 (EV-0629 RCAHMW NA/GL/88/49, EV-0104, EV-0105); NA/GL/89/208 types 'Nov. 1988' | date_note: 6 Dec 1988, the November entry kept as an open question | medium |
| FRAMES F056, F057, F097 | 'a Roman villa' in loglines | Owner depiction rule; the record's word kept in the catalogue only | 'possible Iron Age roundhouse and Roman-period remains' / 'Roman-period dig', villa_note added | medium |
| F001 line (0-30 s) | Catalogue range spoken in the first 30 s | Hook rule: no catalogue IDs spoken in the first 30 s | Moved to the document overlay after 0:30 | medium |
| F007, F008 lines (0-30 s) | DMAT/279 and 'D B E 1-2' spoken in the first 30 s | Hook rule | Removed from the spoken lines; kept on overlay | low |
| F009 tithe line | Typo 'Landough' | Place name Llandough (cy Llandochau) | Corrected | low |
| Sets s10, s13 (FRAMES + tools/cedwyn_movie.py) | s10 listed a villa; s13 'Puerto Madryn coast' with green, flowery images | Owner rules: no villa; Patagonia arid steppe, no flowers | s10 Romano-British fields; s13 arid steppe; tool SCRIPT_SYS carries the 27 Oct rules | low |
| CHRONOLOGY PX-01 to PX-03 | Derived period text uses the word villa | CH-0174 wording | Record left as written; depiction_note added | low |

## 2. Open or noted (not changed)
| scene / line | current text | what the record shows | action | severity |
|---|---|---|---|---|
| F005 monastic founding | The founding story rests on a 2011 letter | Single later source; no earlier record found yet | Kept, phrased as tradition; open | open |
| F082 demolition month | 6 Dec vs 'Nov. 1988' | Two RCAHMW entries differ | Use 6 Dec; November noted | open |
| F008 John Gedrick | Gedrick named beside the Williams family as occupier | Catalogue entries are not yet reconciled | Left; check before render | low |
| F011 'Legal Wiki' | Reference to the research wiki by an informal name | Name style | Left; tidy at render | low |
| Villa record vs depiction | The film shows no villa; the archaeology describes one | CH-0174 | Depiction rule applied; frames reporting the dig use neutral words; documented | note |

## 3. Rule breaches (owner rules 27 Oct: accent, Welsh first, on-camera narrators, subtitles, hook)
| scene | breach | fix |
|---|---|---|
| F001 (live) | 6 voiced stills; narrators not on camera; no hook | Rule pass: 4 OmniHuman, hook shot; v0.3.0; re-render (RERENDER-QUEUE) |
| F002 (live) | English dubbed over Welsh lips; villa words in audio; card-first opening | v2.1 plan (F002-v2-PLAN.json, $5.07) |
| F004, F005, F007-F012 | Voiced stills (5, 5, 7, 7, 3, 2, 4, 5 shots); no hook | Converted to OmniHuman (narrators) or moving i2v; hooks added; v0.2.0 |
| All scripts | No accent or spoken-language fields; narrator voices not thick Welsh | Per-line spoken/accent; cy before ~1970; voices recast (BIBLE cast table) |
| All working VTTs | 490 of 574 cues failed the subtitle check | Re-split: 23 of 1,295 cues still flagged, all inside the fixed live timings of F001/F002 (cleared by the re-renders) |

## 4. Versions
- Scripts: F001 v0.3.0; F003–F012 v0.2.0; F002 v0.1.2 is replaced by the v2.1 plan.
- FRAMES.json v1.2.0 (`changelog_1_2_0`): titles, loglines and i18n for F003/F004/F006, F055/F129, F056/F057/F097, F073, F082, sets s10/s13, `spoken_language` on all frames (49 cy, 99 en), `release_planned`.
- BIBLE.md "Owner 27 Oct" section, PROMPT.md Current steer, RUNNER.md script checker, research/roman-F003.md, RERENDER-QUEUE.md.
- Backups of every pre-review file are kept locally.

— Sion's Tab agent
