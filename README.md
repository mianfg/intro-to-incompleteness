# Intro to incompleteness — companion code

Python programs for the blog series [**Intro to incompleteness**](https://mianfg.me/en/blog/s/intro-to-incompleteness) and the EuroPython talk [*Hacking Truth: Python and the Limits of Mathematics*](https://www.youtube.com/watch?v=oWsqoKkP_sw).

Each listing in the series links here. The programs implement the reductions, simulators, and self-referential scripts used to prove Gödel's First Incompleteness Theorem from a computational perspective.

## Layout

| Path | Role |
| --- | --- |
| [`turing.py`](turing.py) | `Turing` class used by the simulator |
| [`simulate_turing.py`](simulate_turing.py) | Run a `.mt` machine encoding on an input string |
| [`turing_machines/`](turing_machines/) | Example machine encodings (`.mt` files) |
| [`utilities.py`](utilities.py) | Shared helpers (`read`, `write`, encodings, …) |
| [`disk/`](disk/) | Runtime scratch files for programs that store code on “disk” |
| [`godel_peano.py`](godel_peano.py) | Peano-arithmetic incompleteness via a self-referential program |
| [`binary_addition.py`](binary_addition.py) | Toy logical systems (`is_theorem`, `is_true`) |
| … | See filenames for the rest of the reductions and decision problems |

## Quick start

From this directory:

```bash
python
```

```python
from utilities import read
from simulate_turing import simulate_turing_mult

encoding = read('./turing_machines/more_as_than_b.mt')
simulate_turing_mult(encoding, 'abbaa')
```

Or open any linked `.py` file from the blog and run it in context (some programs depend on others or on files under `disk/`).

## Runnable?

| Symbol | Meaning |
| --- | --- |
| ✅ | Runs in CPython as-is |
| ❌ | Depends on oracles / non-halting subprograms (still valid Python) |
| ⭕️ | Not implemented in this repository |

Most files marked ❌ in the thesis are **intentionally** non-executable: they import `is_theorem_peano`, `halting_to_peano`, etc., which would solve undecidable problems if they always halted.

## License

MIT — see [LICENSE](LICENSE).

## Related

- Blog series (EN): https://mianfg.me/en/blog/s/intro-to-incompleteness  
- Blog series (ES): https://mianfg.me/es/blog/s/intro-to-incompleteness  
- Full thesis: https://mianfg.me/en/projects/incompleteness
