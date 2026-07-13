# Example: Adding a New Page to a Subpackage

**Use Case**: Add a secondary page to an existing subpackage.

> **Toolbox reference**: This example adds a `detail` page to the `easy-practice` subpackage of the Sean Dad Toolbox miniprogram. Adapt paths and names to your own project.

---

## Step 1 — Create the four page files

```
subpackages/easy-practice/detail/
  index.wxml
  index.ts
  index.scss
  index.json
```

> In your project, replace `subpackages/easy-practice/detail/` with the appropriate path under your subpackage root.

**index.json** — declare renderer and empty component map:
```json
{
  "navigationBarTitleText": "题集详情",
  "usingComponents": {}
}
```
> Add `"renderer": "webview"` here only if this page will use Canvas.

**index.wxml** — minimal skeleton:
```xml
<view class="detail">
  <view class="detail__title">{{title}}</view>
  <view wx:for="{{problems}}" wx:key="id" class="detail__item">
    {{item.question}}
  </view>
</view>
```

**index.ts** — page with typed data:
```ts
interface Problem {
  id: string;
  question: string;
}

Page({
  data: {
    title: '' as string,
    problems: [] as Problem[],
  },
  onLoad(options) {
    const setId = options.setId ?? '';
    // load problem set data
    const set = require(`../../../data/problem-sets/${setId}.json`);
    this.setData({ title: set.title, problems: set.problems });
  },
});
```

**index.scss** — BEM scoped to the page:
```scss
.detail {
  padding: 32rpx;
  background: var(--color-bg-page);

  &__title {
    font-size: 36rpx;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: 24rpx;
  }

  &__item {
    background: var(--color-bg-card);
    border-radius: 16rpx;
    padding: 24rpx;
    margin-bottom: 16rpx;
    color: var(--color-text-primary);
  }
}
```

---

## Step 2 — Register the page in `app.json`

Add the new page path to the existing `easy-practice` subpackage entry. Use the path **relative to the subpackage root** in the `pages` array:

```json
{
  "subpackages": [
    {
      "root": "subpackages/easy-practice",
      "pages": [
        "session/index",
        "complete/index",
        "history/index",
        "detail/index"
      ]
    }
  ]
}
```

> ⚠ Use only the path **relative to the subpackage root** in the `pages` array, but the **full path** when navigating.

---

## Step 3 — Navigate to the page

From any page in the main package or another subpackage:

```ts
wx.navigateTo({
  url: `/subpackages/easy-practice/detail/index?setId=${encodeURIComponent(setId)}`
});
```

---

## Key Characteristics

- **Complexity**: Low — new page with static data loading
- **Files created**: 4 (`.wxml`, `.ts`, `.scss`, `.json`)
- **Registration**: `app.json` subpackage `pages` array
- **Navigation**: `wx.navigateTo` with full subpackage path
- **Common mistake**: Registering the page under the main `"pages"` key instead of `"subpackages"` — it will work but defeats the subpackage split strategy
