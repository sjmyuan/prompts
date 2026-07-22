# Example: AI-Discovered Insight Becomes Knowledge

**Applies**: `detect-learning-signals` → `determine-provision-target` → `generate-provision-plan` → `review-and-apply`

**Scenario**: During a miniprogram development session, the AI discovers through trial and error that a certain WX API behaves differently than documented. This insight wasn't in any loaded context.

---

## Input (Conversation Excerpt)

```
User: Why isn't wx.getSystemInfoSync() returning the safeArea on this device?

AI: Let me check... According to the WeChat docs, getSystemInfoSync should include
    safeArea. But I notice this device is running WeChat 7.x. Let me verify.

    [AI researches and tests]

AI: I found the issue. On WeChat versions below 8.0, getSystemInfoSync() does NOT
    include safeArea in the return value. The docs don't mention this version
    constraint. You need to use wx.getSystemInfo() with a callback instead, or
    check the WeChat version first and fall back to a manual calculation.

User: That's really helpful — can you save that knowledge somewhere?
```

---

## Step 1: detect-learning-signals

**Signal detected**: AI self-discovered insight — the AI independently found a version-specific behavior not documented in the loaded context and not in the official docs.

**Signal type**: AI self-discovered insight

**Quality gate evaluation**:

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Anyone targeting WeChat < 8.0 will hit this; applies across miniprogram projects |
| Non-obviousness | ✅ Pass | The docs don't mention this version constraint; it's not common knowledge |
| Actionability | ✅ Pass | Can be written as a known limitation with workaround |
| Non-duplication | ✅ Pass | Not in the `develop-miniprogram` skill or any loaded context |
| Specificity | ✅ Pass | Specific: "WeChat < 8.0, getSystemInfoSync, safeArea"; general: applies to all usage of this API |

**Verdict**: ACCEPT.

---

## Step 2: determine-provision-target

**Classification**: Domain-specific knowledge about miniprogram development → `skills/develop-miniprogram/SKILL.md`

**Rationale**: This is platform-specific knowledge that belongs in the miniprogram skill. The skill already has a `<knowledge>` section with platform constraints. This is a known limitation with a workaround.

**Target**: `skills/develop-miniprogram/SKILL.md`, `<knowledge>` section, as a new `<wx-api-limitations>` subsection.

---

## Step 3: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
|---|---|---|---|---|---|
| 1 | `wx.getSystemInfoSync()` does not include `safeArea` on WeChat < 8.0; use async version or version check + fallback | AI-discovered | `skills/develop-miniprogram/SKILL.md` | `<knowledge>` → new `<wx-api-limitations>` | Knowledge entry documenting the version constraint and two workarounds |

**Rationale**: This is platform-specific domain knowledge. The `develop-miniprogram` skill is the most discoverable place for miniprogram developers. If someone encounters this issue, the skill will provide the answer immediately.

---

## Step 4: review-and-apply

Present to user:

> **Lesson to preserve:**
>
> *`wx.getSystemInfoSync()` does not include `safeArea` on WeChat < 8.0.*
>
> **Target**: `skills/develop-miniprogram/SKILL.md` → `<knowledge>` → `<wx-api-limitations>`
>
> **Content to add**:
> ```markdown
> <wx-api-limitations>
> - `wx.getSystemInfoSync()`: On WeChat versions below 8.0, the return value does NOT include `safeArea`. Use `wx.getSystemInfo()` with a callback instead, or check `wx.getSystemInfoSync().version` and fall back to manual safe-area calculation.
> </wx-api-limitations>
> ```
>
> Approve / Modify / Reject?

User approves → write to the skill file.
