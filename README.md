## Sign-Language Translator App

Cross‑platform mobile app built with Expo + React Native + Expo Router. Runs on Android, iOS (macOS only), and Web.

### Prerequisites
- **Node.js**: LTS 18, 20, or 22 and **npm** 9/10. Check:
  ```bash
  node -v && npm -v
  ```
- **Git**: Any recent version.
- **Expo tooling**: Use `npx` (no global install required).
- Platform tools (as needed):
  - **Android**: [Android Studio](https://developer.android.com/studio) with Android SDK + an AVD (emulator).
  - **iOS (macOS only)**: [Xcode](https://developer.apple.com/xcode/) with Command Line Tools and an iOS Simulator.

### Quick start (Windows/macOS/Linux)
```bash
# 1) Install dependencies
npm install

# 2) Start the dev server (Metro bundler)
npx expo start
```

Then choose how to run it:
- **Expo Go (physical device)**: Install the "Expo Go" app on your phone. Scan the QR from the terminal/browser.
- **Android emulator**: Start an AVD from Android Studio, then:
  ```bash
  npm run android
  ```
- **iOS simulator (macOS only)**:
  ```bash
  npm run ios
  ```
- **Web (browser)**:
  ```bash
  npm run web
  ```

### Scripts
```bash
npm run start     # expo start (interactive platform chooser)
npm run android   # launch on Android emulator/device
npm run ios       # launch on iOS simulator (macOS only)
npm run web       # run in the browser
npm run lint      # run linter
npm run reset-project  # replace app/ with a blank template (destructive)
```

### Project structure
- `app/`: App source with [Expo Router](https://docs.expo.dev/router/introduction) file‑based routes.
- `components/`, `hooks/`, `providers/`: Shared UI, logic, and context.
- `assets/`: Images and fonts.

### Platform setup tips
- **Android (Windows/macOS/Linux)**
  - Install Android Studio → SDK Manager → install latest SDK + Build Tools.
  - Create an AVD in Device Manager and start it before `npm run android`.
  - If you see "SDK location not found": set `ANDROID_HOME` to your SDK path and add `platform-tools` to `PATH`.
    - Windows example: `C:\Users\<YOU>\AppData\Local\Android\Sdk`.
- **iOS (macOS only)**
  - Open Xcode once to accept licenses and install components.
  - Ensure an iOS Simulator is installed (Xcode → Settings → Platforms).

### Troubleshooting
- **Stuck/Red screen/Old bundle**: clear caches
  ```bash
  npx expo start -c
  ```
- **Dependencies acting weird**: reinstall
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```
- **Device can’t connect**: ensure phone and computer are on the same Wi‑Fi; try switching connection type in the CLI UI (LAN ↔ Tunnel ↔ Local).
- **Port conflicts**: close other RN/Expo instances; or set a different port: `EXPO_PORT=8082 npx expo start`.
- **Android build tools missing**: open Android Studio → SDK Manager → install required packages; restart the dev server.

### Developing
- Edit files under `app/` and save—hot reload will apply changes.
- Theming and shared UI live under `components/` and `providers/`.
- TypeScript is enabled; keep types accurate for best DX.

### Learn more
- [Expo docs](https://docs.expo.dev/)
- [Expo Go](https://expo.dev/go)
- [Android emulator setup](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator setup](https://docs.expo.dev/workflow/ios-simulator/)

---
If you need a clean slate of the starter, you can run:
```bash
npm run reset-project
```
This moves the current example into `app-example/` and creates a blank `app/`.

### Contributors
- [@amnxd](https://github.com/amnxd)
- [@Ankit-euphemism](https://github.com/Ankit-euphemism)
- [@coderstop244](https://github.com/coderstop244)
- [@Ishaan-ux-coder](https://github.com/Ishaan-ux-coder)
