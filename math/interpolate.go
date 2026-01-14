package math

func InterpolateAt(
    field Field,
    xs []Element,
    ys []Element,
    at Element,
) Element

func InterpolateAt(field Field, xs, ys []Element, at Element) Element {
    result := field.Zero()

    for i := 0; i < len(xs); i++ {
        term := ys[i]

        for j := 0; j < len(xs); j++ {
            if i == j {
                continue
            }

            numerator := field.Sub(at, xs[j])
            denominator := field.Sub(xs[i], xs[j])
            term = field.Mul(term, field.Div(numerator, denominator))
        }

        result = field.Add(result, term)
    }

    return result
}
