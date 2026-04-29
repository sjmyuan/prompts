# Example: Creating a Custom Component

**Use Case**: A reusable `score-badge` component that renders a coloured badge showing a score value.

---

## File structure

```
miniprogram/components/score-badge/
  score-badge.wxml
  score-badge.ts
  score-badge.scss
  score-badge.json
```

---

## score-badge.json — mark as component

```json
{
  "component": true,
  "usingComponents": {}
}
```

---

## score-badge.wxml — template using properties

```xml
<view class="score-badge score-badge--{{level}}">
  {{score}}分
</view>
```

---

## score-badge.ts — typed properties and computed class

```ts
type Level = 'high' | 'mid' | 'low';

Component({
  properties: {
    score: {
      type: Number,
      value: 0,
    },
    level: {
      type: String,
      value: 'mid' as Level,
    },
  },
  data: {},
  methods: {
    // Emit an event so the parent can react to a tap
    onTap() {
      this.triggerEvent('tap', { score: this.properties.score });
    },
  },
});
```

---

## score-badge.scss — BEM scoped to component name

```scss
.score-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8rpx 20rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  font-weight: 600;

  &--high {
    background: var(--color-success);
    color: #fff;
  }

  &--mid {
    background: var(--color-primary);
    color: #fff;
  }

  &--low {
    background: var(--color-danger);
    color: #fff;
  }
}
```

---

## Registering the component

**Option A — Global** (available on all pages): add to `app.json`:
```json
{
  "usingComponents": {
    "score-badge": "/components/score-badge/score-badge"
  }
}
```

**Option B — Local** (available on one page only): add to that page's `.json`:
```json
{
  "usingComponents": {
    "score-badge": "/components/score-badge/score-badge"
  }
}
```

---

## Using the component in a page

```xml
<score-badge score="{{item.score}}" level="{{item.level}}" bindtap="onBadgeTap" />
```

Handling the custom event in the page `.ts`:
```ts
onBadgeTap(e: WechatMiniprogram.CustomEvent<{ score: number }>) {
  const { score } = e.detail;
  wx.showToast({ title: `得分: ${score}`, icon: 'none' });
},
```

---

---

## Advanced patterns

### `observers` — react to property or data changes

```ts
Component({
  properties: { score: { type: Number, value: 0 } },
  observers: {
    'score'(newVal: number) {
      this.setData({ level: newVal >= 80 ? 'high' : newVal >= 60 ? 'mid' : 'low' });
    },
  },
});
```

> `observers` fire whenever the watched property or data path changes. Use them to derive computed display values instead of duplicating logic across `attached` and every `setData` call.

### `lifetimes` — component lifecycle hooks

```ts
Component({
  lifetimes: {
    attached() {
      // component has been added to the page tree; properties are accessible here
      this._timer = setInterval(() => { /* ... */ }, 1000);
    },
    detached() {
      // component is being removed; clean up to prevent memory leaks
      clearInterval(this._timer);
    },
  },
});
```

| Hook | When it fires |
|---|---|
| `created` | Component instance created; `data` not yet set |
| `attached` | Added to page tree; `properties` available; safe to start timers |
| `ready` | Initial rendering done |
| `detached` | Removed from page tree; clean up timers and listeners |

---

## Key Characteristics

- **Four files** required; `"component": true` in `.json` is mandatory
- **`properties`** defines the public API; always supply a default `value`
- **`triggerEvent`** is the only correct way to communicate upward to the parent page — never mutate parent state directly
- **`observers`** derive computed state from property changes; avoids scattered update logic
- **`lifetimes.detached`** is the correct place to clear timers and listeners
- **BEM naming** scoped to the component name prevents CSS leakage
- **Registration path** must be absolute (`/components/...`) to work from any page depth
- **Common mistake**: Registering in `app.json` under `"usingComponents"` but using a relative path — this breaks in subpackages
