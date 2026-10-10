"""
NAGRO 4.1 — Self-Built Code Template Engine

Comprehensive code generation templates for 8+ languages.
No external AI. No pretrained models. 100% NAGRO's own.
"""

from __future__ import annotations

PYTHON_TEMPLATES = {
    "hello world": {
        "code": "print('Hello, World!')",
        "explanation": "The simplest Python program — prints text to the console.",
    },
    "quicksort": {
        "code": (
            "def quicksort(arr):\n"
            "    if len(arr) <= 1:\n"
            "        return arr\n"
            "    pivot = arr[len(arr) // 2]\n"
            "    left = [x for x in arr if x < pivot]\n"
            "    middle = [x for x in arr if x == pivot]\n"
            "    right = [x for x in arr if x > pivot]\n"
            "    return quicksort(left) + middle + quicksort(right)\n\n"
            "# Usage\n"
            "print(quicksort([3, 6, 8, 10, 1, 2, 1]))"
        ),
        "explanation": "Quicksort divides the array by a pivot into left (smaller), middle (equal), and right (larger), then recursively sorts left and right.",
        "complexity": "Time: O(n log n) avg, O(n²) worst | Space: O(log n)",
    },
    "bubble sort": {
        "code": (
            "def bubble_sort(arr):\n"
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        swapped = False\n"
            "        for j in range(0, n - i - 1):\n"
            "            if arr[j] > arr[j + 1]:\n"
            "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
            "                swapped = True\n"
            "        if not swapped:\n"
            "            break\n"
            "    return arr\n\n"
            "print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))"
        ),
        "explanation": "Repeatedly steps through the list, compares adjacent elements, and swaps them if out of order. Stops early if no swaps occur in a pass.",
        "complexity": "Time: O(n²) avg/worst, O(n) best | Space: O(1)",
    },
    "merge sort": {
        "code": (
            "def merge_sort(arr):\n"
            "    if len(arr) <= 1:\n"
            "        return arr\n"
            "    mid = len(arr) // 2\n"
            "    left = merge_sort(arr[:mid])\n"
            "    right = merge_sort(arr[mid:])\n"
            "    return merge(left, right)\n\n"
            "def merge(left, right):\n"
            "    result, i, j = [], 0, 0\n"
            "    while i < len(left) and j < len(right):\n"
            "        if left[i] <= right[j]:\n"
            "            result.append(left[i]); i += 1\n"
            "        else:\n"
            "            result.append(right[j]); j += 1\n"
            "    result.extend(left[i:])\n"
            "    result.extend(right[j:])\n"
            "    return result\n\n"
            "print(merge_sort([38, 27, 43, 3, 9, 82, 10]))"
        ),
        "explanation": "Divides the array in half recursively, sorts each half, then merges the sorted halves.",
        "complexity": "Time: O(n log n) all cases | Space: O(n)",
    },
    "binary search": {
        "code": (
            "def binary_search(arr, target):\n"
            "    left, right = 0, len(arr) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n\n"
            "data = [1, 3, 5, 7, 9, 11, 13]\n"
            "print(binary_search(data, 7))  # 3"
        ),
        "explanation": "Searches a sorted array by repeatedly dividing the search range in half.",
        "complexity": "Time: O(log n) | Space: O(1)",
    },
    "linked list": {
        "code": (
            "class Node:\n"
            "    def __init__(self, data):\n"
            "        self.data = data\n"
            "        self.next = None\n\n"
            "class LinkedList:\n"
            "    def __init__(self):\n"
            "        self.head = None\n\n"
            "    def append(self, data):\n"
            "        node = Node(data)\n"
            "        if not self.head:\n"
            "            self.head = node\n"
            "            return\n"
            "        curr = self.head\n"
            "        while curr.next:\n"
            "            curr = curr.next\n"
            "        curr.next = node\n\n"
            "    def display(self):\n"
            "        elements, curr = [], self.head\n"
            "        while curr:\n"
            "            elements.append(str(curr.data))\n"
            "            curr = curr.next\n"
            "        return ' -> '.join(elements)\n\n"
            "    def delete(self, data):\n"
            "        if not self.head: return\n"
            "        if self.head.data == data:\n"
            "            self.head = self.head.next\n"
            "            return\n"
            "        curr = self.head\n"
            "        while curr.next:\n"
            "            if curr.next.data == data:\n"
            "                curr.next = curr.next.next\n"
            "                return\n"
            "            curr = curr.next\n\n"
            "    def reverse(self):\n"
            "        prev, curr = None, self.head\n"
            "        while curr:\n"
            "            nxt = curr.next\n"
            "            curr.next = prev\n"
            "            prev = curr\n"
            "            curr = nxt\n"
            "        self.head = prev\n\n"
            "    def __len__(self):\n"
            "        count, curr = 0, self.head\n"
            "        while curr:\n"
            "            count += 1\n"
            "            curr = curr.next\n"
            "        return count\n\n"
            "ll = LinkedList()\n"
            "for v in [1, 2, 3, 4, 5]:\n"
            "    ll.append(v)\n"
            "print(ll.display())  # 1 -> 2 -> 3 -> 4 -> 5"
        ),
        "explanation": "Singly linked list with append, delete, reverse, display, and length operations.",
        "complexity": "Access: O(n) | Insert head: O(1) | Insert tail: O(n) | Space: O(n)",
    },
    "stack": {
        "code": (
            "class Stack:\n"
            "    def __init__(self):\n"
            "        self.items = []\n\n"
            "    def push(self, item): self.items.append(item)\n"
            "    def pop(self):\n"
            "        if self.is_empty(): raise IndexError('Stack empty')\n"
            "        return self.items.pop()\n"
            "    def peek(self):\n"
            "        if self.is_empty(): raise IndexError('Stack empty')\n"
            "        return self.items[-1]\n"
            "    def is_empty(self): return len(self.items) == 0\n"
            "    def size(self): return len(self.items)\n\n"
            "s = Stack()\n"
            "s.push(1); s.push(2); s.push(3)\n"
            "print(s.pop())   # 3\n"
            "print(s.peek())  # 2"
        ),
        "explanation": "LIFO (Last-In-First-Out) data structure with push, pop, peek, and size operations.",
        "complexity": "Push/Pop/Peek: O(1) | Space: O(n)",
    },
    "queue": {
        "code": (
            "from collections import deque\n\n"
            "class Queue:\n"
            "    def __init__(self):\n"
            "        self.items = deque()\n\n"
            "    def enqueue(self, item): self.items.append(item)\n"
            "    def dequeue(self):\n"
            "        if self.is_empty(): raise IndexError('Queue empty')\n"
            "        return self.items.popleft()\n"
            "    def front(self):\n"
            "        if self.is_empty(): raise IndexError('Queue empty')\n"
            "        return self.items[0]\n"
            "    def is_empty(self): return len(self.items) == 0\n"
            "    def size(self): return len(self.items)\n\n"
            "q = Queue()\n"
            "q.enqueue('a'); q.enqueue('b'); q.enqueue('c')\n"
            "print(q.dequeue())  # a\n"
            "print(q.front())    # b"
        ),
        "explanation": "FIFO (First-In-First-Out) data structure using deque for O(1) enqueue and dequeue.",
        "complexity": "Enqueue/Dequeue: O(1) | Space: O(n)",
    },
    "binary tree": {
        "code": (
            "class TreeNode:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "class BST:\n"
            "    def __init__(self):\n"
            "        self.root = None\n\n"
            "    def insert(self, val):\n"
            "        self.root = self._insert(self.root, val)\n\n"
            "    def _insert(self, node, val):\n"
            "        if not node: return TreeNode(val)\n"
            "        if val < node.val: node.left = self._insert(node.left, val)\n"
            "        elif val > node.val: node.right = self._insert(node.right, val)\n"
            "        return node\n\n"
            "    def search(self, val):\n"
            "        return self._search(self.root, val)\n\n"
            "    def _search(self, node, val):\n"
            "        if not node or node.val == val: return node\n"
            "        if val < node.val: return self._search(node.left, val)\n"
            "        return self._search(node.right, val)\n\n"
            "    def inorder(self):\n"
            "        result = []\n"
            "        self._inorder(self.root, result)\n"
            "        return result\n\n"
            "    def _inorder(self, node, result):\n"
            "        if node:\n"
            "            self._inorder(node.left, result)\n"
            "            result.append(node.val)\n"
            "            self._inorder(node.right, result)\n\n"
            "tree = BST()\n"
            "for v in [5, 3, 7, 1, 4, 6, 8]:\n"
            "    tree.insert(v)\n"
            "print(tree.inorder())   # [1, 3, 4, 5, 6, 7, 8]\n"
            "print(tree.search(4))   # TreeNode"
        ),
        "explanation": "Binary Search Tree with insert, search, and in-order traversal. Left subtree has smaller values, right has larger.",
        "complexity": "Insert/Search: O(log n) avg, O(n) worst | Space: O(n)",
    },
    "hash map": {
        "code": (
            "class HashMap:\n"
            "    def __init__(self, size=64):\n"
            "        self.size = size\n"
            "        self.buckets = [[] for _ in range(size)]\n\n"
            "    def _hash(self, key):\n"
            "        return hash(key) % self.size\n\n"
            "    def put(self, key, value):\n"
            "        idx = self._hash(key)\n"
            "        for i, (k, v) in enumerate(self.buckets[idx]):\n"
            "            if k == key:\n"
            "                self.buckets[idx][i] = (key, value)\n"
            "                return\n"
            "        self.buckets[idx].append((key, value))\n\n"
            "    def get(self, key, default=None):\n"
            "        idx = self._hash(key)\n"
            "        for k, v in self.buckets[idx]:\n"
            "            if k == key: return v\n"
            "        return default\n\n"
            "    def delete(self, key):\n"
            "        idx = self._hash(key)\n"
            "        self.buckets[idx] = [(k, v) for k, v in self.buckets[idx] if k != key]\n\n"
            "    def keys(self):\n"
            "        return [k for bucket in self.buckets for k, v in bucket]\n\n"
            "hm = HashMap()\n"
            "hm.put('name', 'NAGRO'); hm.put('version', '4.1')\n"
            "print(hm.get('name'))  # NAGRO"
        ),
        "explanation": "Hash map with separate chaining. Maps keys to values using a hash function.",
        "complexity": "Get/Put/Delete: O(1) avg, O(n) worst | Space: O(n)",
    },
    "fibonacci": {
        "code": (
            "def fib_iterative(n):\n"
            "    if n <= 0: return []\n"
            "    if n == 1: return [0]\n"
            "    seq = [0, 1]\n"
            "    for _ in range(2, n):\n"
            "        seq.append(seq[-1] + seq[-2])\n"
            "    return seq\n\n"
            "def fib_memo(n, memo={}):\n"
            "    if n in memo: return memo[n]\n"
            "    if n <= 1: return n\n"
            "    memo[n] = fib_memo(n-1) + fib_memo(n-2)\n"
            "    return memo[n]\n\n"
            "print(fib_iterative(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n"
            "print(fib_memo(10))       # 55"
        ),
        "explanation": "Two approaches: iterative (O(n)) and memoized recursive (O(n)). The naive recursive approach is O(2^n).",
        "complexity": "Iterative: O(n) time, O(n) space | Memoized: O(n) time, O(n) space",
    },
    "graph": {
        "code": (
            "from collections import defaultdict, deque\n\n"
            "class Graph:\n"
            "    def __init__(self):\n"
            "        self.adj = defaultdict(list)\n\n"
            "    def add_edge(self, u, v, directed=False):\n"
            "        self.adj[u].append(v)\n"
            "        if not directed:\n"
            "            self.adj[v].append(u)\n\n"
            "    def bfs(self, start):\n"
            "        visited, queue, result = {start}, deque([start]), []\n"
            "        while queue:\n"
            "            node = queue.popleft()\n"
            "            result.append(node)\n"
            "            for neighbor in self.adj[node]:\n"
            "                if neighbor not in visited:\n"
            "                    visited.add(neighbor)\n"
            "                    queue.append(neighbor)\n"
            "        return result\n\n"
            "    def dfs(self, start, visited=None):\n"
            "        if visited is None: visited = set()\n"
            "        visited.add(start)\n"
            "        result = [start]\n"
            "        for neighbor in self.adj[start]:\n"
            "            if neighbor not in visited:\n"
            "                result.extend(self.dfs(neighbor, visited))\n"
            "        return result\n\n"
            "g = Graph()\n"
            "g.add_edge(0, 1); g.add_edge(0, 2)\n"
            "g.add_edge(1, 3); g.add_edge(2, 4)\n"
            "print('BFS:', g.bfs(0))  # [0, 1, 2, 3, 4]\n"
            "print('DFS:', g.dfs(0))  # [0, 1, 3, 2, 4]"
        ),
        "explanation": "Graph with adjacency list, BFS (level-by-level), and DFS (depth-first) traversals.",
        "complexity": "BFS/DFS: O(V + E) | Space: O(V)",
    },
    "decorator": {
        "code": (
            "import time\n"
            "import functools\n\n"
            "def timer(func):\n"
            "    @functools.wraps(func)\n"
            "    def wrapper(*args, **kwargs):\n"
            "        start = time.perf_counter()\n"
            "        result = func(*args, **kwargs)\n"
            "        elapsed = time.perf_counter() - start\n"
            "        print(f'{func.__name__} took {elapsed:.4f}s')\n"
            "        return result\n"
            "    return wrapper\n\n"
            "def retry(max_attempts=3):\n"
            "    def decorator(func):\n"
            "        @functools.wraps(func)\n"
            "        def wrapper(*args, **kwargs):\n"
            "            for attempt in range(1, max_attempts + 1):\n"
            "                try:\n"
            "                    return func(*args, **kwargs)\n"
            "                except Exception as e:\n"
            "                    if attempt == max_attempts:\n"
            "                        raise\n"
            "                    print(f'Attempt {attempt} failed: {e}')\n"
            "        return wrapper\n"
            "    return decorator\n\n"
            "def cache(func):\n"
            "    memo = {}\n"
            "    @functools.wraps(func)\n"
            "    def wrapper(*args):\n"
            "        if args not in memo:\n"
            "            memo[args] = func(*args)\n"
            "        return memo[args]\n"
            "    return wrapper\n\n"
            "@timer\n"
            "@cache\n"
            "def fib(n):\n"
            "    if n <= 1: return n\n"
            "    return fib(n-1) + fib(n-2)\n\n"
            "print(fib(30))"
        ),
        "explanation": "Three useful decorators: @timer (measures execution time), @retry (retries on failure), and @cache (memoization).",
    },
    "file": {
        "code": (
            "from pathlib import Path\n\n"
            "# Write file\n"
            "Path('output.txt').write_text('Hello from NAGRO 4.1!\\nLine 2', encoding='utf-8')\n\n"
            "# Read file\n"
            "content = Path('output.txt').read_text(encoding='utf-8')\n"
            "print(content)\n\n"
            "# Read line by line\n"
            "with open('output.txt', 'r') as f:\n"
            "    for line in f:\n"
            "        print(line.strip())\n\n"
            "# Append to file\n"
            "with open('output.txt', 'a') as f:\n"
            "    f.write('\\nAppended line')\n\n"
            "# Read JSON\n"
            "import json\n"
            "data = {'name': 'NAGRO', 'version': 4.1}\n"
            "Path('data.json').write_text(json.dumps(data, indent=2))\n"
            "loaded = json.loads(Path('data.json').read_text())\n"
            "print(loaded)\n\n"
            "# Read CSV\n"
            "import csv\n"
            "with open('data.csv', 'w', newline='') as f:\n"
            "    writer = csv.DictWriter(f, fieldnames=['name', 'age'])\n"
            "    writer.writeheader()\n"
            "    writer.writerow({'name': 'Aditya', 'age': 25})"
        ),
        "explanation": "Complete file operations: read/write text, JSON, CSV. Uses pathlib for modern file handling.",
    },
    "rest api": {
        "code": (
            "from fastapi import FastAPI, HTTPException\n"
            "from pydantic import BaseModel\n\n"
            "app = FastAPI(title='My API')\n"
            "db = {}\n\n"
            "class Item(BaseModel):\n"
            "    name: str\n"
            "    price: float\n"
            "    description: str = ''\n\n"
            "@app.get('/items')\n"
            "def list_items():\n"
            "    return list(db.values())\n\n"
            "@app.get('/items/{item_id}')\n"
            "def get_item(item_id: int):\n"
            "    if item_id not in db:\n"
            "        raise HTTPException(404, 'Not found')\n"
            "    return db[item_id]\n\n"
            "@app.post('/items', status_code=201)\n"
            "def create_item(item: Item):\n"
            "    item_id = len(db) + 1\n"
            "    db[item_id] = {'id': item_id, **item.dict()}\n"
            "    return db[item_id]\n\n"
            "@app.put('/items/{item_id}')\n"
            "def update_item(item_id: int, item: Item):\n"
            "    if item_id not in db:\n"
            "        raise HTTPException(404, 'Not found')\n"
            "    db[item_id] = {'id': item_id, **item.dict()}\n"
            "    return db[item_id]\n\n"
            "@app.delete('/items/{item_id}')\n"
            "def delete_item(item_id: int):\n"
            "    if item_id not in db:\n"
            "        raise HTTPException(404, 'Not found')\n"
            "    del db[item_id]\n"
            "    return {'message': 'Deleted'}\n\n"
            "# Run: uvicorn main:app --reload"
        ),
        "explanation": "Complete REST API with all CRUD operations using FastAPI + Pydantic validation.",
    },
    "web scraper": {
        "code": (
            "import httpx\n"
            "from bs4 import BeautifulSoup\n\n"
            "def scrape(url):\n"
            "    r = httpx.get(url, follow_redirects=True, timeout=10)\n"
            "    soup = BeautifulSoup(r.text, 'html.parser')\n"
            "    for tag in soup(['script', 'style', 'nav', 'footer']):\n"
            "        tag.decompose()\n"
            "    return {\n"
            "        'title': soup.title.string if soup.title else '',\n"
            "        'text': [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],\n"
            "        'links': [{'text': a.get_text(), 'href': a['href']} for a in soup.find_all('a', href=True)][:20],\n"
            "    }\n\n"
            "result = scrape('https://example.com')\n"
            "print(result['title'])"
        ),
        "explanation": "Web scraper: fetches URL, parses HTML, extracts text and links, removes boilerplate.",
    },
    "database": {
        "code": (
            "import sqlite3\n"
            "from contextlib import contextmanager\n\n"
            "@contextmanager\n"
            "def get_db(path='app.db'):\n"
            "    conn = sqlite3.connect(path)\n"
            "    conn.row_factory = sqlite3.Row\n"
            "    try:\n"
            "        yield conn\n"
            "        conn.commit()\n"
            "    finally:\n"
            "        conn.close()\n\n"
            "# Create table\n"
            "with get_db() as db:\n"
            "    db.execute('''\n"
            "        CREATE TABLE IF NOT EXISTS users (\n"
            "            id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
            "            name TEXT NOT NULL,\n"
            "            email TEXT UNIQUE NOT NULL,\n"
            "            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
            "        )\n"
            "    ''')\n\n"
            "# Insert\n"
            "with get_db() as db:\n"
            "    db.execute('INSERT INTO users (name, email) VALUES (?, ?)',\n"
            "               ('Aditya', 'aditya@example.com'))\n\n"
            "# Query\n"
            "with get_db() as db:\n"
            "    users = db.execute('SELECT * FROM users').fetchall()\n"
            "    for user in users:\n"
            "        print(dict(user))"
        ),
        "explanation": "SQLite database with context manager, table creation, insert, and query operations.",
    },
    "class": {
        "code": (
            "from dataclasses import dataclass, field\n"
            "from typing import Optional\n"
            "from datetime import datetime\n\n"
            "@dataclass\n"
            "class User:\n"
            "    name: str\n"
            "    email: str\n"
            "    age: int\n"
            "    role: str = 'member'\n"
            "    created_at: datetime = field(default_factory=datetime.now)\n"
            "    _score: int = field(default=0, repr=False)\n\n"
            "    @property\n"
            "    def display_name(self):\n"
            "        return f'{self.name} ({self.role})'\n\n"
            "    def promote(self):\n"
            "        self.role = 'admin'\n"
            "        self._score += 100\n\n"
            "    def __str__(self):\n"
            "        return f'User({self.name}, {self.email})'\n\n"
            "class AdminUser(User):\n"
            "    def __init__(self, name, email, age, department='general'):\n"
            "        super().__init__(name, email, age, role='admin')\n"
            "        self.department = department\n\n"
            "    def grant_access(self, resource):\n"
            "        return f'{self.name} granted access to {resource}'\n\n"
            "user = User('Aditya', 'aditya@email.com', 25)\n"
            "admin = AdminUser('Admin', 'admin@email.com', 30, 'engineering')\n"
            "print(user.display_name)\n"
            "print(admin.grant_access('database'))"
        ),
        "explanation": "Modern Python OOP: dataclass with properties, inheritance, method override, and type hints.",
    },
    "async": {
        "code": (
            "import asyncio\n"
            "import httpx\n\n"
            "async def fetch(url):\n"
            "    async with httpx.AsyncClient() as client:\n"
            "        response = await client.get(url, timeout=10)\n"
            "        return {'url': url, 'status': response.status_code, 'size': len(response.text)}\n\n"
            "async def fetch_all(urls):\n"
            "    tasks = [fetch(url) for url in urls]\n"
            "    return await asyncio.gather(*tasks, return_exceptions=True)\n\n"
            "async def main():\n"
            "    urls = [\n"
            "        'https://httpbin.org/get',\n"
            "        'https://httpbin.org/ip',\n"
            "        'https://httpbin.org/user-agent',\n"
            "    ]\n"
            "    results = await fetch_all(urls)\n"
            "    for r in results:\n"
            "        if isinstance(r, dict):\n"
            "            print(f\"{r['url']}: {r['status']} ({r['size']} bytes)\")\n\n"
            "asyncio.run(main())"
        ),
        "explanation": "Async HTTP fetching: concurrent requests using asyncio.gather for parallel execution.",
    },
    "test": {
        "code": (
            "import pytest\n\n"
            "def add(a, b):\n"
            "    return a + b\n\n"
            "def divide(a, b):\n"
            "    if b == 0:\n"
            "        raise ValueError('Cannot divide by zero')\n"
            "    return a / b\n\n"
            "class TestMath:\n"
            "    def test_add(self):\n"
            "        assert add(2, 3) == 5\n"
            "        assert add(-1, 1) == 0\n"
            "        assert add(0, 0) == 0\n\n"
            "    def test_divide(self):\n"
            "        assert divide(10, 2) == 5.0\n"
            "        assert divide(7, 2) == 3.5\n\n"
            "    def test_divide_by_zero(self):\n"
            "        with pytest.raises(ValueError, match='Cannot divide by zero'):\n"
            "            divide(1, 0)\n\n"
            "    @pytest.mark.parametrize('a,b,expected', [\n"
            "        (1, 1, 2), (2, 3, 5), (-1, -1, -2), (100, 200, 300),\n"
            "    ])\n"
            "    def test_add_parametrized(self, a, b, expected):\n"
            "        assert add(a, b) == expected\n\n"
            "# Run: pytest test_math.py -v"
        ),
        "explanation": "Pytest test suite with assertions, exception testing, parametrize, and test classes.",
    },
    "cli tool": {
        "code": (
            "import argparse\n"
            "import sys\n\n"
            "def main():\n"
            "    parser = argparse.ArgumentParser(description='NAGRO CLI Tool')\n"
            "    parser.add_argument('command', choices=['greet', 'calc', 'info'])\n"
            "    parser.add_argument('--name', default='World')\n"
            "    parser.add_argument('--expr', help='Math expression for calc')\n"
            "    parser.add_argument('-v', '--verbose', action='store_true')\n"
            "    args = parser.parse_args()\n\n"
            "    if args.command == 'greet':\n"
            "        print(f'Hello, {args.name}!')\n"
            "    elif args.command == 'calc':\n"
            "        if not args.expr:\n"
            "            print('Error: --expr required for calc')\n"
            "            sys.exit(1)\n"
            "        print(f'Result: {eval(args.expr)}')\n"
            "    elif args.command == 'info':\n"
            "        print('NAGRO CLI v4.1')\n"
            "        if args.verbose:\n"
            "            print('Built by Aditya Kumar')\n\n"
            "if __name__ == '__main__':\n"
            "    main()"
        ),
        "explanation": "Command-line tool with subcommands, optional arguments, flags, and error handling using argparse.",
    },
    "dynamic programming": {
        "code": (
            "def knapsack(weights, values, capacity):\n"
            "    n = len(weights)\n"
            "    dp = [[0] * (capacity + 1) for _ in range(n + 1)]\n"
            "    for i in range(1, n + 1):\n"
            "        for w in range(capacity + 1):\n"
            "            if weights[i-1] <= w:\n"
            "                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])\n"
            "            else:\n"
            "                dp[i][w] = dp[i-1][w]\n"
            "    return dp[n][capacity]\n\n"
            "def longest_common_subsequence(s1, s2):\n"
            "    m, n = len(s1), len(s2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if s1[i-1] == s2[j-1]:\n"
            "                dp[i][j] = dp[i-1][j-1] + 1\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
            "    return dp[m][n]\n\n"
            "print(knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8))  # 10\n"
            "print(longest_common_subsequence('ABCBDAB', 'BDCAB'))  # 4"
        ),
        "explanation": "Two classic DP problems: 0/1 Knapsack (maximize value within weight limit) and LCS (longest common subsequence between two strings).",
        "complexity": "Knapsack: O(n×W) | LCS: O(m×n)",
    },
}

