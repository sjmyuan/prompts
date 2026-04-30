# Example: apply-typescript-patterns

**Use Case**: Typing a new miniprogram codebase from scratch (capability: **apply-typescript-patterns**).

---

## 1. `tsconfig.json` — strict settings

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "target": "ES6",
    "lib": ["ES6"],
    "moduleResolution": "node",
    "baseUrl": ".",
    "paths": {
      "@typings/*": ["typings/*"]
    }
  },
  "include": ["miniprogram/**/*.ts", "typings/**/*.d.ts"]
}
```

---

## 2. `typings/index.d.ts` — shared types and `IAppOption`

```ts
// typings/index.d.ts

/** Shape of getApp<IAppOption>().globalData */
interface IAppOption {
  globalData: {
    currentFlowItemId: string | null;   // cleared when the flow ends
    userProfile: UserProfile | null;
  };
}

interface UserProfile {
  openId: string;
  nickname: string;
  avatarUrl: string;
}

interface HistoryItem {
  id: string;
  title: string;
  createdAt: number;   // Unix timestamp (ms)
}
```

---

## 3. Typing `getApp()` and globalData

```ts
// pages/detail/detail.ts
const app = getApp<IAppOption>();

Page({
  onLoad() {
    const itemId = app.globalData.currentFlowItemId;
    if (itemId === null) {
      wx.navigateBack();
      return;
    }
    // use itemId safely — TypeScript knows it's string here
  }
});
```

---

## 4. Loading static JSON with a type assertion

```ts
// utils/config.ts
import type { CategoryConfig } from '../typings/index';

const categories = require('../../data/categories.json') as CategoryConfig[];
```

---

## 5. WeChat canvas/image type assertions (with comment)

```ts
// Necessary cast: wx.createSelectorQuery returns a generic SelectorQuery;
// the canvas node is typed as WechatMiniprogram.Canvas only after .fields({ node: true }).
const canvas = res.node as WechatMiniprogram.Canvas;
const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
```

---

## Key Points

- Enable all three strict flags: `strict`, `noImplicitAny`, `strictNullChecks`.
- Declare `IAppOption` in `typings/index.d.ts` before using `getApp<IAppOption>()` anywhere.
- Use `interface` for object shapes; use `type` for unions and aliases.
- The only acceptable `as` casts are for WeChat canvas/image callbacks — always add a comment explaining why.
