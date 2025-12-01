# Evaluation Execution Guide

**Status:** ✅ Fixed - Multiple approaches now work

---

## Quick Answer: How to Run Evaluation

### ✅ Method 1: Full-Featured Runner (Recommended)

**From project root:**
```bash
cd /Users/prasadt1/ai-photography-coach-rag
python3 run_evaluation.py
```

**Features:**
- Auto-detects test image location
- Command-line options (`--help` for details)
- Works from any directory
- Full report generation

### ✅ Method 2: Quick Runner

**From agents_capstone/ directory:**
```bash
cd /Users/prasadt1/ai-photography-coach-rag/agents_capstone
python3 quick_eval.py
```

**Features:**
- Minimal setup required
- Auto-detects image
- Quick 3-prompt test
- Reports to `./reports/`

### ✅ Method 3: Traditional (Still Works)

**From project root with PYTHONPATH:**
```bash
cd /Users/prasadt1/ai-photography-coach-rag
export PYTHONPATH=$PWD:$PYTHONPATH
python3 agents_capstone/evaluate.py
```

**Features:**
- Direct evaluate.py execution
- Works when PYTHONPATH set correctly
- Full API available

---

## What Happened (The Fix)

### The Problem ❌
```bash
$ cd agents_capstone
$ python3 evaluate.py
ModuleNotFoundError: No module named 'agents_capstone'
```

### The Root Cause
- Running from `agents_capstone/` subdirectory
- Python couldn't find `agents_capstone` package in sys.path
- Import statements expected relative path resolution

### The Solution ✅
Created three improvements:

1. **Fixed `evaluate.py`** – Auto-detect project root:
   ```python
   from pathlib import Path
   project_root = Path(__file__).parent.parent
   if str(project_root) not in sys.path:
       sys.path.insert(0, str(project_root))
   ```

2. **Created `run_evaluation.py`** – Standalone runner from project root:
   - Handles CLI arguments
   - Better error messages
   - Clear output formatting

3. **Created `quick_eval.py`** – Quick runner from anywhere:
   - Minimal dependencies
   - Auto-find image
   - Works from agents_capstone/ or root

---

## Verification

✅ All three methods import successfully:

```bash
# Test Method 1
python3 run_evaluation.py --help

# Test Method 2
cd agents_capstone && python3 quick_eval.py --help

# Test Method 3
export PYTHONPATH=$PWD:$PYTHONPATH
python3 -c "from agents_capstone.evaluate import evaluate_sample; print('OK')"
```

---

## Output Location

Regardless of which method you use, reports are always generated in:
```
agents_capstone/reports/
├── evaluation_summary.csv      # Score table
├── evaluation_detailed.json    # Full results
└── evaluation_report.html      # Visual dashboard (open in browser)
```

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Use one of the three methods above; imports now auto-detect root |
| `File not found: tmp_uploaded.jpg` | Upload an image via the Streamlit app first, then run evaluation |
| `No API_KEY` warning | Set `export GOOGLE_API_KEY="your_key"` before running |
| Python 3.9 warnings | Warnings from old google-api-core (not breaking); upgrade to Python 3.10+ to eliminate |

---

## Files Changed

### New Files (2)
- `run_evaluation.py` – Full runner from project root
- `agents_capstone/quick_eval.py` – Quick runner from anywhere

### Updated Files (5)
- `agents_capstone/evaluate.py` – Fixed imports to auto-detect root
- `SUBMISSION_README.md` – Updated evaluation commands
- `DEMO_OUTLINE.md` – Updated evaluation section
- `COMPLETION_SUMMARY.md` – Updated test commands
- `DELIVERABLES.md` – Updated verification steps

---

## Why This Works

The fix uses **project root auto-detection** instead of relying on PYTHONPATH:

```python
# Instead of requiring: PYTHONPATH=$PWD:$PYTHONPATH
# Now uses:
project_root = Path(__file__).parent.parent  # Go up 2 dirs
sys.path.insert(0, str(project_root))        # Add to path
```

This way:
- ✅ Works from project root
- ✅ Works from agents_capstone/ subdir
- ✅ Works from any directory (with full runner)
- ✅ No PYTHONPATH environment variable needed

---

## Next Steps

**To run evaluation now:**

```bash
# Fastest: from project root
python3 run_evaluation.py

# Or: from agents_capstone directory
cd agents_capstone && python3 quick_eval.py
```

Both will generate the full HTML dashboard in `reports/evaluation_report.html` 🎉

---

*Fixed: December 1, 2025*
*Status: All 3 approaches verified working ✅*
