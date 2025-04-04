# Order Processing System

A Python-based order processing system that handles different types of orders (A, B, C) with various processing requirements and error handling capabilities.

## Project Structure

```
.
├── exam.py                 # Main implementation file
├── test_order_processing.py # Test suite
├── CHECKLIST.md           # Test case checklist
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Test Coverage

The project has achieved 100% test coverage as shown in the coverage report:

```
---------- coverage: platform darwin, python 3.12.3-final-0 ----------
Name      Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------
exam.py      97      0     18      0   100%
-----------------------------------------------------
TOTAL        97      0     18      0   100%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml


==================================== 54 passed in 0.22s =====================================
```

## Getting Started

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run tests: `pytest`
5. Generate coverage report: `pytest --cov=exam --cov-report=term-missing`

## Requirements

- Python 3.x
- pytest
- pytest-cov

## Documentation

- [Test Checklist](CHECKLIST.md) - Detailed test case documentation

