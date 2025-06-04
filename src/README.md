A piecewise-based mechanism is instantiated by:
* domain: from `endpoint_a` to `endpoint_b`
* endpoints of each piece: (list) `l` and `r`
* probability of each piece: (list) `p` 
* privacy parameter: `epsilon`
* number of pieces: `total_piece`

File `min_error_mechanism.py` contains the classes for solving the optimal piecewise-based mechanisms under different distance metrics.

File `distance_metric.py` contains the methods for calculating different distances.

File `closed_form_mechanism.py` contains the closed-form expressions of the optimal piecewise mechanism under the absolute error (maybe also optimal for other metrics).

File `PM.py` and `SW.py` contains the PM and SW mechanisms and their variants.
