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

## Step 2: Add Conversation Agent Evaluation with DeepEval

### Goal: Evaluate conversation agent using DeepEval framework with minimal scope

#### Setup DeepEval
- [ ] Install DeepEval (`pip install deepeval`)
- [ ] Set up pytest structure for evaluations
- [ ] Configure DeepEval for KETA agents
- [ ] Verify installation with sample test

#### Dataset Preparation
- [ ] Research suitable QA dataset (SQuAD v2.0 or Natural Questions)
- [ ] Download and explore QA dataset structure
- [ ] Select 10 Q&A samples with context
- [ ] Format samples for DeepEval test cases

#### Implement DeepEval Metrics
- [ ] Create DeepEval test cases (LLMTestCase format)
- [ ] Implement Faithfulness metric (answer grounded in context)
- [ ] Implement Answer Relevancy metric (answer addresses question)
- [ ] Add Contextual Precision metric (retrieved context quality)
- [ ] Configure metrics with appropriate thresholds

#### Create Evaluation Script
- [ ] Create `run_conversation_eval.py` with DeepEval
- [ ] Script flow:
  - [ ] Load 10 Q&A samples
  - [ ] Extract knowledge from context into graph
  - [ ] Run conversation agent with questions
  - [ ] Create LLMTestCase for each Q&A pair
  - [ ] Evaluate with Faithfulness, Answer Relevancy, Contextual Precision
  - [ ] Collect and aggregate metrics
- [ ] Add per-sample metric breakdown
- [ ] Generate summary statistics

#### Testing & Documentation
- [ ] Run evaluation on 10 samples
- [ ] Document baseline metrics:
  - [ ] Faithfulness score (0-1)
  - [ ] Answer Relevancy score (0-1)
  - [ ] Contextual Precision score (0-1)
- [ ] Analyze failure cases (low-scoring responses)
- [ ] Create `CONVERSATION_BASELINE_RESULTS.md`
- [ ] Update README.md with conversation evaluation usage

**Success Criteria:**
- DeepEval pytest tests running successfully
- Three core metrics (Faithfulness, Answer Relevancy, Contextual Precision) calculated
- Baseline established for 10 samples
- Per-sample and aggregate statistics documented

**Estimated Time:** 4-6 hours

---

## Step 2.5: Add Trustworthiness Evaluation (Optional Enhancement)

### Goal: Add Cleanlab TLM for hallucination detection and trustworthiness scoring

#### Setup Cleanlab TLM
- [ ] Get free API key from https://tlm.cleanlab.ai/
- [ ] Install cleanlab-tlm (`pip install cleanlab-tlm`)
- [ ] Set CLEANLAB_API_KEY environment variable
- [ ] Test basic TLM scoring

#### Integrate with Conversation Evaluation
- [ ] Add TLM trustworthiness scoring to `run_conversation_eval.py`
- [ ] Score each conversation response:
  - [ ] Pass question + context + response to TLM
  - [ ] Collect trustworthiness_score (0-1)
  - [ ] Flag low-confidence responses (score < 0.7)
- [ ] Add trustworthiness metrics to output
- [ ] Compare TLM scores with DeepEval Faithfulness scores

#### Analysis & Documentation
- [ ] Identify correlation between TLM scores and DeepEval metrics
- [ ] Document cases where TLM flags issues DeepEval misses
- [ ] Add trustworthiness results to `CONVERSATION_BASELINE_RESULTS.md`
- [ ] Update cost analysis (TLM API usage)

**Success Criteria:**
- TLM trustworthiness scores calculated for all 10 samples
- Correlation analysis with DeepEval metrics completed
- Low-confidence responses identified and analyzed

**Estimated Time:** 1-2 hours

---

## Step 3: Expand Metrics and Dataset

### Goal: Scale evaluation to production-ready dataset sizes and add comprehensive metrics

#### Expand Extraction Evaluation
- [ ] Increase Few-NERD samples to 100
- [ ] Add hallucination rate calculation (entities not in text)
- [ ] Add fuzzy matching for partial entity matches
- [ ] Generate JSON output with detailed metrics
- [ ] Create comparison chart (baseline vs current)
- [ ] Document improvements from Step 1 baseline

#### Expand Conversation Evaluation (DeepEval)
- [ ] Increase QA dataset to 50 samples
- [ ] Add RAGAS metrics alongside DeepEval:
  - [ ] Install RAGAS (`pip install ragas`)
  - [ ] Context Relevancy (retrieval quality)
  - [ ] Context Recall (answer coverage)
  - [ ] Context Entities Recall (NER in RAG)
- [ ] Add Bias metric (DeepEval)
- [ ] Add Toxicity metric (DeepEval)
- [ ] Implement results serialization (JSON output)

#### Expand Trustworthiness Evaluation (Cleanlab TLM)
- [ ] Scale TLM evaluation to 50 samples
- [ ] Track hallucination detection rate
- [ ] Compare TLM vs DeepEval hallucination detection
- [ ] Calculate false positive/negative rates

#### Add System Metrics
- [ ] Track processing time per sample (both agents)
- [ ] Track token usage per sample
- [ ] Calculate cost per sample (LLM + evaluation APIs)
- [ ] Generate cost-performance tradeoff analysis
- [ ] Add metrics to evaluation reports

