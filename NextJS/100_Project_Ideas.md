# 100 – Real-World Project Ideas 🛠️

> Build these projects to go from beginner to job-ready. Each project is designed to teach you specific Next.js concepts.

---

## 🟢 Beginner Level (1–3)

### 1. Personal Portfolio Website

**Description:** A portfolio to showcase your projects, skills, and contact info.

**What You'll Learn:**
- File-based routing (`/`, `/about`, `/projects`, `/contact`)
- Layouts (shared navbar + footer)
- `next/image` for project screenshots
- `next/font` for custom typography
- Static Site Generation (SSG)
- SEO metadata (Open Graph for social sharing)

**Pages:**
| Route | Content |
|-------|---------|
| `/` | Hero section, featured projects |
| `/about` | Bio, skills, experience |
| `/projects` | Project grid with details |
| `/projects/[slug]` | Individual project detail page |
| `/contact` | Contact form |

**Key Features:**
- Dark mode toggle (Client Component with `useState`)
- Responsive design
- Contact form using Server Action
- Deploy to Vercel

**Concepts Covered:** Routing, Layouts, SSG, SEO, Image Optimization, Server Actions

---

### 2. Blog with Markdown / CMS

**Description:** A blog where posts are written in Markdown files or fetched from a headless CMS (like Contentful, Sanity, or Notion).

**What You'll Learn:**
- Static Site Generation per blog post (`generateStaticParams`)
- Dynamic metadata for SEO per post
- ISR for content updates
- Sitemap and robots.txt generation
- Markdown parsing (with `gray-matter` + `remark`)

**Pages:**
| Route | Rendering | Content |
|-------|-----------|---------|
| `/` | SSG | Homepage with recent posts |
| `/blog` | SSG | All blog posts list |
| `/blog/[slug]` | SSG + ISR | Individual blog post |
| `/categories/[name]` | SSG | Posts filtered by category |

**Key Features:**
- Search functionality (Client Component)
- Table of Contents auto-generated from headings
- Reading time estimation
- Social sharing buttons
- Related posts section

**Concepts Covered:** SSG, ISR, Dynamic Routes, Metadata, Sitemap, Markdown Processing

---

### 3. Recipe Finder App

**Description:** Search and browse recipes from a public API (like TheMealDB or Spoonacular).

**What You'll Learn:**
- Client-side data fetching with SWR
- Server Components for initial page load
- Dynamic routes for recipe details
- Search with URL query parameters
- Loading states with `loading.js`

**Pages:**
| Route | Content |
|-------|---------|
| `/` | Featured recipes (SSG) |
| `/search?q=pasta` | Search results (CSR) |
| `/recipe/[id]` | Recipe detail (SSR) |
| `/favorites` | Saved favorites (CSR, localStorage) |

**Concepts Covered:** CSR, SSR, SWR, Dynamic Routes, Loading States, URL Search Params

---

## 🟡 Intermediate Level (4–7)

### 4. E-Commerce Store

**Description:** A full e-commerce storefront with product listings, detail pages, cart, and checkout.

**What You'll Learn:**
- ISR for product pages (prices/stock update periodically)
- Server Components for product data
- Client Components for cart interactions
- Server Actions for cart mutations
- API Routes for checkout/payment webhooks
- Middleware for auth-protected checkout
- SEO + Structured Data (JSON-LD for products)

**Pages:**
| Route | Rendering | Content |
|-------|-----------|---------|
| `/` | ISR (60s) | Homepage, featured products |
| `/products` | ISR (60s) | Product listing with filters |
| `/products/[id]` | ISR (30s) | Product detail page |
| `/cart` | CSR | Shopping cart |
| `/checkout` | SSR (protected) | Checkout flow |
| `/orders` | SSR (protected) | Order history |

**Key Features:**
- Add to Cart button (Client Component + Server Action)
- Product filtering by category, price, size
- Stripe payment integration
- Order confirmation emails
- Admin panel for product management

**Concepts Covered:** ISR, Server Actions, API Routes, Middleware, Auth, Structured Data, Webhooks

---

### 5. Social Media Feed (Instagram Clone)

**Description:** A social media app with posts, likes, comments, and user profiles.

**What You'll Learn:**
- Authentication with NextAuth (Google + credentials)
- Real-time updates with optimistic UI
- Complex Server Actions (like, comment, follow)
- File uploads for post images
- Infinite scroll (Client Component)
- Parallel routes for modals (photo detail)

**Pages:**
| Route | Rendering | Content |
|-------|-----------|---------|
| `/` | SSR | Personalized feed |
| `/[username]` | SSR | User profile |
| `/[username]/post/[id]` | SSR | Single post detail |
| `/explore` | ISR | Discover new content |
| `/messages` | CSR | Direct messages |

**Key Features:**
- Like button with optimistic updates
- Comment system
- Follow/unfollow
- Image upload with preview
- Notification system
- Photo modal using intercepting routes

**Concepts Covered:** Auth, Server Actions, Optimistic Updates, File Uploads, Parallel Routes, Intercepting Routes

---

### 6. Task Management Dashboard (Trello Clone)

