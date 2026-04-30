# Example: apply-styling

**Use Case**: Applying design tokens, BEM naming, and rpx sizing across pages and components (capability: **apply-styling**).

---

## 1. Design tokens in `app.scss`

Define all design values as CSS custom properties on `page {}` so every page and component can reference them via `var()`:

```scss
// app.scss
page {
  --color-primary: #1890ff;
  --color-text: #333333;
  --color-text-secondary: #888888;
  --color-bg: #f5f5f5;
  --color-surface: #ffffff;
  --color-border: #e8e8e8;

  --spacing-xs: 8rpx;
  --spacing-sm: 16rpx;
  --spacing-md: 24rpx;
  --spacing-lg: 32rpx;

  --font-size-sm: 24rpx;
  --font-size-md: 28rpx;
  --font-size-lg: 32rpx;
  --font-size-xl: 36rpx;

  --border-radius-sm: 8rpx;
  --border-radius-md: 16rpx;
  --border-radius-lg: 24rpx;
}
```

---

## 2. BEM naming in a component SCSS file

All classes are scoped to the component name (`history-card`) — no global leakage:

```scss
// components/history-card/history-card.scss

.history-card {
  background: var(--color-surface);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);

  &__title {
    font-size: var(--font-size-lg);
    color: var(--color-text);
    margin-bottom: var(--spacing-xs);
  }

  &__subtitle {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
  }

  &__thumbnail {
    width: 120rpx;
    height: 120rpx;
    border-radius: var(--border-radius-sm);
  }

  &--selected {
    border: 2rpx solid var(--color-primary);
  }
}
```

---

## 3. Using tokens in WXML — `var()` for static styles, `style` only for runtime values

```xml
<!-- history-card.wxml -->
<view class="history-card history-card--{{selected ? 'selected' : ''}}">
  <image
    class="history-card__thumbnail"
    src="{{item.thumbnailUrl}}"
    mode="aspectFill"
  />
  <view class="history-card__title">{{item.title}}</view>
  <!-- runtime-computed width only — static values go in SCSS -->
  <view style="width: {{progressWidth}}rpx;" class="progress-bar" />
</view>
```

---

## 4. rpx vs px — decision rule

| Use case | Unit |
|---|---|
| All layout dimensions (width, height, padding, margin, font-size) | `rpx` |
| Canvas physical pixel dimensions derived from `pixelRatio` | `px` (TypeScript only, not SCSS) |
| Border widths that must be exactly 1 physical pixel | `1px` |

```ts
// canvas-page.ts — px only for physical canvas sizing
const { pixelRatio } = wx.getSystemInfoSync();
canvas.width = logicalWidth * pixelRatio;   // px equivalent
ctx.scale(pixelRatio, pixelRatio);           // draw in logical rpx units
```

---

## Key Points

- All design tokens live in `app.scss` on `page {}`; components reference via `var()`.
- BEM classes are scoped per file; never add global utility classes in component SCSS.
- Inline `style` in WXML is only for values computed at runtime in TypeScript.
- Use `rpx` everywhere in SCSS; `px` only for canvas `canvas.width`/`canvas.height` in TypeScript.
