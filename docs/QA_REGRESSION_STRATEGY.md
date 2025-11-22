# Regression Test Strategy
**Date:** 2025-11-22
**Author:** QC Agent
**Purpose:** Ensure fixes don't break existing functionality

---

## 1. Overview

### 1.1 Purpose

Regression testing ensures that:
- Bug fixes don't introduce new bugs
- New features don't break existing features
- Performance remains acceptable
- All 22 example rule files continue to work
- Backward compatibility is maintained

### 1.2 Scope

**In Scope:**
- All existing functionality in CreateApertiumRules.py
- All 22 example rule files in Rule Assistant directory
- Integration with Apertium pipeline
- FLEx database queries
- File I/O operations

**Out of Scope:**
- FLExTrans GUI (separate testing)
- STAMP module (separate testing)
- Apertium itself (upstream responsibility)

---

## 2. Test All 22 Example Rule Files

### 2.1 Example Files Inventory

Located in `/home/user/FLExTrans/Rule Assistant/`:

1. Ex1a_Def-Noun.xml
2. Ex1b_Def-Noun.xml
3. Ex1c_Indef-Noun.xml
4. Ex2_Adj-Noun.xml
5. Ex3_Adj-Noun.xml
6. Ex4a_Def-Adj-Noun.xml
7. Ex4b_Indef-Adj-Noun.xml
8. GermanEnglishDoubleDefault.xml
9. GermanEnglishDoubleDefaultOverwrite.xml
10. GermanSwedishDefToAffix.xml
11. PatternFeature.xml
12. SpanishFrenchRev2.xml
13. SplitBantu.xml
14. insert_word.xml
15. ranking.xml
16. unmarked_default.xml
17. EnglishGermanTripleRanking.xml
18. EnglishGermanTripleRankingPartialDefault.xml
19. Takwane-Meetto.xml (mentioned but may not be complete)
20-22. Additional files (check directory)

### 2.2 Regression Test Suite for Examples

**Test Template:**

```python
@pytest.mark.parametrize("example_file", [
    "Ex1a_Def-Noun.xml",
    "Ex1b_Def-Noun.xml",
    # ... all 22 files
])
def test_example_file_generates_valid_transfer(example_file, temp_workspace):
    """
    Verify each example file:
    1. Parses without errors
    2. Generates valid transfer file
    3. Transfer file compiles with Apertium
    4. Output matches baseline (if available)
    """
    example_path = os.path.join(RULE_ASSISTANT_DIR, example_file)
    output_path = os.path.join(temp_workspace, f'{example_file}.t1x')

    # Generate
    generator = create_generator()
    generator.ProcessAssistantFile(example_path)
    generator.WriteTransferFile(output_path)

    # Verify valid XML
    tree = ET.parse(output_path)
    assert tree.getroot().tag == 'transfer'

    # Verify compilable (if Apertium available)
    if shutil.which('apertium-preprocess-transfer'):
        compile_result = subprocess.run(
            ['apertium-preprocess-transfer', output_path, output_path + '.bin'],
            capture_output=True
        )
        assert compile_result.returncode == 0, f"Compilation failed: {compile_result.stderr}"

    # Compare with baseline (if available)
    baseline_path = os.path.join(BASELINE_DIR, f'{example_file}.t1x')
    if os.path.exists(baseline_path):
        assert_files_semantically_equivalent(output_path, baseline_path)
```

### 2.3 Creating Regression Baselines

**Process:**

1. **Establish Baseline:**
   ```bash
   # Before making any changes
   mkdir -p tests/baselines
   cd /home/user/FLExTrans
   python test_rule_assistant.py  # Run existing tests to verify clean state

   # Generate baseline outputs for each example
   python scripts/generate_baselines.py
   ```

2. **Baseline Storage:**
   - Store in `/home/user/FLExTrans/tests/baselines/`
   - Version control with git
   - Document baseline creation date and conditions

3. **Baseline Comparison:**
   - Compare generated output with baseline
   - Allow for acceptable differences (e.g., whitespace, comment order)
   - Flag semantic changes

**Baseline Comparison Script:**