**Success Criteria:**
- 100 extraction samples evaluated
- 50 conversation samples evaluated
- 5+ metrics per evaluation type
- System performance metrics documented
- JSON output for all evaluations

**Estimated Time:** 6-10 hours

---

## Step 4: LLM Comparison with Multi-Framework Evaluation

### Goal: Compare current LLM (gpt-4o-mini) with alternatives using comprehensive evaluation suite

#### LLM Selection & Configuration
- [ ] Identify alternative LLMs to test:
  - [ ] Option 1: gpt-4o (higher cost, better accuracy)
  - [ ] Option 2: claude-3-5-sonnet (comparable cost, different strengths)
  - [ ] Option 3: Consider gemini-1.5-pro or llama-3-70b
- [ ] Add LLM configuration to evaluation scripts
- [ ] Set up API keys and rate limiting for each LLM

#### Extraction Agent Comparison
- [ ] Run extraction evaluation with each LLM (100 samples)
- [ ] Metrics to compare:
  - [ ] seqeval: Overall F1, precision, recall
  - [ ] Per-entity-type performance (person, organization, location, etc.)
  - [ ] Processing time per sample
  - [ ] Token usage and cost
  - [ ] Hallucination rate

#### Conversation Agent Comparison
- [ ] Run conversation evaluation with each LLM (50 samples)
- [ ] DeepEval metrics:
  - [ ] Faithfulness score
  - [ ] Answer Relevancy score
  - [ ] Contextual Precision score
  - [ ] Bias score
  - [ ] Toxicity score
- [ ] RAGAS metrics:
  - [ ] Context Relevancy
  - [ ] Context Recall
  - [ ] Context Entities Recall
- [ ] Cleanlab TLM metrics:
  - [ ] Trustworthiness score
  - [ ] Hallucination detection rate
  - [ ] Error reduction percentage

#### Comparative Analysis
- [ ] Generate side-by-side comparison table
- [ ] Create visualization charts:
  - [ ] Accuracy vs Cost scatter plot
  - [ ] Speed vs Accuracy trade-off
  - [ ] Hallucination rate comparison
- [ ] Calculate cost-normalized performance scores
- [ ] Identify use-case-specific recommendations:
  - [ ] Best for extraction accuracy
  - [ ] Best for conversation quality
  - [ ] Best cost-performance ratio
  - [ ] Best for low-latency requirements

#### Documentation & Recommendations
- [ ] Create `LLM_COMPARISON_REPORT.md` with:
  - [ ] Executive summary
  - [ ] Detailed metrics comparison
  - [ ] Cost analysis
  - [ ] Trade-off analysis
  - [ ] Recommendations by use case
- [ ] Document which LLM to use for production
- [ ] Provide migration plan if switching from gpt-4o-mini

**Success Criteria:**
- 3+ LLMs evaluated on both agents
- 10+ metrics compared per LLM
- Clear recommendation with supporting data
- Cost-performance trade-offs documented
- Production LLM selection justified

**Estimated Time:** 8-12 hours

---

## Future Enhancements (Backlog)

### Step 5: Production Monitoring (Optional)
- [ ] Integrate TruLens for production tracing
- [ ] Set up real-time monitoring dashboard
- [ ] Add alerting for low trustworthiness scores
- [ ] Track evaluation metrics over time
- [ ] A/B testing framework for prompt changes

### Relationship Extraction Evaluation
- [ ] Evaluate if relationship evaluation is needed
- [ ] Research DocRED or Re-TACRED dataset
- [ ] Extend DeepEval for relationship metrics
- [ ] Implement relationship extraction evaluation

### Advanced Features
- [ ] Multi-turn conversation evaluation
- [ ] Retrieval quality metrics (beyond context precision)
- [ ] Custom domain-specific metrics
- [ ] Human evaluation integration
- [ ] Automated prompt optimization based on metrics

---

## Summary: Evaluation Framework Stack

### Step 1: ✅ **Hugging Face Evaluate + seqeval**
- **Purpose:** Entity extraction evaluation
- **Status:** Complete (F1=0.576, 10 samples)
- **Time:** 2 hours

### Step 2: **DeepEval**
- **Purpose:** Conversation quality (Faithfulness, Answer Relevancy, Contextual Precision)
- **Status:** Planned
- **Time:** 4-6 hours

### Step 2.5: **Cleanlab TLM** (Optional)
- **Purpose:** Trustworthiness & hallucination detection
- **Status:** Planned
- **Time:** 1-2 hours

### Step 3: **RAGAS** (Supplement)
- **Purpose:** RAG-specific metrics (Context Recall, Entities Recall)
- **Status:** Planned
- **Time:** 2-3 hours (as part of Step 3)

### Step 4: **Multi-Framework LLM Comparison**
- **Purpose:** Compare 3+ LLMs across all metrics
- **Status:** Planned
- **Time:** 8-12 hours

### Step 5: **TruLens** (Optional)
- **Purpose:** Production monitoring & tracing
- **Status:** Future
- **Time:** 2-4 hours

**Total Estimated Time:** 18-28 hours across all steps
**Time Savings vs Manual:** 20-35 hours (~$2,000-$7,000 in engineering cost)

---
