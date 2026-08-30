# Example: Compose a Draft, Track References, Suggest Images, Review, and Refine

**Scenario**: The user has collected material on AI coding tools and legacy systems and asks for a draft. This shows compose, reference-tracking, image-suggestion, review, and style-refinement.

**Applies**: **compose-blog**, **track-references**, **suggest-images**, **review-draft**, **refine-style**

## Compose the Blog

**User**: 素材差不多了，帮我出一版草稿吧。

**Assistant**: 建议用"深度分析型"（问题 → 分析 → 结论），因为你有明确论点加触发案例，适合严密论证。确认后生成草稿，开头部分：

```
<!-- 📌 Title & Summary -->
标题备选：
1. 为什么 AI 编程工具在遗留系统上总是"翻车"？
2. AI 编程工具的隐形前提：干净的上下文
3. 先建上下文，再用 AI：遗留系统上的工具落地

摘要备选：
1. AI 编程工具不是不好用，而是它的隐形前提——干净上下文——在遗留系统里根本不成立。
2. 遗留系统为什么会让 AI 编程工具失效？本文拆解前提、案例与落地路径。
<!-- /Title & Summary -->

<!-- 💡 Assistant Notes -->
- 引言：钩子句 + 背景 + 价值预告，指出核心问题与读者所得
- 第一节：论点最清晰，论据略薄，建议补一个真实案例
- 结论：目前偏开放，可考虑给管理者读者一个行动建议
<!-- /Assistant Notes -->
```

(正文省略，展示引言、三个章节与结论。)

**Assistant** — feedback questions:
- 哪个标题最接近你想传达的核心价值？
- 引言第一句能抓住你的目标读者吗？
- 哪个部分最符合你的真实想法，哪个偏差最大？

## Track References

**User**: 链接找到了：https://example.com/context-engineering

**Assistant**: 已将该资料以链接形式嵌入「第二节」段落：上下文工程比提示词工程更重要（[上下文工程：为什么比提示词工程更重要](https://example.com/context-engineering)）。

**Document** — gaps block updated:
```
<!-- ❓ Gaps -->
- （已填）引用缺口：素材区"上下文工程"文章已嵌入第二节
<!-- /Gaps -->
```

## Suggest Images

**Assistant** — added illustration-suggestion blocks:

```
<!-- 🖼️ Illustration Suggestions -->
位置：紧跟"第一节 前提"之后
类型：概念示意图
内容：左侧"干净上下文"（结构清晰、可追踪）对比右侧"遗留上下文"（噪音、依赖混乱）
作用：让读者一眼看到"前提不成立"的对比，省去一段文字描述
<!-- /Illustration Suggestions -->
```

(第二个建议块指向"落地路径"流程图。)

## Review the Draft

**User**: 标题 2 比较好；第一节那个案例，我补一下细节：那个团队退回的原因是"没人敢合改完的代码"。

**Assistant**:
1. 标题锁定为 2 号候选，刷新 Title & Summary 区块。
2. 补入退回案例细节到第一节，充实论据。
3. 扫描全文，更新助手注：第一节论据已补强，弱点转向"为什么前提错"的推理过渡；结论仍偏开放，建议给管理者一句行动建议。
4. 直接在文档文件中应用修改，只汇报改动摘要，不重复输出全文。

## Refine Style

**User**: 帮我把语言再顺一顺，重点服务技术读者。

**Assistant** — applies **refine-style**:
- 删除两处生硬的过渡词与翻译腔句式。
- 加强每个章节的开头句，结论先行。
- 对技术读者保留实现细节；补充一句"这意味着什么"给管理者读者。
- 结论以行动建议收尾，并留一个开放问题。

(直接在文档文件中应用修改，汇报改动摘要与下一步方向。)
