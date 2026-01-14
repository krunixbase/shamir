type Field interface {
    Add(a, b Element) Element
    Sub(a, b Element) Element
    Mul(a, b Element) Element
    Div(a, b Element) Element
    Zero() Element
    One() Element
}
type Element interface{}

