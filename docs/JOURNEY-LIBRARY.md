# Journey Library — all sources for the Artist Journey Engine (2026-10-25)

> Labeled visual resources for generating multi-stage drawing journeys
> (rough sketch → finished painting). Every entry has: what it is, where
> it lives, what essay it serves, and whether it's a pair or a single image.

## 1. CIRThan dataset — THE gold standard (2,287 pairs)

| What | Detail |
|------|--------|
| Content | 2,287 human-drawn thangka sketches + matching finished thangkas + 3-level text captions |
| Captions | Level 1 (concise subject), Level 2 (mid-detail), Level 3 (full description) |
| Local | `storyboards/cirthan/` (captions + splits, in git) |
| Images | R2 `uploads/samples-thangka/` (already banked as `NNN-plate.png` + `NNN-human.png` zips) |
| Full repo | github.com/jinyuxu-whut/CIRThan (cloned to /tmp) |
| Paper | arxiv.org/abs/2602.08411 (saved: `storyboards/CIRThan-paper.md`) |
| Database | `storyboards/journey-database.json` — 2,287 entries, essay-mapped |
| License | Academic use (check repo LICENSE) |

**Essay mapping (from database):**
- Devotion/Tara: 531 pairs (Green Tara 83, White Tara 59, Avalokiteshvara 33+20+19)
- Rebirth/Yama: 315 (Yamantaka 14, Yama Dharmaraja, Shakyamuni 64+36+15)
- Energy/Vajra: 263 (crossed vajra, Vajradhara, mandala centers)
- Roots/Padmasambhava: 177 (Padmasambhava 30+17, Tsongkhapa 11+10)
- Yogini/Dakini: 110 (Vajrayogini, Simhamukha Dakini, Kurukulla 9)
- Stay-alive/Jambhala: 93 (Yellow Jambhala 30+9)
- Sauh/Manjushri: 75 (Manjushri 13+, Ushnishavijaya 11)
- Dying/Medicine Buddha: 67 (Blue Medicine Buddha 14)
- No-method/Vajrasattva: 61 (White Vajrasattva 10)
- Chakras/Sitatapatra: 24
- Streams/Machig: 8 (Machig Labdrön 8)

## 2. Thangka line-drawing datasets (not yet downloaded)

| Dataset | Content | Where | Status |
|---------|---------|-------|--------|
| **ThangkaDataset_Universal_5081** | 5,081 thangka images, 512×512, for style transfer/colorization/restoration | Kaggle (2.5GB) | **NEEDS DOWNLOAD** |
| ThangkaDataset_SR_82688 | 82,688 pairs (HR/LR), from 128 ultra-high-res originals | Kaggle (42GB) / IEEE DataPort | Too large; the source 128 originals would be better |
| ThangkaDataset_SR_8868 | 8,868 pairs at 512/256/128 | Kaggle (5.6GB) | Possible |
| TK30 / TK1500 | 5 process types, 30 kinds, 15,000+ images (thesis) | Not publicly released | **CANNOT DOWNLOAD** — cite thesis only |
| Regong floral pairs | 1,036 floral sketch↔element pairs | Not released (IET paper) | **CANNOT DOWNLOAD** |

**Priority:** Kaggle `ThangkaDataset_Universal_5081` — smallest usable set, directly pairs with our etch pipeline.

## 3. Iconometry / construction guides (geometric starting points)

These give us the "stage 2: geometric exploration" frame — grids, axes, proportions.

| Source | Content | URL |
|--------|---------|-----|
| **Rubin Museum process** | Full thangka painting process: grid → outline → color → shading → gilding → eyes | rubinmuseum.org/projecthimalayanart/.../process-of-thangka-painting/ |
| **Digital Thangka Grids 101** | Step-by-step grid explanation with Vajrapani example | digitalthangka.com/2015/10/28/grids-101/ |
| **Tibetan Thangka outlines** | 3-stage outline process: blocking → refining → detailing (Dombu/Par-kyang/Che-kyang) | tibetanthangka.org/step-by-step-thangka-creation-process/drawing-thangka-outlines-step-by-step.htm |
| **Matt Jackson** | Iconometric practice: 6 proportional classes (Buddhas, peaceful bodhisattvas, goddesses, wrathful) | online.flipbuilder.com/mpdm/chaj (page 73) |
| **HAR Figure Drawing** | Trengkawa sketchbook: Shakyamuni, Tara, Vajrapani iconometry | himalayanart.org/search/set.cfm?setID=6897 |
| **Chinese textbook** | Head proportions for Buddha/Tara/Vajra (WeChat article) | mp.weixin.qq.com/s/arqnTXSWbx8OKknlhsSOnQ |

## 4. Trika / Kashmir Shaivism final images

| Source | Content | License |
|--------|---------|---------|
| **Robert Beer Archive** (tibetanart.com) | Mahavidya goddesses: Tripura Sundari, Bhairavi, Chinnamasta, Dhumavati, Bagalamukhi, Matangi, Kamala — Newar workshop paintings | Check site terms |
| **MET Museum** | Bhairavi Devi with Shiva (Payag, c.1630), Tripurasundari | CC0 public domain |
| **Wikimedia Commons** | Tripura Sundari category: 35 files (paintings, yantras, temples) | Mixed PD/license |
| **Wikimedia Bhairavi** | Tripura Bhairavi yantra SVG, Mahavidya images | PD |
| **HAR deity pages** | Tara (200+ forms), Mahakala, Vajrapani, Yamantaka — each with iconography + best examples | Browse-only (cite links) |

## 5. Sleeper finds

| What | Where | Why it matters |
|------|-------|----------------|
| **CIRThan captions unused** | `storyboards/cirthan/*.json` | Level 1/2/3 descriptions = ready-made journey prompts at three detail levels |
| **ThangkaDataset_5081** | Kaggle, 2.5GB | Largest free thangka image set for style-transfer + colorization training |
| **Rubin process page** | rubinmuseum.org | The actual artist workflow our 14 axioms should mirror |
| **Robert Beer Mahavidyas** | tibetanart.com | Trika-adjacent goddesses with detailed iconographic descriptions — perfect essay-visual pairing |
| **HAR outline pages** | himalayanart.org | Deity-specific outline drawings (Tara, Mahakala, etc.) — ready sketch references |
| **Trengkawa sketchbook** | HAR setID=6897 | 15/16th century iconometry sketches — historical construction lines |

## 6. Journey prompt template (from CIRThan captions)

Each pair's 3-level caption maps to journey stages:

```
Level 1 (stage 1-2):  "Yellow four-faced Manjushri, crown, teaching mudra..."
                       → what the rough sketch captures
Level 2 (stage 3-5):  "Yellow four-faced Manjushri with teaching mudra, 
                        holding sword/arrow/vajra..., five-Buddha crown..."
                       → construction + proportion correction target
Level 3 (stage 6-12): full description with ornaments, retinue, background
                       → detail + colour + final target
```

This is the prompt chain for `bl image edit` at each stage.
