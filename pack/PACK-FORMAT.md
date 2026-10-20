# VID PACK FORMAT v1 — the factory unit

One pack = one uploadable. A pack is a directory (zipped for handoff) with
exactly these files. Nothing else. The factory takes a pack → renders stills
(vision model) → runs build.sh → finished MP4. No thinking required at build.

```
packs/<slug>/
  meta.json      # title, audio ref+sha+duration, cluster, status, thumbnail rule
  prompts.md     # one tableau prompt per tale (copy-paste into vision model)
  cue.yaml       # assembly skeleton: tales, starts (or TBD), transitions, chapters
  segments.txt   # machine file build.sh reads: title|audio|still|duration per tale
  build.sh       # proven ffmpeg recipe — loops segments.txt, etch per tale,
                 # 3s black between, outro law at end, outputs <slug>-full.mp4
  README.md      # what's missing in THIS pack (stills? locked audio? starts?)
```

## Rules
1. **Slim by default.** Audio is REFERENCED (path + sha256 + duration), never
   copied — the voice bank is the single source. `build.sh --bundle-audio`
   materializes a fat pack only for off-box handoff.
2. **Prompts are copy-paste ready.** Each tableau prompt is self-contained:
   house, preset, subject, world, manner, accent, composition, forbid, refs.
   Vision model renders 16:9 directly (no crop step at factory).
3. **One still per tale.** Pack lists tales in play order; stills land as
   `stills/<n>-<slug>.jpg` at factory time. build.sh etches each for its
   clip duration, fades to black between tales, outro law at the end.
4. **Starts are TBD until text is staged.** cue.yaml ships with audio duration
   + tale ORDER; start times fill in when the read text lands
   (chars/total × duration first pass, word-timing later). Never invent timings.
5. **Status is explicit.** meta.json `ready_for_factory` is true only when:
   prompts complete + audio staged + starts known. Anything else = prep pack.
6. No binaries in git. Packs live in sleepdraw runs/ (gitignored) or R2 —
   never in a repo tree.

## The two pack kinds (don't confuse them)
- **MVP-0 pack** (`damn: fish/mvp.py` → `projects/<house>/mvp/<slug>/`):
  CONTENT pack — validated script + voices + art prompt + meta. Fails
  closed on `validate.py`. Built by the content engine (runtime stages 1–5).
- **Vid pack** (this format): ASSEMBLY pack — cue + prompts + segments +
  build.sh. Consumes an MVP-0 pack's outputs. Built by `pack/build_packs.py`,
  executed by `fable.build`. The factory runs on vid packs.
