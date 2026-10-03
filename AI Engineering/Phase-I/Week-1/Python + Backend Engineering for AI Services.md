# Week 1: Python + Backend Engineering for AI Services

**Goal:** explain and build "a production FastAPI AI service" from scratch.
**Time:** ~7 days, 2-3 h/day. **Final deliverable:** AI Question Answering API (async, tested, logged).

## Day plan

| Day | Focus | Output |
|---|---|---|
| 1 | FastAPI core + Pydantic | Hello API with validated models |
| 2 | Project architecture, config, DI | Layered skeleton |
| 3 | Async Python | Concurrent LLM-style calls |
| 4 | Errors, middleware, logging | Robust API |
| 5 | pytest | 80%+ coverage on services |
| 6 | Build the project | AI QA API |
| 7 | Revise, mock interview | Answer the 10 questions below |

---

## 1. FastAPI core

FastAPI = Starlette (web) + Pydantic (validation) + type hints (auto docs at `/docs`).

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="AI QA API", version="1.0.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    temperature: float = Field(0.2, ge=0, le=1)

class AskResponse(BaseModel):
    answer: str
    model: str
    latency_ms: float

@app.post("/v1/ask", response_model=AskResponse, status_code=200)
async def ask(req: AskRequest) -> AskResponse:
    ...
```

**Key ideas**
- Path params `/items/{id}`, query params `?limit=10`, body = Pydantic model.
- `response_model` filters output (never leak internal fields like password hashes).
- Validation failure returns automatic **422**.
- **Routers** split the app: `APIRouter(prefix="/v1", tags=["qa"])` then `app.include_router(...)`.
- **API versioning:** URL prefix (`/v1`) is simplest and most common.

### Pydantic essentials (v2)
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class Doc(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: int
    text: str
    tags: list[str] = []

    @field_validator("text")
    @classmethod
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError("text must not be blank")
        return v

Doc.model_validate({"id": 1, "text": "hi"})   # dict -> model
doc.model_dump()                               # model -> dict
```
- Use separate models: `XCreate`, `XUpdate`, `XRead` (input vs output shapes differ).
- `pydantic-settings` for config (below). Same Pydantic models later define **LLM structured output** schemas.

### HTTP status codes to know
200 OK, 201 Created, 204 No Content, 400 bad request, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 validation, 429 rate limited, 500 server error, 502/503/504 upstream failure/unavailable/timeout (**use 502/504 when the LLM provider fails**).

---

## 2. Architecture (the interview answer)

```
app/
├── main.py            # app factory, middleware, routers
├── config.py          # Settings (env-driven)
├── dependencies.py    # DI providers (get_llm_service, get_current_user)
├── schemas/           # Pydantic request/response models
├── routes/            # thin HTTP layer: parse, call service, return
├── services/          # business logic (LLMService, RAGService)
├── clients/           # external wrappers (OpenAI/Anthropic, DB, Redis)
├── models/            # DB ORM models
├── core/              # logging, exceptions, security
├── utils/
└── tests/
```

**Layer rules (memorize):**
1. **Routes** know HTTP only. No business logic.
2. **Services** know business logic only. No `Request`/HTTP objects.
3. **Clients** wrap external systems so you can mock or swap them (e.g., change LLM vendor in one file).
4. Dependencies flow downward only: routes → services → clients.

### Config (12-factor: config from environment)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_env: str = "dev"
    llm_api_key: str = ""
    llm_model: str = "fake"
    request_timeout_s: float = 30.0

@lru_cache
def get_settings() -> Settings:
    return Settings()
```
Never commit `.env`. In AWS, secrets come from Secrets Manager injected as env vars.

### Dependency Injection
```python
from fastapi import Depends

def get_llm_service(settings: Settings = Depends(get_settings)) -> "LLMService":
    return LLMService(settings)

@router.post("/ask")
async def ask(req: AskRequest, svc: "LLMService" = Depends(get_llm_service)):
    return await svc.answer(req.question)
```
**Why DI matters:** in tests, `app.dependency_overrides[get_llm_service] = lambda: FakeLLM()` replaces the real thing with zero code changes. Also used for auth, DB sessions, rate limits. Dependencies can be chained and can use `yield` for setup/teardown (DB sessions).

### App lifespan (create shared resources once)
```python
from contextlib import asynccontextmanager
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=30)   # reuse connections
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)
```
Never create a new HTTP client per request.

---

## 3. Async Python (most-asked topic)

**Mental model:** one thread, one event loop. `await` = "I'm waiting on I/O, run something else meanwhile". Concurrency, not parallelism.

```python
import asyncio, time

