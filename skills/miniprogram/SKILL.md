---
name: miniprogram
description: Develop WeChat Miniprogram features following platform conventions and best practices. Use this skill whenever working on any WeChat Miniprogram project.
---

<when-to-use-this-skill>
- Adding, modifying, or deleting pages or subpackages in a miniprogram
- Creating or updating custom components
- Implementing Canvas 2D drawing, image processing, or export features
- Working with WeChat APIs (storage, navigation, media, album, network)
- Debugging WeChat Miniprogram-specific runtime errors
- Configuring routing, TabBar, or subpackage split strategy
- Applying design systems or SCSS styling
</when-to-use-this-skill>

<knowledge>

<project-structure>
**Typical directory layout**:
```
miniprogram/
  app.ts / app.json / app.scss   ← global entry, design tokens, TabBar config
  components/                    ← globally shared custom components
  pages/                         ← main package (TabBar and entry pages)
  subpackages/                   ← lazy-loaded feature subpackages
  utils/                         ← shared helpers and service modules
  data/                          ← static assets such as JSON config files
typings/                         ← project-level TypeScript type declarations
```

- `app.json` is the source of truth for all registered pages and subpackage roots.
- Main package: TabBar pages and globally shared components only.
- Feature non-tab pages: one subpackage per feature under `subpackages/<feature>/`.
</project-structure>

<page-lifecycle>
**Lifecycle hooks**:
- `onLoad(options)` — init data, read storage, parse route params
- `onShow()` — refresh state that may have changed while the page was hidden
- `onReady()` — DOM ready; safe to query canvas nodes with `wx.createSelectorQuery`
- `onUnload()` — clean up timers or listeners
- `onPullDownRefresh()` — call `wx.stopPullDownRefresh()` when done
- `onReachBottom()` — use for pagination/infinite scroll
</page-lifecycle>

<navigation-apis>
**Navigation API**:
| Destination | API |
|---|---|
| TabBar page | `wx.switchTab` |
| Non-TabBar page (push) | `wx.navigateTo` |
| Replace current page | `wx.redirectTo` |
| Go back | `wx.navigateBack` |
| Return data to caller | EventChannel via `getOpenerEventChannel()` |

**Data-passing pattern selection**:
| Situation | Pattern |
|---|---|
| Small scalar (ID, flag) | Route query param |
| Structured result after `redirectTo` | `wx.setStorageSync` → `wx.getStorageSync` |
| In-flight object within one flow | `getApp().globalData` (clear when flow ends) |
| Return value from child picker page | EventChannel |
| Persist across app restart | `wx.setStorageSync` with stable key |
</navigation-apis>

