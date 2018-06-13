# easy_tst

easy_tst is a set of scripts that makes the use of tst easier by automatically doing the checkout and writing a header in the python file (see [daltonserey/tst](https://github.com/daltonserey/tst) for more information).


## Dependencies

Before installing easy_tst you will need: 

1. Python 2.7: Refer to Google for how to install python2.7, or see [Python Website](https://www.python.org/downloads/release/python-2715/)
2. [tst](https://github.com/daltonserey/tst)


## Installing

```sh
pip install easy_tst
```

## Usage

Simply run:

```sh
easy_tst
```

This will start the wizard (on first execution) to configure your settings, and then start easy_tst watcher.

While easy_tst is running, copy a valid checkout code and it will automatically perform a `tst checkout` on that code and move/rename its result according to your settings.

---

Force wizard execution:

```sh
easy_tst wizard
```

Use this to change your settings.


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

