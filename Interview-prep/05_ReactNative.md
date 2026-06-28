# 🚀 Interview Preparation - React Native

> **Domain:** Mobile Development / Cross-Platform  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is React Native and how does it work?**
<details>
<summary><b>👀 Show Answer</b></summary>

React Native is an open-source framework developed by Facebook for building native mobile applications using JavaScript and React.
It works by using a bridge (in legacy architecture) or JSI (in new architecture) to communicate between the JavaScript code and the native platform (iOS/Android) modules. It renders real native UI components, not web views.

> 💡 **Interviewer Focus:** Understanding that it produces real native apps, not hybrid web apps.
</details>
<hr/>

### ❓ Q2. **What is the difference between React and React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **React** is a JS library for building user interfaces on the web. It uses the virtual DOM and HTML tags like `<div>`, `<span>`.
- **React Native** is a framework for building mobile apps. It uses native components like `<View>`, `<Text>` instead of HTML tags, and does not use the browser DOM.

> 💡 **Interviewer Focus:** Knowing the specific component replacements and platform differences.
</details>
<hr/>

### ❓ Q3. **What is the difference between Expo and React Native CLI?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Expo:** A set of tools and services built around React Native. It makes it easier to start, build, and deploy apps without touching native code (Xcode/Android Studio).
- **React Native CLI:** The standard way to build React Native apps. It requires manual setup of Android Studio and Xcode but offers full control over native code.

> 💡 **Interviewer Focus:** Pros and cons of each. Expo is faster for starting; CLI is better for complex apps needing custom native code.
</details>
<hr/>

### ❓ Q4. **How do you style components in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

React Native uses JavaScript objects for styling, very similar to CSS. You use `StyleSheet.create` for performance and organization. It uses Flexbox for layout, but with some differences (e.g., `flexDirection` defaults to `column`).

> 💡 **Interviewer Focus:** Awareness that styling is JS-based and defaults to column layout.
</details>
<hr/>

### ❓ Q5. **What is the purpose of `<View>` and `<Text>`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `<View>` is the most fundamental component for building UI. It maps to the native equivalent (`UIView` on iOS, `android.view` on Android) and is used for layout and styling (like `<div>`).
- `<Text>` is used for displaying text. Unlike the web, all text must be wrapped in a `<Text>` component.

> 💡 **Interviewer Focus:** Basic component knowledge.
</details>
<hr/>

### ❓ Q6. **What is a `FlatList` and why is it preferred over `ScrollView` for long lists?**
<details>
<summary><b>👀 Show Answer</b></summary>

`ScrollView` renders all its children at once, which can cause performance issues for large data sets. `FlatList` renders items lazily (only when they are about to appear on screen) and removes them when they scroll off, saving memory and CPU.

> 💡 **Interviewer Focus:** Memory management and performance awareness.
</details>
<hr/>

### ❓ Q7. **How do you handle user input in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `<TextInput>` component. It has props like `onChangeText` (instead of `onChange`) and `value` for controlled components.

> 💡 **Interviewer Focus:** Small differences in prop names compared to web React.
</details>
<hr/>

### ❓ Q8. **What are the common ways to add images in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `<Image>` component.
- Local images: `source={require('./path/to/img.png')}`
- Network images: `source={{uri: 'https://...'}}` (requires explicit width and height).

> 💡 **Interviewer Focus:** Network images require dimensions specified.
</details>
<hr/>

### ❓ Q9. **What is the purpose of the `SafeAreaView` component?**
<details>
<summary><b>👀 Show Answer</b></summary>

`SafeAreaView` is used to render content within the safe area boundaries of a device. It applies padding to reflect the portion of the view not covered by navigation bars, tab bars, toolbars, and other ancestor views (especially important for devices with notches like iPhone X).

> 💡 **Interviewer Focus:** UI polish and handling device quirks.
</details>
<hr/>

### ❓ Q10. **How do you handle navigation in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

The community standard is **React Navigation** (supporting Stack, Tab, and Drawer navigation). Another option is **React Native Navigation** by Wix (which uses truly native navigation components).

> 💡 **Interviewer Focus:** Familiarity with the ecosystem (React Navigation is most common).
</details>
<hr/>

## 🟡 Intermediate Level

### ❓ Q11. **Explain the React Native Bridge.**
<details>
<summary><b>👀 Show Answer</b></summary>

The Bridge is the message broker that allows the JavaScript thread and the Native threads to communicate. JS code sends serialized JSON messages over the bridge to call native modules, and vice versa. It is asynchronous.

> 💡 **Interviewer Focus:** Understanding the core bottleneck of the legacy architecture.
</details>
<hr/>

### ❓ Q12. **What is the "New Architecture" in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

The new architecture replaces the Bridge with **JSI (JavaScript Interface)**. JSI allows JS to hold a reference to C++ host objects and invoke methods on them synchronously. It also introduces **Fabric** (new rendering system) and **TurboModules** (faster native modules).

> 💡 **Interviewer Focus:** Awareness of modern RN developments (React Native 0.68+).
</details>
<hr/>

### ❓ Q13. **How do you perform Platform-specific code branching?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Using the `Platform` module: `Platform.OS === 'ios'`.
2. Using the `Platform.select` method.
3. Using platform-specific file extensions: `Component.ios.js` and `Component.android.js`.

> 💡 **Interviewer Focus:** Different ways to maintain clean code while handling OS differences.
</details>
<hr/>

