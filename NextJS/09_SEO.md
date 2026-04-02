# 09 – SEO in Next.js

---

## What is SEO?

SEO (Search Engine Optimization) is the practice of making your website **discoverable by search engines** like Google, Bing, and DuckDuckGo so it appears higher in search results.

```
User searches: "best running shoes"
        ↓
Google crawls millions of pages
        ↓
Google ranks pages based on content, performance, and relevance
        ↓
Your page appears on page 1 (if SEO is good) or page 50 (if not)
```

---

## Why Does SEO Matter?

| Fact | Impact |
|------|--------|
| 68% of online experiences start with a search engine | No SEO = No traffic |
| 75% of users never scroll past page 1 | Page 2 = invisible |
| Organic search drives 53% of all website traffic | SEO is the single biggest traffic source |
| SEO leads have 14.6% close rate vs 1.7% for outbound | Higher quality leads |

**Real-world Example:**
Your e-commerce site sells shoes. If someone Googles "buy running shoes online" and your site doesn't appear — you're invisible. With good SEO, you rank on page 1 and get free, organic traffic worth thousands of dollars per month.

---

## How Next.js Helps with SEO

### Why React (CSR) is Bad for SEO

```
Google crawler visits a CSR React app:
        ↓
Receives: <div id="root"></div>   ← Empty HTML!
        ↓
Google sees: NOTHING to index
        ↓
Result: Your page doesn't rank
```

### Why Next.js (SSR/SSG) is Great for SEO

```
Google crawler visits a Next.js SSR/SSG app:
        ↓
Receives: Full HTML with all content
  <h1>Best Running Shoes 2024</h1>
  <p>Compare top brands...</p>
        ↓
Google indexes ALL the content
        ↓
Result: Your page ranks well ✅
```

---

## ⭐ Most Important Concepts

### 1. Metadata API (Next.js 13+)

The Metadata API is the primary way to set SEO tags in the App Router.

#### Static Metadata

```jsx
// app/page.js
export const metadata = {
  title: 'Best Running Shoes 2024 | ShoeStore',
  description: 'Compare and buy the top-rated running shoes. Free shipping on orders over $50.',
  keywords: ['running shoes', 'best shoes 2024', 'athletic footwear'],
  
  openGraph: {
    title: 'Best Running Shoes 2024',
    description: 'Top-rated running shoes compared.',
    images: ['/images/running-shoes-og.jpg'],
    url: 'https://shoestore.com/running-shoes',
    type: 'website',
  },
  
  twitter: {
    card: 'summary_large_image',
    title: 'Best Running Shoes 2024',
    description: 'Top-rated running shoes compared.',
    images: ['/images/running-shoes-og.jpg'],
  },
};

export default function HomePage() {
  return <h1>Best Running Shoes 2024</h1>;
}
```

**What this generates in HTML:**
```html
<head>
  <title>Best Running Shoes 2024 | ShoeStore</title>
  <meta name="description" content="Compare and buy the top-rated running shoes..." />
  <meta property="og:title" content="Best Running Shoes 2024" />
  <meta property="og:image" content="/images/running-shoes-og.jpg" />
  <!-- ... more meta tags -->
</head>
```

#### Dynamic Metadata (Per-Page, Data-Driven)

```jsx
// app/products/[id]/page.js
export async function generateMetadata({ params }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`)
    .then(res => res.json());

  return {
    title: `${product.name} | ShoeStore`,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      images: [product.imageUrl],
    },
  };
}

export default async function ProductPage({ params }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`)
    .then(res => res.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  );
}
```

#### Title Templates (Consistent Branding)

```jsx
// app/layout.js — Set a template
export const metadata = {
  title: {
    template: '%s | ShoeStore',   // %s is replaced by child page title
    default: 'ShoeStore — Best Shoes Online',
  },
};

// app/about/page.js
export const metadata = {
  title: 'About Us',          // Renders as: "About Us | ShoeStore"
};

// app/products/page.js
export const metadata = {
  title: 'All Products',      // Renders as: "All Products | ShoeStore"
};
```

### 2. Structured Data (JSON-LD)

Structured data tells Google exactly what your content is about using a format called JSON-LD.

```jsx
// app/products/[id]/page.js
export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.id);

  // JSON-LD structured data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.imageUrl,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <h1>{product.name}</h1>
      <p>${product.price}</p>
    </>
  );
}
```

**Impact:** Google can show rich results like star ratings, price, and availability directly in search results.

### 3. Sitemap Generation

A sitemap is an XML file that tells search engines about all the pages on your site.

```jsx
// app/sitemap.js
export default async function sitemap() {
  const products = await fetch('https://api.example.com/products')
    .then(res => res.json());

  const productUrls = products.map(product => ({
    url: `https://shoestore.com/products/${product.id}`,
    lastModified: product.updatedAt,
    changeFrequency: 'weekly',
    priority: 0.8,
  }));

  return [
    {
      url: 'https://shoestore.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://shoestore.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...productUrls,
  ];
}