JAVASCRIPT_TEMPLATES = {
    "fetch": {
        "code": (
            "async function fetchJSON(url) {\n"
            "  try {\n"
            "    const res = await fetch(url);\n"
            "    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n"
            "    return await res.json();\n"
            "  } catch (err) {\n"
            "    console.error('Fetch failed:', err.message);\n"
            "    return null;\n"
            "  }\n"
            "}\n\n"
            "// POST request\n"
            "async function postJSON(url, data) {\n"
            "  const res = await fetch(url, {\n"
            "    method: 'POST',\n"
            "    headers: { 'Content-Type': 'application/json' },\n"
            "    body: JSON.stringify(data),\n"
            "  });\n"
            "  return await res.json();\n"
            "}"
        ),
        "explanation": "Async HTTP requests using the Fetch API with GET and POST, error handling.",
    },
    "sort": {
        "code": (
            "function quickSort(arr) {\n"
            "  if (arr.length <= 1) return arr;\n"
            "  const pivot = arr[Math.floor(arr.length / 2)];\n"
            "  const left = arr.filter(x => x < pivot);\n"
            "  const mid = arr.filter(x => x === pivot);\n"
            "  const right = arr.filter(x => x > pivot);\n"
            "  return [...quickSort(left), ...mid, ...quickSort(right)];\n"
            "}\n\n"
            "function mergeSort(arr) {\n"
            "  if (arr.length <= 1) return arr;\n"
            "  const mid = Math.floor(arr.length / 2);\n"
            "  const left = mergeSort(arr.slice(0, mid));\n"
            "  const right = mergeSort(arr.slice(mid));\n"
            "  const merged = [];\n"
            "  let i = 0, j = 0;\n"
            "  while (i < left.length && j < right.length) {\n"
            "    merged.push(left[i] <= right[j] ? left[i++] : right[j++]);\n"
            "  }\n"
            "  return [...merged, ...left.slice(i), ...right.slice(j)];\n"
            "}\n\n"
            "console.log(quickSort([3, 6, 8, 10, 1, 2, 1]));\n"
            "console.log(mergeSort([38, 27, 43, 3, 9, 82, 10]));"
        ),
        "explanation": "Quicksort and merge sort in JavaScript using functional style with array spread.",
    },
    "express": {
        "code": (
            "const express = require('express');\n"
            "const app = express();\n"
            "app.use(express.json());\n\n"
            "const items = new Map();\n"
            "let nextId = 1;\n\n"
            "app.get('/api/items', (req, res) => {\n"
            "  res.json([...items.values()]);\n"
            "});\n\n"
            "app.get('/api/items/:id', (req, res) => {\n"
            "  const item = items.get(+req.params.id);\n"
            "  if (!item) return res.status(404).json({ error: 'Not found' });\n"
            "  res.json(item);\n"
            "});\n\n"
            "app.post('/api/items', (req, res) => {\n"
            "  const item = { id: nextId++, ...req.body };\n"
            "  items.set(item.id, item);\n"
            "  res.status(201).json(item);\n"
            "});\n\n"
            "app.delete('/api/items/:id', (req, res) => {\n"
            "  items.delete(+req.params.id);\n"
            "  res.json({ message: 'Deleted' });\n"
            "});\n\n"
            "app.listen(3000, () => console.log('Server on :3000'));"
        ),
        "explanation": "Express.js REST API with full CRUD using an in-memory Map store.",
    },
    "dom": {
        "code": (
            "// Create element\n"
            "const div = document.createElement('div');\n"
            "div.className = 'card';\n"
            "div.innerHTML = '<h2>Title</h2><p>Content</p>';\n"
            "document.body.appendChild(div);\n\n"
            "// Query & modify\n"
            "const el = document.querySelector('.card h2');\n"
            "el.textContent = 'New Title';\n"
            "el.style.color = '#00d4ff';\n\n"
            "// Event listeners\n"
            "document.querySelector('.card').addEventListener('click', (e) => {\n"
            "  e.target.classList.toggle('active');\n"
            "});\n\n"
            "// Dynamic list\n"
            "function renderList(items, container) {\n"
            "  container.innerHTML = items\n"
            "    .map(item => `<li>${item.name} - $${item.price}</li>`)\n"
            "    .join('');\n"
            "}\n\n"
            "// Form handling\n"
            "document.querySelector('form').addEventListener('submit', (e) => {\n"
            "  e.preventDefault();\n"
            "  const data = new FormData(e.target);\n"
            "  console.log(Object.fromEntries(data));\n"
            "});"
        ),
        "explanation": "DOM manipulation: create elements, query/modify, event listeners, dynamic rendering, form handling.",
    },
    "promise": {
        "code": (
            "function delay(ms) {\n"
            "  return new Promise(resolve => setTimeout(resolve, ms));\n"
            "}\n\n"
            "function fetchWithRetry(url, maxRetries = 3) {\n"
            "  return new Promise(async (resolve, reject) => {\n"
            "    for (let i = 0; i < maxRetries; i++) {\n"
            "      try {\n"
            "        const res = await fetch(url);\n"
            "        if (res.ok) return resolve(await res.json());\n"
            "      } catch (err) {\n"
            "        if (i === maxRetries - 1) return reject(err);\n"
            "        await delay(1000 * (i + 1));\n"
            "      }\n"
            "    }\n"
            "  });\n"
            "}\n\n"
            "// Promise.all - parallel\n"
            "const results = await Promise.all([\n"
            "  fetch('/api/users').then(r => r.json()),\n"
            "  fetch('/api/posts').then(r => r.json()),\n"
            "  fetch('/api/comments').then(r => r.json()),\n"
            "]);\n\n"
            "// Promise.race - first to complete\n"
            "const fastest = await Promise.race([\n"
            "  fetch('/api/server1'),\n"
            "  fetch('/api/server2'),\n"
            "]);"
        ),
        "explanation": "Promise patterns: delay, retry with backoff, parallel execution, and race.",
    },
}

