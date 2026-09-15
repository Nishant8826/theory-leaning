# 09 — Website & UTM Tracking

## 📌 1. Overview & Client-Side Attribution Dynamics

The company website is the ultimate conversion hub where traffic from Instagram, Google, LinkedIn, YouTube, and offline QR campaigns transforms into verified business leads. 

However, **70% of attribution data is lost on websites** due to naive implementations:
* A user clicks an Instagram ad with UTMs on `example.com/promo`.
* They click "About Us" $\rightarrow$ UTM parameters disappear from the URL.
* They browse 4 more pages and finally click "Contact Sales".
* Naive form captures: `source: "direct"`, permanently erasing the Instagram campaign credit.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CROSS-PAGE ATTRIBUTION PERSISTENCE LIFECYCLE                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ Step 1: Entry Page ] ──► [ Step 2: Internal Browsing ] ──► [ Step 3: Form Submit ]  │
│  https://acme.com/promo?    https://acme.com/pricing          https://acme.com/contact │
│  utm_source=instagram&      (URL has NO UTMs!)                (Submits Lead Form)      │
│  utm_campaign=summer26                                                                 │
│         │                             │                                 │              │
│         ▼                             ▼                                 ▼              │
│  [ LMS Tracker SDK ]        [ LMS Tracker SDK ]               [ Form Interceptor ]     │
│  Saves to 1st-Party         Reads existing session            Attaches First-Touch &   │
│  Cookies & LocalStorage     maintains touchpoint history      Last-Touch to POST body  │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🍪 2. Multi-Layer Storage Architecture

