# Week 2 — LLM Fundamentals & AI Application Engineering

> **Goal:** Understand how LLMs work, how to use them effectively through APIs, and how structured outputs and tool calling turn an LLM into a reliable application component.

---

## Table of Contents

1. [LLM Fundamentals](#1-llm-fundamentals)
2. [Tokens & Tokenization](#2-tokens--tokenization)
3. [Embeddings](#3-embeddings)
4. [Transformers](#4-transformers)
5. [Self-Attention](#5-self-attention)
6. [Q, K, V](#6-q-k-v)
7. [Multi-Head Attention](#7-multi-head-attention)
8. [Causal Attention](#8-causal-attention)
9. [Training vs Inference](#9-training-vs-inference)
10. [Context Windows](#10-context-windows)
11. [LLM API Architecture](#11-llm-api-architecture)
12. [Temperature](#12-temperature)
13. [Top-p](#13-top-p)
14. [Max Output Tokens](#14-max-output-tokens)
15. [Model Selection](#15-model-selection)
16. [Small vs Large Models](#16-small-vs-large-models)
17. [Model Routing](#17-model-routing)
18. [LLM Cost Optimization](#18-llm-cost-optimization)
19. [LLM Latency](#19-llm-latency)
20. [Streaming](#20-streaming)
21. [Production Reliability](#21-production-reliability)
22. [AI Service Architecture](#22-ai-service-architecture)
23. [Structured Output](#23-structured-output)
24. [Pydantic as an LLM Contract](#24-pydantic-as-an-llm-contract)
25. [Tool / Function Calling](#25-tool--function-calling)
26. [Tool Calling Flow](#26-tool-calling-flow)
27. [Tool Design](#27-tool-design)
28. [Tool Permissions & Security](#28-tool-permissions--security)
29. [SQL Agents](#29-sql-agents)
30. [Tool Calling vs MCP](#30-tool-calling-vs-mcp)
31. [Production Rules](#31-production-rules)
32. [Interview Cheat Sheet](#32-interview-cheat-sheet)
33. [Week 2 Mental Model](#33-week-2-mental-model)

---

# 1. LLM Fundamentals

## What is an LLM?

An LLM (Large Language Model) is fundamentally a model that predicts the **next token** given previous tokens.

Conceptually:

```text
"The weather today is"
             ↓
          LLM
             ↓
     probability distribution
             ↓
"sunny" / "good" / "cloudy" / ...
```

The model repeatedly predicts the next token:

```text
Token 1 → Token 2 → Token 3 → Token 4 → ...
```

This is called **autoregressive generation**.

### Important

An LLM does not initially produce an entire answer at once.

It generates:

```text
next token
   ↓
next token
   ↓
next token
   ↓
...
```

---

# 2. Tokens & Tokenization

LLMs don't directly process raw text.

They process **tokens**.

Example:

```text
"Artificial intelligence is powerful"
```

may become something conceptually like:

```text
["Artificial", " intelligence", " is", " powerful"]
```

Each token is mapped to an integer:

```text
token → token ID
```

Example:

```text
"Artificial" → 12345
" intelligence" → 67891
"is" → 234
" powerful" → 9182
```

The exact tokenization depends on the tokenizer/model.

## Why tokens matter

Tokens affect:

* context window
* API cost
* latency
* memory
* maximum prompt size
* maximum output size

Therefore:

```text
More tokens
   ↓
More computation
   ↓
Higher latency
   ↓
Higher cost
```

---

# 3. Embeddings

There are two important concepts that are often confused.

## Token embeddings

Inside an LLM:

```text
Token ID
   ↓
Embedding lookup
   ↓
Vector
   ↓
Transformer
```

The model converts token IDs into dense vectors that represent the tokens in the model's learned representation space.

## Text embeddings

Embeddings are also used outside the LLM for:

* semantic search
* RAG
* recommendation
* similarity search
* clustering

Example:

```text
"How do I reset my password?"
              ↓
       embedding model
              ↓
       [0.21, -0.43, 0.91, ...]
```

Documents can also be converted into vectors.

Then we can compare vectors for semantic similarity.

### Key distinction

```text
Token embedding
→ internal representation used by the LLM

Text embedding
→ vector representation used by applications such as RAG/search
```

---

# 4. Transformers

Modern GPT-style LLMs are based on the **Transformer architecture**.

High-level flow:

```text
Text
 ↓
Tokenizer
 ↓
Token IDs
 ↓
Token Embeddings
 ↓
Positional Information
 ↓
Transformer Layers
 ↓
Logits
 ↓
Probabilities
 ↓
Next Token
```

A Transformer layer contains mechanisms such as:

* self-attention
* feed-forward neural network
* normalization
* residual connections

---

# 5. Self-Attention

Self-attention allows each token to determine which other tokens are important when understanding the current context.

Example:

```text
"The animal didn't cross the road because it was tired."
```

What does `"it"` refer to?

Attention helps the model determine relationships between tokens.

Conceptually:

```text
Token
 ↓
Look at other tokens
 ↓
Determine relevance
 ↓
Combine information
```

The important idea:

> **Attention allows tokens to interact with other tokens in the context.**

---

# 6. Q, K, V

Self-attention uses:

* Query (Q)
* Key (K)
* Value (V)

Think of it like a database lookup.

### Query

"What information am I looking for?"

### Key

"What information do I contain?"

### Value

"What information should I return?"

Example:

```text
Query → What information is relevant?
Key   → How relevant is this token?
Value → Actual information from that token
```

The attention formula is:

```text
Attention(Q, K, V)
=
softmax(QKᵀ / √dₖ)V
```

Where:

* `Q` = Queries
* `K` = Keys
* `V` = Values
* `dₖ` = dimensionality of the keys

### Step-by-step

```text
QKᵀ
 ↓
Similarity between tokens
 ↓
Scale by √dₖ
 ↓
Softmax
 ↓
Attention weights
 ↓
Weighted sum of V
```

---

# 7. Multi-Head Attention

Instead of having one attention mechanism, Transformers use multiple attention heads.

```text
              Input
                |
      -----------------------
      |    |    |    |      |
    Head1 Head2 Head3 Head4 ...
      |    |    |    |
      -----------------------
                |
            Concatenate
                |
          Linear projection
```

Different heads can learn different relationships.

For example:

```text
Head 1 → grammatical relationships
Head 2 → long-range dependencies
Head 3 → semantic relationships
Head 4 → positional relationships
```

The exact learned behavior is determined during training.

---

# 8. Causal Attention

GPT-style models use **causal attention**.

A token cannot look at future tokens while predicting the next token.

Example:

```text
I love eating pizza
```

When predicting:

```text
pizza
```

the model can see:

```text
I
love
eating
```

but not:

```text
pizza
```

before predicting it.

Conceptually:

```text
I      → can attend to I
love   → I, love
eating → I, love, eating
pizza  → I, love, eating, pizza
```

A causal mask prevents access to future positions.

### Why?

Because during generation, future tokens don't exist yet.

---

# 9. Training vs Inference

## Training

During training:

```text
Huge dataset
     ↓
Tokenization
     ↓
Transformer
     ↓
Predict next token
     ↓
Compare with correct token
     ↓
Calculate loss
     ↓
Backpropagation
     ↓
Update parameters
```

The model learns its parameters.

## Inference

During inference:

```text
User prompt
    ↓
Tokenizer
    ↓
Model
    ↓
Next-token probabilities
    ↓
Sampling / selection
    ↓
Next token
    ↓
Repeat
    ↓
Final response
```

Parameters are generally not updated during normal inference.

### Key difference

```text
Training
→ learns the model

Inference
→ uses the learned model
```

---

# 10. Context Windows

A context window is the amount of token information the model can consider within a request.

Conceptually:

```text
Context Window
├── system instructions
├── conversation history
├── user prompt
├── retrieved documents
├── tool results
└── generated output
```

The exact accounting depends on the model/API.

## Why context matters

More context can mean:

* more information available
* potentially better answers

But also:

* more tokens
* higher cost
* higher latency
* more noise
* potentially worse retrieval/usefulness if irrelevant content is included

### AI Engineering principle

> More context is not automatically better context.

---

# 11. LLM API Architecture

A typical application looks like:

```text
Client
   ↓
FastAPI
   ↓
Authentication
   ↓
LLM Service
   ↓
Provider API
   ↓
Tokenizer
   ↓
Model Inference
   ↓
Generated Tokens
   ↓
API Response
   ↓
Client
```

Your application should generally **not** tightly couple business logic to a specific model provider.

---

# 12. Temperature

Temperature controls the randomness of token selection.

### Low temperature

```text
More deterministic
More consistent
Less variation
```

Useful for:

* classification
* extraction
* structured responses
* predictable workflows

### Higher temperature

```text
More variation
More randomness
```

Useful when creative variation is desirable.

### Important

Temperature does **not** make the model smarter.

It changes how the model samples from the probability distribution.

---

# 13. Top-p

Top-p is also called **nucleus sampling**.

Instead of considering every possible token, the model considers a dynamically selected set of tokens whose cumulative probability reaches `p`.

Example:

```text
Token A → 0.50
Token B → 0.25
Token C → 0.15
Token D → 0.05
Token E → 0.05
```

If:

```text
top_p = 0.90
```

the model considers enough high-probability tokens to reach approximately 90% cumulative probability.

### Temperature vs Top-p

```text
Temperature
→ changes probability distribution / randomness

Top-p
→ limits candidate tokens using cumulative probability
```

They solve related but different problems.

---

# 14. Max Output Tokens

Do not confuse:

```text
Context window
```

with:

```text
Maximum output tokens
```

### Context window

Maximum amount of context the model can process for a request.

### Max output tokens

Maximum amount of new output the model can generate.

Conceptually:

```text
Context
+ Input
+ Output
----------------
Model limits
```

The exact limits and accounting vary by model/provider.

---

# 15. Model Selection

Choosing an LLM is an engineering decision.

Don't ask only:

> "Which model is smartest?"

Instead evaluate:

### 1. Quality

Does it solve the task correctly?

### 2. Latency

How quickly does it respond?

### 3. Cost

How expensive is each request?

### 4. Context

Can it handle the required context?

### 5. Reasoning

Does the task require complex reasoning?

### 6. Tool calling

Does the model support the required tool/function workflow?

### 7. Structured output

Can it reliably produce schema-constrained responses?

### 8. Multimodality

Does it need:

* text
* image
* audio
* video?

### 9. Reliability

Consider:

* availability
* rate limits
* provider stability
* failure behavior

### 10. Security / Privacy

Consider:

* data sensitivity
* retention
* compliance
* enterprise requirements

---

# 16. Small vs Large Models

Don't automatically use the largest model.

## Small model

Good for:

* classification
* simple extraction
* routing
* summarization
* simple transformations
* high-volume workloads

Advantages:

```text
Lower cost
Lower latency
Higher throughput
```

## Large model

Useful for:

* complex reasoning
* difficult synthesis
* complicated agent workflows
* nuanced tasks

### Engineering principle

> Use the smallest model that reliably achieves the required quality.

---

# 17. Model Routing

Instead of using one model for everything:

```text
             Request
                ↓
             Router
          /     |      \
       Simple  Medium  Complex
         ↓       ↓        ↓
      Small    Medium    Large
      Model    Model     Model
```

Example:

```text
"Classify this ticket"
→ Small model

"Summarize this document"
→ Medium model

"Analyze this complex financial scenario"
→ Large/reasoning model
```

This can significantly reduce:

* cost
* latency

while maintaining quality.

---

# 18. LLM Cost Optimization

If asked:

> "How would you reduce LLM cost by 50%?"

Think systematically.

## 1. Reduce input tokens

Remove unnecessary:

* conversation history
* retrieved documents
* tool output
* duplicated instructions

## 2. Improve retrieval

Don't send 30 irrelevant documents when 5 relevant chunks are sufficient.

## 3. Model routing

Use smaller models for simpler tasks.

## 4. Cache

Cache repeated results.

Examples:

```text
Embedding cache
LLM response cache
Retrieval cache
```

## 5. Reduce unnecessary LLM calls

Bad:

```text
User
 ↓
LLM
 ↓
LLM
 ↓
LLM
 ↓
LLM
```

Ask:

> Can these calls be combined?

## 6. Limit output length

Don't generate unnecessary text.

## 7. Evaluate cheaper models

Test whether a cheaper model gives acceptable quality.

---

# 19. LLM Latency

End-to-end latency is not just LLM latency.

Think:

```text
Total latency
=
Network
+ Authentication
+ Retrieval
+ Database
+ Tool calls
+ LLM
+ Serialization
+ Response delivery
```

For a RAG application:

```text
User
 ↓
FastAPI
 ↓
Embedding
 ↓
Vector DB
 ↓
Reranker
 ↓
LLM
 ↓
Response
```

Any component can become the bottleneck.

### Interview approach

If an AI application takes 8 seconds:

Don't immediately blame the LLM.

Measure each component.

---

# 20. Streaming

Without streaming:

```text
User
 ↓
Request
 ↓
LLM generates entire answer
 ↓
Response
```

With streaming:

```text
User
 ↓
Request
 ↓
LLM
 ↓
Token
 ↓
Token
 ↓
Token
 ↓
Token
 ↓
...
```

The user starts seeing the answer earlier.

### Important

Streaming primarily improves:

> **Perceived latency**

It does not necessarily reduce the total computation required.

---

# 21. Production Reliability

Production LLM applications need more than:

```python
response = llm.invoke(prompt)
```

Consider:

### Timeouts

Prevent requests from hanging indefinitely.

### Retries

Retry transient failures.

### Exponential backoff

Avoid immediately hammering a failing service.

### Rate limits

Protect the system from overload.

### Fallback models

Example:

```text
Primary model fails
       ↓
Fallback model
```

### Logging

Track:

* request ID
* user/request metadata
* model
* latency
* errors

### Tracing

Track the complete workflow:

```text
Request
 ↓
Retrieval
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Response
```

---

# 22. AI Service Architecture

Avoid putting LLM provider logic directly inside FastAPI routes.

Bad:

```python
@app.post("/ask")
def ask(request):
    response = openai_client(...)
    return response
```

Better:

```text
routes/
    ask.py

schemas/
    ask.py

services/
    llm_service.py
    prompt_service.py

config.py

main.py
```

Architecture:

```text
FastAPI Route
      ↓
Request Schema
      ↓
AI Service
      ↓
LLM Provider
```

### Why?

Separation of concerns.

The route should handle:

* HTTP
* validation
* response

The AI service should handle:

* model calls
* prompts
* provider abstraction
* model selection

---

# 23. Structured Output

LLMs naturally produce text.

For applications, we often need predictable data.

Example:

```text
User:
"Analyze customer ABC123"
```

Instead of:

```text
Customer ABC123 appears to be medium risk...
```

we may want:

```json
{
  "risk_level": "medium",
  "reason": "Late payments increased",
  "recommended_action": "Review account"
}
```

Structured output means asking the model to conform to a defined schema.

---

# 24. Pydantic as an LLM Contract

In Python/FastAPI applications, Pydantic is excellent for defining the expected structure.

Example:

```python
from pydantic import BaseModel


class CustomerAnalysis(BaseModel):
    risk_level: str
    reason: str
    recommended_action: str
```

Now your application expects:

```text
CustomerAnalysis
├── risk_level
├── reason
└── recommended_action
```

### Why schema > "Return JSON"

Simply telling an LLM:

```text
"Return valid JSON"
```

doesn't provide the same reliability as a schema-enforced workflow.

A schema provides:

* required fields
* data types
* validation
* predictable application interfaces

### Important

Even structured output should be treated as **untrusted input**.

Validate it.

---

# 25. Tool / Function Calling

Tool calling allows an LLM to request an external capability.

Examples:

```text
get_weather()
get_customer()
search_documents()
query_database()
send_email()
create_ticket()
```

The model itself does not directly execute your Python function.

Instead:

```text
LLM
 ↓
Requests tool
 ↓
Application validates request
 ↓
Application executes tool
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

---

# 26. Tool Calling Flow

Example:

User:

```text
"What is the weather in Dallas?"
```

Architecture:

```text
User
 ↓
LLM
 ↓
"I should call get_weather(Dallas)"
 ↓
Application
 ↓
Authorization / validation
 ↓
Weather API
 ↓
Weather result
 ↓
LLM
 ↓
Final response
```

The key idea:

> The LLM decides what capability it wants to use; the application controls whether and how that capability is executed.

---

# 27. Tool Design

Tools should be:

* narrow
* explicit
* predictable
* validated
* permission-aware

### Bad

```text
database_tool(query)
```

This potentially allows arbitrary database operations.

### Better

```text
get_customer(customer_id)
```

or:

```text
get_customer_transactions(customer_id, start_date, end_date)
```

The narrower the capability, the easier it is to secure.

---

# 28. Tool Permissions & Security

Never assume:

```text
LLM requested it
→ therefore it is allowed
```

Instead:

```text
LLM request
    ↓
Application
    ↓
Authentication
    ↓
Authorization
    ↓
Input validation
    ↓
Tool execution
```

For example:

```text
User asks:
"Delete customer 123"
```

The LLM might request:

```text
delete_customer(123)
```

But the application should check:

```text
Is user authenticated?
        ↓
Does user have delete permission?
        ↓
Is customer 123 accessible?
        ↓
Is this action allowed?
        ↓
Should human approval be required?
        ↓
Execute
```

---

# 29. SQL Agents

A naive SQL agent looks like:

```text
User
 ↓
LLM
 ↓
Generate SQL
 ↓
Database
```

This is dangerous.

Potential problems:

* destructive SQL
* unauthorized tables
* expensive queries
* data leakage
* unrestricted access
* SQL injection-like risks
* huge result sets

## Better architecture

```text
User
 ↓
LLM
 ↓
SQL Tool
 ↓
SQL Validation
 ↓
Authorization
 ↓
Read-only DB
 ↓
Query Limits
 ↓
Execute
 ↓
Result
 ↓
LLM
 ↓
Answer
```

Recommended controls:

* read-only credentials
* table/column allowlists
* query validation
* query timeout
* result-size limits
* audit logging
* user-level authorization
* row-level security where appropriate

---

# 30. Tool Calling vs MCP

These concepts are related but different.

## Tool calling

Answers:

> "How can the model request an external capability?"

Example:

```text
LLM → get_customer(customer_id)
```

## MCP

MCP provides a standardized protocol for exposing capabilities to AI applications.

Conceptually:

```text
AI Client
    ↓
MCP
    ↓
MCP Server
    ↓
Tools / Resources / Prompts
    ↓
External systems
```

### Simple mental model

```text
Tool calling
→ capability mechanism

MCP
→ standardized protocol for connecting AI systems to capabilities/context
```

MCP can expose tools such as:

```text
Database
GitHub
Files
Internal APIs
Business systems
```

---

# 31. Production Rules

These are some of the most important rules from Week 2.

### Rule 1

> Never blindly trust LLM output.

Treat it as untrusted input.

### Rule 2

> LLMs should not directly control sensitive systems.

The application should enforce permissions.

### Rule 3

> Use schemas for application-facing LLM output.

### Rule 4

> Use narrow tools rather than unrestricted tools.

### Rule 5

> Use the smallest model that achieves the required quality.

### Rule 6

> Don't send unnecessary context to the LLM.

### Rule 7

> Measure before optimizing.

### Rule 8

> Streaming improves perceived latency, not necessarily total computation.

### Rule 9

> Separate FastAPI/API logic from AI provider logic.

### Rule 10

> Security must be enforced outside the model.

---

# 32. Interview Cheat Sheet

## Q: What is an LLM?

An autoregressive model that predicts the next token based on previous tokens.

---

## Q: Why do tokens matter?

They affect:

* cost
* latency
* context limits
* memory
* output limits

---

## Q: Token embedding vs text embedding?

Token embeddings are internal representations used by the LLM.

Text embeddings represent text as vectors for applications such as semantic search and RAG.

---

## Q: Why do Transformers use attention?

To allow tokens to dynamically determine which other tokens are relevant when processing context.

---

## Q: What are Q, K, V?

```text
Q → what am I looking for?
K → what information do I contain?
V → what information should I provide?
```

---

## Q: Why is causal masking needed?

Because a GPT-style model must not see future tokens when predicting the next token.

---

## Q: Training vs inference?

```text
Training
→ learn/update model parameters

Inference
→ use learned parameters to generate output
```

---

## Q: Temperature vs top-p?

```text
Temperature
→ controls randomness of sampling

Top-p
→ limits candidate tokens using cumulative probability
```

---

## Q: Context window vs max output tokens?

```text
Context window
→ total context the model can process

Max output tokens
→ maximum new tokens generated
```

---

## Q: How would you reduce LLM cost?

Mention:

1. Reduce input tokens
2. Improve retrieval
3. Use smaller models
4. Model routing
5. Cache
6. Reduce unnecessary calls
7. Reduce output length
8. Evaluate cheaper models

---

## Q: How would you debug high AI latency?

Break latency down:

```text
Network
+ Retrieval
+ DB
+ Tools
+ LLM
+ Serialization
+ Streaming
```

Measure each component rather than assuming the LLM is responsible.

---

## Q: Why use structured output?

Because applications need predictable, validated data instead of arbitrary natural-language text.

---

## Q: Why use Pydantic?

For:

* schema definition
* validation
* type safety
* predictable API contracts

---

## Q: Does an LLM directly execute a Python function?

No.

The LLM generates a structured tool request.

The application decides whether to execute the tool and performs the actual execution.

---

## Q: Why should tools be narrow?

Narrow tools reduce:

* security risk
* unintended actions
* complexity
* authorization problems

---

## Q: How would you secure a SQL agent?

Use:

```text
Read-only DB
+
Authorization
+
SQL validation
+
Table/column restrictions
+
Timeouts
+
Result limits
+
Audit logs
```

---

## Q: Tool calling vs MCP?

```text
Tool calling
→ model requests a capability

MCP
→ standardized protocol for exposing capabilities/context to AI applications
```

---

# 33. Week 2 Mental Model

The most important thing to remember from this week:

```text
                         USER
                           |
                           ↓
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           |
                           ↓
                    Request Schema
                           |
                           ↓
                    ┌─────────────┐
                    │ AI Service  │
                    └──────┬──────┘
                           |
                    ┌──────┴───────┐
                    ↓              ↓
                Prompt         Model Router
                                   |
                       ┌───────────┼───────────┐
                       ↓           ↓           ↓
                    Small       Medium       Large
                    Model       Model        Model
                       \           |           /
                        \          |          /
                         └─────── LLM ───────┘
                                  |
                     ┌────────────┴────────────┐
                     ↓                         ↓
              Structured Output           Tool Calling
                     |                         |
                     ↓                         ↓
                Pydantic                  Application
                 Validation              Authorization
                                               |
                                               ↓
                                           Tool/API/DB
                                               |
                                               ↓
                                          Tool Result
                                               |
                                               ↓
                                              LLM
                                               |
                                               ↓
                                            Response
```

## The AI Engineer mindset

Don't think:

```text
"How do I call an LLM?"
```

Think:

```text
What model?
     ↓
What context?
     ↓
What prompt?
     ↓
What output schema?
     ↓
Does it need tools?
     ↓
Are tools authorized?
     ↓
How much will it cost?
     ↓
How fast will it be?
     ↓
How do I handle failure?
     ↓
How do I evaluate quality?
     ↓
How do I observe it in production?
```

That is the shift from **"using an LLM"** to **AI Engineering**.

---

# Week 2 — Final Checklist

* [x] LLM fundamentals
* [x] Autoregressive generation
* [x] Tokens and tokenization
* [x] Token embeddings vs text embeddings
* [x] Transformer architecture
* [x] Self-attention
* [x] Q/K/V
* [x] Attention formula
* [x] Multi-head attention
* [x] Causal attention
* [x] Training vs inference
* [x] Context windows
* [x] LLM APIs
* [x] Temperature
* [x] Top-p
* [x] Max output tokens
* [x] Model selection
* [x] Small vs large models
* [x] Model routing
* [x] Cost optimization
* [x] Latency analysis
* [x] Streaming fundamentals
* [x] Production reliability
* [x] AI service architecture
* [x] Structured output
* [x] Pydantic contracts
* [x] Tool/function calling
* [x] Tool design
* [x] Tool authorization
* [x] SQL agent security
* [x] Tool calling vs MCP
* [x] Production AI engineering principles
* [x] Interview questions


