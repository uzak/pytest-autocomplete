# pytest-zsh / autocomplete

This provides a script for fast(er) pytest testnames autocomplete. For how to install and use, see: https://stackoverflow.com/a/54048138

Then use in `.zsh-completions/_pytest` as follows:

```
#compdef pytest

_pytest_complete() {
    local curcontext="$curcontext" state line
    typeset -A opt_args
    compadd "$@" $( python ~/repos/pytest-zsh/autocomplete.py )
}

_pytest_complete "$@"

```