### ❓ Q14. **What is the Hermes engine?**
<details>
<summary><b>👀 Show Answer</b></summary>

Hermes is an open-source JavaScript engine optimized for running React Native. It improves app performance by decreasing memory utilization, reducing download size, and decreasing the time it takes for the app to become interactive (TTI). It pre-compiles JS into bytecode at build time.

> 💡 **Interviewer Focus:** Performance optimization and bundle size reduction.
</details>
<hr/>

### ❓ Q15. **How do you handle animations in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. **Animated API:** Built-in, good for standard animations.
2. **LayoutAnimation:** Good for animating layout changes globally.
3. **Reanimated:** (Community library) Highly performant, runs animations on the UI thread directly.

> 💡 **Interviewer Focus:** Knowing that running animations on the JS thread causes stutter; UI thread execution is key.
</details>
<hr/>

### ❓ Q16. **What is the difference between `useEffect` in React and React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

There is no difference in the hook itself. However, the effects you perform might be different (e.g., listening to `AppState` changes or hardware back button presses instead of window resize).

> 💡 **Interviewer Focus:** Understanding that hooks are purely JS/React features and work the same way.
</details>
<hr/>

### ❓ Q17. **How do you handle the Android back button in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `BackHandler` API provided by React Native. You can add an event listener for `hardwareBackPress` and return `true` to indicate that the app has handled the event, or `false` to let the default behavior happen.

> 💡 **Interviewer Focus:** Handling platform-specific hardware features.
</details>
<hr/>

### ❓ Q18. **What is the purpose of `interactionManager`?**
<details>
<summary><b>👀 Show Answer</b></summary>

`InteractionManager` allows long-running work to be scheduled after any active interactions or animations have completed. This is crucial for keeping animations smooth (60fps).

> 💡 **Interviewer Focus:** Advanced performance optimization for smooth UI.
</details>
<hr/>

### ❓ Q19. **How do you optimize images in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use appropriate sizes (don't load a 4K image for a thumbnail).
2. Use modern formats like WebP.
3. Use a library like `react-native-fast-image` which provides aggressive caching and better performance than the default `<Image>` component.

> 💡 **Interviewer Focus:** Ecosystem knowledge for solving performance issues.
</details>
<hr/>

### ❓ Q20. **What is the difference between `flexDirection` in CSS and React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

- In web CSS, `flexDirection` defaults to `row`.
- In React Native, `flexDirection` defaults to `column`.

> 💡 **Interviewer Focus:** Attention to detail regarding Flexbox implementation in RN.
</details>
<hr/>

## 🔴 Advanced Level

### ❓ Q21. **How do you write a custom Native Module in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

You write the native code in Java/Kotlin (Android) or Objective-C/Swift (iOS). You then register the module with React Native and expose its methods to the JavaScript thread.
In the new architecture, you use TurboModules which requires defining a typed specification (usually in TypeScript) and running a codegen tool.

> 💡 **Interviewer Focus:** Understanding how to extend RN capabilities with native code.
</details>
<hr/>

### ❓ Q22. **Explain the threading model in React Native.**
<details>
<summary><b>👀 Show Answer</b></summary>

React Native uses 3 main threads:
1. **JS Thread:** Where your JavaScript code is executed (logic, API calls, etc.).
2. **Main/UI Thread:** Where native UI rendering happens and user interactions are handled.
3. **Shadow Thread:** Where the layout is calculated (using Yoga) before being passed to the UI thread.

> 💡 **Interviewer Focus:** Deep understanding of how RN operates under the hood.
</details>
<hr/>

### ❓ Q23. **How do you optimize the performance of a large `FlatList`?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use `getItemLayout` if items have a fixed height (skips layout calculation).
2. Use `removeClippedSubviews={true}`.
3. Use `keyExtractor` correctly.
4. Keep the render item component simple and memoized (`React.memo`).
5. Adjust `windowSize` and `maxToRenderPerBatch` props.

> 💡 **Interviewer Focus:** Practical experience with list performance tuning.
</details>
<hr/>

### ❓ Q24. **How do you handle Push Notifications in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use a library like `@react-native-firebase/messaging` or Expo Notifications. You need to configure APNS for iOS and FCM for Android, handle the token generation, and listen for messages in the foreground, background, and quit states.

> 💡 **Interviewer Focus:** Complex integration involving native setup and cloud services.
</details>
<hr/>

### ❓ Q25. **What is the difference between shallow and deep linking in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Shallow Linking:** Navigating within the app or opening another app using a custom scheme (e.g., `myapp://profile`).
- **Deep Linking:** Opening the app from a standard web URL (e.g., `https://myapp.com/profile`). On iOS, this uses Universal Links; on Android, it uses App Links. It requires server-side verification.

> 💡 **Interviewer Focus:** Advanced navigation and OS integration.
</details>
<hr/>

### ❓ Q26. **How do you handle state persistence in a React Native app?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `AsyncStorage` (legacy but common) or `react-native-mmkv` (modern, much faster because it uses JSI and is synchronous). You can use these directly or integrate them with Redux Persist.

> 💡 **Interviewer Focus:** Knowledge of modern alternatives like MMKV for speed.
</details>
<hr/>

### ❓ Q27. **How do you secure sensitive data (like API tokens) in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Do **not** use `AsyncStorage` or `MMKV` for sensitive data as they are not encrypted by default. Use Keychain on iOS and Keystore on Android. Libraries like `react-native-keychain` or `expo-secure-store` provide a unified API for this.