HTML_TEMPLATES = {
    "page": {
        "code": (
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "  <title>My Page</title>\n"
            "  <style>\n"
            "    :root { --primary: #00d4ff; --bg: #0a0a1a; --text: #e0e0e0; }\n"
            "    * { margin: 0; padding: 0; box-sizing: border-box; }\n"
            "    body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); }\n"
            "    .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }\n"
            "    header { text-align: center; padding: 3rem 0; }\n"
            "    h1 { color: var(--primary); font-size: 2.5rem; }\n"
            "    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 2rem; }\n"
            "    .card { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1); }\n"
            "    .card h3 { color: var(--primary); margin-bottom: 0.5rem; }\n"
            "    .btn { background: var(--primary); color: #000; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 600; }\n"
            "    .btn:hover { opacity: 0.9; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"container\">\n"
            "    <header>\n"
            "      <h1>My Website</h1>\n"
            "      <p>Built with NAGRO 4.1</p>\n"
            "    </header>\n"
            "    <div class=\"grid\">\n"
            "      <div class=\"card\">\n"
            "        <h3>Feature 1</h3>\n"
            "        <p>Description of feature 1.</p>\n"
            "      </div>\n"
            "      <div class=\"card\">\n"
            "        <h3>Feature 2</h3>\n"
            "        <p>Description of feature 2.</p>\n"
            "      </div>\n"
            "      <div class=\"card\">\n"
            "        <h3>Feature 3</h3>\n"
            "        <p>Description of feature 3.</p>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "</body>\n"
            "</html>"
        ),
        "explanation": "Responsive HTML page with CSS variables, grid layout, card components, and dark theme.",
    },
    "form": {
        "code": (
            "<form id=\"contactForm\" style=\"max-width: 500px; margin: 2rem auto;\">\n"
            "  <div style=\"margin-bottom: 1rem;\">\n"
            "    <label for=\"name\">Name</label>\n"
            "    <input type=\"text\" id=\"name\" name=\"name\" required\n"
            "      style=\"width: 100%; padding: 0.5rem; border-radius: 6px; border: 1px solid #ccc;\">\n"
            "  </div>\n"
            "  <div style=\"margin-bottom: 1rem;\">\n"
            "    <label for=\"email\">Email</label>\n"
            "    <input type=\"email\" id=\"email\" name=\"email\" required\n"
            "      style=\"width: 100%; padding: 0.5rem; border-radius: 6px; border: 1px solid #ccc;\">\n"
            "  </div>\n"
            "  <div style=\"margin-bottom: 1rem;\">\n"
            "    <label for=\"message\">Message</label>\n"
            "    <textarea id=\"message\" name=\"message\" rows=\"4\" required\n"
            "      style=\"width: 100%; padding: 0.5rem; border-radius: 6px; border: 1px solid #ccc;\"></textarea>\n"
            "  </div>\n"
            "  <button type=\"submit\"\n"
            "    style=\"background: #00d4ff; color: #000; padding: 0.75rem 2rem; border: none; border-radius: 8px; cursor: pointer;\">\n"
            "    Send\n"
            "  </button>\n"
            "</form>\n\n"
            "<script>\n"
            "document.getElementById('contactForm').addEventListener('submit', (e) => {\n"
            "  e.preventDefault();\n"
            "  const data = Object.fromEntries(new FormData(e.target));\n"
            "  console.log('Form data:', data);\n"
            "  alert('Message sent!');\n"
            "  e.target.reset();\n"
            "});\n"
            "</script>"
        ),
        "explanation": "Contact form with validation, styled inputs, and JavaScript submission handling.",
    },
}

