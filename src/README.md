A piecewise mechanism is instantiated by:
* domain: from endpoint_a to endpoint_b
* l: (list) endpoints of pieces
* p: (list) probability list of pieces
* epsilon: privacy budget
* total piece: number of pieces

File `min_error_mechanism` contains the class of solving the optimal piecewise mechanism under different distance metrics.

File `distance_metric` contains the methods of calculating different distance.

File `closed_form_mechanism` contains the closed-form solution of the optimal piecewise mechanism under absolute error (maybe also optimal for other metrics).
