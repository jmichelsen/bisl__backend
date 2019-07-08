# Programming Best Practices

This guide is a list of things you can do to become a not only a better programmer, but to become a better programmer on a team.  When multiple people are contributing to the same code base there is a level of discipline required to make sure it's clean and consistent.

Below are several things to keep in mind when designing and implementing your code. 

## The Zen of Python, by Tim Peters

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one - and preferably only one - obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than *right* now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea - let's do more of those!

## Should This Be Tested?

- Data Collection (**Yes**)
    - *Views*/APIs (**get** and **post** methods and Django class-based views excluded)
    - *Forms* (**customized validation**, any customizations to Django base forms)
- 3rd Party Tools (**No**)
    - Django ORM
    - Python Library
- Algorithm (**Yes**)
- Data Manipulation (**Yes**)

## Should This Be Mocked?

- Non-local Implementations (**Yes**)
    - Communicating with 3rd party systems
    
## Package vs. Module

- One-Among-Many (**Package**)
    - API Handlers
    - Parsers
- One-Of-A-Kind (**Module**)
    - Specific API Handler
    - Specific Parser
    
## Functions/Methods

- Completes a single unit task
- No more than 15 lines of functional code
- Should be testable (even if it does not require a test)
- Name should be meaningful
- Underscore prepend for protected (*def _a_protected_method()*)
- Dunder (double-underscore, ie "__") prepend for private (name mangling occurs)

## Other Best Practices

- Follow PEP8 (with a few exceptions)
- Line Length = 100 characters
- A method should return a single type
    
```
def bad_example(foo, bar):
    if foo:
        return bar
    
    if not bar:
        return False
    
```

- Prefer *list comprehension* to *for* loops. (Python is optimized for them)
- Embedded loops and/or *if* statements should make you reconsider your design
- Be careful stacking *if*/*else* statements as a use for *case* statements (Python does not have *case*)
- If you are building something in a *Form* or *View* that needs testing, you are probably doing something wrong.  (Refactor into a utility method and test it.)