> 💡 **Interviewer Focus:** Security awareness in mobile development.
</details>
<hr/>

### ❓ Q28. **Explain how CodePush works.**
<details>
<summary><b>👀 Show Answer</b></summary>

CodePush (by Microsoft) is a cloud service that enables React Native developers to deploy mobile app updates directly to their users’ devices. It works by targeting the JS bundle. If you only change JS or assets, you can bypass the App Store/Play Store review process. If you change native code, you must release a new store version.

> 💡 **Interviewer Focus:** Over-The-Air (OTA) update strategies and limitations.
</details>
<hr/>

## 🔷 Scenario-Based & Real-World Questions

### ❓ Q29. **How would you debug a memory leak in a React Native app?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use **Flipper** or **Xcode Instruments** (Leaks instrument) for iOS, and **Profiler** in Android Studio. Look for detached views or objects that are not being garbage collected. Common culprits are active timers, event listeners not removed on unmount, or large images kept in memory.

> 💡 **Interviewer Focus:** Profiling tools and common causes of memory leaks.
</details>
<hr/>

### ❓ Q30. **How do you handle keyboard overlapping inputs in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `<KeyboardAvoidingView>` component provided by React Native. You can set the `behavior` prop to `padding`, `height`, or `position` depending on the platform and layout. Alternatively, use community libraries like `react-native-keyboard-aware-scroll-view`.

> 💡 **Interviewer Focus:** Solving a very common mobile UI issue.
</details>
<hr/>

### ❓ Q31. **How would you implement an offline-first feature in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. **Local Storage:** Use SQLite or MMKV/WatermelonDB to store data locally.
2. **Sync Queue:** Queue network requests when offline and execute them when connectivity returns using `NetInfo` to detect network status.
3. **State Management:** Use Redux Offline or Apollo Client cache to manage optimistic UI updates.

> 💡 **Interviewer Focus:** Architecture for offline capabilities.
</details>
<hr/>

### ❓ Q32. **What is the difference between a "Cold Boot" and a "Warm Boot" in mobile apps?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Cold Boot:** The app starts from scratch (not in memory). The OS creates the process, initializes the app, and loads the JS bundle.
- **Warm Boot:** The app is already in memory (running in background) and is brought to the foreground. It is much faster because the JS bundle doesn't need to be reloaded.

> 💡 **Interviewer Focus:** App lifecycle understanding.
</details>
<hr/>

### ❓ Q33. **How do you handle different screen sizes and orientations?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use percentages, flexbox, or the `Dimensions` API to get the screen width and height. For more complex layouts, use the `useWindowDimensions` hook which automatically updates when the screen size or orientation changes.

> 💡 **Interviewer Focus:** Responsive design in mobile.
</details>
<hr/>

### ❓ Q34. **How would you optimize the startup time of a React Native app?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use **Hermes** engine (bytecode pre-compilation).
2. Minimize the size of the JS bundle (remove unused dependencies).
3. Lazy load components or data that are not needed immediately on the first screen.
4. Inline requires for heavy modules.

> 💡 **Interviewer Focus:** TTI (Time to Interactive) optimization.
</details>
<hr/>

### ❓ Q35. **How do you use Native UI Components in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

If a native UI component exists (like a custom map or specialized chart) and you want to use it in RN, you need to create a `ViewManager` in native code (Java/Obj-C) that exposes the component, and then use `requireNativeComponent` in JS.

> 💡 **Interviewer Focus:** Bridging native UI views to React.
</details>
<hr/>

### ❓ Q36. **What is the purpose of the `metro.config.js` file?**
<details>
<summary><b>👀 Show Answer</b></summary>

Metro is the JavaScript bundler for React Native. The `metro.config.js` file is used to configure the bundler, such as adding support for custom file extensions (like SVG), configuring asset plugins, or changing the root directory.

> 💡 **Interviewer Focus:** Tooling and build configuration knowledge.
</details>
<hr/>

### ❓ Q37. **How do you handle splash screens in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Do not create a splash screen in JavaScript as it will only appear after the JS bundle loads. Create a native splash screen in Xcode (LaunchScreen.storyboard) and Android (styles.xml/drawable) to show immediately on app launch. Libraries like `react-native-splash-screen` can help hide it once the JS is ready.

> 💡 **Interviewer Focus:** Native vs JS splash screens.
</details>
<hr/>

### ❓ Q38. **What is the difference between `shadow` props in iOS and Android?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **iOS:** Supports detailed shadow properties like `shadowColor`, `shadowOffset`, `shadowOpacity`, and `shadowRadius`.
- **Android:** Does not support these props. You must use the `elevation` prop, which uses the Android system's elevation API to cast a shadow based on material design guidelines.

> 💡 **Interviewer Focus:** Platform inconsistencies and how to handle them.
</details>
<hr/>

### ❓ Q39. **How do you handle deep links when the app is killed (not in memory)?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `Linking.getInitialURL()`. When the app is launched from a deep link while it was killed, this method will return the URL that opened it. If it returns null, the app was opened normally.

> 💡 **Interviewer Focus:** Handling cold start deep links.
</details>
<hr/>