**Description:** A Kanban board for managing tasks with drag-and-drop, teams, and real-time sync.

**What You'll Learn:**
- Complex state management (Client Components)
- Drag and drop (dnd-kit library)
- Server Actions for CRUD operations
- Database integration (Prisma + PostgreSQL)
- Team collaboration features
- Middleware for workspace auth

**Pages:**
| Route | Rendering | Content |
|-------|-----------|---------|
| `/` | SSG | Landing page |
| `/login` | CSR | Auth page |
| `/boards` | SSR (protected) | All boards |
| `/board/[id]` | SSR | Kanban board with columns/tasks |
| `/board/[id]/settings` | SSR | Board settings |

**Key Features:**
- Drag tasks between columns
- Create/edit/delete boards, columns, tasks
- Assign team members
- Due dates and labels
- Activity log

**Concepts Covered:** Server Actions, Prisma, Auth, Middleware, Complex Client State, Revalidation

---

### 7. Multi-Tenant SaaS Dashboard

**Description:** A SaaS application where each company gets their own dashboard with subdomains.

**What You'll Learn:**
- Middleware for subdomain routing
- Role-based access (admin, editor, viewer)
- Multi-tenant data isolation
- Nested layouts (sidebar + topbar)
- API rate limiting
- Environment variable management

**Pages:**
| Route | Rendering | Content |
|-------|-----------|---------|
| `app.domain.com/` | SSG | Marketing site |
| `[company].domain.com/dashboard` | SSR | Company dashboard |
| `[company].domain.com/settings` | SSR | Settings |
| `[company].domain.com/team` | SSR | Team management |
| `[company].domain.com/billing` | SSR | Billing & plans |

**Concepts Covered:** Middleware, Auth, Nested Layouts, Route Groups, Multi-Tenant Architecture

---

## 🔴 Advanced Level (8–10)

### 8. Real-Time Chat Application

**Description:** A full-featured chat app with WebSockets, typing indicators, and read receipts.

**What You'll Learn:**
- WebSocket integration with Next.js
- Server-Sent Events (SSE)
- Custom API routes for real-time features
- Authentication and authorization
- Message persistence with database
- Optimistic UI for message sending

**Key Features:**
- 1-on-1 and group chats
- Typing indicator
- Online/offline status
- Message read receipts
- File/image sharing
- Push notifications

**Concepts Covered:** API Routes, Auth, Real-Time Communication, Database, Optimistic Updates

---

### 9. AI-Powered Content Platform

**Description:** A platform that uses AI APIs (OpenAI, Claude) to generate, summarize, and translate content.

**What You'll Learn:**
- Streaming responses (AI responses stream word-by-word)
- Server Actions for AI API calls
- Caching strategies for generated content
- Rate limiting middleware
- Cost management (tracking API usage)
- Edge functions for fast AI responses

**Key Features:**
- Blog post generator
- Content summarizer
- Language translator
- Image generator integration
- Usage dashboard with limits
- Saved generations history

**Concepts Covered:** Streaming, Server Actions, Caching, Middleware, API Integration, Edge Functions

---

### 10. Full-Stack E-Learning Platform

**Description:** A complete learning platform like Udemy with courses, video streaming, progress tracking, and payments.

**What You'll Learn:**
- Everything in Next.js combined into one project
- Video streaming and player integration
- Payment processing (Stripe subscriptions)
- Complex database schema (Prisma)
- Admin CMS for course management
- Performance optimization at scale

**Key Features:**
- Course catalog with filtering and search
- Video player with progress tracking
- Quiz system
- Certificate generation
- Instructor dashboard
- Student progress dashboard
- Stripe subscription billing
- Admin panel

**Concepts Covered:** ALL Next.js concepts — this is the capstone project

---

## 📋 Project Difficulty Progression

```
Beginner:
  1. Portfolio         → Routing, Layouts, SSG, SEO
  2. Blog              → SSG, ISR, Dynamic Routes, Metadata
  3. Recipe Finder     → CSR, SSR, SWR, API Fetching

Intermediate:
  4. E-Commerce        → ISR, Server Actions, API Routes, Auth
  5. Social Media      → Auth, Optimistic UI, File Upload
  6. Task Dashboard    → Drag & Drop, Prisma, Complex State
  7. SaaS Dashboard    → Middleware, Multi-Tenant, RBAC

Advanced:
  8. Chat App          → WebSockets, Real-time, Streaming
  9. AI Platform       → AI APIs, Streaming, Edge Functions
  10. E-Learning       → EVERYTHING combined (capstone)
```

---

## 💡 Tips for Building Projects

1. **Start simple, add complexity** — Get the basics working before adding advanced features
2. **Use a real database** — Don't mock data. Use PostgreSQL/MongoDB with Prisma
3. **Deploy early** — Push to Vercel from day 1. Fix deployment issues early
4. **Write clean code** — Future employers will review your GitHub
5. **Document your work** — Add a good README with screenshots and live demo link
6. **Take notes on what you learn** — Your notes become interview preparation

---

### 🔗 Navigation

---

← Previous: [99_Revision_CheatSheet.md](99_Revision_CheatSheet.md) | Next: []()