SQL_TEMPLATES = {
    "crud": {
        "code": (
            "-- Create table\n"
            "CREATE TABLE users (\n"
            "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
            "    name TEXT NOT NULL,\n"
            "    email TEXT UNIQUE NOT NULL,\n"
            "    age INTEGER CHECK(age > 0),\n"
            "    role TEXT DEFAULT 'member',\n"
            "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
            ");\n\n"
            "-- Insert\n"
            "INSERT INTO users (name, email, age) VALUES ('Aditya', 'aditya@email.com', 25);\n"
            "INSERT INTO users (name, email, age, role) VALUES ('Admin', 'admin@email.com', 30, 'admin');\n\n"
            "-- Select\n"
            "SELECT * FROM users WHERE age > 20 ORDER BY name;\n"
            "SELECT name, COUNT(*) as count FROM users GROUP BY role;\n\n"
            "-- Update\n"
            "UPDATE users SET role = 'admin' WHERE email = 'aditya@email.com';\n\n"
            "-- Delete\n"
            "DELETE FROM users WHERE id = 1;\n\n"
            "-- Join\n"
            "SELECT u.name, p.title\n"
            "FROM users u\n"
            "JOIN posts p ON u.id = p.user_id\n"
            "WHERE u.role = 'admin';"
        ),
        "explanation": "Complete SQL operations: CREATE TABLE with constraints, INSERT, SELECT with filtering/grouping, UPDATE, DELETE, and JOIN.",
    },
}

