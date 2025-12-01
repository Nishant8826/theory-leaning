# How Render Works in React
A React component follows this cycle:

1. Component renders  
2. `useEffect` (and other effects) run after the render phase  
3. Side effects update state  
4. State updates trigger a re-render  

---

# Render Patterns in React

## 1. Render then fetch (Client-Side Fetching)
- Component renders first (often with empty UI or loader)
- API call happens inside `useEffect`
- State updates when data arrives
- Component re-renders with fetched data

**Example:**
```jsx
function Users() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/api/users")
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading...</p>;
  return <List data={data} />;
}
/*
Flow:
Render → Fetch → Re-render
*/
```

## 2. Render while fetching (RTK Query / React Query)
- Component renders immediately
- Library starts fetching automatically
- Loading UI is shown during fetch
- Data is cached and reused on later renders
- Background refetching updates UI without blocking render

**Example (RTK Query):**
```jsx
const { data, isLoading, isFetching } = useGetUsersQuery();

if (isLoading) return <p>Loading...</p>;

return (
  <>
    {isFetching && <p>Updating...</p>}
    <List data={data} />
  </>
);

/*
Flow:
Initial: Render (loading) → Fetch → Re-render
Later: Render (cached data) → Background fetch → Optional re-render
*/
```

## 3. Fetch then render (Server-Side Rendering / Server Components)
- Data is fetched before rendering the component
- Server returns fully rendered HTML
- Client hydrates if needed

**Example (Next.js Server Component):**
```jsx
export default async function Page() {
  const data = await fetch("https://api.com/users").then(res => res.json());
  return <List data={data} />;
}


/*
Flow:
Fetch → Render → Hydrate (optional)
*/
```

