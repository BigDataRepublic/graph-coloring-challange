# Graph Coloring Challenge!

## Instuctions

Install a Simulated Annealing Scheme Package

```
pip install frigidum
```

Run the code
```
python gcp.py
```

Try improve the solution! Try use as less colors as possible;

1. Change the Temperature / Repeats ?
2. Change the proposals ?
3. Change the objective function ?


## SA

```
import frigidum

from frigidum.examples import rastrigin

frigidum.sa(random_start=rastrigin.random_start,
           objective_function=rastrigin.rastrigin_function,
           neighbours=[rastrigin.random_small_step],
           copy_state=frigidum.annealing.naked,
           T_start=1,
           T_stop=0.000001,
           repeats=10**4)
```