async def fake_llm(prompt: str) -> str:
    await asyncio.sleep(1)        # non-blocking wait
    return f"answer to {prompt}"

async def main():
    t = time.perf_counter()
    results = await asyncio.gather(*(fake_llm(p) for p in ["a", "b", "c"]))
    print(results, time.perf_counter() - t)   # ~1s, not 3s

asyncio.run(main())
```

**Vocabulary**
- **Coroutine:** result of calling an `async def` (does nothing until awaited/scheduled).
- **Event loop:** scheduler that runs coroutines.
- **Task:** coroutine scheduled to run (`asyncio.create_task`).
- `gather` (run many, collect results), `wait_for` (timeout), `Semaphore` (limit concurrency, e.g. max 5 LLM calls at once), `TaskGroup` (3.11+, structured concurrency).

```python
sem = asyncio.Semaphore(5)
async def limited(p):
    async with sem:
        return await asyncio.wait_for(fake_llm(p), timeout=10)
```

### When to use async vs not
| Use `async def` | Use plain `def` |
|---|---|
| Network calls (LLM APIs, HTTP, DB with async driver, Redis) | CPU-heavy work (embeddings locally, parsing, reranking models) |
| Streaming responses, WebSockets | Libraries with only blocking APIs |
| Many concurrent I/O waits | Simple code with no I/O |

**The #1 bug:** blocking call inside `async def` (`time.sleep`, `requests.get`, sync DB driver, heavy loop). It **freezes the whole event loop** for every user.

Fixes:
- Use async libs: `httpx.AsyncClient`, `asyncpg`/SQLAlchemy async, `redis.asyncio`.
- Offload blocking work: `await asyncio.to_thread(blocking_fn, arg)` or `run_in_threadpool`.
- CPU-bound: process pool / separate worker (Celery, ARQ, SQS consumers).

FastAPI detail: a plain `def` endpoint is automatically run in a threadpool; an `async def` endpoint runs on the loop directly.

### Background jobs
- `BackgroundTasks`: tiny post-response work (log, send email). Lost if process dies.
- Real queues (Celery/ARQ/RQ + Redis, or SQS): ingestion, long RAG indexing. Return **202 Accepted + job id**, client polls.

---

## 4. Errors, middleware, logging

### Custom exceptions + global handlers
```python
class LLMError(Exception):
    def __init__(self, msg: str, status: int = 502):
        self.msg, self.status = msg, status

@app.exception_handler(LLMError)
async def llm_error_handler(request, exc: LLMError):
    return JSONResponse(status_code=exc.status,
                        content={"error": "llm_error", "detail": exc.msg})
```
Services raise domain errors; handlers translate to HTTP. Use `HTTPException(404, "...")` for simple cases. Consistent error shape: `{"error": code, "detail": msg, "request_id": id}`.

### Middleware (runs on every request)
```python
import uuid, time, logging
logger = logging.getLogger("app")