To withstand browser refreshes, cross-subdomain transitions (`blog.acme.com` $\rightarrow$ `app.acme.com`), and browser privacy restrictions (Apple Safari ITP / Firefox ETP), we deploy a **3-tier client storage model**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLIENT-SIDE STORAGE TIERS                          │
├───────────────────┬──────────────────────────┬──────────────────────────────┤
│ Storage Tier      │ Scope & Lifetime         │ Architectural Purpose        │
├───────────────────┼──────────────────────────┼──────────────────────────────┤
│ 1. 1st-Party      │ Domain-wide (`.acme.com`)│ Cross-subdomain attribution. │
│    Cookie         │ Lifetime: 90 days        │ Preserves First-Touch state. │
├───────────────────┼──────────────────────────┼──────────────────────────────┤
│ 2. LocalStorage   │ Origin-scoped            │ Resilient backup against     │
│                   │ Lifetime: Persistent     │ cookie clearing / strict ITP.│
├───────────────────┼──────────────────────────┼──────────────────────────────┤
│ 3. SessionStorage │ Single Browser Tab       │ Maintains intra-session      │
│                   │ Lifetime: Tab session    │ journey and page view count. │
└───────────────────┴──────────────────────────┴──────────────────────────────┘
```

---

## ⚙️ 3. First-Touch vs. Last-Touch Persistence Algorithm

The LMS Client SDK maintains two distinct attribution payloads in client storage:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DUAL-SLOT ATTRIBUTION CAPTURE LOGIC                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  Incoming Visit with UTMs / Click IDs                                                  │
│         │                                                                              │
│         ├────────► Check if `lms_first_touch` cookie exists?                           │
│         │          ├── NO:  Write current UTMs to `lms_first_touch` (Never overwrite)  │
│         │          └── YES: Keep existing `lms_first_touch` untouched                  │
│         │                                                                              │
│         └────────► Always overwrite `lms_last_touch` cookie with latest UTMs           │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Storage Payload Example (`lms_attribution`)
```json
{
  "anonymousId": "anon_98f4a1c2-3e81-4b72-a982-129849102834",
  "firstTouch": {
    "source": "instagram",
    "medium": "paid_social",
    "campaign": "summer_sale_2026",
    "content": "story_video_v1",
    "clickId": "fbclid_IwAR28301982039",
    "landingPage": "https://acme.com/features",
    "referrer": "https://l.instagram.com/",
    "timestamp": "2026-06-01T10:15:30.000Z"
  },
  "lastTouch": {
    "source": "google",
    "medium": "cpc",
    "campaign": "brand_search_usa",
    "content": "headline_demo",
    "clickId": "gclid_EAIaIQobChMI892",
    "landingPage": "https://acme.com/pricing",
    "referrer": "https://www.google.com/",
    "timestamp": "2026-06-15T14:22:10.000Z"
  },
  "session": {
    "pageViewsCount": 6,
    "sessionStartTime": "2026-06-15T14:10:00.000Z"
  }
}
```

---

## 💻 4. Production-Grade JavaScript Tracking Snippet (`lms-tracker.js`)

```javascript
(function (window, document) {
  'use strict';

  const STORAGE_KEY_FIRST = 'lms_first_touch';
  const STORAGE_KEY_LAST = 'lms_last_touch';
  const STORAGE_KEY_ANON = 'lms_anon_id';

  function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  function getUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0,
        v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  function parseAttribution() {
    const url = new URL(window.location.href);
    const params = url.searchParams;

    const source = params.get('utm_source') || (document.referrer ? new URL(document.referrer).hostname : 'direct');
    const medium = params.get('utm_medium') || (source === 'direct' ? 'direct' : 'organic');
    const campaign = params.get('utm_campaign') || 'unspecified';
    const content = params.get('utm_content') || '';
    const term = params.get('utm_term') || '';

    // Extract Platform Click IDs
    const clickId = params.get('gclid') || params.get('fbclid') || params.get('li_fat_id') || params.get('ttclid') || params.get('twclid') || '';

    return {
      source: source.toLowerCase().trim(),
      medium: medium.toLowerCase().trim(),
      campaign: campaign.toLowerCase().trim(),
      content: content.trim(),
      term: term.trim(),
      clickId: clickId,
      landingPage: window.location.href,
      referrer: document.referrer,
      timestamp: new Date().toISOString()
    };
  }

  function initTracker() {
    let anonId = localStorage.getItem(STORAGE_KEY_ANON);
    if (!anonId) {
      anonId = getUUID();
      localStorage.setItem(STORAGE_KEY_ANON, anonId);
    }

    const currentAttribution = parseAttribution();

    // 1. First-Touch Persistence (Immutable)
    if (!localStorage.getItem(STORAGE_KEY_FIRST)) {
      localStorage.setItem(STORAGE_KEY_FIRST, JSON.stringify(currentAttribution));
      document.cookie = `${STORAGE_KEY_FIRST}=${encodeURIComponent(JSON.stringify(currentAttribution))}; path=/; max-age=7776000; SameSite=Lax`;
    }

    // 2. Last-Touch Persistence (Only update if current visit has explicit UTMs or Referrer is external)
    const hasExplicitUTM = window.location.search.includes('utm_') || currentAttribution.clickId;
    if (hasExplicitUTM || !localStorage.getItem(STORAGE_KEY_LAST)) {
      localStorage.setItem(STORAGE_KEY_LAST, JSON.stringify(currentAttribution));
      document.cookie = `${STORAGE_KEY_LAST}=${encodeURIComponent(JSON.stringify(currentAttribution))}; path=/; max-age=7776000; SameSite=Lax`;
    }

    // 3. Auto-Inject into all Form Submissions on page
    document.addEventListener('submit', function (e) {
      const form = e.target;
      const firstTouch = JSON.parse(localStorage.getItem(STORAGE_KEY_FIRST) || '{}');
      const lastTouch = JSON.parse(localStorage.getItem(STORAGE_KEY_LAST) || '{}');

      const appendHidden = (name, val) => {
        let input = form.querySelector(`input[name="${name}"]`);
        if (!input) {
          input = document.createElement('input');
          input.type = 'hidden';
          input.name = name;
          form.appendChild(input);
        }
        input.value = typeof val === 'object' ? JSON.stringify(val) : val;
      };

      appendHidden('lms_anonymous_id', anonId);
      appendHidden('lms_first_touch', firstTouch);
      appendHidden('lms_last_touch', lastTouch);
    }, true);
  }

  window.LMS_Tracker = { init: initTracker };
  initTracker();
})(window, document);
```

---

## ⚡ 5. SPA Route Change Handling (Next.js / React)

In Single Page Applications (SPAs), page transitions occur via the HTML5 `History.pushState()` without triggering a full browser reload. The tracker listens to route events:

```typescript
// React / Next.js Hook Integration
import { useEffect } from 'react';
import { useRouter } from 'next/router';

export function useAttributionTracker() {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      if (typeof window !== 'undefined' && (window as any).LMS_Tracker) {
        (window as any).LMS_Tracker.init();
      }
    };

    router.events.on('routeChangeComplete', handleRouteChange);
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router.events]);
}
```

---

Previous : [08_YouTube_Lead_Integration.md](./08_YouTube_Lead_Integration.md) | Index: [00_Index.md](../00_Index.md) | Next: [10_Offline_Lead_Attribution.md](./10_Offline_Lead_Attribution.md)
