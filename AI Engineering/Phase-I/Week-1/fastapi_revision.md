# FastAPI Revision Sheet — Week 1

## Topics Covered

- API and request/response cycle
- HTTP methods
- FastAPI basics
- GET and POST endpoints
- Pydantic models
- Request and response validation
- HTTP status codes
- Error handling
- `async` and `await`

---

# 1. What is an API?

An **API (Application Programming Interface)** allows different applications to communicate with each other.

```text
User
  ↓
Frontend / Browser
  ↓ HTTP Request
FastAPI Backend
  ↓
Python / Business Logic
  ↓
JSON Response
  ↓
Frontend / User
```

## Important Terms

- **Client** → Sends a request
- **Server** → Receives and processes the request
- **Request** → Information sent to the server
- **Response** → Information returned by the server
- **Endpoint** → A URL that performs a specific operation

Example:

```text
POST /ask
```

---

# 2. HTTP Methods

| Method | Purpose | Example |
|---|---|---|
| `GET` | Retrieve data | `/health` |
| `POST` | Send data for processing | `/ask` |
| `PUT` | Update data | `/users/1` |
| `DELETE` | Delete data | `/users/1` |

---

# 3. FastAPI Basics

```python
from fastapi import FastAPI

app = FastAPI()
```

Create a route:

```python
@app.get("/")
async def root():
    return {"message": "Hello"}
```

Flow:

```text
GET /
   ↓
FastAPI matches the route
   ↓
root() function runs
   ↓
Return JSON
```

---

# 4. GET Endpoint

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

Request:

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

# 5. POST Endpoint

A POST endpoint accepts data from the client.

```python
@app.post("/ask")
async def ask():
    return {"answer": "Hello"}
```

For structured input, we use **Pydantic**.

---

# 6. Pydantic

Pydantic defines and validates the structure of data.

```python
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
```

Expected JSON:

```json
{
  "question": "What is RAG?"
}
```

Inside Python:

```python
request.question
```

Mental model:

```text
JSON Request
      ↓
Pydantic Model
      ↓
Validated Python Object
```

---

# 7. Request Models

```python
class AskRequest(BaseModel):
    question: str
```

Use it in an endpoint:

```python
@app.post("/ask")
async def ask(request: AskRequest):
    return {
        "question": request.question
    }
```

Flow:

```text
Client sends JSON
       ↓
Pydantic validates it
       ↓
FastAPI calls the function
       ↓
request.question
       ↓
Response
```

---

# 8. Required Fields

```python
class AskRequest(BaseModel):
    question: str
```

`question` is required.

Valid:

```json
{
  "question": "What is RAG?"
}
```

Invalid:

```json
{}
```

FastAPI returns:

```text
422 Unprocessable Entity
```

The route function does not run because validation fails first.

---

# 9. Optional Fields

```python
from typing import Optional

class AskRequest(BaseModel):
    question: str
    model: Optional[str] = None
```

Both are valid:

```json
{
  "question": "What is RAG?"
}
```

```json
{
  "question": "What is RAG?",
  "model": "gpt"
}
```

If `model` is missing, `request.model` returns `None`.

---

# 10. Default Values

```python
class AskRequest(BaseModel):
    question: str
    temperature: float = 0.2
```

If `temperature` is not provided:

```python
request.temperature
```

returns:

```text
0.2
```

---

# 11. Validation with Field

```python
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )
```

An empty question is invalid and results in a `422` validation error.

---

# 12. Response Models

```python
class AskResponse(BaseModel):
    question: str
    answer: str
```

Use it like this:

```python
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    return {
        "question": request.question,
        "answer": "RAG stands for Retrieval-Augmented Generation."
    }
```

API contract:

```text
INPUT
{"question": "..."}

        ↓

APPLICATION

        ↓

OUTPUT
{"question": "...", "answer": "..."}
```

---

# 13. HTTP Status Codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Resource created |
| `400` | Bad request |
| `401` | Authentication required |
| `403` | Permission denied |
| `404` | Resource not found |
| `422` | Validation failed |
| `500` | Unexpected server error |

---

# 14. 422 vs 400

## 422 — Validation Problem

The request does not match the expected Pydantic model.

```text
Client
   ↓
Pydantic Validation
   ↓
Invalid input
   ↓
422
```

## 400 — Application-Level Problem

The request structure may be valid, but the application decides it cannot process it.

```python
raise HTTPException(
    status_code=400,
    detail="Invalid request"
)
```

---

# 15. HTTPException

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
async def get_user(user_id: int):

    users = {
        1: "Nishtha",
        2: "Alice"
    }

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user_id,
        "name": users[user_id]
    }
```

Request:

```text
GET /users/99
```

Response:

```json
{
  "detail": "User not found"
}
```

Status:

```text
404 Not Found
```

---

# 16. Error Flow

```text
                    REQUEST
                       │
                       ▼
              Pydantic Validation
                 │           │
              Invalid       Valid
                 │           │
                 ▼           ▼
                422     Business Logic
                              │
                         ┌────┴────┐
                         │         │
                      Error      Success
                         │         │
                         ▼         ▼
                     400/404      200

