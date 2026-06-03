# 🐍 Python Interview Cheat Sheet — Complete Edition

> **Covers every topic from the curriculum:** Syntax · Variables · Operators · Conditions · Loops · Collections · Strings · Functions · OOP · Dataclasses · Pydantic · Asyncio · Exceptions · Files · Modules · Logging · NumPy · Pandas

---

## 📑 Table of Contents

1. [Syntax & Semantics](#syntax--semantics)
2. [Variables & Operators](#variables--operators)
3. [Conditions & Loops](#conditions--loops)
4. [Collections](#collections)
5. [Strings](#strings)
6. [Functions](#functions)
7. [OOP](#oop)
8. [Exceptions](#exceptions)
9. [Files & Modules](#files--modules)
10. [Dataclasses & Pydantic](#dataclasses--pydantic)
11. [Asyncio](#asyncio)
12. [Logging](#logging)
13. [NumPy](#numpy)
14. [Pandas](#pandas)

---

## Syntax & Semantics

### Python syntax fundamentals

**What it is:** Python uses indentation to define code blocks — no curly braces. Every block starts with a colon and must be consistently indented (4 spaces). This makes Python readable but sensitive to whitespace.

**Key Ideas:**

- Indentation defines blocks — mixing tabs and spaces causes `IndentationError`.
- Statements end at the newline — no semicolons needed.
- Use `\` to continue a long line, or wrap in parentheses (preferred).
- Comments start with `#`. Docstrings use triple quotes `"""..."""` .

**Code Example:**

```python
# comment
result = (1 + 2
         + 3 + 4)   # preferred line continuation

def add(a, b):
    """Add two numbers."""
    return a + b

# Python is case-sensitive
name = "alice"
Name = "bob"   # different variable!

# PEP 8 naming conventions
snake_case_var = 1      # variables / functions
PascalCaseClass = None  # classes
UPPER_CONST = 3.14      # constants
```

> 💡 **Interview Tip:** **PEP 8:** 4 spaces per indent. `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_CASE` for constants.

---

### Basic data types

**What it is:** Python has several built-in primitive types. Mutable objects can be changed in place; immutable objects create new objects on every change. Understanding this is essential for avoiding bugs.

**Key Ideas:**

- `int` — unlimited precision integers. `float` — 64-bit decimal numbers.
- `str` — immutable character sequence. `bool` — True/False (subclass of int).
- `None` — the null singleton. Always check with `x is None`, never `x == None`.
- Falsy values: `0`, `0.0`, `''`, `[]`, `{}`, `set()`, `None`, `False`. Everything else truthy.

**Code Example:**

```python
# int — no overflow
x = 10 ** 100   # googol!

# float — IEEE 754 (not exact!)
0.1 + 0.2       # 0.30000000000000004
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")  # 0.3 (exact)

# bool is subclass of int
int(True)    # 1
True + True  # 2

# type conversion
int("42")       # 42
float("3.14")   # 3.14
str(100)        # "100"
bool(0)         # False
bool([0])       # True (non-empty list!)
```

> 💡 **Interview Tip:** **Floating point is not exact** — `0.1 + 0.2 != 0.3` in Python. For financial/exact decimal math always use the `decimal` module or integer arithmetic.

---

## Variables & Operators

### Variables & assignment

**What it is:** Variables are names that point to objects in memory. Python uses reference semantics — variables hold references, not values directly. This matters with mutable objects like lists and dicts.

**Key Ideas:**

- Variables are created on first assignment — no declaration needed.
- `id(x)` gives the memory address of the object x points to.
- Augmented assignment: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.
- `del x` removes the variable name; the object is garbage-collected if no other references.

**Code Example:**

```python
# multiple assignment
x = y = z = 0
a, b = 1, 2
a, b = b, a          # swap — no temp variable needed!
first, *rest, last = [1, 2, 3, 4, 5]
# first=1, rest=[2,3,4], last=5

# reference semantics — mutable objects
a = [1, 2, 3]
b = a            # SAME object in memory!
b.append(4)
print(a)         # [1, 2, 3, 4]  ← a changed too!

b = a.copy()     # shallow copy — now independent
import copy
c = copy.deepcopy(a)  # deep copy — fully independent

# augmented assignment
x = 10
x += 5     # x = 15
x **= 2    # x = 225
```

> 💡 **Interview Tip:** Use `copy.deepcopy(obj)` for nested structures. `a.copy()` or `a[:]` only shallow-copies — nested lists/dicts inside are still shared!

---

### Operators

**What it is:** Python has arithmetic, comparison, logical, bitwise, membership, and identity operators. `is` vs `==` and short-circuit evaluation are common interview topics.

**Key Ideas:**

- `//` floor division, `%` modulo, `**` power.
- `is` / `is not` — identity (same object in memory). `==` / `!=` — equality (same value).
- `in` / `not in` — membership. O(1) for sets/dicts, O(n) for lists.
- `and` / `or` short-circuit: return the actual operand, not True/False.

**Code Example:**

```python
# arithmetic
17 // 5     # 3   floor division
17 % 5      # 2   remainder
2 ** 10     # 1024

# identity vs equality
a = [1, 2, 3]
b = [1, 2, 3]
a == b      # True  (same value)
a is b      # False (different objects)
x = None
x is None   # True  ← correct way to check None

# short-circuit — returns the operand, not bool
0 or "default"    # "default"
5 or "default"    # 5  ← 5 is truthy, returns it
None and boom()   # None (boom() never called)

# walrus operator := (Python 3.8+)
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"Large: {n}")   # Large: 5
```

> 💡 **Interview Tip:** `x or default` is a common fallback pattern. **Gotcha:** if x is `0`, `''`, or `False`, the default triggers even when x has a meaningful value. Use `x if x is not None else default` for safety.

---

## Conditions & Loops

### Conditional statements

**What it is:** Python uses `if`/`elif`/`else` for branching. The `match`-`case` statement (Python 3.10+) is the modern pattern-matching alternative to long elif chains. Conditions accept any truthy/falsy value.

**Key Ideas:**

- Falsy: `0`, `''`, `[]`, `{}`, `set()`, `None`, `False`. Everything else truthy.
- `elif` chain is evaluated top-to-bottom — first match wins, rest are skipped.
- Ternary: `x if condition else y` — use only for simple one-liners.
- `match`-`case` supports patterns: literals, types, tuples, guards (`if` clause).

**Code Example:**

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# ternary
status = "pass" if score >= 60 else "fail"

# match-case (Python 3.10+) — structural pattern matching
match command:
    case "quit":                quit()
    case "help":                show_help()
    case ["go", direction]:     go(direction)    # list pattern
    case {"action": act}:       do(act)          # dict pattern
    case _ if debug:            log(command)     # guard
    case _:                     print("unknown") # default
```

> 💡 **Interview Tip:** `match`-`case` is **not** just a switch statement — it can destructure lists, dicts, and objects. `case [x, y]` matches any 2-element list and binds x and y. Very powerful for parsing structured data.

---

### Loops — for, while & comprehensions

**What it is:** Python's `for` loop iterates over any iterable. `while` for condition-based repetition. List/dict/set comprehensions replace most `map`/`filter` usage and are idiomatic Python.

**Key Ideas:**

- `enumerate(it, start=0)` — index + value pairs without a counter variable.
- `zip(*its, strict=False)` — pairs iterables. `strict=True` raises on length mismatch.
- **loop else** — runs if loop finishes without `break`. Great for search patterns.
- Comprehension pattern: `[expr for x in it if cond]` — list, dict, set, generator.

**Code Example:**

```python
# enumerate with custom start
for i, v in enumerate(items, start=1):
    print(f"#{i}: {v}")

# zip — pairs elements from two iterables
for name, score in zip(names, scores):
    print(name, score)

# dict comprehension
sq = {x: x**2 for x in range(5)}
# {0:0, 1:1, 2:4, 3:9, 4:16}

# set comprehension
evens = {x for x in range(20) if x % 2 == 0}

# loop else — runs if NO break occurred
for item in collection:
    if item == target:
        found = item
        break
else:
    print("Not found")  # only if loop completed normally

# generator expression — lazy, memory efficient
total = sum(x**2 for x in range(10**6))
```

> 💡 **Interview Tip:** Generator expressions `(x**2 for x in it)` are lazy — values computed on demand. Use inside `sum()`, `any()`, `all()`, `max()` for memory efficiency without building a list.

---

## Collections

### Lists — patterns & tricks

**What it is:** Lists are ordered, mutable sequences. Key interview patterns: stack (append/pop), queue (use deque), two-pointer, sliding window. Know time complexities — they matter in interviews.

**Key Ideas:**

- `append()` / `pop()` — O(1). `insert(0,x)` / `pop(0)` — O(n) — avoid for queues.
- Use `collections.deque` for O(1) append/pop from **both** ends.
- `list.sort()` sorts in-place (stable, Timsort). `sorted(lst)` returns a new list.
- `bisect` module for binary search on sorted lists — O(log n).

**Code Example:**

```python
from collections import deque

# stack — LIFO
stack = []
stack.append(1)   # push  O(1)
stack.pop()       # pop   O(1)

# queue — FIFO (use deque, NOT list!)
q = deque()
q.append(1)       # enqueue  O(1)
q.popleft()       # dequeue  O(1)

# sort by multiple keys
students = [("Alice", 90), ("Bob", 85), ("Eve", 90)]
sorted(students, key=lambda s: (-s[1], s[0]))
# score DESC, then name ASC

# remove duplicates preserving order
seen = set()
unique = [x for x in lst if not (x in seen or seen.add(x))]

# flatten nested list
nested = [[1, 2], [3, 4], [5]]
flat = [x for sub in nested for x in sub]
# [1, 2, 3, 4, 5]
```

> 💡 **Interview Tip:** `list.pop(0)` is O(n) — it shifts all elements left. Use `collections.deque` for O(1) pops from the left. **Always use deque for queue-based interview problems.**

---

### Dictionaries

**What it is:** Dicts are hash maps — O(1) average for insert, lookup, delete. The most used data structure after lists. Dicts preserve insertion order (Python 3.7+).

**Key Ideas:**

- `d[key]` raises `KeyError`. `d.get(key, default)` is always safe.
- `d.setdefault(k, [])` — set default if absent, return value. Great for grouping.
- `Counter(iterable)` — count occurrences. `most_common(n)` top n. `c[missing]` → 0.
- Dict merge (3.9+): `merged = d1 | d2`. In-place: `d1 |= d2`.

**Code Example:**

```python
from collections import Counter, defaultdict, ChainMap

# Counter — count and query frequencies
words = ["a", "b", "a", "c", "a", "b"]
c = Counter(words)
c.most_common(2)   # [("a", 3), ("b", 2)]
c["z"]             # 0  ← no KeyError!
c.subtract(["a"])  # subtract counts

# defaultdict — auto-group
groups = defaultdict(list)
for word in ["cat", "car", "dog"]:
    groups[word[0]].append(word)
# {"c": ["cat", "car"], "d": ["dog"]}

# ChainMap — layered config / scopes
defaults  = {"color": "red",  "size": 10}
user_cfg  = {"size": 20}
config = ChainMap(user_cfg, defaults)
config["color"]   # "red"  (from defaults)
config["size"]    # 20     (from user_cfg)

# dict merge (Python 3.9+)
merged = defaults | user_cfg
# {"color": "red", "size": 20}
```

> 💡 **Interview Tip:** `Counter` subtraction removes elements with ≤ 0 count. `Counter('aab') - Counter('ab')` → `Counter({'a': 1})`. Useful for sliding window and anagram problems.

---

### Sets & Tuples

**What it is:** Sets provide O(1) membership testing and powerful set operations. Tuples are immutable sequences used as dict keys, function return values, and fixed records.

**Key Ideas:**

- Set ops: `|` union, `&` intersection, `-` difference, `^` symmetric diff.
- Membership in a set is O(1) vs O(n) for a list — use sets for 'seen' tracking.
- Tuples are immutable and hashable — usable as dictionary keys.
- `namedtuple` gives readable field names. `@dataclass(frozen=True)` is the modern alternative.

**Code Example:**

```python
from collections import namedtuple

# set — unique items, O(1) lookup
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
a | b   # {1,2,3,4,5,6}  union
a & b   # {3,4}           intersection
a - b   # {1,2}           difference
a ^ b   # {1,2,5,6}       symmetric diff
3 in a  # True  O(1)

# frozenset — immutable, hashable set
fs = frozenset([1, 2, 3])

# tuple — immutable, hashable
point = (3, 4)
x, y = point            # unpack
a, *rest = (1,2,3,4)    # starred unpack

# named tuple — readable fields
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y                # 3, 4
p._asdict()             # OrderedDict({x:3, y:4})
```

> ⚠️ **Warning:** **Common mistake:** `{}` is an empty **dict**, not a set! Use `set()` for an empty set. `{1,2,3}` is a set literal, but `{}` is always a dict literal.

---

## Strings

### String methods & formatting

**What it is:** Strings are immutable sequences of characters. Every method returns a NEW string — the original never changes. f-strings are the fastest and most readable formatting approach.

**Key Ideas:**

- f-strings `f'...'` embed expressions inline. `f'{x:.2f}'` formats to 2 decimal places.
- Slicing: `s[start:stop:step]`. `s[::-1]` reverses. `s[1:4]` = chars 1, 2, 3.
- Immutable — `s[0] = 'x'` raises `TypeError`. Build new strings instead.
- `str.join(iterable)` is faster than `+=` in a loop for building strings.

**Code Example:**

```python
s = "Hello, World!"
s.upper()                # "HELLO, WORLD!"
s.lower()                # "hello, world!"
s.strip()                # remove leading/trailing whitespace
s.replace("World", "Python")
s.split(",")             # ["Hello", " World!"]
"-".join(["a","b","c"]) # "a-b-c"
s.startswith("Hello")   # True
s.find("World")         # 7  (-1 if not found)
s.count("l")            # 3

# f-string formatting
name = "Alice"; score = 98.567
f"Hi {name}, score: {score:.2f}"  # 2 decimal places
f"{42:08b}"    # "00101010"  binary with padding
f"{1000000:,}" # "1,000,000" thousands separator

# strip + title chain
"  hello world  ".strip().title()  # "Hello World"
```

> 💡 **Interview Tip:** Use `'sep'.join(list)` not string concatenation in loops. `s += x` in a loop is O(n²) because each `+=` creates a new string. `join` builds it in O(n).

---

### String patterns for interviews

**What it is:** These patterns come up constantly in coding interviews — palindromes, anagrams, reversals, character counting, sliding window on strings. Know them cold.

**Key Ideas:**

- `s[::-1]` reverses a string in one line — the most Pythonic way.
- `ord(c)` → int code. `chr(n)` → character. `ord('a')` = 97, `ord('A')` = 65.
- `sorted(s)` returns a sorted list of chars — clean anagram check.
- Use `Counter` for frequency maps — replaces manual dict building.

**Code Example:**

```python
from collections import Counter

# reverse
"hello"[::-1]    # "olleh"

# palindrome check
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# anagram check — O(n)
def is_anagram(a, b):
    return Counter(a) == Counter(b)
is_anagram("listen", "silent")  # True

# char code
ord("A")    # 65
chr(65)     # "A"
ord("a")    # 97

# most frequent character
Counter("abracadabra").most_common(1)   # [("a", 5)]

# sliding window — longest substring with unique chars
def longest_unique(s):
    seen, left, best = {}, 0, 0
    for right, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = right
        best = max(best, right - left + 1)
    return best
```

> 💡 **Interview Tip:** `Counter(a) == Counter(b)` is O(n) anagram check and cleaner than `sorted(a) == sorted(b)` which is O(n log n). For interview speed problems, Counter is usually the answer.

---

## Functions

### Function signatures & argument types

**What it is:** Functions are first-class objects — passed as arguments, returned, stored in data structures. Understanding all argument types and their order is critical for interview questions.

**Key Ideas:**

- Order: positional → `/` → normal → `*args` → `*` → keyword-only → `**kwargs`.
- `*args` = extra positional args as tuple. `**kwargs` = extra keyword args as dict.
- Never use mutable objects (`[]`, `{}`) as default values — use `None`.
- Type hints don't enforce at runtime — they're for tools and documentation.

**Code Example:**

```python
# all argument types in one function
def func(pos_only, /, normal, *args, kw_only, **kwargs):
    print(pos_only, normal, args, kw_only, kwargs)

func(1, 2, 3, 4, kw_only=5, x=6)
# 1  2  (3,4)  5  {"x": 6}

# WRONG — mutable default bug
def bad(lst=[]):       # same list reused every call!
    lst.append(1)
    return lst
bad()   # [1]
bad()   # [1, 1]  ← BUG!

# CORRECT — use None
def good(lst=None):
    if lst is None: lst = []
    lst.append(1)
    return lst

# type hints
def divide(a: float, b: float) -> float | None:
    return a / b if b != 0 else None

# unpack into call
args = (10, 2)
divide(*args)        # 5.0
divide(10, **{"b":2})  # 5.0
```

> 💡 **Interview Tip:** **Mutable default is Python's most famous gotcha.** Default values are evaluated ONCE at function definition time — `def f(lst=[])` reuses the SAME list object across every call.

---

### Lambda, map, filter & functools

**What it is:** `lambda` creates anonymous inline functions. `map` and `filter` return lazy iterators. `functools` provides higher-order tools: `partial`, `reduce`, `wraps`, `lru_cache`, `cached_property`.

**Key Ideas:**

- `lambda args: expr` — single expression, implicit return, no statements allowed.
- `functools.partial(fn, *args)` — fix some arguments, return new callable.
- `functools.reduce(fn, it, init)` — fold/accumulate left to right.
- `@lru_cache(maxsize=None)` — memoize results. Python 3.9+: `@cache` (simpler).

**Code Example:**

```python
from functools import partial, reduce, lru_cache, cache
import operator

# lambda
sq = lambda x: x ** 2
sq(5)   # 25

# map / filter — lazy iterators
nums = [1, 2, 3, 4, 5]
list(map(lambda x: x * 2, nums))         # [2,4,6,8,10]
list(filter(lambda x: x % 2 == 0, nums)) # [2,4]

# sorted with key — very common in interviews
people = [("Bob", 25), ("Alice", 22)]
sorted(people, key=lambda p: p[1])
# [("Alice", 22), ("Bob", 25)]

# partial — fix arguments
double = partial(operator.mul, 2)
double(5)    # 10

# reduce — fold left to right
reduce(lambda acc, x: acc + x, [1,2,3,4], 0)  # 10

# lru_cache — memoization
@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

fib(100)   # instant — results cached
```

> 💡 **Interview Tip:** `@cache` (Python 3.9+) is `@lru_cache(maxsize=None)`. Use it for recursive memoization. `@lru_cache` with a size limit evicts old entries (LRU policy) — better for memory-constrained environments.

---

### Closures & decorators

**What it is:** A closure captures variables from its enclosing scope. Decorators use closures to wrap functions. They are the foundation of Flask routes, Django views, pytest fixtures, and more.

**Key Ideas:**

- Decorators are functions that return functions. `@timer` = `func = timer(func)`.
- Always use `@wraps(func)` — preserves `__name__`, `__doc__`, `__annotations__`.
- `nonlocal` lets inner function modify (not just read) an enclosing variable.
- Stacked decorators apply **bottom-up**: `@A @B def f` → `f = A(B(f))`.

**Code Example:**

```python
from functools import wraps

# closure — inner function captures outer variable
def make_multiplier(factor):
    def multiply(x):
        return x * factor   # captures factor
    return multiply

double = make_multiplier(2)
double(5)   # 10

# nonlocal — modify enclosing variable
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

# decorator with arguments — 3 levels of nesting
def retry(times=3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

@retry(times=3, exceptions=(IOError,))
def fetch_data(url): ...
```

> 💡 **Interview Tip:** `@wraps(func)` is **not optional** — without it, your decorated function loses `__name__` and `__doc__`. This breaks pytest, Sphinx, and any tool that reads function metadata.

---

### Generators & iterators

**What it is:** Generators produce values lazily using `yield`. They implement the iterator protocol automatically. Use them for large datasets, infinite sequences, and memory-efficient pipelines.

**Key Ideas:**

- A function with `yield` is a generator function. Calling it returns a generator object.
- `yield from iterable` — delegate to sub-generator or any iterable.
- Generator expressions: `(expr for x in it)` — lazy, O(1) memory regardless of size.
- A list of 1M numbers ≈ 8MB. The same as a generator ≈ 200 bytes.

**Code Example:**

```python
# infinite generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(8)]
# [0, 1, 1, 2, 3, 5, 8, 13]

# generator pipeline — process huge file lazily
def read_chunks(filename, size=1024):
    with open(filename) as f:
        while chunk := f.read(size):
            yield chunk

def parse_lines(chunks):
    for chunk in chunks:
        yield from chunk.splitlines()

def filter_empty(lines):
    return (l for l in lines if l.strip())

# chain — each step is lazy, ~0 extra memory
for line in filter_empty(parse_lines(read_chunks("big.txt"))):
    process(line)

# custom iterator class
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self):    return self
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1

list(Countdown(5))   # [5, 4, 3, 2, 1]
```

> 💡 **Interview Tip:** Generator pipelines process data one piece at a time — a 10GB file uses only ~1KB of memory. This is why generators are the backbone of data processing frameworks and ETL pipelines.

---

## OOP

### Classes, properties & class methods

**What it is:** Classes bundle state (attributes) and behaviour (methods). Properties let you add validation without breaking the public API. `__slots__` reduces memory usage by 40-50% for many small objects.

**Key Ideas:**

- `@property` getter. `@name.setter` setter. `@name.deleter` deleter.
- `__slots__` restricts attributes and reduces memory — no `__dict__` per instance.
- `@classmethod` for alternative constructors (receives `cls`).
- `@staticmethod` for utility functions inside the class (receives neither `self` nor `cls`).

**Code Example:**

```python
class Circle:
    __slots__ = ["_radius"]   # saves ~40% memory

    def __init__(self, radius):
        self.radius = radius   # calls setter

    @property
    def radius(self): return self._radius
    @radius.setter
    def radius(self, v):
        if v < 0: raise ValueError("negative radius")
        self._radius = v

    @property
    def area(self):            # computed — no setter = read-only
        import math
        return math.pi * self._radius ** 2

    @classmethod
    def unit(cls):             # alternative constructor
        return cls(1)

    @staticmethod
    def is_valid(r):           # utility function
        return r > 0

c = Circle.unit()
c.area             # 3.14159...
Circle.is_valid(-1)  # False
```

> 💡 **Interview Tip:** A `@property` with no `@name.setter` is **read-only** — setting it raises `AttributeError`. This is the Pythonic alternative to private getters/setters in Java.

---

### Inheritance, MRO & mixins

**What it is:** Python supports multiple inheritance. MRO (Method Resolution Order) determines which method is called. Mixins add reusable behaviour without being stand-alone base classes.

**Key Ideas:**

- Always call `super().__init__()` — follows MRO and initialises the full chain.
- `ClassName.__mro__` shows resolution order. Uses C3 linearisation algorithm.
- Mixins add behaviour without state — they should NOT have `__init__`.
- `isinstance(obj, (A, B))` checks multiple types at once.

**Code Example:**

```python
class LogMixin:
    def log(self, msg):
        print(f"[{self.__class__.__name__}] {msg}")

class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Animal:
    def __init__(self, name):
        self.name = name

class Dog(LogMixin, JsonMixin, Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # follows MRO properly
        self.breed = breed
    def speak(self):
        self.log("Woof!")

rex = Dog("Rex", "Lab")
rex.to_json()   # {"name": "Rex", "breed": "Lab"}
rex.speak()     # [Dog] Woof!

# MRO — left to right, depth first
Dog.__mro__
# (Dog, LogMixin, JsonMixin, Animal, object)

isinstance(rex, (Dog, Animal))   # True
```

> 💡 **Interview Tip:** Never call `ParentClass.__init__(self, ...)` directly in multiple inheritance — it bypasses MRO and leaves other parents uninitialised. Always use `super().__init__()`.

---

### Magic methods & operator overloading

**What it is:** Dunder (double underscore) methods define how objects interact with Python's built-in syntax. Implement them to make your objects feel native — behaving just like built-in types.

**Key Ideas:**

- `__repr__` for devs (unambiguous). `__str__` for users (readable). `print()` calls `__str__`.
- Define `__eq__` → Python sets `__hash__ = None` unless you also define `__hash__`.
- `@functools.total_ordering` — define `__eq__` + one comparison, gets all others free.
- `__enter__` / `__exit__` — make objects work as context managers with `with`.

**Code Example:**

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.v = (major, minor, patch)

    def __repr__(self):  return f"Version{self.v}"
    def __str__(self):   return ".".join(map(str, self.v))
    def __eq__(self, o): return self.v == o.v
    def __lt__(self, o): return self.v < o.v
    def __hash__(self):  return hash(self.v)

v1 = Version(1, 2, 3)
v2 = Version(2, 0, 0)
v1 < v2     # True
v1 <= v2    # True  ← filled in by total_ordering
sorted([v2, v1])      # [1.2.3, 2.0.0]
{v1: "stable"}        # usable as dict key

# context manager protocol
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self
    def __exit__(self, *args):
        import time
        self.elapsed = time.time() - self.start

with Timer() as t:
    sum(range(10**6))
print(t.elapsed)
```

> 💡 **Interview Tip:** `@total_ordering`: define `__eq__` and ONE comparison method — Python fills in the rest automatically. Saves writing all 6 comparison methods.

---

### Abstraction — ABCs & context managers

**What it is:** Abstract Base Classes define contracts — subclasses must implement certain methods or Python refuses to instantiate them. `@contextmanager` is the easiest way to write resource managers.

**Key Ideas:**

- Any un-implemented `@abstractmethod` raises `TypeError` on instantiation.
- You can also make abstract `@property`, `@classmethod`, `@staticmethod`.
- `@contextmanager`: code before `yield` = `__enter__`, `finally` = `__exit__`.
- `contextlib.suppress(ExcType)` — ignore a specific exception cleanly.

**Code Example:**

```python
from abc import ABC, abstractmethod
from contextlib import contextmanager, suppress

class Repository(ABC):
    @abstractmethod
    def get(self, id): ...
    @abstractmethod
    def save(self, entity): ...
    @abstractmethod
    def delete(self, id): ...
    def exists(self, id):       # concrete shared method
        return self.get(id) is not None

class UserRepo(Repository):
    def get(self, id):    return db.query(id)
    def save(self, u):    db.insert(u)
    def delete(self, id): db.delete(id)

# @contextmanager — easiest way to write one
@contextmanager
def managed_connection(url):
    conn = connect(url)
    try:
        yield conn          # __enter__ returns conn
    finally:
        conn.close()        # __exit__ always runs

with managed_connection("db://...") as conn:
    conn.execute(query)

# contextlib.suppress — ignore specific errors
with suppress(FileNotFoundError):
    Path("maybe_missing.txt").unlink()
```

> 💡 **Interview Tip:** `contextlib.suppress(ExcType)` is cleaner than `try/except/pass`. It's self-documenting and avoids the empty `except` block anti-pattern.

---

## Exceptions

### Exception handling

**What it is:** Python exceptions form a hierarchy. Catch at the right level — never use bare `except` (catches `SystemExit` and `KeyboardInterrupt`). Use exception chaining in production code.

**Key Ideas:**

- `BaseException` includes `SystemExit`, `KeyboardInterrupt` — never catch this bare.
- `Exception` is the base for all normal exceptions — safe to catch broadly.
- `raise X from Y` — chains exceptions preserving original traceback.
- `raise X from None` — suppresses chaining (hides original cause).

**Code Example:**

```python
# exception hierarchy
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception
#         ├── ValueError, TypeError, AttributeError
#         ├── OSError (FileNotFoundError, PermissionError)
#         └── RuntimeError, StopIteration, RecursionError

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except (TypeError, ValueError) as e:
        print(f"Bad input: {e}")
        return None
    else:
        return result       # only if no exception raised
    finally:
        print("Done")       # ALWAYS runs

# exception chaining
try:
    open("missing.txt")
except IOError as e:
    raise RuntimeError("Setup failed") from e

# suppress — ignore specific errors
from contextlib import suppress
with suppress(FileNotFoundError):
    Path("missing.txt").unlink()
```

> 💡 **Interview Tip:** Use `logger.exception('msg')` inside except blocks — logs ERROR level AND automatically includes the full traceback. Much better than `logger.error(str(e))`.

---

### Custom exceptions

**What it is:** Create your own exception classes that carry context. Callers can catch your specific error types precisely. Build a hierarchy with one base class for the whole app.

**Key Ideas:**

- Always inherit from `Exception` or a more specific built-in subclass.
- Add extra attributes (`field`, `code`, `status`) to carry context about the error.
- Build hierarchy: `AppError` base → specific sub-classes.
- Catching `AppError` also catches all sub-classes — very powerful.

**Code Example:**

```python
class AppError(Exception):
    """Base for all application exceptions."""
    pass

class ValidationError(AppError):
    def __init__(self, field: str, msg: str):
        self.field = field
        super().__init__(f"{field}: {msg}")

class DatabaseError(AppError):
    def __init__(self, code: int, msg: str):
        self.code = code
        super().__init__(f"[{code}] {msg}")

class NotFoundError(DatabaseError):
    def __init__(self, resource: str, id):
        super().__init__(404, f"{resource} {id} not found")

# usage
try:
    raise ValidationError("email", "invalid format")
except ValidationError as e:
    print(e.field, str(e))
    # email   email: invalid format
except AppError:
    print("Generic app error")  # catches all subclasses

# Python 3.11+ ExceptionGroup
try:
    raise ExceptionGroup("errors", [
        ValueError("bad val"),
        TypeError("bad type")])
except* ValueError as eg:
    print("value errors:", eg.exceptions)
```

> 💡 **Interview Tip:** `ExceptionGroup` (Python 3.11+) holds multiple exceptions at once. `except*` handles specific types within the group. Used in `asyncio.TaskGroup` when multiple tasks fail simultaneously.

---

## Files & Modules

### File I/O & pathlib

**What it is:** Always use `with open(...)` — files are closed automatically even if an exception occurs. `pathlib.Path` is the modern cross-platform API — replaces all `os.path` string-based code.

**Key Ideas:**

- `Path.read_text()` / `write_text()` — read/write in one line, auto-closes.
- `Path.rglob('*.py')` — recursive glob. Returns a generator — iterate directly.
- `shutil` module — copy, move, delete entire directories.
- `tempfile.TemporaryDirectory()` — auto-cleanup temp dirs on exit.

**Code Example:**

```python
from pathlib import Path
import shutil, tempfile, json, csv

# pathlib
p = Path("data") / "reports" / "q1.csv"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hello", encoding="utf-8")
p.read_text()
p.stat().st_size         # file size in bytes
list(Path(".").rglob("*.py"))   # all Python files

# file I/O
with open("data.txt", "r", encoding="utf-8") as f:
    content  = f.read()        # all at once
    lines    = f.readlines()   # list of lines
    for line in f: ...         # lazy — best for large files

# JSON
with open("config.json") as f:
    cfg = json.load(f)
with open("out.json", "w") as f:
    json.dump(cfg, f, indent=2)

# CSV
with open("data.csv") as f:
    rows = list(csv.DictReader(f))

# shutil
shutil.copy(src, dst)
shutil.move(src, dst)
shutil.rmtree("dir_to_delete")

# temp directory — auto-deleted on exit
with tempfile.TemporaryDirectory() as tmp:
    (Path(tmp) / "work.txt").write_text("temp")
```

> 💡 **Interview Tip:** `Path.rglob('*.csv')` is equivalent to `Path('.').glob('**/*.csv')`. Both return generators — iterate directly for memory efficiency, or `list()` to materialise.

---

### Modules, packages & stdlib

**What it is:** A module is a `.py` file. A package is a folder with `__init__.py`. Python's stdlib is enormous — these are the modules that appear in almost every real project.

**Key Ideas:**

- `import package.module` — absolute import (always preferred in production).
- `from . import module` — relative import (inside a package only).
- `__all__` controls what `from module import *` exports.
- `importlib.import_module(name)` — dynamic import at runtime.

**Code Example:**

```python
# stdlib essentials — know these cold
import os, sys, math, random, re
from datetime import datetime, timedelta
from collections import Counter, defaultdict, deque, ChainMap
from itertools import chain, islice, groupby, combinations, permutations
from functools import wraps, partial, reduce, lru_cache, cached_property
from contextlib import contextmanager, suppress, ExitStack
from pathlib import Path
from typing import Optional, Union, Any, Callable

# useful patterns
math.ceil(3.2)        # 4
math.floor(3.9)       # 3
math.gcd(48, 18)      # 6
random.choice(["a","b","c"])
random.shuffle(lst)   # in-place

now = datetime.now()
tomorrow = now + timedelta(days=1)

# script guard
if __name__ == "__main__":
    main()

# cached_property — compute once, cache forever
from functools import cached_property
class DataSet:
    @cached_property
    def stats(self):
        return expensive_compute(self.data)
    # first access: computes; subsequent: returns cached
```

> 💡 **Interview Tip:** `@cached_property` computes the value once and stores it as an instance attribute. Subsequent accesses skip the method entirely — O(1) after first call. Perfect for expensive computed properties.

---

## Dataclasses & Pydantic

### @dataclass — typed classes without boilerplate

**What it is:** `dataclasses` auto-generate `__init__`, `__repr__`, `__eq__` from field annotations. The modern Pythonic way to define data-holding classes without writing repetitive boilerplate code.

**Key Ideas:**

- `@dataclass` — generates `__init__`, `__repr__`, `__eq__` from annotated fields.
- `frozen=True` — immutable + adds `__hash__` (usable as dict key / set member).
- `field(default_factory=list)` — for mutable defaults. **Never** use `[]` directly.
- `order=True` — also generates `__lt__`, `__le__`, `__gt__`, `__ge__`.

**Code Example:**

```python
from dataclasses import dataclass, field, asdict, replace

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"   # default value

p = Point(1.0, 2.0)
print(p)        # Point(x=1.0, y=2.0, label="origin")
asdict(p)       # {"x": 1.0, "y": 2.0, "label": "origin"}
replace(p, x=5.0)  # new Point with only x changed

# frozen + order — immutable, sortable, hashable
@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

v1 = Version(1, 2, 3)
v2 = Version(2, 0, 0)
v1 < v2         # True
{v1, v2}        # usable in a set (frozen → hashable)

# mutable default — MUST use field()
@dataclass
class Team:
    name: str
    members: list[str] = field(default_factory=list)
    _id: int = field(default=0, repr=False)  # hidden from repr

# post-init validation
@dataclass
class Circle:
    radius: float
    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("negative radius")
```

> 💡 **Interview Tip:** `replace(obj, field=val)` creates a new dataclass instance with some fields changed — essential when using `frozen=True` since you can't modify in place.

---

### Pydantic — runtime data validation

**What it is:** Pydantic validates data at runtime using type hints. It's the standard for FastAPI request/response models, config management, and data parsing. It auto-converts types and gives clear error messages.

**Key Ideas:**

- Pydantic models inherit from `BaseModel`. Fields are annotated with type hints.
- Pydantic validates AND coerces: `'42'` → `42` for an `int` field automatically.
- `model.model_dump()` → dict. `model.model_json_schema()` → JSON Schema.
- `@field_validator` for custom field validation. `@model_validator` for cross-field validation.

**Code Example:**

```python
from pydantic import BaseModel, field_validator
from typing import Optional

class Address(BaseModel):
    street: str
    city:   str
    zip:    str

class User(BaseModel):
    id:      int
    name:    str
    email:   str
    age:     Optional[int] = None
    address: Optional[Address] = None  # nested model

    @field_validator("age")
    @classmethod
    def check_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("age must be positive")
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()   # transform value

# auto-coercion: "1" (str) → 1 (int)
user = User(id="1", name="Alice", email="A@B.COM")
user.id      # 1  (coerced from str)
user.email   # "a@b.com"  (lowercased by validator)
user.model_dump()        # dict
user.model_dump_json()   # JSON string
```

> 💡 **Interview Tip:** Pydantic is the backbone of FastAPI — every endpoint's request body, response model, and query params are Pydantic models. Knowing Pydantic well is **essential** for Python backend roles.

---

### Pydantic BaseSettings — config management

**What it is:** `pydantic-settings` reads configuration from environment variables and `.env` files. It's the standard way to manage app configuration in modern Python projects — apps fail fast at startup on bad config.

**Key Ideas:**

- `BaseSettings` reads from environment variables automatically (case-insensitive).
- Nested models group related settings. `env_nested_delimiter='__'` maps `DB__HOST` → `db.host`.
- `SecretStr` hides sensitive values in logs and repr output.
- Validation happens at startup — misconfigured apps fail immediately, not silently.

**Code Example:**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class DatabaseSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    name: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"  # DB__HOST → db.host
    )
    app_name: str = "MyApp"
    debug:    bool = False
    db:       DatabaseSettings
    secret:   SecretStr      # hidden in repr/logs
    workers:  int = 4

settings = Settings()   # reads .env + environment vars

# .env file:
# APP_NAME=Production
# DB__HOST=postgres.example.com
# DB__NAME=mydb
# SECRET=super-secret-key

settings.secret.get_secret_value()   # actual value
str(settings.secret)                 # "**********"
```

> 💡 **Interview Tip:** `SecretStr` hides sensitive values — `str(settings.secret)` shows `'**********'`. Call `.get_secret_value()` to get the raw string when needed (e.g. passing to a DB connection).

---

## Asyncio

### async/await — concurrency without threads

**What it is:** asyncio provides cooperative multitasking — one thread, many concurrent tasks. When a task waits for I/O, it yields control so other tasks can run. Perfect for I/O-bound work: web servers, API calls, databases.

**Key Ideas:**

- `async def` defines a coroutine — it doesn't run until awaited.
- `await expr` pauses the current coroutine until expr completes.
- `asyncio.run(main())` — entry point. Creates the event loop and runs the coroutine.
- `asyncio.gather()` — run multiple coroutines **concurrently** and wait for all.

**Code Example:**

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(1)    # simulate I/O — yields control
    return f"data from {url}"

async def main():
    # sequential — takes 3 seconds total
    r1 = await fetch("url1")
    r2 = await fetch("url2")
    r3 = await fetch("url3")

    # concurrent — takes ~1 second total
    r1, r2, r3 = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(r1, r2, r3)

asyncio.run(main())

# create_task — start now, await later
async def main():
    t1 = asyncio.create_task(fetch("url1"))
    t2 = asyncio.create_task(fetch("url2"))
    # tasks start immediately in background
    do_other_work()
    r1 = await t1   # wait for result
    r2 = await t2
```

> 💡 **Interview Tip:** asyncio is **NOT parallelism** — it's concurrency. One thread runs at a time, but while waiting for I/O another task runs. For CPU-bound work use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.

---

### Async patterns — timeouts, queues & TaskGroup

**What it is:** Real async apps need timeouts to prevent hanging, queues to coordinate producers/consumers, and `TaskGroup` for clean error handling. These are the core building blocks.

**Key Ideas:**

- `asyncio.wait_for(coro, timeout=5)` — raises `asyncio.TimeoutError` if too slow.
- `asyncio.Queue` — async-safe producer/consumer queue.
- `asyncio.TaskGroup` (Python 3.11+) — preferred over `gather()` for error handling.
- `async for` iterates async iterators. `async with` manages async context managers.

**Code Example:**

```python
import asyncio

# timeout — prevent hanging forever
async def main():
    try:
        result = await asyncio.wait_for(
            fetch("slow-url"), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out!")

# TaskGroup (Python 3.11+) — preferred over gather
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("url1"))
        t2 = tg.create_task(fetch("url2"))
    # all tasks done — errors propagated cleanly
    print(t1.result(), t2.result())

# producer-consumer with Queue
async def producer(q):
    for item in range(5):
        await q.put(item)
    await q.put(None)   # sentinel value

async def consumer(q):
    while (item := await q.get()) is not None:
        print(f"processing {item}")

async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))
```

> 💡 **Interview Tip:** `asyncio.TaskGroup` (3.11+) is preferred over `gather()` for error handling — if one task fails, it cancels remaining tasks and re-raises cleanly. `gather()` can silently swallow errors.

---

### aiohttp & httpx — async HTTP clients

**What it is:** For async HTTP use `aiohttp` or `httpx`. Never use the `requests` library inside async code — it blocks the event loop and defeats the purpose of asyncio.

**Key Ideas:**

- Reuse `aiohttp.ClientSession` across requests — enables connection pooling.
- `httpx.AsyncClient` — async-compatible with a similar API to `requests`.
- Always use `async with` for sessions — ensures proper cleanup.
- `asyncio.Semaphore` limits concurrency — prevents overwhelming remote servers.

**Code Example:**

```python
import asyncio, aiohttp

# fetch many URLs concurrently
async def fetch_all(urls: list[str]) -> list:
    async with aiohttp.ClientSession() as session:
        async def fetch_one(url):
            async with session.get(url) as r:
                r.raise_for_status()
                return await r.json()
        return await asyncio.gather(
            *[fetch_one(u) for u in urls]
        )

# rate-limit with Semaphore
async def fetch_limited(urls, max_concurrent=10):
    sem = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:
        async def fetch_one(url):
            async with sem:    # max 10 at once
                async with session.get(url) as r:
                    return await r.text()
        return await asyncio.gather(
            *[fetch_one(u) for u in urls])

# httpx — requests-like API, async
import httpx
async def get_data(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json()

results = asyncio.run(fetch_all([url1, url2, url3]))
```

> 💡 **Interview Tip:** Fetching 100 URLs sequentially takes ~100s. With `asyncio` + `aiohttp.gather()` it takes ~1s. This is the core value of async I/O — **100x throughput** improvement for I/O-bound tasks.

---

## Logging

### Logging setup & best practices

**What it is:** Structured logging is the foundation of observable production systems. Python's logging module is highly configurable. Configure once at the app entry point; use `getLogger(__name__)` in every module.

**Key Ideas:**

- Five levels: `DEBUG(10)` < `INFO(20)` < `WARNING(30)` < `ERROR(40)` < `CRITICAL(50)`.
- Use `getLogger(__name__)` in every module — creates hierarchy matching package structure.
- Never use `print()` in production — can't be filtered, redirected, or levelled.
- Lazy `%s` formatting: `logger.debug('val: %s', x)` — string only built if level active.

**Code Example:**

```python
import logging, sys

# configure ONCE at app entry point
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

# in EVERY module — use __name__
logger = logging.getLogger(__name__)

# lazy formatting — string only built if level active
logger.debug("Processing item %s", item_id)
logger.info("User %s logged in", username)
logger.warning("Retrying: attempt %d of %d", n, max_n)
logger.error("DB query failed", exc_info=True)

# log exception + full traceback — best practice
try:
    risky_operation()
except Exception:
    logger.exception("Unexpected error")
```

> 💡 **Interview Tip:** Use lazy `%s` not f-strings in log calls. With `f'Value: {x}'` the string is **always** built even if the log level suppresses output. `%s` formatting is deferred — zero cost when level is off.

---

### RotatingFileHandler & structured (JSON) logging

**What it is:** Rotating handlers prevent log files from filling disk. Structured (JSON) logging makes logs machine-readable and searchable in tools like Elasticsearch, Datadog, or CloudWatch.

**Key Ideas:**

- `RotatingFileHandler` — rotates when file reaches `maxBytes`, keeps `backupCount` files.
- `TimedRotatingFileHandler` — rotates daily/hourly regardless of size.
- JSON logging: use `python-json-logger` (`pip install python-json-logger`).
- `logging.config.dictConfig(cfg)` — configure from a dict (or YAML). Good for large apps.

**Code Example:**

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # rotating — 5 files x 10MB = 50MB max disk usage
    handler = RotatingFileHandler(
        "app.log",
        maxBytes=10_000_000,
        backupCount=5
    )

    # JSON formatter (pip install python-json-logger)
    from pythonjsonlogger import jsonlogger
    handler.setFormatter(jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    ))
    logger.addHandler(handler)

# Output (one JSON line per record):
# {"asctime":"2024-01-15T10:30:00","name":"app.api",
#  "levelname":"INFO","message":"Request received"}

# separate error log file
error_handler = logging.FileHandler("errors.log")
error_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(error_handler)
```

> 💡 **Interview Tip:** **Structured (JSON) logs** are essential for production. Text logs need regex to parse; JSON logs can be queried with `jq`, indexed in Elasticsearch, filtered in CloudWatch — without custom parsers.

---

### Logging with context — ContextVar & filters

**What it is:** Real apps need per-request context (request ID, user ID, trace ID) in every log line. `ContextVar` stores per-coroutine state in async code. `logging.Filter` injects context into every log record.

**Key Ideas:**

- `LoggerAdapter` — wraps a logger and adds extra context to every record.
- `logging.Filter.filter(record)` — add/modify/drop records. Return `True` to keep.
- `contextvars.ContextVar` — per-async-task storage. Isolated between concurrent requests.
- `propagate=False` — stops records from bubbling up to ancestor loggers (avoids duplicates).

**Code Example:**

```python
import logging
from contextvars import ContextVar

# per-request context variable
request_id: ContextVar[str] = ContextVar("request_id", default="—")

class RequestFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id.get()
        return True   # True = keep the record

# format must include %(request_id)s
logger = logging.getLogger(__name__)
logger.addFilter(RequestFilter())
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(request_id)s] %(levelname)s %(message)s"
))
logger.addHandler(handler)

# in an async request handler
async def handle_request(req_id: str):
    token = request_id.set(req_id)   # set for this task
    try:
        logger.info("Processing")    # includes req_id
        await do_work()
    finally:
        request_id.reset(token)      # restore
```

> 💡 **Interview Tip:** `ContextVar` is the correct way to store per-request state in async code. Unlike `threading.local`, it's isolated per async `Task` — concurrent requests get their own context without interference.

---

## NumPy

### NumPy arrays — creation & properties

**What it is:** NumPy's `ndarray` stores data in a contiguous memory block. Operations run in compiled C/Fortran — 10-100x faster than Python loops. It is the foundation of scientific Python and machine learning.

**Key Ideas:**

- Arrays have a fixed `dtype` — all elements must be the same type (int64, float32, etc).
- **Broadcasting**: NumPy automatically expands smaller arrays to match larger ones.
- **Views vs copies**: slices are views (shared memory). Use `.copy()` for independence.
- Boolean indexing: `arr[arr > 0]` returns all positive elements — no loop needed.

**Code Example:**

```python
import numpy as np

# array creation
a = np.array([1, 2, 3, 4, 5])
np.zeros((3, 3))       # 3x3 zeros
np.ones((2, 4))        # 2x4 ones
np.arange(0, 10, 2)    # [0,2,4,6,8]
np.linspace(0, 1, 5)   # [0,.25,.5,.75,1]
np.eye(3)              # 3x3 identity matrix
np.random.randn(3, 3)  # normal distribution

# array properties
a.shape    # (5,)
a.ndim     # 1
a.dtype    # int64
a.size     # 5

# reshape
a.reshape(1, 5)    # (1,5)
a.reshape(-1, 1)   # column vector (5,1)
a.flatten()        # 1D copy

# indexing & slicing
a[0]          # first element
a[-1]         # last element
a[1:4]        # [2, 3, 4]
a[::2]        # [1, 3, 5]  every other
a[::-1]       # reversed
```

> 💡 **Interview Tip:** `arr.reshape(-1)` flattens to 1D. The `-1` means 'figure out this dimension automatically'. `arr.reshape(-1,1)` makes a column vector. Very common in ML preprocessing pipelines.

---

### NumPy operations & aggregations

**What it is:** Element-wise operations, aggregations, and broadcasting are the core of NumPy programming. Understanding `axis` is essential — it tells NumPy which dimension to collapse.

**Key Ideas:**

- `axis=0` collapses rows → one value per column (column statistics).
- `axis=1` collapses columns → one value per row (row statistics).
- `np.where(cond, x, y)` — vectorised if-else, applied to every element.
- `np.argmax / np.argmin` returns the **index** of max/min, not the value.

**Code Example:**

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# element-wise ops — no loops!
a + b           # [11, 22, 33, 44, 55]
a * 2           # [2, 4, 6, 8, 10]
np.sqrt(a)      # [1, 1.41, 1.73, 2, 2.24]

# boolean indexing
a[a > 3]                 # [4, 5]
np.where(a > 3, a, 0)   # [0, 0, 0, 4, 5]

# broadcasting
m = np.array([[1,2,3],[4,5,6]])   # (2,3)
v = np.array([10, 20, 30])        # (3,) → broadcasts to (2,3)
m + v   # [[11,22,33],[14,25,36]]

# aggregations
m.sum()          # 21  (all)
m.sum(axis=0)   # [5, 7, 9]   column sums
m.sum(axis=1)   # [6, 15]     row sums
m.mean(axis=0)  # [2.5, 3.5, 4.5]
m.argmax()      # 5 (flat index of max value)

# normalise 0-1
mn, mx = a.min(), a.max()
norm = (a - mn) / (mx - mn)

# matrix multiply
np.dot(m, m.T)       # (2,2)
np.matmul(m, m.T)    # same
```

> 💡 **Interview Tip:** Vectorised NumPy ops are 50-100x faster than Python for-loops. If you find yourself writing `for i in range(len(arr))` on a NumPy array, there is almost always a vectorised alternative.

---

## Pandas

### DataFrame basics & selection

**What it is:** A DataFrame is a 2D table with labelled rows (index) and columns. The key mental model: **think in columns, not rows**. Vectorised column operations are always faster than row-by-row `apply()`.

**Key Ideas:**

- `df.loc[label]` selects by index label. `df.iloc[n]` selects by integer position.
- `df[col]` returns a Series. `df[[c1,c2]]` returns a DataFrame.
- `df.info()` shows dtypes and null counts — run this first on any new dataset.
- `df.query()` filters with a readable SQL-like string — cleaner than chained brackets.

**Code Example:**

```python
import pandas as pd

df = pd.read_csv("sales.csv")
df.head(5)         # first 5 rows
df.info()          # dtypes, null counts
df.describe()      # statistics for numeric columns
df.shape           # (rows, cols)
df.dtypes          # column types
df.columns         # column names

# column selection
df["price"]              # Series (one column)
df[["name", "price"]]   # DataFrame (multiple)

# row selection
df.loc[0]                       # by label
df.iloc[0:5]                    # first 5 by position
df.loc[0:3, "name":"price"]    # rows AND columns

# filtering
df[df["price"] > 100]
df[(df.price > 100) & (df.qty > 5)]   # AND
df[df.name.isin(["Alice", "Bob"])]
df.query("price > 100 and qty > 5")   # cleaner

# add / modify columns
df["revenue"] = df["price"] * df["qty"]
df["tier"] = df["revenue"].apply(
    lambda x: "high" if x > 1000 else "low")
```

> 💡 **Interview Tip:** Always check `df.isnull().sum()` after loading data. Missing values silently break calculations — handle with `fillna()` or `dropna()` **before** any analysis.

---

### Groupby, aggregation & merging

**What it is:** groupby + agg is the Pandas workhorse: split-apply-combine. `merge` is SQL JOIN. `concat` is SQL UNION. Method chaining makes pipelines readable without intermediate variables.

**Key Ideas:**

- Named aggregations give clean output column names directly: `total=('revenue', 'sum')`.
- `df.pipe(fn)` — apply a function to the whole DataFrame (great for pipelines).
- `pd.merge(df1, df2, on='key', how='left')` — how: inner, left, right, outer.
- `pd.concat([df1, df2])` — stacks DataFrames vertically (like UNION ALL).

**Code Example:**

```python
import pandas as pd

# groupby + named aggregations
summary = (
    df.groupby("category")
      .agg(
          total=("revenue", "sum"),
          avg_price=("price", "mean"),
          count=("qty", "count")
      )
      .reset_index()
      .sort_values("total", ascending=False)
)

# method chaining — full pipeline
result = (
    pd.read_csv("sales.csv")
      .dropna(subset=["price", "qty"])
      .assign(revenue=lambda df: df.price * df.qty)
      .query("revenue > 1000")
      .groupby("category")
      .agg(total=("revenue", "sum"))
      .reset_index()
)

# merge — SQL join
merged = pd.merge(orders, customers,
    on="customer_id", how="left")

# concat — stack vertically
all_data = pd.concat([df_2022, df_2023, df_2024],
    ignore_index=True)

# pivot table
df.pivot_table(values="revenue",
    index="region", columns="category", aggfunc="sum")
```

> 💡 **Interview Tip:** Named aggregations `total=('revenue','sum')` give clean column names directly — no renaming afterwards. Method chaining is the **pandas equivalent of a Unix pipeline** — each step is clear and composable.

---

### Missing data, dtypes & reading various sources

**What it is:** Real data is messy — missing values, wrong types, inconsistent formats. Parquet is the preferred format for large data. Chunked reading handles files too large to fit in memory.

**Key Ideas:**

- `pd.read_csv(chunksize=N)` — read large CSVs in chunks without loading all to memory.
- `pd.read_parquet()` — columnar, compressed, fast. Preferred over CSV for big data.
- Use `category` dtype for low-cardinality string columns — saves 90% memory.
- `df.select_dtypes(include='number')` — filter columns by dtype.

**Code Example:**

```python
import pandas as pd, sqlalchemy

# handle missing data
df.isnull().sum()                       # count NaN per column
df.isnull().sum() / len(df)            # % missing
df.dropna()                             # drop rows with ANY NaN
df.dropna(subset=["price", "qty"])     # only check these cols
df["price"].fillna(df["price"].median())
df["cat"].fillna("Unknown")

# fix dtypes — memory efficient
df = pd.read_csv("data.csv", dtype={
    "category": "category",  # saves 90% vs str
    "age":      "int8",      # saves vs int64
    "price":    "float32",   # saves vs float64
})
df["date"] = pd.to_datetime(df["date"])

# CSV in chunks — process huge files
chunks = pd.read_csv("big.csv", chunksize=10_000)
result = pd.concat(
    [chunk[chunk.value > 0] for chunk in chunks])

# Parquet — fast columnar format
df.to_parquet("data.parquet", index=False)
df = pd.read_parquet("data.parquet")

# SQL
engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
df = pd.read_sql("SELECT * FROM sales", engine)
df.to_sql("results", engine, if_exists="replace", index=False)
```

> 💡 **Interview Tip:** **Parquet vs CSV:** Parquet is 5-10x smaller (columnar + compression), reads 10-100x faster (column skipping), and preserves dtypes exactly. Always prefer Parquet over CSV for data pipelines and intermediate storage.

---
