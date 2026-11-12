# turkish-anti-ai-skill

**Turns Turkish text into Turkish a reader understands on the first pass.**

It removes the output pattern where the words are Turkish but the sentence skeleton is English. It rebuilds sentence architecture, TDK spelling and human rhythm instead of swapping a few words.

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-v1.0-blue)](https://agentskills.io/specification)
[![Version](https://img.shields.io/badge/version-1.1.0-informational)](SKILL.md)
[![Tests](https://img.shields.io/badge/tests-51%2F51-success)](docs/TEST_VE_DOGRULAMA_RAPORU.txt)
[![TDK](https://img.shields.io/badge/TDK-Yaz%C4%B1m_K%C4%B1lavuzu-red)](https://sozluk.gov.tr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[**Türkçe**](README.md) · English

|  |  |
| :--- | :--- |
| **What it does** | Repairs Turkish text, writes it from scratch, audits it, and drafts social posts |
| **How it is built** | One instruction file (`SKILL.md`), five reference files, three local Python scripts |
| **Where it installs** | Claude Code, Cursor, Codex, Gemini CLI, Windsurf, OpenCode, Custom GPT |
| **Dependencies** | None. It ships no packages and makes no network calls |

**Contents:** [Problem](#problem) · [Before and After](#before-and-after) · [Install](#install) · [Usage](#usage) · [Architecture](#architecture) · [Register](#register-calibration) · [CLI Tools](#command-line-tools) · [Security](#security) · [Repository Layout](#repository-layout) · [Contributing](#contributing)

> The skill operates on **Turkish text**. This README explains it in English; the rules themselves live in Turkish because they describe Turkish grammar.

## Problem

Large language models are trained mostly on English and rewarded for English rhetorical patterns, so they carry that skeleton into Turkish. Clauses branch rightward, sequential actions get glued with `ve`, every predicate closes with `-DIr` or `-mAktAdIr`, and every sentence lands in the same 18-to-22-word band.

English humanizer tools change surface words: *"yadsınamaz"*, *"âdeta"*, *"kritik bir rol oynamaktadır"*. The defect is not in the dictionary, it is in how the sentence is built. This skill restores Turkish's agglutinative, left-branching structure, follows the TDK spelling guide, and rebuilds human rhythm.

## Before and After

**Input: typical AI Turkish**

> Günümüzün hızla değişen iş dünyasında, uzaktan çalışma modeli sadece geçici bir trend değil, aynı zamanda kurumsal kültürün temel bir yapı taşı haline gelmiştir — ve bu durumun önemi yadsınamaz. Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki, çalışanlara esneklik sağlamak verimlilik üzerinde kritik bir rol oynamaktadır. Bununla birlikte, iletişim kopukluklarını önlemek adına bütüncül bir yaklaşım benimsenmelidir. Sonuç olarak, geleceğin çalışma dünyasında başarılı olmak isteyen kurumlar bu dönüşüme ayak uydurmak zorundadır.

**Output: rewrite mode, blog/essay register**

> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurmak.

<details>
<summary><b>What was repaired (7 items)</b></summary>

1. **Staged opening (P0):** *"Günümüzün hızla değişen iş dünyasında"* is gone; the text starts on the topic.
2. **Negative parallelism (P0):** *"not only X but also Y"* collapsed into one affirmative claim.
3. **Em dash and Tier-1 cliché (P0/P2):** `—`, which TDK allows only in dialogue, and *"önemi yadsınamaz"* were removed.
4. **Passive voice and `ki` calque (P1):** *"Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki"* became an active, direct sentence.
5. **Light verbs and `-mAktAdIr` (P1):** *"esneklik sağlamak... kritik bir rol oynamaktadır"* became *"esneklik tanıdığınızda verimlilik artıyor"*.
6. **Preaching conclusion (P0):** *"Sonuç olarak... ayak uydurmak zorundadır"* was cut.
7. **Factual fidelity:** No number, date or anecdote was added that the source did not contain.

</details>

Both texts come from the regression scenarios in `evals/evals.json` and are re-checked on every push.

## Install

| Environment | Path |
| :--- | :--- |
| Universal (`npx skills`, `gh skill`) | One command into `~/.agents/skills/` |
| Claude Code, Cowork | Plugin marketplace or `~/.claude/skills/` |
| Cursor | `.cursor/rules/turkish-anti-ai-skill.mdc` |
| Codex, Gemini CLI, Windsurf, OpenCode | `~/.agents/skills/` or `~/.gemini/skills/` |
| Custom GPT, Claude Projects, AI Studio | Single file `dist/turkish-anti-ai-skill.full.md` |

### 1. Universal Agent Skills CLI

```bash
npx skills add yucezerey/turkish-anti-ai-skill
```

With GitHub CLI (v2.90+):

```bash
gh skill install yucezerey/turkish-anti-ai-skill
```

### 2. Claude Code and Claude Cowork

As a plugin (recommended):

```text
/plugin marketplace add yucezerey/turkish-anti-ai-skill
/plugin install turkish-anti-ai-skill@yucezerey
```

Or clone it directly:

```bash
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.claude/skills/turkish-anti-ai-skill
```

### 3. Cursor

```bash
mkdir -p .cursor/rules
curl -sL https://raw.githubusercontent.com/yucezerey/turkish-anti-ai-skill/main/.cursor/rules/turkish-anti-ai-skill.mdc \
  -o .cursor/rules/turkish-anti-ai-skill.mdc
```

### 4. Codex, Gemini CLI, Windsurf

```bash
# Shared .agents/skills/ directory
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.agents/skills/turkish-anti-ai-skill

# Gemini CLI only:
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.gemini/skills/turkish-anti-ai-skill
```

### 5. Web interfaces

`dist/turkish-anti-ai-skill.full.md` merges every reference table into one file. Paste it into Custom GPT **Instructions**, Claude Projects **Project knowledge**, or the AI Studio system prompt.

> `npx skills` and `gh skill` download only `skills/turkish-anti-ai-skill/`: `SKILL.md` plus `references/`. The scripts are not part of that package.

## Usage

There is no command to memorize. The skill triggers from its own `description` field:

| Mode | When | Example prompt |
| :--- | :--- | :--- |
| `rewrite` (default) | A text exists and needs repair | *"Humanize this blog post and strip the AI feel: `<text>`"* |
| `write` | Writing Turkish from scratch | *"Write about cache invalidation in distributed systems, technical register."* |
| `audit` | Report only, no rewriting | *"Do not change this corporate text, just report AI-Turkish and TDK errors."* |
| `post` | LinkedIn, Instagram, X | *"Write a LinkedIn post introducing this project, with a hook, hashtags and a CTA."* |

You do not have to name the mode. It is inferred from the request. In `audit` mode the text stays untouched; only P0/P1/P2 signals are quoted back.

## Architecture

Every rule belongs to one of three layers. The layer sets how hard the intervention is.

| Layer | Focus | Signal it catches | Transformation |
| :--- | :--- | :--- | :--- |
| **1. Composition (P0)** | Opening, closing, rhetoric | *"Günümüzün hızla değişen..."*, *"not X but Y"*, *"Sonuç olarak..."*, triple adjective lists | Open with a scene or a thesis, drop negative parallelism, cut the moralizing close |
| **2. Sentence architecture (P1)** | Syntax and morphology | Right-branching clauses, the Indo-European `ki`, reflexive `ve`, `-DIr / -mAktAdIr` inflation, redundant `bir` and `tarafından` | Left-branch with participles, converb system (`-Ip, -IncA, -dIkçA`), pre-verbal focus slot, pro-drop, evidential `-mIş` |
| **3. TDK and surface (P2)** | Punctuation, spelling, terms | Em dash, en dash, commas around `ve/veya`, semicolon bridges, forced translations (*"uç nokta"*), suffix errors (*"cache'ı", "SQL'ı"*) | Separate `[TDK]` rules from `[Üslup]` preferences, apply compound-word rules, inflect loanwords by Turkish pronunciation (`cache'i, SQL'i`) |

Details live under `references/`; `SKILL.md` carries only the workflow and decision points (136 lines). The model reads reference files on demand.

| File | Contents |
| :--- | :--- |
| [`references/sentaks-ve-morfoloji.md`](references/sentaks-ve-morfoloji.md) | Sentence geometry, left branching, converbs, focus slot, `-DIr`/`-mAktAdIr`, pro-drop, light verbs |
| [`references/ai-turkcesi-sozlugu.md`](references/ai-turkcesi-sozlugu.md) | 60+ patterns in three tiers plus chat residue |
| [`references/tdk-ve-noktalama.md`](references/tdk-ve-noktalama.md) | Five absolute punctuation bans, TDK compound words, phonetic suffix table |
| [`references/register-ve-ornekler.md`](references/register-ve-ornekler.md) | 5 registers × 9 dimensions, end-to-end before/after pairs |
| [`references/sosyal-medya.md`](references/sosyal-medya.md) | LinkedIn, Instagram, X register: hook geometry, budgets, emoji, CTA, publish gate |

## Register Calibration

Natural Turkish has more than one tone. Inverted word order in a contract reads as sloppiness; `-mAktAdIr` in a blog post reads as a robot. The skill assigns one of five profiles before touching the text.

| Register | `-mAktAdIr` (per 100 words) | Inverted sentences | Composition intervention |
| :--- | :--- | :--- | :--- |
| Blog / Essay / Social | 0.0 - 0.5 | 2-3 per 400 words | Full |
| Technical / Engineering | 0.0 - 1.0 | None | Moderate |
| Corporate / SaaS / Business | 0.0 - 1.0 | None | Moderate |
| Academic / Official / Legal | 0.5 - 2.5 | Forbidden | Closed (keep the document skeleton) |
| Literary / Narrative | 0.0 - 0.5 | Rhythm-driven | Full |

These ranges are not corpus-calibrated; they are the starting values inside `scripts/detect_tr_ai.py`. If the user supplies a writing sample (few-shot), that sample outranks every default.

## Command Line Tools

Three scripts, no third-party packages.

### `detect_tr_ai.py`: deterministic scanner

It does not detect authorship. Human-written official Turkish can hit the same patterns, and a well-steered model can avoid all of them. What it gives you is a score plus an itemized list that says where editing should start.

```bash
python3 scripts/detect_tr_ai.py text.md                  # readable report
python3 scripts/detect_tr_ai.py text.md --json           # machine-readable
python3 scripts/detect_tr_ai.py article.md --register akademik-resmi
```

`--register` accepts `blog-deneme`, `teknik`, `kurumsal`, `akademik-resmi`, `edebi-anlati`. With a register set, `-mAktAdIr` density is compared against that register's target band.

What it measures:

- AI clichés (Tier-1/2/3) and TDK-based surface errors
- `-mAktAdIr` density and runs of three sentences ending in the same suffix
- Sentence-length variation (burstiness CoV): 0.40 and above is the target, below 0.35 is mechanical

Deliberate behaviours: code fences, inline code, HTML comments and bare URLs are skipped. In academic/official register, phrases like `söz konusu` and `bu bağlamda` are listed as info rather than warnings. Below 50 words no "out of band" warning is emitted for `-mAktAdIr`. Duration words such as `yıllardır` are not counted as `-DIr`.

Its limit: regex and simple statistics only catch surface traces. Left branching, converb choice and register fit are sentence-architecture decisions that stay with the model and the reader.

### `denetle_post.py`: publish gate

A social post has its own budget: the first 210 characters, a hashtag range, one CTA, and a ban on invented numbers. This script measures the post before it goes out and closes the gate on any `hata` (error).

```bash
python3 scripts/denetle_post.py post.md                    # one post
python3 scripts/denetle_post.py calendar/                  # all posts
python3 scripts/denetle_post.py --takvim calendar/         # cross-post repetition and balance
python3 scripts/denetle_post.py post.md --canli            # link health (K17)
python3 scripts/denetle_post.py post.md --json             # machine-readable
python3 scripts/denetle_post.py post.md --katı             # warnings close the gate too
python3 scripts/denetle_post.py post.md --kural-kapat K12,K14
python3 scripts/denetle_post.py post.md --config gate.json
```

Also available: `--platform linkedin|instagram|x`, `--tur tanitim|teknik|ipucu|carousel`, and `--metin` for inline text instead of a file.

<details>
<summary><b>Rule catalogue (K0-K17)</b></summary>

| Rule | What it measures | Default |
| :--- | :--- | :--- |
| K0 | Platform budget, hook, hashtags, paragraphs, emoji, CTA, repetition | error / warning |
| K1 | Required sections | error / warning |
| K2 | Carousel: 6 slides, TR + EN parity | error |
| K3 | Slide length (cover 10, slide 14 words) | warning |
| K4 | Turkish letters or missing translation in EN lines | warning |
| K5 | Type-A repository link present in the body | error (LinkedIn) |
| K6 | Fork disclosure | warning |
| K7 | Technology and license claims | error / warning |
| K8 | Private leak (install command, link, privacy note) | error |
| K9 | Email, phone, IBAN, token, IP, local path | error |
| K10 | Technology name spelling (`Github` → `GitHub`) | warning |
| K11 | Feature dump (4+ items, 6+ element sentence) | warning |
| K12 | Internal jargon (`Faz 3`, `W46`, `sprint`) | warning |
| K13 | Mojibake | error |
| K14 | Version and status claim note | warning |
| K15 | Cross-post repetition | warning / error |
| K16 | Content pillar balance | info |
| K17 | Live link health (`--canli`) | error / warning |

`error` blocks publishing (exit code 1), `warning` does not, `info` only logs. A config file overrides per rule: `{"K12": "bilgi"}`. `--kural-kapat` grants a one-off exception and leaves it visible in the report.

</details>

### `run_tests.py` and `build_dist.py`

```bash
python3 scripts/run_tests.py      # 51 tests: package, detector, post gate, evals
python3 scripts/build_dist.py     # build dist/ and sync skills/
```

`run_tests.py` writes its report to `docs/TEST_VE_DOGRULAMA_RAPORU.txt` (`--no-report` disables it). The report is generated, never hand-edited. The same command runs in GitHub Actions on every push and pull request, followed by `build_dist.py` and `git diff --exit-code` to catch an out-of-sync `dist/`.

## Security

The package is Markdown instructions plus three local Python scripts. The scripts make no network calls, spawn no commands and import nothing outside the standard library.

| Script | What it does | Writes files |
| :--- | :--- | :--- |
| `scripts/detect_tr_ai.py` | Reads a text file, prints a report | No |
| `scripts/denetle_post.py` | Audits posts and calendars; `--canli` sends HTTP requests to URLs | No |
| `scripts/run_tests.py` | Checks package, detector and eval scenarios | Only `docs/TEST_VE_DOGRULAMA_RAPORU.txt` |
| `scripts/build_dist.py` | Builds `dist/`, syncs `skills/turkish-anti-ai-skill/` | Only inside the repo |

During sync, `build_dist.py` deletes and recreates `skills/turkish-anti-ai-skill/references/`. Security scanners (Socket, Snyk) may flag that line as a file deletion. It is guarded: the script stops without deleting anything if the target is not exactly that folder or is a symlink. Apart from `--canli`, no script makes an outbound request.

## Repository Layout

```text
turkish-anti-ai-skill/
├── SKILL.md                           # Orchestrator: YAML frontmatter + 4-step workflow
├── skills/turkish-anti-ai-skill/      # Compatibility dir for npx skills and plugin packagers
├── references/                        # Progressive-disclosure Turkish linguistics database
│   ├── sentaks-ve-morfoloji.md        # Left branching, converbs, focus, -DIr/-mAktAdIr, pro-drop
│   ├── ai-turkcesi-sozlugu.md         # Tier-1/2/3 dictionary (60+ patterns) and chat residue
│   ├── tdk-ve-noktalama.md            # [TDK]/[Üslup] rules, spelling, phonetic suffix table
│   ├── register-ve-ornekler.md        # 5 registers × 9 dimensions, before/after pairs
│   └── sosyal-medya.md                # Post register: hook, budget, CTA, gate rules
├── scripts/
│   ├── detect_tr_ai.py                # Deterministic AI-slop, TDK and CoV scanner
│   ├── denetle_post.py                # Social post publish gate (K0-K17)
│   ├── run_tests.py                   # Package + detector + post gate + eval tests
│   └── build_dist.py                  # Builds dist/ and skills/
├── evals/evals.json                   # Factual-fidelity and anti-slop regression scenarios
├── dist/turkish-anti-ai-skill.full.md # Single file for web interfaces
├── docs/
│   ├── ARASTIRMA_VE_MIMARI_RAPORU.md  # Linguistics and anti-AI architecture research
│   ├── DENETLE_POST_GELISTIRME_PLANI.md
│   └── TEST_VE_DOGRULAMA_RAPORU.txt   # Generated by run_tests.py
├── .cursor/rules/turkish-anti-ai-skill.mdc
├── .claude-plugin/plugin.json         # Claude Code / Cowork manifest
├── .github/workflows/tests.yml        # CI: tests + dist sync
├── AGENTS.md · CLAUDE.md · GEMINI.md  # Agent adapters
├── CONTRIBUTING.md
└── LICENSE                            # MIT
```

## Contributing

If you spot a new AI-Turkish pattern, a translated-sounding SaaS phrase, or a TDK edge case, open an issue or a pull request.

Claims need sources. A `[TDK]` tag requires an entry from the spelling guide, a `[Dil bilgisi]` tag requires an example where breaking the rule changes the meaning, and a `[Üslup]` tag requires a named register exception. Personal taste alone is not enough. The template and verification steps are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

After a change:

```bash
python3 scripts/build_dist.py && python3 scripts/run_tests.py
```

## License

[MIT](LICENSE). Use it, change it, ship it.

Author: [Yüce Zerey](https://github.com/yucezerey) · Agent Skills Specification v1.0
