## Project Overview

**LabIFSC2** is a Python library for physics laboratory calculations, used by undergraduates at IFSC (Instituto de Física de São Carlos — USP). It provides **automatic uncertainty propagation via Monte Carlo simulation** and **unit conversion** powered by [pint](https://pint.readthedocs.io/). It is a complete modernization of the original [LabIFSC](https://github.com/gjvnq/LabIFSC) library.

- **Language**: Python ≥ 3.11 (tested on 3.11, 3.12, 3.13, 3.14)
- **License**: GPL-3.0
- **Package Manager / Build System**: [Poetry](https://python-poetry.org/) with `poetry-core` masonry backend
- **Task Runner**: [Poe the Poet](https://github.com/nat-n/poethepoet) (`poethepoet`)
- **Documentation**: [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- **Human Language**: Brazilian Portuguese — documentation, docstrings, variable names, and error messages are all in Portuguese

## Conventions
- Always provide type hints for functions, trying to constrain the type as minimal as possible, trying to use protocols and interfaces whenever it's possible.
- Whenever a function it's better being thought as broken down by multiple overloaded functions, use the @overload decorator and provide type hints for each overload.
- Always prefer to thrown an error instead of returning `None` or `False`.
- Follow the PEP8 style guide.
- Use Google-style docstrings with `Args`, `Returns`, and `Raises` sections, written in Portuguese
- Whenever a bug it's found, the bug should be corrected and a unit test should be added that would otherwise trigger that bug, so we don't have regressions.
- Avoid to break encapsulation of classes/methods/modules and so on.
- Don't add unnecessary comments, code in 99% of the cases should be self explanatory be choosing good variables/function names, and following good coding practices. Use comments only for very complicated or non-obvious code.

## Performance Considerations

- Always do histogram calculations lazyly and prefer analytical results than to simulate the histograms, use vectorized numpy operations whenever possible

## Architecture 

### Core Abstraction: `Medida`

The `Medida` class is the central type of the library. It represents a physical measurement with:
- A **nominal value** stored as `pint.Quantity` (with units, auto-reduced)
- An **uncertainty** stored as `pint.Quantity`
- A lazily-generated **Monte Carlo histogram** (`numpy` array × `pint` units)

### Monte Carlo Uncertainty Propagation

LabIFSC2 uses **Monte Carlo sampling** (default: 100,000 samples) for uncertainty propagation. 
The `montecarlo()` function is the propagation engine: it samples histograms from input `Medida` objects, applies the given function, and returns a new `Medida` with the mean and std of the result.

### NumPy Interoperability

`Medida` should work interoperably with NumPy functions and NumPy arrays,
`Medida.__getattr__` intercepts calls like `np.sin(medida)` and routes them through Monte Carlo propagation. Supported functions: `sin`, `cos`, `tan`, `exp`, `sqrt`, `log`, `log2`, `log10`, hyperbolic functions, inverse trig, `cbrt`, `power`.

### Physical Constants

`constantes.py` is **auto-generated** from CODATA 2022 data by `scripts/gerar_codata_constantes.py`. Do **not** edit this file manually — regenerate it by running the script. Additionally includes mathematical constants (`pi`, `euler`, `golden_ratio`) and astronomical constants.

## Development Setup

### Prerequisites

- Python ≥ 3.11
- [Poetry](https://python-poetry.org/) (v2.1.4+)
- [poethepoet](https://github.com/nat-n/poethepoet) plugin for Poetry

### Installation

```bash
# Clone the repository
git clone https://github.com/viniciusdutra314/LabIFSC2.git
cd LabIFSC2

# Install all dependencies (including test and linter groups)
poetry install --no-root

# Ensure poethepoet is available
poetry self add poethepoet@0.37
```

### Task Commands

All tasks are defined in `pyproject.toml` under `[tool.poe.tasks]`:

| Command                    | Description                                       |
| -------------------------- | ------------------------------------------------- |
| `poetry poe tests`         | Run mypy type checking + pytest (full suite)      |
| `poetry poe type-checking` | Run mypy on `LabIFSC2/`                           |
| `poetry poe unit-tests`    | Run pytest with verbose output (`-vv -x -s`)      |
| `poetry poe test-coverage` | Run pytest with branch coverage report (HTML)      |
| `poetry poe docs`          | Serve documentation locally via `mkdocs serve`    |

### DevContainer

A `.devcontainer/` configuration is provided for VS Code, based on Debian with Python 3.11 and Poetry pre-installed.

## Important Gotchas

1. **Stochastic results**: Monte Carlo propagation produces slightly different results each run. Always use tolerances in assertions, never exact equality for propagated values
