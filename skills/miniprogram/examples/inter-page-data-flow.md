# Example: Inter-Page Data Flow

**Use Case**: Passing data between pages across a multi-step user flow.

> **Toolbox reference**: Examples below are taken from the Sean Dad Toolbox. The ID photo flow uses `globalData`; the easy-practice session flow uses `wx.setStorageSync`. Adapt key names, types, and paths to your own project.

---

## Pattern selection guide

| Situation | Use |
|---|---|
| Small scalar value (ID, flag, count) | Route query param |
| Structured result that survives `redirectTo` | `wx.setStorageSync` → `wx.getStorageSync` |
| In-flight object within one user flow (not persisted) | `getApp().globalData` |
| Data that must survive app restart | `wx.setStorageSync` with a stable key |

---

## Pattern 1 — Route query param

**When**: Passing a single ID or small string from a list page to a detail page.

```ts
// list page — navigate with param
wx.navigateTo({
  url: `/subpackages/feature-a/detail/index?itemId=${encodeURIComponent(itemId)}`
});

// detail page — receive in onLoad
onLoad(options) {
  const itemId = decodeURIComponent(options.itemId ?? '');
  // load data using itemId
},
```

> Do not pass complex objects as query params. Encode as JSON string only when necessary and keep the payload small (< 1 KB).

---

## Pattern 2 — Storage handoff (structured result that survives `redirectTo`)

**When**: `redirectTo` replaces the current page so there is no `EventChannel`; the receiving page needs a full result object.

> **Toolbox reference**: The easy-practice session page writes `lastSessionResult` to storage before redirecting to the complete page.

```ts
// source page — write before redirecting
const result: SessionResult = { /* ... */ };
wx.setStorageSync('myResultKey', JSON.stringify(result));
wx.redirectTo({ url: '/subpackages/feature-a/complete/index' });

// destination page — read in onLoad
onLoad() {
  try {
    const raw = wx.getStorageSync('myResultKey') as string;
    const result = JSON.parse(raw) as SessionResult;
    this.setData({ result });
  } catch {
    wx.showToast({ title: '加载失败', icon: 'none' });
  }
},
```

---

## Pattern 3 — `globalData` handoff (in-flight object within one user flow)

**When**: An in-flight object is shared across multiple navigations within a single user flow and does not need to be persisted after the flow ends.

> **Toolbox reference**: The ID photo flow stores `{ tempImagePath, backgroundColor, photoSizeKey }` in `globalData` across three pages (upload → preview → layout).

```ts
// Define the shape in typings/index.d.ts
interface IAppOption {
  globalData: {
    flowData?: MyFlowData;
  };
}

// source page — set global data then navigate
const app = getApp<IAppOption>();
app.globalData.flowData = { /* ... */ };
wx.navigateTo({ url: '/subpackages/feature-b/step2/index' });

// intermediate/destination page — read and optionally update
onLoad() {
  const data = getApp<IAppOption>().globalData.flowData!;
  this.setData({ /* derived from data */ });
},

// final page — use and clean up when flow ends
onSave() {
  const data = getApp<IAppOption>().globalData.flowData!;
  // use data ...
  getApp<IAppOption>().globalData.flowData = undefined; // clean up
  wx.switchTab({ url: '/pages/home/index' });
},
```

---

## Key Characteristics

- **Route params**: simplest, but limited to small scalar values; always encode/decode with `encodeURIComponent`
- **Storage handoff**: survives page stack replacement (`redirectTo`); always `JSON.stringify` / `JSON.parse`; wrap reads in `try/catch`
- **`globalData`**: convenient for multi-step flows; always type `IAppOption`; clear after the flow completes
- **EventChannel**: the only correct mechanism for returning a value from a child page to the `navigateTo` parent
- **Common mistake**: Using `globalData` for data that must persist across app restarts — it is reset every time the app is launched

---

## Pattern 4 — EventChannel (return data from child to parent)

**When**: A child page (e.g. picker, colour selector) needs to pass a chosen value back to the page that navigated to it.

```ts
// parent page — register event listener inside the navigateTo call
wx.navigateTo({
  url: '/subpackages/feature-a/picker/index',
  events: {
    onPicked(data: { value: string }) {
      // called when the child emits 'onPicked'
      this.setData({ selected: data.value });
    },
  },
});

// child page — emit event then go back
onConfirm() {
  const channel = this.getOpenerEventChannel();
  channel.emit('onPicked', { value: this.data.highlighted });
  wx.navigateBack();
},
```

> Use EventChannel instead of `globalData` here. `globalData` works but creates hidden coupling; EventChannel makes the contract explicit and typed.