### ❓ Q40. **How do you implement Biometric Authentication (FaceID/TouchID)?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use a library like `react-native-biometrics` or `expo-local-authentication`. These libraries provide methods to check if biometrics are available and to prompt the user for authentication, returning a promise with the result.

> 💡 **Interviewer Focus:** Integrating with native security features.
</details>
<hr/>

### ❓ Q41. **What is the difference between `yarn ios` and running from Xcode?**
<details>
<summary><b>👀 Show Answer</b></summary>

`yarn ios` is a CLI command that builds the app and launches it in the simulator. Running from Xcode gives you more control, allows you to view native logs easily, use the Xcode debugger, and configure build settings/signing for physical devices.

> 💡 **Interviewer Focus:** Developer workflow and debugging tools.
</details>
<hr/>

### ❓ Q42. **How do you handle runtime permissions in Android 6.0+?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `PermissionsAndroid` API provided by React Native. You must check if the permission is granted, and if not, request it from the user before performing the action (e.g., accessing camera or location).

> 💡 **Interviewer Focus:** Platform-specific permission models.
</details>
<hr/>

### ❓ Q43. **How do you implement localized text in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use a library like `react-native-i18n` or `i18next` combined with a library that detects the device locale (like `react-native-localize`).

> 💡 **Interviewer Focus:** Localization strategies in mobile.
</details>
<hr/>

### ❓ Q44. **What is the benefit of using TypeScript with React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Provides static type checking, which prevents runtime errors (like accessing properties of undefined). It also improves developer experience with better autocomplete and documentation in the editor.

> 💡 **Interviewer Focus:** Type safety in large projects.
</details>
<hr/>

### ❓ Q45. **How do you handle app state changes (Background/Foreground)?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `AppState` API. You can add an event listener for `change` and check if the state is `active` (foreground), `background`, or `inactive` (iOS transition state).

> 💡 **Interviewer Focus:** Handling app lifecycle events.
</details>
<hr/>

### ❓ Q46. **What is the purpose of the `pointerEvents` prop?**
<details>
<summary><b>👀 Show Answer</b></summary>

It controls how a `View` handles touch events.
- `auto`: Standard behavior.
- `none`: The view never receives touch events.
- `box-none`: The view itself doesn't receive events but its children can.
- `box-only`: The view receives events but its children don't.

> 💡 **Interviewer Focus:** Fine-grained touch event control.
</details>
<hr/>

### ❓ Q47. **How do you optimize network requests in mobile apps?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use caching (HTTP cache or custom store).
2. Use smaller payloads (GraphQL or filtered REST responses).
3. Batch requests where possible.
4. Use image CDNs for optimized image sizes.

> 💡 **Interviewer Focus:** Data usage and battery life considerations.
</details>
<hr/>

### ❓ Q48. **How do you handle API timeouts?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `AbortController` with `fetch` and a `setTimeout` to abort the request if it takes too long.
```javascript
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
fetch(url, { signal: controller.signal });
```

> 💡 **Interviewer Focus:** Resilient network handling.
</details>
<hr/>

### ❓ Q49. **What is the difference between `ScrollView` and `VirtualizedList`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `ScrollView` renders everything.
- `VirtualizedList` is the base component for `FlatList` and `SectionList`. It provides virtualization (lazy rendering) and is much more performant for long lists.

> 💡 **Interviewer Focus:** Deep knowledge of list components.
</details>
<hr/>

### ❓ Q50. **How do you implement a custom font in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Add the font files to the project, configure them in `react-native.config.js` or `assets` folder, and run `npx react-native-asset` (or link manually in Xcode/Android Studio). Then use the font name in the `fontFamily` style prop.

> 💡 **Interviewer Focus:** Asset management in RN.
</details>
<hr/>

### ❓ Q51. **What is the purpose of `LayoutAnimation`?**
<details>
<summary><b>👀 Show Answer</b></summary>

It allows you to globally configure animations that will be used for all views in the next render/layout pass. It is very performant because it runs entirely on the native side without JS intervention.

> 💡 **Interviewer Focus:** Simple but highly performant animation option.
</details>
<hr/>

### ❓ Q52. **How do you handle secure storage in Expo?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `expo-secure-store`. It encrypts data and stores it securely on the device.

> 💡 **Interviewer Focus:** Expo-specific security APIs.
</details>
<hr/>

### ❓ Q53. **What is the difference between `react-native-svg` and web SVG?**
<details>
<summary><b>👀 Show Answer</b></summary>

Web SVGs use HTML tags like `<svg>`, `<path>`. React Native does not support these natively. `react-native-svg` provides React Native components that mimic these tags and render them using native drawing APIs.

> 💡 **Interviewer Focus:** Handling SVGs in mobile.
</details>
<hr/>

### ❓ Q54. **How do you implement a progress bar?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use a `<View>` container with a specific width, and a child `<View>` with a width percentage based on the progress state. Or use community libraries or platform-specific components like `ProgressBarAndroid`.

> 💡 **Interviewer Focus:** Basic custom component building.
</details>
<hr/>

### ❓ Q55. **What is the purpose of `useCallback` in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

To prevent functions from being recreated on every render. This is especially important when passing callbacks to optimized child components (like items in a `FlatList`) to prevent them from re-rendering unnecessarily.

> 💡 **Interviewer Focus:** Performance optimization in lists.
</details>
<hr/>

### ❓ Q56. **How do you handle API errors globally?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use an Axios interceptor or a wrapper function around `fetch` that checks the response status and handles errors (e.g., showing a global alert or logging out on 401) before returning the data.

