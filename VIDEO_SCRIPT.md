## START (30 sec)

### Open: `exercise/CANDIDATE_BRIEF.md`

**Say:**
- Hi, I’m Nishant.
- In this exercise I am the integrator.
- Someone else built a poll module and said it is drop-in and all green.
- My job is to make it a normal part of the host app.
- In this video I will cover 4 things:
  1. what the poll module does
  2. what I changed and why
  3. what the green tests miss
  4. whether I would ship it

---

## 1) What the module does (about 1.5 min)

### Open: `project-b-poll-module/README.md`

**Say:**
- This module is a polling / voting feature.
- Users can do these things:
  - **Create** a poll with one question and 2 to 4 options
  - **List** only their own polls
  - **Vote** on one option
  - **See results** / vote counts
  - **Rename** a poll
  - **Delete** a poll
- Create is rate limited: max **5 new polls per user per minute**
- That limit is stored in the database, not in memory

### Open: `project-b-poll-module/src/trpc/poll.router.ts`

**Say:**
- Here is the data flow, step by step:
  1. `create` saves the poll, then saves the options
  2. `listMine` returns polls for the current user
  3. `vote` finds an option and increases its vote count
  4. `results` returns the poll and all option counts
  5. `rename` changes the question
  6. `remove` deletes the poll
- So this is the full feature surface I needed to fold into the host app

### Open: `project-a-host-app/src/server/trpc/notes.router.ts`

**Say:**
- Before changing anything, I read the host pattern.
- Notes is the example feature they want me to copy.
- From notes I learned 3 rules:
  1. user id is a **string** from Clerk, like `"user_abc..."`
  2. row ids are **text**, not auto integer numbers
  3. when you update or delete, you must check **id and ownerId** together
- So my plan was: make poll follow these same rules

---

## 2) What I changed to make it native (about 3 min)

For each change: first open old file (project-b), then new file (host).

---

### Change A — one tRPC, not two

**Open 1:** `project-b-poll-module/src/trpc/trpc.ts`

**Say:**
- Look here: the poll module creates its **own** tRPC setup.
- It also expects `userId` as a **number**.
- That does not match the host app.

**Open 2:** `project-a-host-app/src/server/trpc/trpc.ts`

**Say:**
- Host app already has **one** tRPC setup.
- Here `userId` is a **string or null**.
- Auth uses `protectedProcedure`, which blocks if user is not logged in.
- The rule is: do not create a second tRPC instance.

**Open 3:** `project-a-host-app/src/server/trpc/poll.router.ts` (top of file)

**Say:**
- So I rebuilt the poll router on the host side.
- It imports `router` and `protectedProcedure` from the host `trpc.ts`.
- It does **not** use project-b’s own tRPC file.

**Open 4:** `project-a-host-app/src/server/trpc/root.ts`

**Say:**
- Then I mounted it on the root router as `polls`.
- Now the app has `notes` and `polls` together.
- Client can call `trpc.polls.create`, `trpc.polls.vote`, and so on, with full TypeScript types.

**Why this matters:**
- Native means there should on =ly one router tree not multiple.

---

### Change B — one database client, not two

**Open 1:** `project-b-poll-module/src/db/client.ts`

**Say:**
- Project-b opens its **own** database connection.
- It even supports a separate `POLL_DATABASE_URL`.
- That makes it feel “self-contained,” but it is wrong for this host.

**Open 2:** `project-a-host-app/src/server/db/client.ts`

**Say:**
- Host says clearly: there is **one** `db` for the whole app.
- Every feature should import this same client.
- This matters more on Cloudflare Workers, because Workers are short-lived and should not open many connections.

**Open 3:** `project-a-host-app/src/server/trpc/poll.router.ts`

**Say:**
- In my integrated poll router, all queries use the host `db`.
- I did not keep project-b’s separate DB client.

**Why this matters:**
- Native integration = share host infrastructure, do not bring a second pool.

---

### Change C — fix IDs and schema

**Open 1:** `project-b-poll-module/src/db/schema.ts`

**Say:**
- Old schema uses:
  - `serial` integer primary keys
  - integer `ownerId`
- That matches an old app with numeric users.
- It does **not** match Clerk.

**Open 2:** `project-a-host-app/src/server/db/schema.ts`

**Say:**
- In host schema I added:
  - `polls`
  - `options`
  - `poll_create_events`
