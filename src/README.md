A piecewise-based mechanism is instantiated by:
* domain: from endpoint_a to endpoint_b
* l, r: (list) endpoints of each piece
* p: (list) probability of each piece
* epsilon: privacy parameter
* total piece: number of pieces

File `min_error_mechanism` contains the classes for solving the optimal piecewise-based mechanisms under different distance metrics.

File `distance_metric` contains the methods for calculating different distances.

File `closed_form_mechanism` contains the closed-form expressions of the optimal piecewise mechanism under the absolute error (maybe also optimal for other metrics).
