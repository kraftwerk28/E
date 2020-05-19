# E-lang

### This language highly inspired by Haskell and Lisp
### WIP: the parser still doesn't fully support syntax from code above

### Code example:

```
-{ This is a
   multiline
   comment
 }-

-{ Const variable }-
a <- 42

-{ Let variable }-
b <~ minus a 33

-{ [Pure] function declaration }-
fact :: n ->
  ?: n < 2 | n
  :? mul n (fact (pred n))

-{ Printing to stdout }-
out (fact 10)
```