- All ids are **text**
- `ownerId` / `userId` are **string**
- This matches notes and Clerk

---

### Change D — ownership bug (most important)

**Open 1:** `project-b-poll-module/src/trpc/poll.router.ts`  
Scroll to `rename` and `remove`

**Say:**
- This is the biggest problem in the original module.
- `rename` updates by `pollId` only.
- `remove` deletes by `pollId` only.
- There is **no owner check**.
- So any logged-in user can rename or delete **someone else’s** poll.
- That is not safe for production.

**Open 2:** `project-a-host-app/src/server/trpc/poll.router.ts`  
Scroll to `rename` and `remove`

**Say:**
- I fixed it like notes.
- Update/delete only happens when **both** match:
  - poll id
  - current user’s `ownerId`
- On delete, I also remove options first, so no orphan rows stay behind.

**Why this matters:**
- This is a real security/auth bug.
- Green tests never caught it, because they only use one user.

---

### Change E — safer voting

**Open:** `project-a-host-app/src/server/trpc/poll.router.ts` → `vote`

**Say:**
- Old vote logic was:
  1. read current votes
  2. add 1 in code
  3. write back
- If two people vote at the same time, one update can overwrite the other.
- That is a race condition.
- My version uses SQL `votes = votes + 1` in one step.
- That is safer under concurrent votes.
- Also, host `npm run build` / type-check passes after integration.

---

## 3) What the tests miss (about 1.5 min)

### Open: `project-b-poll-module/tests/poll.test.ts`

**Say:**
- The README says tests are all green.
- So I opened the test file to see what they really protect.

**What they do cover (happy path only):**
- create a poll
- list my polls
- vote three times one after another
- get results
- block the 6th create in one minute

**What they miss (important):**

1. **Only one user**
   - Every test uses `userId = 1`
   - No second user tries to attack another user’s poll

2. **No ownership tests**
   - No test for rename/remove by a different user
   - So the auth hole can stay hidden

3. **rename and remove are not tested at all**
   - Those endpoints exist in code, but the suite never calls them

4. **Votes are sequential only**
   - They vote one by one
   - They never test two votes at the same time
   - So the race bug is not caught

5. **Wrong auth model for host**
   - Tests assume numeric user ids
   - Host uses Clerk string ids
   - These tests cannot prove the module fits the host

6. **Infrastructure mismatches not tested**
   - Separate tRPC instance
   - Separate DB connection
   - These are integration risks, not unit happy-path checks

**Main line to say:**
- Green tests are useful for basic flow.
- They are **not enough** to sign off for production.

---

## 4) Would you ship? (about 1 min)

**Say clearly:**

### For original project-b “drop-in”: **NO**

Reasons:
- wrong user id type (number vs Clerk string)
- separate tRPC instance
- separate DB client
- missing ownership checks on rename/remove

I would **not** merge that as-is.

### For my integrated host version: **not full ship yet**

It is much better and it type-checks in the host.
But before production I still want:

1. real database migrations for the new tables
2. new tests with string Clerk ids and two users (ownership cases)
3. product decision: can any logged-in user vote/view, or only some users?
4. confirm DB connection style is safe on Cloudflare Workers

**One line:**
- I would not block forever, but I would not ship blind either.

---

## 5) Least confident + more time (45 sec)

**Say:**
- The part I am least confident about:
  - exact database pooling behavior on Cloudflare Workers in this skeleton
  - and the product rule for who can vote and see results
- With more time I would:
  - write host-side tests for ownership and concurrent votes
  - add migrations
  - do a small end-to-end smoke check through the app

---

## END (15 sec)

**Say:**
- Thanks.
- My focus was ownership and judgment:
  - integrate natively
  - call out real risks
  - be honest about what I would not ship yet

---

## Super short cue card

1. `CANDIDATE_BRIEF.md` → I am integrator
2. `README.md` + `poll.router.ts` (b) → features + flow
3. `notes.router.ts` → host rules
4. tRPC compare → one instance + string user id
5. DB client compare → one shared `db`
6. schema compare → text ids + string owner
7. rename/remove compare → ownership bug fix
8. vote → atomic increment
9. `poll.test.ts` → green is not enough
10. Ship? Original no / integrated not yet
11. Least sure → Workers pooling + vote policy
