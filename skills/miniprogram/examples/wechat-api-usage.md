# Example: WeChat API Usage

**Use Case**: Common WeChat API patterns — network requests, permission authorization, and media selection.

---

## Network request (`wx.request`)

```ts
interface ItemsResponse {
  items: MyItem[];
  total: number;
}

wx.request<ItemsResponse>({
  url: 'https://api.example.com/items',
  method: 'GET',
  data: { page: 1, pageSize: 20 },
  header: { 'Content-Type': 'application/json' },
  success(res) {
    if (res.statusCode === 200) {
      this.setData({ items: res.data.items });
    } else {
      wx.showToast({ title: '请求失败', icon: 'none' });
    }
  },
  fail() {
    wx.showToast({ title: '网络异常，请稍后重试', icon: 'none' });
  },
});
```

> Only domains registered in the server domain allowlist in the WeChat Developer Console can be called. Calling an unlisted domain silently fails in production.

---

## Permission authorization

Check the current authorization status first; only call `wx.authorize` if not yet granted. If the user previously denied the permission, `wx.authorize` fails immediately — guide them to the settings page instead.

```ts
function requestAlbumPermission(onGranted: () => void): void {
  wx.getSetting({
    success(res) {
      if (res.authSetting['scope.writePhotosAlbum']) {
        // already granted
        onGranted();
      } else {
        wx.authorize({
          scope: 'scope.writePhotosAlbum',
          success() { onGranted(); },
          fail() {
            wx.showModal({
              title: '需要相册权限',
              content: '请前往系统设置开启相册访问权限',
              confirmText: '去设置',
              success(modal) {
                if (modal.confirm) {
                  wx.openSetting(); // open the miniprogram permission settings page
                }
              },
            });
          },
        });
      }
    },
  });
}
```

**Common scopes**:
| Scope | Purpose |
|---|---|
| `scope.writePhotosAlbum` | Save images to album |
| `scope.camera` | Access camera |
| `scope.userLocation` | Access GPS location |
| `scope.record` | Microphone / audio recording |

---

## Media selection (`wx.chooseMedia`)

```ts
wx.chooseMedia({
  count: 1,
  mediaType: ['image'],
  sourceType: ['album', 'camera'],
  success(res) {
    const tempFilePath = res.tempFiles[0].tempFilePath;
    // use tempFilePath — valid until the miniprogram session ends
    this.setData({ imagePath: tempFilePath });
  },
  fail() {
    wx.showToast({ title: '选择失败', icon: 'none' });
  },
});
```

> `tempFilePath` is only valid for the current miniprogram session. If the path must survive a `redirectTo`, copy it to `globalData` or storage before navigating.

---

## Key Characteristics

- **Network**: always check `res.statusCode` in `success`; a non-2xx response does not trigger `fail`
- **Permission**: check `wx.getSetting` before `wx.authorize`; guide denied users to `wx.openSetting`
- **Media**: `tempFilePath` is session-scoped; persist it if the flow spans multiple pages
- **System info**: call `wx.getSystemInfoSync()` once per function/hook and cache the result — never call it in a loop