> 💡 **Interviewer Focus:** Centralized error handling.
</details>
<hr/>

### ❓ Q57. **How do you use `StyleSheet.create`?**
<details>
<summary><b>👀 Show Answer</b></summary>

It sends the style object to the native side only once, instead of creating a new object on every render. It also returns an ID rather than a new object, which is faster to pass over the bridge.

> 💡 **Interviewer Focus:** Why it is better than inline styles.
</details>
<hr/>

### ❓ Q58. **What is the difference between `margin` and `padding`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `margin` is the space outside the component's border.
- `padding` is the space between the component's border and its content.
Works the exact same way as on the web.

> 💡 **Interviewer Focus:** Basic CSS layout concepts.
</details>
<hr/>

### ❓ Q59. **How do you handle hardware back button on iOS?**
<details>
<summary><b>👀 Show Answer</b></summary>

iOS devices do not have a hardware back button. Back navigation is usually handled by swipe gestures or a back button in the navigation header (managed by React Navigation).

> 💡 **Interviewer Focus:** Platform differences in UX.
</details>
<hr/>

### ❓ Q60. **What is the purpose of `keyExtractor` in `FlatList`?**
<details>
<summary><b>👀 Show Answer</b></summary>

It is used to extract a unique key for a given item at the specified index. It helps React identify which items have changed, are added, or are removed for efficient re-rendering.

> 💡 **Interviewer Focus:** List optimization.
</details>
<hr/>

### ❓ Q61. **How do you implement a toggle switch?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the built-in `<Switch>` component. It has a `value` prop (boolean) and an `onValueChange` callback.

> 💡 **Interviewer Focus:** Basic component usage.
</details>
<hr/>

### ❓ Q62. **What is the difference between `position: 'absolute'` on web and React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

On the web, `position: absolute` is relative to the nearest positioned ancestor. In React Native, it is always relative to the parent view.

> 💡 **Interviewer Focus:** Nuances of RN layout engine (Yoga).
</details>
<hr/>

### ❓ Q63. **How do you handle large images that cause out-of-memory errors?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `resizeMethod="resize"` prop on the `<Image>` component for Android, or resize the image before loading it using a library or CDN.

> 💡 **Interviewer Focus:** Android-specific image memory issues.
</details>
<hr/>

### ❓ Q64. **What is the purpose of `accessibilityLabel`?**
<details>
<summary><b>👀 Show Answer</b></summary>

It is used by screen readers (like VoiceOver on iOS and TalkBack on Android) to read out a description of the component to visually impaired users.

> 💡 **Interviewer Focus:** Accessibility (a11y) awareness.
</details>
<hr/>

### ❓ Q65. **How do you implement a modal in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the built-in `<Modal>` component or community libraries like `react-native-modal` for more features.

> 💡 **Interviewer Focus:** Modal presentation options.
</details>
<hr/>

### ❓ Q66. **What is the difference between `flex: 1` and `flex: 0`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `flex: 1` makes the component grow to fill all available space.
- `flex: 0` makes the component size based on its content (no growth).

> 💡 **Interviewer Focus:** Flexbox understanding.
</details>
<hr/>

### ❓ Q67. **How do you handle keyboard dismissal?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `Keyboard.dismiss()`. You can call this on button press or use a `<TouchableWithoutFeedback>` wrapping the screen to dismiss the keyboard when the user taps outside the inputs.

> 💡 **Interviewer Focus:** Mobile UX polish.
</details>
<hr/>

### ❓ Q68. **What is the purpose of `hitSlop` prop?**
<details>
<summary><b>👀 Show Answer</b></summary>

It expands the touchable area of a component without changing its layout size. Very useful for making small buttons easier to tap on mobile screens.

> 💡 **Interviewer Focus:** Mobile-specific UX enhancement.
</details>
<hr/>

### ❓ Q69. **How do you pass data between screens in React Navigation?**
<details>
<summary><b>👀 Show Answer</b></summary>

Pass parameters in the `navigate` function: `navigation.navigate('Details', { itemId: 86 })`. Access them in the target screen using `route.params.itemId`.

> 💡 **Interviewer Focus:** Navigation data flow.
</details>
<hr/>

### ❓ Q70. **What is the difference between `npm install` and `pod install`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `npm install` installs JavaScript packages and dependencies listed in `package.json`.
- `pod install` installs native iOS dependencies listed in `Podfile` (CocoaPods). You must run it in the `ios` directory after installing an RN package with native iOS code.

> 💡 **Interviewer Focus:** iOS build process understanding.
</details>
<hr/>

### ❓ Q71. **What is the role of the shadow tree and Yoga layout engine?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Shadow Tree:** An internal C++ representation of the layout structure. As JS executes, it defines UI elements. React Native creates a shadow tree corresponding to the JS virtual tree structure.
- **Yoga Engine:** An open-source layout engine (written in C++) that implements Flexbox layout specifications. It parses the shadow tree, calculates exact dimensions and coordinates for each component, and passes these coordinates to the native UI manager to render real platforms view layers.

> 💡 **Interviewer Focus:** Understanding the intermediate layout step between JS definitions and native views.
</details>
<hr/>

### ❓ Q72. **How do you implement SSL Pinning in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

