# Example: Storage Patterns

**Use Case**: Safely read, write, and trim data with `wx.setStorageSync` / `wx.getStorageSync`.

---

## Safe read (with default fallback)

```ts
function loadItems(): MyItem[] {
  try {
    return (wx.getStorageSync(STORAGE_KEY) as MyItem[]) ?? [];
  } catch {
    return [];
  }
}
```

---

## Safe write (with quota error handling)

```ts
function saveItems(items: MyItem[]): void {
  try {
    wx.setStorageSync(STORAGE_KEY, items);
  } catch {
    wx.showToast({ title: '保存失败', icon: 'none' });
  }
}
```

---

## Trim before save (prevent QuotaExceededError)

```ts
const MAX_ITEMS = 100;

function appendAndSave(existing: MyItem[], newItem: MyItem): void {
  const updated = [...existing, newItem].slice(-MAX_ITEMS); // keep most recent N
  try {
    wx.setStorageSync(STORAGE_KEY, updated);
  } catch {
    wx.showToast({ title: '保存失败', icon: 'none' });
  }
}
```

---

## Centralised storage module (`utils/storage.ts`)

Centralise all reads and writes so error handling and trimming logic is not duplicated across pages:

```ts
// utils/storage.ts
import { STORAGE_KEY, MAX_ITEMS } from './constants';
import type { MyItem } from '../typings/index';

export function loadItems(): MyItem[] {
  try {
    return (wx.getStorageSync(STORAGE_KEY) as MyItem[]) ?? [];
  } catch {
    return [];
  }
}

export function saveItems(items: MyItem[]): void {
  const trimmed = items.slice(-MAX_ITEMS);
  try {
    wx.setStorageSync(STORAGE_KEY, trimmed);
  } catch {
    wx.showToast({ title: '保存失败', icon: 'none' });
  }
}
```

```ts
// utils/constants.ts
export const STORAGE_KEY = 'myFeature_items';
export const MAX_ITEMS   = 100;
```

---

## Key Characteristics

- Both `getStorageSync` and `setStorageSync` can throw — always wrap in `try/catch`
- Trim arrays to a fixed max length before every write to stay well under the 10 MB quota
- Use named constants for storage keys to prevent typos and aid refactoring
- Centralise all reads/writes in a `utils/storage.ts` module; never scatter raw `wx.setStorageSync` calls across pages
