# Athena Module Algorithms - Simplified for Paper

Concise algorithmic descriptions for each Athena module.

---

## 1. Advanced RAG

```
Input: Documents D, Query q
Output: Answer with sources

1. Split documents into chunks
2. Create embeddings for each chunk
3. Build FAISS vector index
4. Retrieve top-k similar chunks for query
5. Generate answer using LLM with retrieved context
6. Return answer with source attribution
```

---

## 2. ArXiv Search

```
Input: Query q
Output: Research papers P

1. Send query to ArXiv API
2. Parse XML response
3. Extract (title, authors, abstract, URL) for each paper
4. Remove duplicates
5. Sort by relevance
6. Return top-n papers
```

---

## 3. Chat Engine

```
Input: User message u, History H, Context C
Output: Response r

1. Build prompt with history H and context C
2. Append user message u
3. Send to LLM
4. Receive response r
5. Update history H ← H + (u, r)
6. Return r
```

---

## 4. Document Comparison

```
Input: Documents D₁, D₂
Output: Comparison report R

1. Generate embeddings: e₁ ← embed(D₁), e₂ ← embed(D₂)
2. Calculate similarity: sim ← cosine(e₁, e₂)
3. Extract technologies from both documents
4. Compare structural features (word count, unique terms)
5. Generate AI insights using LLM
6. Return report R
```

---

## 5. Knowledge Graph

```
Input: Research text T
Output: Graph G = (V, E)

1. Extract entities (methods, datasets, metrics, models)
2. Add entities as nodes to graph G
3. Identify relationships between entities
4. Add relationships as edges to graph G
5. Calculate node importance (centrality)
6. Return G
```

---

## 6. Knowledge Graph Visualizer

```
Input: Graph G = (V, E)
Output: Interactive visualization

1. For each node v in V:
   - Set size based on degree
   - Assign color by type
2. For each edge (u,v) in E:
   - Add labeled connection
3. Apply force-directed layout
4. Generate interactive HTML
5. Return visualization
```

---

## 7. Paper Fetcher

```
Input: Query q, Sources S
Output: Papers P

1. For each source s in S:
   - Search for papers matching q
   - Collect results
2. Merge results from all sources
3. Remove duplicates by title similarity
4. Sort by citations and year
5. Return top papers
```

---

## 8. PDF Utils

```
Input: PDF file F
Output: Clean text T

1. Extract raw text from PDF pages
2. Fix character spacing: "M a y" → "May"
3. Restore punctuation spacing
4. Normalize whitespace
5. Quality check (ensure minimal loss)
6. Return cleaned text T
```

---

## 9. QA Engine

```
Input: Document text T, Question q
Output: Answer a

1. Split text T into chunks
2. Create embeddings and FAISS index
3. Retrieve top-k relevant chunks for q
4. Build prompt with retrieved context
5. Generate answer using LLM
6. Return answer a
```

---

## 10. Semantic Search

```
Input: Corpus T, Query q
Output: Top-k results

1. Split corpus into chunks
2. Generate embeddings for all chunks
3. Build FAISS index
4. Embed query q
5. Find k nearest neighbors
6. Convert distances to similarity scores
7. Return ranked results
```

---

## 11. Web Search

```
Input: Query q
Output: Web results W

1. Connect to search API (DuckDuckGo)
2. Execute search with query q
3. Parse results (title, snippet, URL)
4. Format results
5. Return W
```

---

## 12. Voice Interface

```
Input: Audio A or Text T
Output: Text T' or Audio A'

Speech-to-Text:
1. Validate audio file A
2. Load and preprocess audio
3. Transcribe using Whisper model
4. Return text T'

Text-to-Speech:
1. Preprocess text T
2. Generate audio using TTS engine
3. Save audio file A'
4. Return A'
```

---

## System Architecture

```
Input: User request R, Mode M
Output: Response S

1. Initialize required modules
2. Route based on mode M:
   - PDF_QA → Extract text → Build index → Answer
   - CHAT → Build context → Generate response
   - RESEARCH → Search papers → Fetch → Present
   - COMPARE → Load docs → Compare → Report
   - KNOWLEDGE_GRAPH → Extract → Build → Visualize
   - VOICE → Transcribe → Process → Synthesize
3. Execute pipeline
4. Return response S
```

---

## Complexity Summary

| Module | Time | Space |
|--------|------|-------|
| RAG | O(n·d) | O(n·d) |
| Search | O(n) | O(n) |
| Chat | O(h+l) | O(h) |
| Comparison | O(n²) | O(n) |
| KG | O(n²) | O(n) |
| QA | O(n·d) | O(n·d) |

*n=chunks, d=dimensions, h=history, l=response length*

---

## References

1. **Vaswani, A., et al. (2017).** "Attention Is All You Need." *Advances in Neural Information Processing Systems*, 30.

2. **Lewis, P., et al. (2020).** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *arXiv preprint arXiv:2005.11401*.

3. **Johnson, J., et al. (2019).** "Billion-scale similarity search with GPUs." *IEEE Transactions on Big Data*, 7(3), 535-547. [FAISS]

4. **Reimers, N., & Gurevych, I. (2019).** "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *EMNLP 2019*.

5. **Radford, A., et al. (2023).** "Robust Speech Recognition via Large-Scale Weak Supervision." *ICML 2023*. [Whisper]

6. **Page, L., et al. (1999).** "The PageRank Citation Ranking: Bringing Order to the Web." *Stanford InfoLab Technical Report*.

7. **Hagberg, A., et al. (2008).** "Exploring Network Structure, Dynamics, and Function using NetworkX." *SciPy 2008*.

8. **Gao, J., et al. (2018).** "Neural Approaches to Conversational AI." *Foundations and Trends in Information Retrieval*, 13(2-3), 127-298.