Unexpected Server Error
          │
          ▼
         500
```

---

# 17. What is Async?

In synchronous code, one task may wait for another to finish.

```text
Task A
   ↓
Wait
   ↓
Finish
   ↓
Task B
```

With asynchronous programming, when one operation is waiting for I/O, the application can work on other ready tasks.

```text
Task A → Waiting for LLM
              │
              ├── Handle Task B
              ├── Handle Task C
              │
              ▼
        LLM responds
              │
              ▼
          Continue Task A
```

---

# 18. async def

Normal function:

```python
def get_answer():
    return "Hello"
```

Async function:

```python
async def get_answer():
    return "Hello"
```

Important:

> Adding `async` does not automatically make code faster.

Async is especially useful when waiting for I/O.

---

# 19. await

```python
import asyncio

async def fake_llm(question: str):
    await asyncio.sleep(3)
    return f"Answer: {question}"
```

`await` pauses the current coroutine until the asynchronous operation completes while allowing the event loop to run other ready tasks.

---

# 20. Why Async Matters for AI Engineering

AI applications often wait for:

- LLM APIs
- External APIs
- Vector databases
- Databases
- Redis
- Cloud services

Example:

```python
@app.post("/ask")
async def ask(request: AskRequest):
    answer = await ai_service.ask(request.question)

    return {
        "answer": answer
    }
```

Architecture:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
AI Service
   │
   ├── await Vector Search
   ├── await Database
   └── await LLM
            │
            ▼
          Answer
```

---

# 21. time.sleep() vs asyncio.sleep()

## Blocking

```python
import time

time.sleep(3)
```

This blocks the current thread.

## Async waiting

```python
import asyncio

await asyncio.sleep(3)
```

This suspends the current coroutine while allowing the event loop to run other tasks.

---

# 22. When Should I Use Async?

## Good candidates

- LLM API calls
- External API calls
- Async database calls
- Redis/network operations
- Network I/O

## Not automatically useful

- Heavy calculations
- Large CPU-bound loops
- ML model training

For CPU-heavy work, simply adding `async` does not solve the problem.

---

# 23. Complete FastAPI Example

```python
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Engineering Practice API"
)


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )


class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
async def root():
    return {
        "message": "AI Engineering API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@app.get("/about")
async def about():
    return {
        "name": "AI Engineering Practice API",
        "version": "1.0"
    }


async def fake_llm(question: str):
    await asyncio.sleep(3)
    return f"AI answer to: {question}"


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):

    if "error" in request.question.lower():
        raise HTTPException(
            status_code=400,
            detail="Invalid question"
        )

    answer = await fake_llm(request.question)

    return {
        "question": request.question,
        "answer": answer
    }


@app.get("/users/{user_id}")
async def get_user(user_id: int):

    users = {
        1: "Nishtha",
        2: "Alice"
    }

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user_id,
        "name": users[user_id]
    }
```

---

# 24. Final Mental Model

```text
                    CLIENT
                       │
                       │ HTTP Request
                       ▼
                 ┌───────────┐
                 │  FASTAPI  │
                 └───────────┘
                       │
                       ▼
               Pydantic Validation
                  │          │
               Invalid      Valid
                  │          │
                  ▼          ▼
                 422      Route Function
                               │
                               ▼
                         Business Logic
                               │
                      ┌────────┴────────┐
                      ▼                 ▼
                   Error              Success
                      │                 │
                   400/404             200
                                        │
                                        ▼
                                   JSON Response
                                        │
                                        ▼
                                      CLIENT
```

---

# Practice Checklist

Build a small FastAPI application with:

- [ ] `GET /`
- [ ] `GET /health`
- [ ] `GET /about`
- [ ] `GET /users/{user_id}`
- [ ] `POST /ask`

Your `/ask` endpoint should use:

- [ ] `AskRequest`
- [ ] `AskResponse`
- [ ] `Field(min_length=1, max_length=500)`
- [ ] `HTTPException`
- [ ] `async`
- [ ] `await`
- [ ] `asyncio.sleep(3)`

## Test Cases

### Valid Question

```json
{
  "question": "What is RAG?"
}
```

Expected: `200 OK`

### Missing Question

```json
{}
```

Expected: `422 Validation Error`

### Empty Question

```json
{
  "question": ""
}
```

Expected: `422 Validation Error`

### Application-Level Error

```json
{
  "question": "Give me an error"
}
```

Expected: `400 Bad Request`

### Existing User

```text
GET /users/1
```

Expected: `200 OK`

### Missing User

```text
GET /users/99
```

Expected: `404 Not Found`

---

# Key Things to Remember

1. **FastAPI receives requests and returns responses.**
2. **Routes connect URLs to Python functions.**
3. **GET is generally used to retrieve data.**
4. **POST is used to send data for processing.**
5. **Pydantic validates incoming and outgoing data.**
6. **422 usually means request validation failed.**
7. **HTTPException is used for expected application errors.**
8. **async/await is especially useful for I/O-bound operations.**
9. **Async does not automatically make CPU-heavy code faster.**
10. **FastAPI + Pydantic + async are foundational skills for AI backend engineering.**

---


