# PII Permission Checklist

**User data permissions** — any API or component in the table below triggers a privacy obligation. Check this table whenever adding a new feature.

| Data collected | Triggering API / Component |
|---|---|
| Nickname / avatar | `<button open-type="chooseAvatar">`, `<input type="nickname">` |
| Precise location | `wx.authorize({scope:'scope.userLocation'})`, `wx.getLocation`, `wx.startLocationUpdate`, `wx.startLocationUpdateBackground`, `MapContext.moveToLocation` |
| Background location | `wx.authorize({scope:'scope.userLocationBackground'})` |
| Fuzzy location | `wx.authorize({scope:'scope.userFuzzyLocation'})`, `wx.getFuzzyLocation` |
| Chosen POI / location | `wx.choosePoi`, `wx.chooseLocation` |
| Delivery address | `wx.chooseAddress` |
| Invoice info | `wx.chooseInvoiceTitle`, `wx.chooseInvoice` |
| WeRun step count | `wx.authorize({scope:'scope.werun'})`, `wx.getWeRunData` |
| Phone number | `<button open-type="getPhoneNumber">`, `<button open-type="getRealtimePhoneNumber">` |
| License plate | `wx.chooseLicensePlate` |
| Photos / videos | `wx.chooseImage`, `wx.chooseMedia`, `wx.chooseVideo` |
| Files | `wx.chooseMessageFile` |
| Microphone | `wx.authorize({scope:'scope.record'})`, `wx.startRecord`, `RecorderManager.start`, `<live-pusher>`, `wx.joinVoIPChat` |
| Camera | `wx.authorize({scope:'scope.camera'})`, `wx.createVKSession`, `<camera>`, `<live-pusher>`, `<voip-room>` |
| Bluetooth | `wx.authorize({scope:'scope.bluetooth'})`, `wx.openBluetoothAdapter`, `wx.createBLEPeripheralServer` |
| Album (write only) | `wx.authorize({scope:'scope.writePhotosAlbum'})`, `wx.saveImageToPhotosAlbum`, `wx.saveVideoToPhotosAlbum` |
| Contacts (write only) | `wx.authorize({scope:'scope.addPhoneContact'})`, `wx.addPhoneContact` |
| Calendar (write only) | `wx.authorize({scope:'scope.addPhoneCalendar'})`, `wx.addPhoneRepeatCalendar`, `wx.addPhoneCalendar` |
| Accelerometer | `wx.startAccelerometer` |
| Compass | `wx.startCompass` |
| Device motion | `wx.startDeviceMotionListening` |
| Gyroscope | `wx.startGyroscope` |
| Clipboard | `wx.setClipboardData`, `wx.getClipboardData` |

**Before shipping any feature that uses an API above, verify all four obligations**:
1. **`requiredPrivateInfos`** — declare the API name in `app.json → "requiredPrivateInfos"` (required for most location, media, sensor, and contact APIs).
2. **Privacy-agreement popup** — implement `wx.onNeedPrivacyAuthorization` and block all listed API calls until the user accepts; the miniprogram will be rejected at review if any listed API is called before consent.
3. **Denied-permission guidance** — call `wx.getSetting` before `wx.authorize`; if the scope is already denied, show a modal and open `wx.openSetting` rather than failing silently.
4. **Privacy policy** — update the miniprogram's privacy policy on the WeChat MP platform to document every newly collected data type.
