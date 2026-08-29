# Example: Ingest Notes, Collect Ideas, and Find Gaps

**Scenario**: The user pastes rough notes on AI coding tools failing on legacy systems and wants them shaped into a blog. This shows the ingest, collect, and gap-finding flow before any draft.

**Applies**: **ingest-existing-content**, **collect-ideas**, **identify-gaps**

## Ingest Existing Content

**User input** (pasted notes):
> 工具需要高质量上下文，遗留代码上下文全是噪音。团队用 AI 工具最大痛点：改完的代码没人敢合。脚手架项目演示效果好，真实项目翻车。也许要"先建上下文，再用 AI"，而不是直接用。有篇文章说上下文工程比提示词工程更重要（链接没存）。

**Assistant** — classification summary:
- 前三句：成型观点，可直接作正文骨架。
- 第四句：草稿片段，有想法但表达粗糙，移入素材区。
- 第五句：零散笔记 + 引用缺口，移入素材区并标注缺口。

**Document** (excerpt showing placement):
```
<!-- 📌 Title & Summary -->
<!-- /Title & Summary -->

<!-- 📋 Materials -->
- 也许要先建上下文、再用 AI，而不是直接用
- 有篇文章说上下文工程比提示词工程更重要（链接缺失 → 缺口）
<!-- /Materials -->

<!-- ❓ Gaps -->
- 引用缺口：第五句提到"有篇文章"，缺链接，待用户补充
- 论据缺口：三条成型观点缺少具体案例支撑
<!-- /Gaps -->

<!-- 💡 Assistant Notes -->
- 风格参照：短句、口语化、带真实场景
<!-- /Assistant Notes -->

# 为什么 AI 编程工具在遗留系统上效果差

工具需要高质量上下文，遗留代码的上下文全是噪音。

团队用 AI 工具的最大痛点是：改完的代码没人敢合。

脚手架项目演示效果好，真实项目却翻车。
```

**Assistant** closing questions:
- 这三条成型观点里，哪条最接近你想表达的核心？
- 有没有一个真实案例可以支撑其中一条？
- 那篇"上下文工程"的文章链接方便发我吗？

## Collect Ideas

**User**: 触发点是上周我帮一个团队试点 Copilot，两周后他们悄悄退回老流程了。

**Assistant**: restates — 所以核心不是"工具不好用"，而是"团队默认工具能直接理解烂代码"这个前提错了。深挖问题：
- 是什么具体场景让你觉得"前提不对"？
- 你希望读者看完之后有什么改变？

**Document** — materials block appended:
```
<!-- 📋 Materials -->
- 也许要先建上下文、再用 AI，而不是直接用
- 有篇文章说上下文工程比提示词工程更重要（链接缺失 → 缺口）
- 触发案例：帮团队试点 Copilot，两周后悄悄退回老流程
- 核心判断：前提错在"团队默认工具能直接理解烂代码"
<!-- /Materials -->
```

## Identify Gaps

**Assistant** — gap list with questions:
- 论据缺口：缺退回案例的具体原因 → 问：团队退回时说了什么理由？
- 结构缺口：文章缺结论方向 → 问：你希望读者带走一个行动建议，还是一个开放问题？
- 读者视角缺口：管理者读者会问"这意味着什么" → 建议补一段"对团队的启示"。

**Document** — gaps block updated:
```
<!-- ❓ Gaps -->
- 引用缺口：缺"上下文工程"文章链接
- 论据缺口：缺退回案例的具体原因
- 结构缺口：缺结论方向（行动建议或开放问题）
- 读者视角缺口：缺"对团队的启示"，服务管理者读者
<!-- /Gaps -->
```