```python
def assert_files_semantically_equivalent(output_file, baseline_file):
    """
    Compare two transfer files semantically, ignoring:
    - Whitespace differences
    - Comment order
    - Element order where order doesn't matter
    """
    tree1 = ET.parse(output_file)
    tree2 = ET.parse(baseline_file)

    # Normalize both trees
    normalize_transfer_tree(tree1)
    normalize_transfer_tree(tree2)

    # Compare
    diff = compare_trees(tree1, tree2)
    if diff:
        print(f"Differences found:\n{diff}")
        raise AssertionError("Files are not semantically equivalent")


def normalize_transfer_tree(tree):
    """Normalize tree for comparison."""
    # Sort children where order doesn't matter
    for parent in tree.iter():
        if parent.tag in ['section-def-cats', 'section-def-attrs', 'section-def-vars']:
            parent[:] = sorted(parent, key=lambda x: x.get('n', ''))

    # Remove comments (optional)
    for comment in tree.xpath('//comment()'):
        comment.getparent().remove(comment)

    # Normalize whitespace
    ET.indent(tree, space='  ')
```

---

## 3. Backward Compatibility

### 3.1 Version Compatibility Matrix

| FLExTrans Version | Transfer File Format | Rule Assistant XML | Compatibility Target |
|-------------------|----------------------|--------------------|----------------------|
| 3.14.4 (current) | Current | Current | 100% |
| 3.13.x | Legacy | Legacy | Read only |
| 3.12.x | Legacy | Legacy | Read only |

### 3.2 Backward Compatibility Tests

**Test Cases:**

```python
class TestBackwardCompatibility:
    """Ensure old files can still be read."""

    def test_load_v3_13_transfer_file(self):
        """Verify we can load transfer files from v3.13."""
        old_file = "tests/fixtures/legacy/v3.13_transfer.t1x"
        generator = create_generator()
        generator.ProcessExistingTransferFile(old_file)
        # Verify no errors
        assert not generator.report.has_errors()

    def test_load_v3_13_rule_assistant_xml(self):
        """Verify we can process old Rule Assistant XML."""
        old_rule = "tests/fixtures/legacy/v3.13_rule.xml"
        generator = create_generator()
        generator.ProcessAssistantFile(old_rule)
        # Verify successful processing
        assert not generator.report.has_errors()
```

### 3.3 Migration Testing

**If File Format Changes:**

```python
def test_auto_migration_from_old_format():
    """Test automatic migration of old format to new."""
    old_file = "tests/fixtures/old_format.t1x"
    new_file = "temp/migrated.t1x"

    # Load old
    generator = create_generator()
    generator.ProcessExistingTransferFile(old_file)

    # Save in new format
    generator.WriteTransferFile(new_file)

    # Verify migration successful
    tree = ET.parse(new_file)
    # Check for new format markers
    assert tree.find('.//new-element') is not None

    # Verify functionality preserved
    # ...
```

---

## 4. Performance Regression Tests

### 4.1 Performance Metrics

**Metrics to Track:**

1. **Rule Generation Time**
   - Time to process single rule
   - Time to process all 22 examples
   - Time for large ruleset (100+ rules)

2. **Transfer File Size**
   - File size for typical project
   - Macro deduplication effectiveness
   - Compression ratio

3. **Memory Usage**
   - Peak memory during generation
   - Memory for large projects

### 4.2 Performance Test Suite

