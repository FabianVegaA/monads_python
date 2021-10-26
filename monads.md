# Qué es un Monad

## Y sus aplicaciones en Python

Últimamente he estudiado el concepto de **Monad** y sus aplicaciones, y ciertamente es una herramienta tan poderosa como difícil de comprender en un principio.
Proviene de las matemáticas, en particular [Category theory](https://en.wikipedia.org/wiki/Category_theory) lo define como:

> A monad (also triple, triad, standard construction and fundamental construction) is an [endofunctor](https://en.wikipedia.org/wiki/Endofunctor) (a functor mapping a category to itself), together with two natural transformations required to fulfill certain coherence conditions.

Pero esta definición puede ser difícil de comprender, por ello lo veremos como una herramienta de la programación funcional. Este paradigma lo define como una abstracción que nos permite la [programación genérica](https://en.wikipedia.org/wiki/Generic_programming), que a grandes razgos es un estilo de programación que permite escribir con tipos que serán especificados más tarde. Un lenguaje que permite esto es Haskell. Por ejemplo:

```haskell
length :: [a] -> Int
length [] = 0
length (_:xs) = 1 + length xs
```

En este caso `length` recibe una lista que dentro posee valores de tipo `a` y devuelve un entero.

Tal como se define en un principio en la teoria de las categorias, un **Monad** se crea con dos operaciones:

- **unit** o **return**, pero para no confundirnos le llamaremos **unit**. Esta operación toma un valor `a` lo envuelve en un _monadic_, obteniendo un valor _monadic_ `m a`.
- **bind** o **>>=**, esta operación recibe un valor _monadic_ `m a` y una función `f`, aplicando `f` a `m a` y devolviendo el resultado.

El poder de esta estructura, es que permite componer una secuencia de funciones (un "pipeline") usando el operador **bind**.



Un ejemplo común es _Maybe_, usualmente usado en **Haskell**, este se define como:

```haskell
data Maybe T  =  Just T | Nothing
```

_Maybe_ es un **Monad** que envuelve un tipo de dato genérico, de modo que puede entregar un `Just T`, donde `T` es el tipo genérico o `Nothing` si no se puede entregar nada. Un ejemplo en Haskell:

```haskell
intergerDiv :: Int -> Int -> Maybe Int
IntergerDiv x 0 = Nothing
IntergerDiv x y = Just (x `div` y)
```

En este ejemplo, si `intergerDiv` recibe un valor `x` cualquiera y un 0, devuelve `Nothing`, de lo contrario devuelve un `Just` con el resultado de la división.

### Maybe en Python

Si bien **Haskell** es un lenguaje poderosísimo, elegante y uno de mis lenguajes preferidos, es un lenguaje muy poco conocido a comparación de **Python**. Por ello te mostraré cómo implementar esta clase de estructuras en **Python**.

Para ello utilizaremos paradogicamente **OOP**, dado que a pesar de que **Python** sea un lenguaje multiparadigma, está mucho más inclinado a este paradigma.

Ahora bien, implementaremos la clase **Maybe**, utilizando el decorador `dataclass` con el parámetro `frozen=true`, de este modo las instancias de esta clase no serán modificables, dado que no queremos **side-effects** en nuestro programa puramente funcional :wink:.

```python
T = TypeVar("T", covariant=True)

@dataclass(frozen=True)
class Maybe(Generic[T]):
    ...
```

**Maybe** hereda de `Generic`, que recibe `T`, esto nos permitirá que nuestro **Monad** pueda envolver un tipo genérico.

Además de eso, esta clase implementa el método `bind`, así como definimos en un principio a los **Monads**, en el caso de `unit` este queda cubierto por el constructor de la clase (`__init__`).

```python
@dataclass(frozen=True)
class Maybe(Generic[T]):
    def bind(self, f):
        if isinstance(self, Nothing):
            return Nothing()

        try:
            x = f(self.get())
            return Just(x)
        except:
            return Nothing()

    def __rshift__(self, f):
        return self.bind(f)
```

`__rshift__` es un _magic method_, estos métodos nos permite darle ciertos comportamientos a una clase con un operador dado, en este caso _rigth shift_ (`>>`), si recuerdas `bind` se representa con el operador `>>=` y en Python el operador más parecido es este.

Además de **Maybe**, también implementaremos las clases **Just** y **Nothing**.

```python
@dataclass(frozen=True)
class Just(Maybe):
    value: T

    def get(self):
        return self.value

    def __repr__(self):
        x = self.get()
        return "Just {}".format(str(x) if type(x) is not str else f'"{x}"')
```

**Just** es una clase que hereda de **Maybe** y también usa `@dataclass(frozen=True)`. del mismo modo **Nothing**.

```python
@dataclass(frozen=True)
class Nothing(Maybe):

    def get(self):
        return None

    def __repr__(self):
        return "Nothing"
```

Con esto puedes construir un pipeline, donde está será serie de composiciones de funciones, por ejemplo:

```python
x = Just("1")

y = (
    x
    >> int                        # Transforma a int
    >> (lambda x: -x)             # Obtiene el negativo
    >> (lambda x: x + 3)          # Suma 3
    >> (lambda x: x ** 2)         # Eleva a la potencia de 2
    >> (lambda x: list(range(x))) # Crea una lista desde el 0 a x
)
```

Se obtiene que `y` vale:

```
Just [0, 1, 2, 3]
```

Y si introducimos un error a propósito:

```python
x = Just("1")

y = (
    x
    >> int                                # Transforma a int
    >> (lambda x: -x)                     # Obtiene el negativo
    >> (lambda x: x / 0)                  # Divide entre 0
    >> (lambda x: x + "This is an Error") # Se suma con un str
)
```

Esta vez se obtiene:

```
Nothing
```

Esto permite que nuestro programa no falle, además es posible obtener más información almacenando los errores o lanzando una alerta cada vez que `brind` retorne `Nothing`.

**Maybe** no es el único **Monad** que se puede implementar para obtener todo el poder de la programación funcional. Si tienes preguntas no dudes en dejarlas en comentarios.

Además te dejo el repositorio de GitHub del código.