// Generates: https://shoestore.com/sitemap.xml
```

### 4. Robots.txt

Controls which pages search engines should or shouldn't crawl.

```jsx
// app/robots.js
export default function robots() {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/dashboard/'],
      },
    ],
    sitemap: 'https://shoestore.com/sitemap.xml',
  };
}

// Generates: https://shoestore.com/robots.txt
```

### 5. Canonical URLs

Prevent duplicate content issues when the same page is accessible via multiple URLs.

```jsx
export const metadata = {
  alternates: {
    canonical: 'https://shoestore.com/products/running-shoes',
  },
};
```

---

## Impact – SEO Checklist for a Real Application

| Item | Implementation | Priority |
|------|---------------|----------|
| ✅ Title tags on every page | `metadata.title` | Critical |
| ✅ Meta descriptions | `metadata.description` | Critical |
| ✅ Open Graph tags | `metadata.openGraph` | High |
| ✅ Structured data (JSON-LD) | Script tag in pages | High |
| ✅ Sitemap | `app/sitemap.js` | High |
| ✅ Robots.txt | `app/robots.js` | High |
| ✅ Canonical URLs | `metadata.alternates.canonical` | Medium |
| ✅ SSR/SSG for public pages | Rendering strategy | Critical |
| ✅ Semantic HTML tags | `<h1>`, `<article>`, `<nav>` | High |
| ✅ Image alt text | `alt` prop on `<Image>` | High |
| ✅ Fast page load (< 2.5s LCP) | Performance optimization | Critical |
| ✅ Mobile responsive | CSS media queries | Critical |

---

## Interview Questions & Answers

### Q1: Why is Next.js better for SEO than React (CRA)?
**Answer:** React (CRA) uses Client-Side Rendering, which sends an empty HTML shell to browsers and search crawlers. Google sees minimal content to index. Next.js uses SSR/SSG to send fully rendered HTML, so search engines can crawl and index all content immediately.

### Q2: How do you add meta tags in the Next.js App Router?
**Answer:** Export a `metadata` object (static) or a `generateMetadata` function (dynamic) from your page or layout. It accepts `title`, `description`, `openGraph`, `twitter`, `robots`, and more. Next.js automatically renders these as `<meta>` tags in the HTML `<head>`.

### Q3: What is the difference between static and dynamic metadata?
**Answer:** Static metadata uses `export const metadata = {...}` — values are hardcoded. Dynamic metadata uses `export async function generateMetadata({ params })` — values are fetched from an API or database based on the page parameters. Dynamic is used for product pages, blog posts, etc.

### Q4: What is Open Graph and why is it important?
**Answer:** Open Graph (OG) meta tags control how your page looks when shared on social media (Facebook, Twitter, LinkedIn, WhatsApp). They define the preview title, description, and image. Without OG tags, social platforms show generic or incorrect previews.

### Q5: What is structured data (JSON-LD)?
**Answer:** JSON-LD is a format for providing structured information about your content to search engines. It enables rich results in Google — like star ratings, prices, and FAQs appearing directly in search results. Common schemas: Product, Article, FAQ, Organization.

### Q6: What is a sitemap and how do you create one in Next.js?
**Answer:** A sitemap is an XML file listing all your site's URLs for search engines. In Next.js, create `app/sitemap.js` that exports a function returning an array of URL objects. Next.js auto-generates the XML at `/sitemap.xml`.

### Q7 (Scenario): Your e-commerce product pages have great content but no Google traffic. What could be wrong?
**Answer:** Check for: (1) Missing or poor meta descriptions, (2) CSR-only rendering, (3) No sitemap submitted to Google Search Console, (4) `robots.txt` blocking crawlers, (5) No structured data for rich results, (6) Slow page load (high LCP), (7) Duplicate content without canonical URLs.

### Q8 (Scenario): The same product page is accessible at 3 different URLs. Google is penalizing for duplicate content. How do you fix it?
**Answer:** Set a canonical URL using `metadata.alternates.canonical` pointing to the primary URL. This tells Google which version is the "real" one and to ignore duplicates.

---

### 🔗 Navigation

---

← Previous: [08_Performance_Optimization.md](08_Performance_Optimization.md) | Next: [10_Deployment.md](10_Deployment.md) →