SSL Pinning prevents Man-In-The-Middle (MITM) attacks by checking the server's certificate or public key against a pinned local certificate copy.
- **Implementation:**
  - You cannot configure SSL pinning directly in standard JS `fetch` or `axios`.
  - Use native libraries like `react-native-ssl-pinning` which wrap native iOS (`AFNetworking`) and Android (`OkHttp`) network clients.
  - Alternatively, configure the native project files directly (e.g. `network_security_config.xml` on Android and trust policies on iOS).

> 💡 **Interviewer Focus:** Security engineering: why default HTTPS is vulnerable to proxy intercepts (like Charles Proxy or Fiddler) and how pinning resolves it.
</details>
<hr/>

### ❓ Q73. **Explain how worklets work in React Native Reanimated (v2/v3).**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Worklets:** Small JavaScript functions compiled to run on the **UI thread** directly in a separate JS context (using a secondary engine context).
- **How they work:**
  - Standard JS functions run on the JS thread, causing animation lag if the JS thread is busy with API calls or calculations.
  - Adding the `"worklet";` directive tells Reanimated to compile the function so it executes synchronously on the UI thread, facilitating 60/120fps animations even when the main JS thread is blocked.

> 💡 **Interviewer Focus:** Multi-JS-runtime concepts and keeping animations running at maximum frame rates.
</details>
<hr/>

### ❓ Q74. **What is the difference between TurboModules and Legacy Native Modules?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Legacy Native Modules:** Loaded eagerly during app startup over the JSON Bridge, increasing cold start time even if the module is never used.
- **TurboModules (New Architecture):**
  - Loaded lazily on demand.
  - Uses JSI (JavaScript Interface) to invoke native C++ methods directly without JSON serialization overhead, minimizing latency.

> 💡 **Interviewer Focus:** Cold start optimizations and direct invocation benefits.
</details>
<hr/>

### ❓ Q75. **How does the Fabric rendering engine differ from the legacy UI Manager?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Legacy UI Manager:** Calculates layout in the shadow thread, serializes coordinate instructions to JSON, and sends them over the bridge to the main thread to render. It cannot handle synchronous layout interactions (like scroll inputs) smoothly.
- **Fabric Renderer (New Architecture):**
  - Written in C++ to run across platforms.
  - Direct communication using JSI, allowing the UI thread to fetch layouts synchronously.
  - Prioritizes UI updates to keep user interactions responsive.

> 💡 **Interviewer Focus:** Layout synchronization and eliminating lag on complex scroll layouts.
</details>
<hr/>

### ❓ Q76. **How do you handle deep links Universal Links (iOS) and App Links (Android) verification?**
<details>
<summary><b>👀 Show Answer</b></summary>

Universal Links (iOS) and App Links (Android) are secure deep links associated directly with a domain.
- **Verification Setup:**
  - **Server-side:** Host a verification file at `/.well-known/apple-app-site-association` (iOS) and `/.well-known/assetlinks.json` (Android) linking your domain to your mobile app bundle ID/signature fingerprints.
  - **App-side:** Configure capabilities (Associated Domains in Xcode, Intent Filters in Android Manifest).
  - When the user clicks a URL, the OS verifies the domain files and routes the link to the app without showing browser picker prompts.

> 💡 **Interviewer Focus:** Server-to-app cryptographic handshakes configuration.
</details>
<hr/>

### ❓ Q77. **What is the role of Fastlane in React Native CI/CD?**
<details>
<summary><b>👀 Show Answer</b></summary>

Fastlane is an open-source tool written in Ruby that automates iOS and Android deployment.
- **Role:**
  - Manages provisioning profiles and signing certificates (`match`).
  - Automates incrementing build versions, building release binaries (`gym` for iOS, `gradle` for Android), and uploading builds to TestFlight and Google Play Console.

> 💡 **Interviewer Focus:** Automating delivery workflows to eliminate manual building tasks.
</details>
<hr/>

### ❓ Q78. **How do you analyze and optimize the bundle size of a React Native app?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Analysis:** Use `react-native-bundle-visualizer` to see which dependencies consume the most kilobytes in the JS bundle.
- **Optimization:**
  - Exclude large libraries; use lightweight alternatives (like `date-fns` instead of `moment`).
  - Configure Proguard on Android to strip unused Java bytecode.
  - Enable `shrinkResources` and `minifyEnabled` in the `build.gradle` file.

> 💡 **Interviewer Focus:** Minimizing download sizes for users on limited bandwidth networks.
</details>
<hr/>

### ❓ Q79. **Explain how code obfuscation is configured for React Native apps.**
<details>
<summary><b>👀 Show Answer</b></summary>

Since JS code bundles are packaged inside the APK/IPA files, they can be easily decompiled and read.
- **Android Obfuscation:** Enable **ProGuard** in `android/app/build.gradle` (`minifyEnabled true`). It obfuscates compiled Java/Kotlin bytecode.
- **JavaScript Obfuscation:** Use tools like `javascript-obfuscator` during Metro bundling phases, or use commercial products (like Dexguard or Guardsquare) to encrypt strings and obfuscate logic paths.

> 💡 **Interviewer Focus:** Protecting API keys and proprietary algorithms from reverse engineering.
</details>
<hr/>

### ❓ Q80. **What is the difference between `react-native-gesture-handler` and the default Responder System?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Default Responder System:** Evaluates gestures entirely on the JavaScript thread. If the JS thread is busy or dropped frames occur, gesture tracking lags.
- **`react-native-gesture-handler`:**
  - Moves gesture interaction logic to the native thread.
  - Communicates directly with native platform touch handlers, keeping gestures smooth and responsive even under heavy JS thread load.

