# Elang

### Highly inspired by Haskell and Lisp

### TODO:
- [ ] rewrite everything in Rust
- [ ] infix expressions + shunting yard (maybe need special syntax?)
- [ ] semantic analysis

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

### Grammar:

```
<program> ::= <expr> { <expr> }
<expr> ::= <atom>
         | <if> <expr> <then> <expr> { <then> <expr } { <else> <expr> }
         | <list>
         | <const-ass>
         | <let-ass>
         | <func>
         | <lb> <expr> <rb>

<if> ::= "?:"
<elif> ::= "?"
<then> ::= "|"
<else> ::= ":?"

<comment-start> ::= "-{"
<comment-end> ::= "}-"
<comment> ::= "--"

<lb> ::= "("
<rb> ::= ")"
<sqbr> ::= "["
<sqbl> ::= "]"
<func-arrow> ::= "->"
<func-decl> ::= "::"
<const-ass> ::= <id> "<-" <expr>
<let-ass> ::= <id> "<~" <expr>

<list> ::= <sqbl> <expr> { , <expr> } <sqbr>
<id> ::= <letter>

<atom> ::= <integer> | <float> | <string>
<integer> ::= <digit> | <digit><integer>
<float> ::= <integer> | <integer>"."<integer>
<string> ::= """ <letter>, { <letter> } """

<id> ::= <letter>
<operator> ::= "+" | "-" | "*" | "/" | "//"
<letter> ::= "a" | "b" | ... | "z"
<digit> ::= "0" | "1" | ... | "9"
```