@app.middleware("http")
async def request_context(request, call_next):
    rid = request.headers.get("x-request-id", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["x-request-id"] = rid
    logger.info("request", extra={"rid": rid, "path": request.url.path,
                                  "status": response.status_code, "ms": round(ms, 1)})
    return response
```
Typical middleware: request ID, timing, CORS (`CORSMiddleware`), auth, rate limiting, gzip.

### Logging rules
- Use the `logging` module, never `print`. Prefer **JSON structured logs** (easy in CloudWatch).
- Log: request id, latency, status, model, tokens, errors. **Never log secrets or raw PII.**
- Levels: DEBUG (dev detail), INFO (events), WARNING (recoverable), ERROR (failures with `exc_info=True`).

### Retries and timeouts (essential for LLM calls)
```python
async def call_with_retry(fn, retries=3, base=0.5):
    for i in range(retries):
        try:
            return await asyncio.wait_for(fn(), timeout=30)
        except (asyncio.TimeoutError, httpx.HTTPError):
            if i == retries - 1:
                raise LLMError("upstream failed")
            await asyncio.sleep(base * 2 ** i)    # exponential backoff
```
Library option: `tenacity`. Always add **jitter** in production; retry only idempotent/transient errors (429, 5xx, timeouts).

---

## 5. Testing with pytest

```
tests/
├── conftest.py        # shared fixtures
├── unit/              # services in isolation
└── integration/       # API end-to-end
```

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_llm_service

class FakeLLM:
    async def answer(self, q: str):
        return {"answer": "fake", "model": "fake", "latency_ms": 1.0}

@pytest.fixture
def client():
    app.dependency_overrides[get_llm_service] = lambda: FakeLLM()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```
```python
# test_ask.py
import pytest

def test_ask_ok(client):
    r = client.post("/v1/ask", json={"question": "What is RAG?"})
    assert r.status_code == 200
    assert r.json()["answer"] == "fake"

@pytest.mark.parametrize("q", ["", "ab", "x" * 2001])
def test_ask_validation(client, q):
    assert client.post("/v1/ask", json={"question": q}).status_code == 422
```

**Async tests:** `pip install pytest-asyncio`, then
```python
@pytest.mark.asyncio
async def test_service():
    assert await LLMService(settings).answer("hi")
```
**Mocking:** `unittest.mock.patch`, `AsyncMock` for coroutines, `monkeypatch` fixture for env vars. Mock at the **client boundary** (the LLM wrapper), not deep internals.

**What to test:** services (unit), routes (integration), validation, error paths (LLM timeout returns 504), auth. **Don't call real LLMs in CI** (slow, costly, flaky). Run: `pytest -v --cov=app`.

Test pyramid: many unit, some integration, few end-to-end. Later (Week 4) add **LLM evals**, which are a different thing from unit tests.

---

## 6. Week 1 project: AI Question Answering API

**Requirements**
1. `POST /v1/ask`: validated input, returns answer + model + latency.
2. `GET /health` (liveness) and `GET /ready` (dependencies OK).
3. `LLMService` behind an interface, with `FakeLLM` and one real provider (Anthropic or OpenAI) selectable via `LLM_PROVIDER` env var.
4. Async endpoint, shared `httpx.AsyncClient` via lifespan, timeout + retry.
5. Request-ID middleware + structured logging.
6. Global exception handlers with a consistent error JSON.
7. pytest suite: validation, success, LLM failure -> 502/504, dependency override.
8. README: run, test, architecture diagram.

**Interface pattern (swap providers cleanly)**
```python
from typing import Protocol

class LLMClient(Protocol):
    async def complete(self, prompt: str, temperature: float) -> str: ...

class FakeLLMClient:
    async def complete(self, prompt, temperature):
        await asyncio.sleep(0.1)
        return f"Fake answer to: {prompt}"
```

**Stretch:** `/v1/ask/batch` using `gather` + semaphore; simple in-memory TTL cache; API-key auth dependency; Dockerfile.

Run: `uvicorn app.main:app --reload`, open `/docs`.

---

## 7. Interview Q&A (answer out loud)

1. **How would you structure a production FastAPI AI service?** Layered (routes/services/clients), config via env, DI, lifespan-managed shared clients, middleware for request IDs/logging, global error handlers, tests with overridden dependencies, Docker + CI.
2. **async vs sync, when?** Async for I/O-bound concurrency; sync/threadpool/workers for CPU-bound or blocking libs.
3. **What happens if you call `time.sleep` in `async def`?** Blocks the event loop; all requests stall.
4. **`def` vs `async def` endpoint in FastAPI?** `def` runs in a threadpool; `async def` runs on the loop.
5. **What is dependency injection and why use it?** Provide collaborators from outside; enables swapping and test overrides, reuse for auth/DB.
6. **How do you handle LLM provider failures?** Timeouts, retries with backoff + jitter, fallback model, circuit breaker, 502/504 responses, logging.
7. **Why Pydantic for LLM apps?** Validates input, defines structured output schemas, config management.
8. **BackgroundTasks vs Celery?** Lightweight in-process vs durable distributed queue with retries.
9. **How do you test code that calls an LLM?** Mock the client boundary, fixed fake responses; separate offline evals for quality.
10. **How do you stop one slow dependency hurting everyone?** Timeouts, bounded concurrency (semaphore), connection pools, rate limits.

---

## 8. Cheat sheet (quick revision)

- **Validate at the edge** (Pydantic), **keep routes thin**, **logic in services**.
- **Never block the loop.** Reuse clients. Always set timeouts.
- **Separate input/output schemas.** Version your API (`/v1`).
- **Config from env; secrets never in code.**
- **Fake the LLM in tests; use `dependency_overrides`.**
- **Log request id, latency, status, errors; no secrets/PII.**
- Commands: `uvicorn app.main:app --reload` · `pytest -v --cov=app` · `ruff check .` · `mypy app`