> 💡 **Interviewer Focus:** Thread boundaries and gesture responsiveness.
</details>
<hr/>

### ❓ Q81. **How do you debug JS on physical devices when using Hermes?**
<details>
<summary><b>👀 Show Answer</b></summary>

Since Hermes runs pre-compiled bytecode:
- You cannot use the legacy Chrome remote debugger because Hermes does not use Chrome's JS engine.
- **Hermes Debugging:** Connect the device via USB and use **Flipper** or Chrome DevTools pointing to the local debugger port (`chrome://inspect`). This connects directly to the Hermes engine debugging port on the physical device via a WebSocket bridge.

> 💡 **Interviewer Focus:** Modern debugging workflows using Hermes.
</details>
<hr/>

### ❓ Q82. **What are custom Metro bundler options for asset routing?**
<details>
<summary><b>👀 Show Answer</b></summary>

Configure `metro.config.js` to modify how files are bundled:
- **`assetExts`**: Append support for custom binary assets (like `.ttf`, `.svg`).
- **`sourceExts`**: Prioritize specific code resolutions (e.g., placing `ts`, `tsx` before `js`).
- Use custom transformers (like `react-native-svg-transformer`) to compile SVG files to React components on the fly.

> 💡 **Interviewer Focus:** Metro bundle lifecycle customization.
</details>
<hr/>

### ❓ Q83. **Explain the concept of monorepos in React Native and Expo projects.**
<details>
<summary><b>👀 Show Answer</b></summary>

Monorepos group multiple packages (web app, mobile app, shared API layer) inside a single Git repository.
- **Implementation:**
  - Uses workspaces (Yarn Workspaces, pnpm, or npm workspaces).
  - **Metro configuration:** Metro expects all dependencies in the local `node_modules`. In monorepos, dependencies are hoisted to the root directory. You must configure Metro's `watchFolders` to scan root directories.

> 💡 **Interviewer Focus:** Code sharing and resolution of Metro path hoisting issues.
</details>
<hr/>

### ❓ Q84. **How do you write E2E tests for React Native using Detox?**
<details>
<summary><b>👀 Show Answer</b></summary>

Detox is a grey-box testing framework for mobile apps:
- Unlike black-box testers (like Appium), Detox monitors the internal state of the app, automatically waiting for network requests, layout animations, and thread queues to clear before running test assertions.
- **Writing Tests:** Select elements using `by.id('testID')` and trigger actions: `await element(by.id('login_btn')).tap()`.

> 💡 **Interviewer Focus:** Automated UI testing stability and resolving asynchronous test flakes.
</details>
<hr/>

### ❓ Q85. **How does CodePush perform updates rollback on failure?**
<details>
<summary><b>👀 Show Answer</b></summary>

CodePush tracks deployment health:
- When a new JS bundle is downloaded, CodePush marks it as pending.
- On startup, the app calls `codePush.notifyAppReady()`.
- If the app crashes on launch before calling `notifyAppReady()`, CodePush rolls back to the previous stable JS bundle automatically on the next restart.

> 💡 **Interviewer Focus:** Safe OTA rollouts and crash protection.
</details>
<hr/>

### ❓ Q86. **Explain how memory is managed in JSI (JavaScript Interface) using garbage collection.**
<details>
<summary><b>👀 Show Answer</b></summary>

JSI allows JS code to hold references to C++ Host Objects directly.
- **Memory Management:**
  - JSI objects are garbage collected by the JS engine (Hermes/V8).
  - When the JS reference is garbage collected, the engine triggers the corresponding C++ destructor to free the native memory blocks, preventing memory leaks across runtime boundaries.

> 💡 **Interviewer Focus:** Cross-runtime memory management mechanics.
</details>
<hr/>

### ❓ Q87. **How do you configure SSL Pinning on Android network security config files?**
<details>
<summary><b>👀 Show Answer</b></summary>

Configure `res/xml/network_security_config.xml`:
```xml
<network-security-config>
  <domain-config>
    <domain includeSubdomains="true">example.com</domain>
    <pin-set>
      <pin digest="SHA-256">Base64PublicKeyFingerprint=</pin>
    </pin-set>
  </domain-config>
</network-security-config>
```
Link this file in `AndroidManifest.xml` under the `<application>` tag using `android:networkSecurityConfig`.

> 💡 **Interviewer Focus:** Native Android network security configurations.
</details>
<hr/>

### ❓ Q88. **Explain the difference between `useMemo` and `useCallback` in React Native thread context.**
<details>
<summary><b>👀 Show Answer</b></summary>

While they work identically to React web:
- In React Native, saving computational overhead is even more critical because JS runs on a single thread.
- If a component re-renders and recalculates values, it blocks the JS thread, delaying messages sent to the native thread and causing dropped frames (stuttering UI).

> 💡 **Interviewer Focus:** Performance impacts on mobile thread queues.
</details>
<hr/>

### ❓ Q89. **How do you optimize long-running background tasks in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Mobile operating systems suspend app execution shortly after the app goes to the background.
- **Optimization:**
  - Use native services like `react-native-background-actions` or `react-native-background-fetch`.
  - These register native background tasks with the OS (using Android Foreground Services with a persistent notification, or iOS Background Tasks APIs) to run code when the app is minimized.

