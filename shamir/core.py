import random

PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481


def _eval_polynomial(coefficients, x, prime):
    result = 0
    for power, coefficient in enumerate(coefficients):
        result = (result + coefficient * pow(x, power, prime)) % prime
    return result


def split_secret(secret, threshold, shares_count, prime=PRIME):
    if threshold < 2:
        raise ValueError("Threshold must be at least 2")
    if threshold > shares_count:
        raise ValueError("Threshold cannot exceed number of shares")
    if not 0 <= secret < prime:
        raise ValueError("Secret must be within finite field range")

    coefficients = [secret] + [
        random.randrange(0, prime) for _ in range(threshold - 1)
    ]

    shares = []
    for x in range(1, shares_count + 1):
        y = _eval_polynomial(coefficients, x, prime)
        shares.append((x, y))

    return shares


def _lagrange_interpolate(x, x_values, y_values, prime):
    total = 0
    k = len(x_values)

    for i in range(k):
        xi, yi = x_values[i], y_values[i]
        term = yi
        for j in range(k):
            if i != j:
                xj = x_values[j]
                term *= (x - xj) * pow(xi - xj, -1, prime)
                term %= prime
        total += term

    return total % prime


def reconstruct_secret(shares, prime=PRIME):
    if len(shares) < 2:
        raise ValueError("At least two shares are required")

    x_values, y_values = zip(*shares)
    return _lagrange_interpolate(0, x_values, y_values, prime)