<wechat-api-reference>
**User feedback** (adjust text to the project's language):
- Toast success: `wx.showToast({ title: '保存成功', icon: 'success' })`
- Toast error: `wx.showToast({ title: '操作失败，请重试', icon: 'none' })`
- Confirmation: `wx.showModal({ title, content, success(res) { if (res.confirm) { ... } } })`

**Key APIs**:
- Media: `wx.chooseMedia({ count, mediaType, sourceType, success })`
- Save to album: `wx.saveImageToPhotosAlbum({ filePath, success, fail })` — requires `scope.writePhotosAlbum`
- Network: `wx.request<T>({ url, method, data, header, success, fail })` — domain must be in the server allowlist
- Permission: check with `wx.getSetting`, request with `wx.authorize`; show modal guidance if denied
- System info: `wx.getSystemInfoSync()` — call once per scope, cache the result

→ See `examples/wechat-api-usage.md` for network request, permission authorization, and media code templates.
</wechat-api-reference>

<platform-constraints>
- Storage total quota: **10 MB**; store only serialisable metadata, not binary blobs.
- Canvas: always `type="2d"`; the legacy `wx.createCanvasContext` API is deprecated and must not be used.
- Banned in all committed code: `console.log`; hardcoded `appId` or secrets; `wx.getSystemInfoSync()` inside loops.
</platform-constraints>

<example-selector>
Load only the example directly relevant to the current task to minimize context size.

- **Adding a new page to a subpackage** — use with **configure-subpackage**: [examples/add-subpackage-page.md](examples/add-subpackage-page.md)
- **Implementing a Canvas feature** (node acquisition, drawing, export) — use with **canvas-setup-and-draw**: [examples/canvas-feature.md](examples/canvas-feature.md)
- **Creating a custom component** (observers and lifetimes) — use with **create-component**: [examples/custom-component.md](examples/custom-component.md)
- **Inter-page data flow** (route params, storage, globalData, EventChannel) — use with **add-page**: [examples/inter-page-data-flow.md](examples/inter-page-data-flow.md)
- **Storage patterns** (read/write/trim with error handling) — use with **manage-storage**: [examples/storage-patterns.md](examples/storage-patterns.md)
- **WeChat API usage** (network, permission, media) — use with **add-page** or **create-component**: [examples/wechat-api-usage.md](examples/wechat-api-usage.md)
- **Typing a miniprogram codebase** (tsconfig, strict mode, shared types, globalData) — use with **apply-typescript-patterns**: [examples/apply-typescript-patterns.md](examples/apply-typescript-patterns.md)
- **Applying SCSS design system** (design tokens, BEM naming, rpx vs px) — use with **apply-styling**: [examples/apply-styling.md](examples/apply-styling.md)
</example-selector>

</knowledge>

<capabilities>

<add-page>
Steps to create and register a new page:
1. Read `app.json` to determine whether the page belongs in the main package or a subpackage.
2. Create `<page>.wxml`, `<page>.ts`, `<page>.scss`, `<page>.json` in the correct directory.
3. Add `"usingComponents": {}` in the page `.json`; add `"renderer": "webview"` if the page uses Canvas.
4. Register in `app.json` → `"pages"` (main package) or `"subpackages[].pages"` (subpackage, path relative to subpackage root).
5. Use `this.setData()` for all data mutations; never mutate `this.data` directly; batch calls, avoid in loops.
6. Encode complex route params with `encodeURIComponent(JSON.stringify(obj))`; decode in `onLoad(options)`.

→ See `examples/inter-page-data-flow.md` for route param encoding, storage hand-off, globalData, and EventChannel patterns.
</add-page>

<create-component>
Steps to build a custom component:
1. Create `<comp>.wxml`, `<comp>.ts`, `<comp>.scss`, `<comp>.json` with `"component": true` in the `.json`.
2. Expose the public API through `properties`; never reach into parent page state.
3. Communicate upward exclusively via `this.triggerEvent()`.
4. Use BEM class names scoped to the component name.
5. React to property/data changes with `observers`; use `lifetimes` (`attached`/`detached`) for setup and teardown.
6. Register the component using an absolute path (e.g. `/components/my-comp/my-comp`).

→ See `examples/custom-component.md` for full file templates, observers, and lifetimes patterns.
</create-component>

<canvas-setup-and-draw>
Steps to implement a Canvas 2D feature:
1. In `onReady`, call `wx.getSystemInfoSync()` once and cache `pixelRatio`.
2. Inside `wx.nextTick`, acquire the canvas node via `wx.createSelectorQuery().select('#id').fields({ node: true, size: true })`.
3. Set physical dimensions: `canvas.width = logicalWidth * pixelRatio`; call `ctx.scale(ratio, ratio)` so all drawing uses logical units.
4. Load images with `canvas.createImage()`; assign `src` after setting `img.onload` and `img.onerror`.
5. Export the result with `wx.canvasToTempFilePath({ canvas, ... })`.

→ See `examples/canvas-feature.md` for the complete node acquisition, drawing, and export pattern.
</canvas-setup-and-draw>

<manage-storage>
Steps to implement persistent storage:
1. Centralise all access in `utils/storage.ts`; define keys as named constants.
2. Before every array write, trim to the project limit: `items = items.slice(-MAX_ITEMS)`.
3. Wrap every read and write in `try/catch`; return safe defaults on read failure; show a toast on write failure.

→ See `examples/storage-patterns.md` for read/write/trim code templates.
</manage-storage>

<apply-typescript-patterns>
How to type a miniprogram codebase:
1. Enable `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true` in `tsconfig.json`.
2. Place shared types in `typings/index.d.ts`; always declare `IAppOption` to type `getApp<IAppOption>().globalData`.
3. Prefer `interface` for object shapes and `type` for unions/aliases.
4. Load static JSON via `require('../../data/file.json') as MyType`.
5. Use `as WechatMiniprogram.Canvas` / `as CanvasRenderingContext2D` only for WeChat canvas types; add a comment explaining why.

→ See `examples/apply-typescript-patterns.md` for tsconfig setup, `IAppOption` declaration, and WeChat canvas type casts.
</apply-typescript-patterns>

<apply-styling>
How to style pages and components:
1. Define design tokens as CSS custom properties on `page {}` in `app.scss`; reference via `var(--token-name)`.
2. Use BEM naming (`block__element--modifier`) scoped to each page or component SCSS file; no global class leakage.
3. Use inline `style` in WXML only for values computed at runtime in TypeScript; never for static styles.

→ See `examples/apply-styling.md` for design token definitions, BEM class naming patterns, and rpx vs px guidance.
</apply-styling>

<configure-subpackage>
Steps to add a page to a subpackage:
1. Create the page files under `subpackages/<feature>/pages/<page>/`.
2. In `app.json`, add or update the entry under `"subpackages"`: set `"root"` to `subpackages/<feature>` and list the page path **relative to that root** under `"pages"`.
3. Navigate to the page using the **full absolute path** including the subpackage root (e.g. `subpackages/feature/pages/detail/detail`).
4. Never import large assets or libraries from inside a subpackage into the main package.

→ See `examples/add-subpackage-page.md` for the full file-creation and registration walkthrough.
</configure-subpackage>

</capabilities>

<rules>

<rule> When adding any new page, use **add-page**. Read `app.json` first — navigating to an unregistered page causes silent failures. </rule>

<rule> When a page needs Canvas, use **canvas-setup-and-draw**. Never draw in `onLoad`; never use the legacy `wx.createCanvasContext` API. </rule>

<rule> When building a reusable component, use **create-component**. Register it with an absolute path to prevent depth-dependent breakage in subpackages. </rule>

<rule> When placing a non-TabBar feature page, use **configure-subpackage**. Only TabBar pages and globally shared components belong in the main package. </rule>

<rule> When choosing a navigation call, consult the **navigation-apis** knowledge table. Using the wrong API silently does nothing. </rule>

<rule> When passing data between pages, select the pattern from the **navigation-apis** data-passing table based on the situation. </rule>

<rule> When reading or writing persistent data, use **manage-storage**. All storage access must be centralised, trimmed before array writes, and wrapped in `try/catch`. </rule>

<rule> When writing TypeScript, follow **apply-typescript-patterns**. Do not use `any` except for WeChat canvas/image callbacks; annotate those with a comment. </rule>

<rule> When sizing UI elements, follow **apply-styling** (`rpx` for layout). Use `px` only for canvas physical pixel dimensions derived from `pixelRatio` in **canvas-setup-and-draw**. </rule>

<rule> All user-visible strings must be in the project's primary language. </rule>

<rule> When referencing examples, load only the one file relevant to the current task. </rule>

</rules>