```python
class TestPerformanceRegression:
    """Ensure performance doesn't degrade."""

    @pytest.mark.benchmark
    def test_single_rule_generation_time(self, benchmark):
        """Benchmark time to generate one rule."""
        def generate_rule():
            generator = create_generator()
            generator.ProcessAssistantFile("fixtures/simple_rule.xml")
            generator.WriteTransferFile("temp/bench.t1x")

        result = benchmark(generate_rule)
        # Should complete in under 1 second
        assert result < 1.0

    @pytest.mark.benchmark
    def test_all_examples_generation_time(self, benchmark):
        """Benchmark time to generate all 22 examples."""
        def generate_all():
            for example in ALL_EXAMPLE_FILES:
                generator = create_generator()
                generator.ProcessAssistantFile(example)
                generator.WriteTransferFile(f"temp/{example}.t1x")

        result = benchmark(generate_all)
        # Should complete in under 30 seconds
        assert result < 30.0

    def test_large_ruleset_performance(self):
        """Test with 100+ rules."""
        generator = create_generator()

        start = time.time()
        for i in range(100):
            generator.ProcessAssistantFile("fixtures/simple_rule.xml")
        elapsed = time.time() - start

        # Should handle 100 rules in under 60 seconds
        assert elapsed < 60.0

    def test_memory_usage_acceptable(self):
        """Ensure memory usage doesn't explode."""
        import tracemalloc

        tracemalloc.start()

        generator = create_generator()
        for i in range(50):
            generator.ProcessAssistantFile("fixtures/simple_rule.xml")

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak memory should be under 100 MB for 50 rules
        assert peak < 100 * 1024 * 1024
```

### 4.3 Performance Baselines

**Establish Baselines:**

```bash
# Run performance suite and capture metrics
pytest tests/test_performance.py --benchmark-only --benchmark-json=baselines/perf_baseline.json

# Store baseline
git add baselines/perf_baseline.json
git commit -m "Establish performance baseline"
```

**Compare Against Baseline:**

```python
def compare_with_baseline(current_metrics, baseline_file):
    """Compare current performance with baseline."""
    with open(baseline_file) as f:
        baseline = json.load(f)

    for metric_name, current_value in current_metrics.items():
        baseline_value = baseline[metric_name]
        degradation = (current_value - baseline_value) / baseline_value * 100

        if degradation > 10:  # More than 10% slower
            warnings.warn(f"{metric_name} degraded by {degradation:.1f}%")
```

---

## 5. Test Execution Strategy

### 5.1 Test Levels

**Level 1: Smoke Tests (Fast - Run on Every Commit)**
- Basic functionality
- Critical paths
- Example file parsing
- Run time: < 2 minutes

**Level 2: Integration Tests (Medium - Run on PR)**
- All integration tests
- File I/O workflows
- 5-10 example files
- Run time: < 10 minutes

**Level 3: Full Regression (Slow - Run Nightly)**
- All 22 example files
- Performance tests
- Stress tests
- Run time: < 30 minutes

### 5.2 Continuous Integration Pipeline

```yaml
# .github/workflows/regression.yml
name: Regression Tests

on: [push, pull_request]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
      - name: Run smoke tests
        run: |
          pytest tests/ -m smoke --cov=Dev/Lib

  full-regression:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov pytest-benchmark
      - name: Run full regression
        run: |
          pytest tests/ --cov=Dev/Lib --benchmark-skip
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### 5.3 Test Markers

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: quick smoke tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "regression: full regression tests")
    config.addinivalue_line("markers", "benchmark: performance benchmarks")
```

---

## 6. Regression Test Checklist

### 6.1 Pre-Implementation Checklist

Before implementing FR fixes:

- [ ] All existing tests pass
- [ ] Performance baseline established
- [ ] All 22 examples compile successfully
- [ ] Baseline outputs captured
- [ ] Git branch created from clean state

### 6.2 During Implementation Checklist

- [ ] Run smoke tests after each significant change
- [ ] Monitor for new warnings
- [ ] Check code coverage remains >80%
- [ ] Review diff of generated transfer files

### 6.3 Pre-Merge Checklist

- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] All 22 example files work
- [ ] No performance degradation >10%
- [ ] Baseline comparison shows only expected changes
- [ ] Code coverage target met
- [ ] Manual testing completed (see QC_VALIDATION_CHECKLIST.md)

---

## 7. Dealing with Test Failures

### 7.1 Failure Investigation Process

**When a Regression Test Fails:**

1. **Identify the Failure:**
   - Which test failed?
   - What was the error message?
   - Is it repeatable?

2. **Classify the Failure:**
   - **True Regression:** New bug introduced
   - **Test Issue:** Test needs updating
   - **Expected Change:** Intentional behavior change

3. **Root Cause Analysis:**
   - Review recent code changes
   - Check git blame for relevant code
   - Examine test logs and stack traces