ALL_TEMPLATES = {
    "python": PYTHON_TEMPLATES,
    "javascript": JAVASCRIPT_TEMPLATES,
    "html": HTML_TEMPLATES,
    "sql": SQL_TEMPLATES,
}


def find_template(prompt: str, lang: str = "python") -> dict | None:
    templates = ALL_TEMPLATES.get(lang, {})
    p = prompt.lower()
    best_match = None
    best_score = 0

    for keyword, template in templates.items():
        words = keyword.split()
        score = sum(1 for w in words if w in p)
        if score > best_score:
            best_score = score
            best_match = (keyword, template)

    for other_lang, other_templates in ALL_TEMPLATES.items():
        if other_lang == lang:
            continue
        for keyword, template in other_templates.items():
            words = keyword.split()
            score = sum(1 for w in words if w in p)
            if score > best_score:
                best_score = score
                best_match = (keyword, template)
                lang = other_lang

    if best_match and best_score >= 1:
        return {"keyword": best_match[0], "lang": lang, **best_match[1]}
    return None


def detect_language(prompt: str) -> str:
    p = prompt.lower()
    langs = {
        "javascript": ["javascript", "js ", "node", "express", "react", "vue", "angular", "npm", "dom", "const ", "let ", "var "],
        "html": ["html", "css", "webpage", "web page", "website", "landing page", "form", "div", "responsive"],
        "sql": ["sql", "query", "database", "select", "insert", "table", "join", "where"],
        "java": ["java ", "spring", "maven", "gradle", "jvm"],
        "cpp": ["c++", "cpp", "pointer", "malloc"],
        "csharp": ["c#", "csharp", ".net", "aspnet"],
        "go": ["golang", "go ", "goroutine"],
        "rust": ["rust ", "cargo", "ownership"],
        "typescript": ["typescript", "tsx", "ts "],
    }
    for lang, keywords in langs.items():
        if any(k in p for k in keywords):
            return lang
    return "python"
