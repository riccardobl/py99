# Py99
This script aims to fix python by allowing to use a C-like syntax.

In this way you can write code faster, without caring about indentation and leave to your ide the task to fix it. And it's also prettier, if you ask me.

The generated code is plain python, thus it can be used with everything that runs normal python and the python police will never know.

There is nothing fancy going on here, just a bunch of hackish regexes runned across the code, so it may fail with some python structures that i'm not aware of and potentialy with everything, but we are optimistic, aren't we?


##  C-like syntax?
With that i mean:

- no enforced indentation
- semi-colon as line separator
- code blocks between { }
- round parenthesis where they should be  (i.e `for( x in range(0,10)){ }` instead of `for x in range(0,10):` )
- Some other stuff, see the list below.

For the rest it stays normal python. 


### Translations list
`&&` -> `and`

`||` -> `or`

`!abc` -> `not abc`

`class A{ }` -> `class A:`

`class A( ){ }` -> `class A( ):`

`def B( ){ }`->`def B( ):`

`for(a in range(0,9)){ }` -> `for a in range(0,9):`

`true` -> `True`

`false` -> `False`

`null` -> `None`

For examples, see the tests/ folder.


## Usage
1. Write your script in py99
2. Convert it in plain python with `python3 py99.py in_script.py99 out_script.py` 
3. Use the converted script where you want. It's normal python.
