# Example: Generate an Illustration from a Suggestion

**Scenario**: The user picks the concept-diagram suggestion in an article on AI coding tools and asks the assistant to generate the image. This shows the generate-illustrations flow end to end.

**Applies**: **generate-illustrations**

## Request

**User**: 帮我生成第一节后面那个概念示意图。

**Suggestion block** (target):
```
<!-- 🖼️ Illustration Suggestions -->
位置：紧跟"第一节 前提"之后
类型：概念示意图
内容：左侧"干净上下文"（结构清晰、可追踪）对比右侧"遗留上下文"（噪音、依赖混乱）
作用：让读者一眼看到"前提不成立"的对比
<!-- /Illustration Suggestions -->
```

## Generation

1. 从文章上下文提取关键术语：干净上下文、遗留上下文、可追踪、噪音、依赖混乱。
2. 默认用 SVG 生成对比示意图（用户未要求 PlantUML）。
3. 图内文字使用中文，与正文一致；风格偏专业简洁。
4. 保存为 `assets/why-ai-fails-on-legacy-context-comparison.svg`（与文章同级的 assets 文件夹）。
5. 替换建议块为图片引用加图注：

```
![干净上下文 vs 遗留上下文对比](assets/why-ai-fails-on-legacy-context-comparison.svg)
*图注：前提不成立——遗留上下文无法支撑 AI 编程工具的默认假设*
```

## Validation

- 图片内容与建议块描述一致：左右对比、关键元素齐全。
- 文件名符合命名规则，位于文章同级的 assets 文件夹。
- 建议块已替换为 Markdown 图片引用。

## Optimization

**User**: 右边想再加一条"文档过期没人更新"的噪音。

**Assistant**: 重扫文章上下文，在 SVG 右侧追加该元素，覆盖原文件（文件名不变），输出更新后的文档。
