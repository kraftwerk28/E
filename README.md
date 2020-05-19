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

### Language grammar

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
