# Human Voice: Rules to Kill the "AI Flavor"

Used by **compose-blog** and **refine-style** to keep prose sounding like a real person narrating real experience, not like an essay generator. Apply these rules while composing and run the **Human-Voice Gate** before delivering a draft.

The target feel: a colleague telling a story over coffee — plain words, uneven rhythm, first-person, honest caveats. Reference the exemplars in [style-exemplars.md](style-exemplars.md) for the feel in full.

## 1. Plain-words rule

**Rule**: If you would not say the word to a colleague in conversation, do not write it. Default to everyday words; keep technical terms only where they carry real meaning (e.g., a library name, an algorithm). Do not pad with synonyms to sound smart.

### AI-flavor words blacklist (replace, don't reuse)

| AI-flavor word | Plain replacement |
|---|---|
| 阴险 / 险恶 / 居心叵测 | 挖了坑 / 不好对付 / 坑 |
| 赋能 | 帮助 / 支持 / 让……能 |
| 抓手 / 着力点 | 切入点 / 办法 / 途径 |
| 综上所述 / 总而言之 / 归根结底 | drop it; or 所以 / 说到底 |
| 值得注意的是 / 值得一提的是 | drop it; say the thing directly |
| 让我们一起 / 让我们 | 我们 / 大家 |
| 愈发 / 愈加 | 越来越 |
| 洞悉 / 洞察 / 深谙 | 看穿 / 看出 / 很懂 |
| 倘若 | 如果 |
| 乃至 / 亦 | 甚至 / 也 |
| 缔造 | 做出 / 创建 |
| 弊端 | 问题 / 毛病 |
| 痛点 | 难处 / 麻烦的地方 |
| 场景化 / 场景落地 | 在具体的场景里用 |
| 闭环 / 形成闭环 | 完整走一遍 / 能自洽 |
| 沉淀 | 积累 / 留下来 |
| 底层逻辑 | 背后的原因 / 根本原因 |
| 颗粒度 | 详细程度 / 粗细 |
| 心智模型 | 想法 / 看问题的方式 (keep only if it's the actual topic) |

**Behavior**: If a draft sentence needs a blacklisted word, rewrite the sentence instead of swapping in a near-synonym. Swapping keeps the stiff rhythm.

## 2. Rhythm rule (fixes "too terse")

The reader should feel a natural breathing rhythm. Two failure modes to avoid:

- **Telegraph mode**: many short sentences in a row — reads like bullet points, uncomfortable to read aloud.
- **Pillow mode**: endless long sentences — loses the reader.

**Rule**: alternate sentence length. Do not write 3+ consecutive short sentences; after a short punch sentence, follow with a longer explanation or connecting thought. Use spoken connectives to glue ideas: 不过 / 其实 / 说白了 / 你会发现 / 话说回来 / 有意思的是 / 关键在于.

**Example (telegraph → human):**

> ✗ 这个问题很难。它需要很多经验。很多人都做不好。
>
> ✓ 这个问题其实很难，需要不少经验。你会发现，很多人第一次都会栽在这里——不是能力不够，而是根本没见过类似的坑。

## 3. First-person and reader address

- Write from "我 / 笔者" perspective; address the reader directly ("你", "大家", "你有没有遇到过……").
- Show the reasoning process, including the initial wrong take, then the correction: "起初，我并没有觉得这句话有什么不对。但在分析了几个 Bug 之后，我发现……" Self-correction is what makes prose feel human.
- Allow honest caveats and hedges: "由于作者能力有限，本文不对这些概念做严格区分。" Do not claim false precision.

## 4. Concrete over abstract

Every claim should anchor to something real: a scene, a number, a conversation, a specific tool, a before/after. If a paragraph has no concrete anchor, treat it as a gap and ask the user for the real material.

## 5. No florification

- No parallel (排比) structures for their own sake; no aphorism-per-paragraph (金句收尾); no symmetric section endings.
- No "总结腔" transitions ("让我们看到……", "由此可见……"). Move on naturally.
- Do not make every section end with a neat conclusion. Unevenness is a feature.

## 6. Ending rule

Do not force a summary. End with one of:
- a rhetorical question that leaves the reader thinking ("现在你还会觉得……是在浪费时间么？"),
- an open thought / direction,
- a concrete action for the reader.

## 7. Human-Voice Gate (run in refine-style before delivery)

Executable checklist — not "does it feel okay", but these checks:

1. **Blacklist scan**: no AI-flavor words from the table survive. Count them; if > 0, rewrite those sentences.
2. **Telegraph scan**: find the longest run of consecutive short sentences (≤ 12 characters). If ≥ 3, add connecting thought or merge sentences.
3. **Florification scan**: no parallel triplets, no aphorism closing any section, no 总结腔 transition.
4. **Anchor scan**: every section has at least one concrete anchor (scene, number, example, tool). If missing, mark a gap and ask the user.
5. **Voice scan**: first-person present ("我") present; reader addressed at least once.
6. **Ending scan**: the ending is a question, open thought, or action — not a summary.

Report the results per check: pass / fixed (what changed) / gap (ask user). Only deliver when all checks pass or the gaps are explicitly deferred with the user's consent.
