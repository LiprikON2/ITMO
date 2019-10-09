function workon() {
  if test -z "$1" ; then
    echo "Specify the name of the virtual environment"
  elif test ! -f "$HOME/.virtualenvs/$1/bin/activate" ; then
    echo "Environment doesn't exists"
  else
    deactivate 2> /dev/null
    source "$HOME/.virtualenvs/$1/bin/activate"
  fi
}