4. **Resolution:**
   - **If True Regression:** Fix the bug
   - **If Test Issue:** Update test
   - **If Expected Change:** Update baseline and document

### 7.2 Test Maintenance

**When to Update Tests:**
- Behavior intentionally changes (document why)
- Test was incorrect (validate fix first)
- Test is flaky (fix flakiness, don't just skip)

**When to Update Baselines:**
- Format change (non-semantic)
- Optimization (same output, different structure)
- Feature addition (new elements expected)

**Never:**
- Skip failing tests without investigation
- Update baselines without understanding changes
- Ignore performance degradation

---

## 8. Regression Test Metrics

### 8.1 Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test Pass Rate | 100% | TBD | ⏳ |
| Code Coverage | >80% | ~50% | 🔴 |
| Example Files Working | 22/22 | TBD | ⏳ |
| Performance Degradation | <10% | N/A | ⏳ |
| Test Execution Time | <30 min | TBD | ⏳ |

### 8.2 Tracking Over Time

```python
# Store metrics in JSON for trending
{
    "date": "2025-11-22",
    "commit": "abc123",
    "metrics": {
        "tests_passed": 45,
        "tests_failed": 0,
        "coverage_percent": 82.5,
        "examples_working": 22,
        "avg_rule_time_ms": 150,
        "total_suite_time_s": 180
    }
}
```

---

## 9. Documentation

### 9.1 Regression Test Documentation

Each regression test should document:

- **Purpose:** What is being tested
- **Expected Behavior:** What should happen
- **Baseline:** Reference to baseline data
- **Change History:** When/why baseline changed

### 9.2 Example Documentation Template

```python
def test_example_def_noun():
    """
    Regression test for Ex1a_Def-Noun.xml

    Purpose:
        Verify basic determiner-noun rule generation continues to work

    Expected Behavior:
        - Generates valid transfer file
        - Compiles with Apertium
        - Output matches baseline (allowing for whitespace diffs)

    Baseline:
        tests/baselines/Ex1a_Def-Noun.xml.t1x
        Created: 2025-11-22
        Last Updated: 2025-11-22 (initial creation)

    Change History:
        - 2025-11-22: Initial baseline established
    """
    # Test implementation
```

---

## 10. Success Criteria

### 10.1 Regression Testing Complete When:

- ✅ All 22 example files have regression tests
- ✅ Performance baselines established
- ✅ Backward compatibility tests in place
- ✅ CI pipeline running regression tests
- ✅ Baseline outputs stored and version controlled
- ✅ Test documentation complete
- ✅ Test pass rate 100%

### 10.2 Ongoing Success Criteria:

- ✅ Zero regression test failures on main branch
- ✅ Performance within 10% of baseline
- ✅ All new features have regression tests
- ✅ Test suite completes in <30 minutes
- ✅ Code coverage >80% maintained

---

## Appendix A: All 22 Example Files Test Suite

```python
# tests/test_all_examples.py

import pytest
import os

EXAMPLE_FILES = [
    "Ex1a_Def-Noun.xml",
    "Ex1b_Def-Noun.xml",
    "Ex1c_Indef-Noun.xml",
    "Ex2_Adj-Noun.xml",
    "Ex3_Adj-Noun.xml",
    "Ex4a_Def-Adj-Noun.xml",
    "Ex4b_Indef-Adj-Noun.xml",
    "GermanEnglishDoubleDefault.xml",
    "GermanEnglishDoubleDefaultOverwrite.xml",
    "GermanSwedishDefToAffix.xml",
    "PatternFeature.xml",
    "SpanishFrenchRev2.xml",
    "SplitBantu.xml",
    "insert_word.xml",
    "ranking.xml",
    "unmarked_default.xml",
    "EnglishGermanTripleRanking.xml",
    "EnglishGermanTripleRankingPartialDefault.xml",
    # Add any additional example files
]

@pytest.mark.regression
@pytest.mark.parametrize("example_file", EXAMPLE_FILES)
def test_example_file_regression(example_file, temp_workspace):
    """Regression test for each example file."""
    # Implementation as shown above
    pass
```

---

**Document Status:** Complete
**Next Action:** Set up test fixtures and baselines
**Owner:** QC Agent