> 💡 **Interviewer Focus:** OS background restrictions and system resource governance.
</details>
<hr/>

### ❓ Q90. **What is the purpose of native UI managers?**
<details>
<summary><b>👀 Show Answer</b></summary>

Native UI managers translate React components into platform-specific views (e.g. converting a `<View>` into `ViewGroup` on Android and `UIView` on iOS) and coordinate layout updates calculated by the Yoga engine.

> 💡 **Interviewer Focus:** View rendering pipeline.
</details>
<hr/>

### ❓ Q91. **Explain how you would implement offline synchronizations in WatermelonDB.**
<details>
<summary><b>👀 Show Answer</b></summary>

WatermelonDB is a reactive local database built for offline-first apps:
- It tracks unsynced local changes (creates, updates, deletes).
- **Sync Workflow:**
  - Call `synchronize()` passing `pullChanges` and `pushChanges` function parameters.
  - `pullChanges` fetches remote updates and applies them locally.
  - `pushChanges` sends local unsynced records to the backend, marking them as synced once successful.

> 💡 **Interviewer Focus:** Designing robust offline-first synchronization protocols.
</details>
<hr/>

### ❓ Q92. **How do you troubleshoot thread block issues causing frame drops?**

<details>
<summary><b>👀 Show Answer</b></summary>

- Monitor performance using **Flipper Performance Plugin** or **Xcode Instruments** to isolate CPU usage.
- Look for long-running calculations on the JS thread. Move heavy computations to native modules, use worklets, or chunk execution using `setTimeout` / requestAnimationFrame to yield control back to the thread scheduler.

> 💡 **Interviewer Focus:** Frame budget optimizations (maintaining 16.6ms window for 60fps).
</details>
<hr/>

### ❓ Q93. **Explain the difference between CocoaPods static frameworks and dynamic libraries.**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Static Frameworks:** Compiled code is copied directly into the main application executable binary at build time. Increases binary size but loads faster at startup.
- **Dynamic Libraries:** Linked at runtime. Kept separate from the main binary, reducing compilation sizes but adding loading latency during app startup.

> 💡 **Interviewer Focus:** iOS dependency compilation structures.
</details>
<hr/>

### ❓ Q94. **What is the role of the `Android.mk` and `CMakeLists.txt` files in React Native new architecture?**
<details>
<summary><b>👀 Show Answer</b></summary>

They are build configurations for C++ compilation:
- **`Android.mk`**: Used by the Android NDK (Native Development Kit) to compile C++ source files for legacy builds.
- **`CMakeLists.txt`**: Modern standard used by CMake to compile JSI/C++ code (TurboModules/Fabric components) into shared libraries for Android.

> 💡 **Interviewer Focus:** Android native compilation chains.
</details>
<hr/>

### ❓ Q95. **How do you implement custom SVG rendering in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `react-native-svg` to declare paths and shapes, or compile `.svg` files directly to React component functions using `react-native-svg-transformer`.

> 💡 **Interviewer Focus:** Scalable asset management.
</details>
<hr/>

### ❓ Q96. **Explain how app launch times (TTI) are measured using Flipper.**
<details>
<summary><b>👀 Show Answer</b></summary>

Using the Flipper Performance Profiler, you measure the time from process creation (native init) to the point where the JS bundle completes loading and renders the first interactive screen (Time to Interactive).

> 💡 **Interviewer Focus:** Launch speed analytics.
</details>
<hr/>

### ❓ Q97. **How do you implement dynamic orientation layout changes using Hooks?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `useWindowDimensions()` hook to fetch layout bounds:
```typescript
const { width, height } = useWindowDimensions();
const isLandscape = width > height;
```
This hook automatically triggers a re-render when the device orientation changes.

> 💡 **Interviewer Focus:** Responsive layout architectures.
</details>
<hr/>

### ❓ Q98. **What is the role of `AppState` listener in stopping active threads?**
<details>
<summary><b>👀 Show Answer</b></summary>

When the app goes to the `background` state, it is best practice to stop active socket connections, pause background tracking, and clear CPU-heavy polling tasks to prevent the OS from force-killing the app due to excessive background battery usage.

> 💡 **Interviewer Focus:** App lifecycle governance.
</details>
<hr/>

### ❓ Q99. **Explain how `react-native-keychain` secures access to storage keys using biometrics.**
<details>
<summary><b>👀 Show Answer</b></summary>

It writes sensitive credentials to Keychain (iOS) or Keystore (Android) configured with biometric access requirements. Accessing the key at runtime prompts the user for FaceID/Fingerprint authentication before returning the decrypted secret.

> 💡 **Interviewer Focus:** Native hardware security integration.
</details>
<hr/>

### ❓ Q100. **How do you build multi-bundle applications for micro-frontends in React Native?**
<details>
<summary><b>👀 Show Answer</b></summary>

By splitting the JavaScript code into multiple bundles:
- Run a core bundle containing shared dependencies (React, React Native, common state).
- Load feature-specific bundles dynamically using tools like **Re.Pack** (a Webpack-based bundler for React Native) to lazy-load micro-frontend bundles over a CDN.

> 💡 **Interviewer Focus:** Scaling large apps using micro-frontend architecture.
</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Next.js](./04_Nextjs.md) | [Home](./00_Index.md) | [➡️ Angular](./06_Angular.md) |
