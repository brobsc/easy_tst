# easy_tst

easy_tst is a set of scripts that makes the use of tst easier (see [daltonserey/tst](https://github.com/daltonserey/tst) for more information).


## Dependencies

Before installing easy_tst you will need: 

1. [Python 2.7](https://www.python.org/downloads/release/python-2715/)
2. [tst](https://github.com/daltonserey/tst)
3. [pip](https://pip.pypa.io/en/stable/installing/)


## Installing

```sh
pip install easy_tst
```

## Modes

### Watcher
This mode will automatically do the checkout with what is in your clipboard, organize the directory created by moving it to a padronized tst directory (exercicios_tst) that will be subdivided in units (exercicios_tst/unidadeXX). It will also change that directory name to the exercise's name, and create a python file with a header. Checkout will be tried whenever the clipboard changes.

#### Usage

```sh
easy_tst watch
```
or simply
```
easy_tst
```
To stop watcher mode and exit easy_tst just press Ctrl + C (Keyboard Interrupt).

### Organizer
This mode will organize all your tst directories. It will identify a tst directory and do the same process of moving and renaming the directory that watcher does. It will ask if you are sure that you want to move that directory.

#### Usage

```sh
easy_tst organize
```
To force organizer to move all directories without confirmation, add `-f` (or `--force`)
```sh
easy_tst organize -f
```

### Help
If you have any doubts, easy_tst has a built-in helper. To run it use `-h` as an argument.

#### Example
```sh
easy_tst -h
```

## Contributing

When contributing to this repository, please first discuss the change you wish to make via an issue,
email, or any other method with the owners of this repository before making a change.

### Pull Request Process

1. Fork it (https://github.com/brobsc/easy_tst/fork)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request


## Authors

- Bruno Siqueira – bruno.siqueira@ccc.ufcg.edu.br
- Pedro Espíndula – joao.espindula@ccc.ufcg.edu.br

## License

Distributed under the AGPL 3.0 license. See ``LICENSE`` for more information.
