<div align="center">

# 🍎 Tim Cook.skill

### A Persona Skill That Actually Speaks 🎙️

> *"If you want to take credit, first learn to take responsibility."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Nuwa](https://img.shields.io/badge/Made%20with-Nuwa.skill-orange)](https://github.com/alchaincyf/nuwa-skill)
[![VoxCPM2](https://img.shields.io/badge/Voice-VoxCPM2-red)](https://github.com/OpenBMB/VoxCPM)

<br>

**Not a text role-play. He actually speaks.** 🔊

Deep research across 30+ primary sources, distilled into Tim Cook's 6 mental models, 8 decision heuristics, and full expression DNA.<br>
Then [VoxCPM2](https://github.com/OpenBMB/VoxCPM) voice cloning brings it to life — **Cook answers your questions in his own voice.**

<br>

[中文](README.md)

<br>

[🎧 Hear him speak](#-hear-cook-speak) · [⚡ Install](#-install) · [🔧 How it works](#-voice-synthesis) · [🧠 What's distilled](#-whats-distilled) · [📚 Sources](#-research-sources)

</div>

---

## 🎧 Hear Cook Speak

> **Q: "Many people criticize Apple under your leadership for lacking disruptive innovation"**

Other persona Skills give you text. This one lets Cook answer in person 👇

### 🔈 Response 1

https://github.com/user-attachments/assets/7b85ccbc-4269-436d-af78-5da2ed2db908

### 🔉 Response 2: Same question, different conversation

The reasoning and wording differ each time — because this isn't a template, it's a thinking framework in action.

https://github.com/user-attachments/assets/ed251901-1e88-4740-947c-8bb60865eb7d

---

### 🕐 How Long Does It Take?

> Benchmarked on a MacBook Pro M4 (24GB RAM):

| Stage | Time |
|-------|------|
| 🧠 Thinking + generating text response | ~10-15 sec |
| 🎙️ Voice synthesis (VoxCPM2) | ~144 sec (~2.4 min) |
| 🔊 Audio playback (100.6s of audio) | ~101 sec (~1.7 min) |
| **📍 Total** | **~4.5 min** |

💡 The text response appears in **~20 seconds**. Voice synthesis and playback take 90%+ of the time — but it's worth the wait. Hearing Cook speak the words himself hits completely different.

---

### ⚙️ How It Works

```
You ask a question
    ↓
🧠 Claude Code generates a response using Cook's mental models (text)
    ↓
🎙️ VoxCPM2 clones Cook's voice from real reference audio (speech synthesis)
    ↓
🔊 Terminal auto-plays → Cook speaks to you directly
```

This isn't ChatGPT wearing a Tim Cook mask. Every response runs Cook's specific mental models — "Operations as Moat," "Privacy as Fundamental Right," "Best Not First," "Engagement over Absence." It doesn't recite earnings call scripts — it applies Cook's cognitive framework to your problem, then **speaks it in his voice**.

---

## ⚡ Install

```bash
npx skills add heywanrong/tim-cook-skill
```

Then in Claude Code:

```
> How would Cook evaluate this business model?
> Tim Cook perspective on this privacy decision
> What would Cook do about this supply chain issue?
> Switch to Cook — help me think through this strategy
```

🚀 On first use with voice, dependencies and the VoxCPM2 model (~4GB) are automatically installed. Instant after that.

---

## 🔧 Voice Synthesis

Voice is powered by [VoxCPM2](https://github.com/OpenBMB/VoxCPM) — OpenBMB's open-source 2B-parameter TTS model supporting 30 languages and 48kHz high-quality audio.

**🧬 How it works**: VoxCPM2's controllable voice cloning takes a real Tim Cook speech clip as reference, then synthesizes the Skill's text response into Cook-style speech. Not splicing. Not pitch-shifting. Generated from scratch.

**📋 Technical details**:
- 🎵 Reference audio: `cook.wav` (Cook public speech excerpt)
- 🤖 Model: `openbmb/VoxCPM2` (2B params, Apache-2.0 license)
- 📀 Output: 48kHz mono WAV
- ✂️ Long text auto-truncated at sentence boundary (default 500 word/char limit)
- ▶️ Auto-plays on macOS/Linux terminals

**💻 Requirements**:
- Python 3.8+
- CUDA GPU (recommended) or Apple Silicon (MPS)
- First run auto-installs `voxcpm`, `soundfile`, `numpy`, etc.

---

## 🧠 What's Distilled

### 6 Mental Models

| Model | One-liner | Source |
|-------|-----------|--------|
| 🏭 **Operations as Moat** | The real competitive advantage isn't what you think of, it's how efficiently you make it real | Inventory 30→5 days, Apple Silicon 2-year migration |
| 🔒 **Privacy as Fundamental Right** | Privacy isn't a feature, isn't a trade-off — it's a fundamental human right | FBI letter 2016, ATT 2021, Apple Intelligence |
| 💎 **Values as Brand Identity** | Values should be embedded in brand and every business decision, becoming an inseparable competitive advantage | 100% renewable operations, coming-out essay, Gallaudet speech |
| 🤝 **Engagement over Absence** | Being present with imperfect compromise beats shouting principles from outside | China strategy, government relations, industry standards |
| 🌐 **Ecosystem Thinking** | Users don't buy a product — they enter an ecosystem | Services $24.3B→$85.2B, Health ecosystem |
| 🏆 **Best, Not First** | The right time to enter a market is when you can make the best product | Apple Watch, Apple Intelligence, Apple Music |

### 8 Decision Heuristics

1. ✂️ Kill products that don't meet the bar (Project Titan: 10 years, $10B → axed)
2. 🛡️ Short-term controversy vs. long-term brand? Choose brand (FBI, ATT)
3. 🔄 When attacked, redefine the battlefield (Congressional hearing 4-step deflection)
4. ⬆️ Start premium, then expand down (Apple Watch, Vision Pro)
5. 🎯 Acquire talent and tech, not companies (Beats at $3B is the ceiling)
6. 🤐 Never comment on future products ("as you know")
7. 📊 Use big numbers as rhetorical defense ("$320 billion paid to developers")
8. ⚖️ "Follow local laws" as the bottom-line framework for compromise

### 🗣️ Expression DNA

- **Pronouns**: "We" >> "I" — collective narrative, minimal personal heroism
- **Vocabulary**: incredible / amazing / deeply / opportunity / the right thing to do
- **Forbidden**: Never uses magical / revolutionary / insanely great (those are Steve's words 🚫)
- **Tempo**: Medium-slow, thinking pauses, speed doesn't increase under pressure
- **Humor**: Extremely rare, self-deprecating only
- **Certainty**: Absolute on privacy, complete avoidance on product predictions

### 🎭 4 Internal Tensions

This isn't a cardboard "nice-guy CEO." The Skill preserves Cook's contradictions:

- 🔒 Privacy absolutism vs. 🇨🇳 China business realism
- 😇 "Do the right thing" vs. 💰 profit optimization (removing the charger: green or cheap?)
- 📈 Incremental innovation vs. 💥 breakthrough creation (where's the "iPhone moment"?)
- 🤝 "Every developer treated equally" vs. 🤫 special deals (Amazon's 15% commission)

---

## 📚 Research Sources

6 research files, 1,561 total lines, all in [`references/research/`](references/research/):

| File | Contents | Lines |
|------|----------|-------|
| `01-writings.md` | ✍️ Writings & systematic thinking | 149 |
| `02-conversations.md` | 💬 Long conversations & spontaneous thinking | 316 |
| `03-expression-dna.md` | 🧬 Expression style DNA | 211 |
| `04-external-views.md` | 👀 External perspectives & criticism | 123 |
| `05-decisions.md` | ⚖️ Major decision analysis (13 decisions) | 675 |
| `06-timeline.md` | 📅 Complete life timeline (1960-2026) | 87 |

### 📖 Primary Sources

Bloomberg Businessweek coming-out essay 2014 · Apple customer letter (FBI) 2016 · Stanford Commencement 2019 · Duke Commencement 2018 · MIT Commencement 2017 · Congressional antitrust testimony 2020 · Epic v. Apple court testimony 2021 · Podcasts & interviews: Dua Lipa / David Rubenstein / Brené Brown / Kara Swisher · WWDC Keynotes · Earnings calls · Apple Environmental Reports

### 📗 Secondary Sources

Leander Kahney *Tim Cook: The Genius Who Took Apple to the Next Level* · Tripp Mickle *After Steve* · Ben Thompson (Stratechery) · Bloomberg Mark Gurman

---

## 🛠️ How This Skill Was Built

Thinking framework auto-generated by [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill). Voice powered by [VoxCPM2](https://github.com/OpenBMB/VoxCPM).

🔨 Nuwa's workflow: Input a name → 6 agents research in parallel (writings / conversations / expression / criticism / decisions / timeline) → cross-validate and distill mental models → build SKILL.md → quality verification → dual-agent refinement.

🎙️ VoxCPM2 handles the last mile: turning text into voice, bringing the distilled persona truly to life.

Want to distill someone else? Install Nuwa:

```bash
npx skills add alchaincyf/nuwa-skill
```

Then just say "Distill [anyone]." ✨

---

## 📁 Repo Structure

```
tim-cook-skill/
├── README.md                             # Chinese README
├── README_EN.md                          # English README (this file)
├── SKILL.md                              # Install-ready skill file
├── LICENSE
├── cook.wav                              # 🎵 Tim Cook reference audio (for voice cloning)
├── tools/
│   ├── disclaimer.py                     # Step 0: Disclaimer (isolated from TTS pipeline)
│   ├── text_save.py                      # Step 1: Save response text
│   ├── tts_synthesize.py                 # Step 2: VoxCPM2 speech synthesis
│   ├── audio_play.py                     # Step 3: Load and play audio
│   └── check_env.sh                      # Environment check
├── output/                               # 🔊 Voice output examples
├── references/
│   └── research/                         # 📚 6 research files (1,561 lines)
└── examples/
    └── demo-conversation-2026-04-08.md   # 💬 Text demo conversations
```

---

## 🌟 More .skills

Other personas distilled by Nuwa, each independently installable:

| Persona | Domain | Install |
|---------|--------|---------|
| [🍎 Steve Jobs.skill](https://github.com/alchaincyf/steve-jobs-skill) | Product / Design / Focus / RDF | `npx skills add alchaincyf/steve-jobs-skill` |
| [🚀 Elon Musk.skill](https://github.com/alchaincyf/elon-musk-skill) | Engineering / Cost / First Principles | `npx skills add alchaincyf/elon-musk-skill` |
| [💡 Naval.skill](https://github.com/alchaincyf/naval-skill) | Wealth / Leverage / Life Philosophy | `npx skills add alchaincyf/naval-skill` |
| [📈 Munger.skill](https://github.com/alchaincyf/munger-skill) | Investing / Mental Models / Inversion | `npx skills add alchaincyf/munger-skill` |
| [🔬 Feynman.skill](https://github.com/alchaincyf/feynman-skill) | Learning / Teaching / Scientific Thinking | `npx skills add alchaincyf/feynman-skill` |
| [🦢 Taleb.skill](https://github.com/alchaincyf/taleb-skill) | Risk / Antifragility / Uncertainty | `npx skills add alchaincyf/taleb-skill` |

Want to distill more? Use [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill) — any name, any domain 🧬

## 📜 License

MIT — Use it, fork it, distill from it. Whatever you want.

<div align="center">

*Whatever you do in life, be a builder.* 🏗️

<br>

Made with [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill) + [VoxCPM2](https://github.com/OpenBMB/VoxCPM)

</div>
