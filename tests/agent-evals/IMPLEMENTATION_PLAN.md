# Agent Evaluation Implementation Plan

## Incremental Approach

Start small, prove the concept, then expand:
1. **Step 1**: Extraction agent + 1 metric + 10 samples
2. **Step 2**: Conversation agent + 1 metric + 10 samples
3. **Step 3**: Expand metrics and dataset size
4. **Step 4**: Compare with different LLMs

---

## Step 1: Minimal Extraction Agent Evaluation (MVP)

### Goal: End-to-end evaluation working with minimal scope

- [x] Install `datasets` library from Hugging Face
- [x] Download Few-NERD dataset (`DFKI-SLT/few-nerd`, supervised config)
- [x] Explore dataset structure and select 10 samples from test split
- [x] Create `packages/evaluation/` directory structure
- [x] Implement basic entity F1 score calculation (exact match)
- [x] Create simple evaluation script that:
  - [x] Loads 10 Few-NERD samples
  - [x] Runs extraction agent on each sample
  - [x] Compares extracted entities to ground truth
  - [x] Calculates and prints F1 score
- [x] Document entity type mapping (Few-NERD → KETA)
- [x] Run evaluation and document baseline F1 score

**Success Criteria:** Script runs end-to-end, outputs single F1 score ✅

**Results:** Average F1 Score = 0.562 (56.2%), Precision = 0.478, Recall = 0.742

---

## Step 2: Add Conversation Agent Evaluation

### Goal: Evaluate conversation agent with minimal scope

- [ ] Research suitable QA dataset (SQuAD v2.0 or Natural Questions)
- [ ] Download and explore QA dataset structure
- [ ] Select 10 Q&A samples
- [ ] Implement answer F1 score calculation (token overlap)
- [ ] Create conversation evaluation script that:
  - [ ] Loads 10 Q&A samples
  - [ ] Extracts knowledge from context into graph
  - [ ] Runs conversation agent with questions
  - [ ] Compares answers to ground truth
  - [ ] Calculates and prints F1 score
- [ ] Run evaluation and document baseline F1 score

**Success Criteria:** Both extraction and conversation evaluations working

---

## Step 3: Expand Metrics and Dataset

### Goal: More comprehensive evaluation

#### Expand Extraction Evaluation
- [ ] Increase dataset to 100 samples
- [ ] Add precision and recall metrics (in addition to F1)
- [ ] Add per-entity-type metrics breakdown
- [ ] Add hallucination rate calculation
- [ ] Implement results serialization (JSON output)
- [ ] Generate evaluation report with metric breakdown

#### Expand Conversation Evaluation
- [ ] Increase dataset to 50 samples
- [ ] Add exact match accuracy metric
- [ ] Add citation precision/recall metrics
- [ ] Implement results serialization (JSON output)
- [ ] Generate evaluation report

#### Add System Metrics
- [ ] Track processing time per sample
- [ ] Track token usage per sample
- [ ] Calculate cost per sample
- [ ] Add metrics to evaluation reports

**Success Criteria:** Comprehensive metrics for both agents on larger dataset

---

## Step 4: LLM Comparison

### Goal: Compare current LLM (gpt-4o-mini) with alternatives

- [ ] Identify alternative LLM to test (e.g., gpt-4o, claude-3-5-sonnet, llama-3)
- [ ] Add LLM configuration to evaluation script
- [ ] Run extraction evaluation with both LLMs (100 samples each)
- [ ] Run conversation evaluation with both LLMs (50 samples each)
- [ ] Compare metrics side-by-side:
  - [ ] Entity extraction F1, precision, recall
  - [ ] Answer F1, exact match
  - [ ] Processing time
  - [ ] Token usage and cost
- [ ] Generate comparison report with recommendations
- [ ] Document trade-offs (accuracy vs cost vs speed)

**Success Criteria:** Clear comparison showing which LLM performs better for KETA

---

## Future Enhancements (Backlog)

### LLM-as-Judge Evaluation
- [ ] Design judge prompts for answer quality dimensions
- [ ] Implement LLM judge wrapper
- [ ] Run judge evaluation alongside metrics

### Relationship Extraction Evaluation
- [ ] Evaluate if relationship evaluation is needed
- [ ] Research DocRED or Re-TACRED dataset
- [ ] Implement relationship extraction evaluation

---
