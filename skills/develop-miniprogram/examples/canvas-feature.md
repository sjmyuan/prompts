# Example: Implementing a Canvas Feature

**Use Case**: Draw content onto a canvas and let the user save it to their album.

> **Toolbox reference**: This example is drawn from the ID photo print-layout page (`subpackages/id-photo/layout`) of the Sean Dad Toolbox. It draws a grid of ID photos onto a canvas then exports to the album. Adapt the drawing logic and dimensions to your own use case.

---

## Page JSON — enable WebView renderer

```json
{
  "navigationBarTitleText": "打印排版",
  "renderer": "webview",
  "usingComponents": {}
}
```

---

## WXML — canvas and save button

```xml
<view class="layout">
  <canvas
    type="2d"
    id="printCanvas"
    style="width:{{canvasW}}px;height:{{canvasH}}px;"
    class="layout__canvas"
  />
  <button class="layout__btn" bindtap="onSave">保存到相册</button>
</view>
```

---

## TypeScript — node acquisition, drawing, export

```ts
// Physical dimensions for A4 at 300 dpi (scaled to logical pixels on device)
const LOGICAL_W = 360; // rpx-equivalent logical px for the canvas element
const LOGICAL_H = 510;

Page({
  data: {
    canvasW: LOGICAL_W,
    canvasH: LOGICAL_H,
  },

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  _canvas: null as any,   // WeChat canvas node — typed as any (WeChat internal type)

  onReady() {
    wx.nextTick(() => {
      this._initCanvas();
    });
  },

  _initCanvas() {
    const query = wx.createSelectorQuery();
    query.select('#printCanvas').fields({ node: true, size: true }).exec((res) => {
      const canvas = res[0].node as WechatMiniprogram.Canvas; // WeChat node type
      const ctx    = canvas.getContext('2d') as CanvasRenderingContext2D;
      const ratio  = wx.getSystemInfoSync().pixelRatio;

      canvas.width  = res[0].width  * ratio;
      canvas.height = res[0].height * ratio;
      ctx.scale(ratio, ratio);

      this._canvas = canvas;
      this._draw(ctx, canvas.width / ratio, canvas.height / ratio);
    });
  },

  _draw(ctx: CanvasRenderingContext2D, w: number, h: number) {
    const app      = getApp<IAppOption>();
    const { tempImagePath, backgroundColor } = app.globalData.idPhotoData!;

    // Fill background
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, w, h);

    // Draw photo grid (3 columns × 4 rows)
    const cols = 3, rows = 4;
    const cellW = w / cols, cellH = h / rows;

    const img = this._canvas.createImage();
    img.onload = () => {
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          ctx.drawImage(img, c * cellW, r * cellH, cellW, cellH);
        }
      }
    };
    img.src = tempImagePath;
  },

  onSave() {
    if (!this._canvas) {
      wx.showToast({ title: '画布未就绪', icon: 'none' });
      return;
    }
    wx.canvasToTempFilePath({
      canvas: this._canvas,
      fileType: 'jpg',
      quality: 0.95,
      success(res) {
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success() { wx.showToast({ title: '已保存到相册', icon: 'success' }); },
          fail()    { wx.showToast({ title: '保存失败，请检查相册权限', icon: 'none' }); },
        });
      },
      fail() { wx.showToast({ title: '导出失败', icon: 'none' }); },
    });
  },
});
```

---

## Key Characteristics

- **Renderer**: `"renderer": "webview"` in page JSON is mandatory
- **Node query**: always inside `wx.nextTick` in `onReady`, never in `onLoad`
- **Pixel ratio**: multiply logical size by `pixelRatio` for the canvas physical dimensions, then `ctx.scale(ratio, ratio)` so drawing coordinates stay in logical units
- **Image loading**: use `canvas.createImage()` (not `new Image()`); drawing must happen inside `img.onload`
- **Export**: `wx.canvasToTempFilePath` → `wx.saveImageToPhotosAlbum`
- **Common mistakes**:
  - Querying canvas in `onLoad` (DOM not ready) → blank canvas
  - Forgetting `ctx.scale(ratio, ratio)` → blurry on high-DPI devices
  - Using `new Image()` instead of `canvas.createImage()` → runtime error in WeChat
