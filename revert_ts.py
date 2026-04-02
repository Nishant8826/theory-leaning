import os
import re

directories = ['d:/learning/theory/React', 'd:/learning/theory/NextJS']

for dir_path in directories:
    if not os.path.exists(dir_path):
        continue
    files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
    for filename in files:
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        content = re.sub(r'```tsx\b', r'```jsx', content)
        content = re.sub(r'```ts\b', r'```javascript', content)
        content = re.sub(r'```typescript\b', r'```javascript', content)
        
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print("Reverted TS to JS successfully.")
