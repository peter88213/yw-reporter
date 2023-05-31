# yw-reporter - Configurable report generator for yWriter projects

For more information, see the [project homepage](https://peter88213.github.io/yw-reporter) with description and download instructions.

## Development

*yw-reporter* is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Conventions

See https://github.com/peter88213/PyWriter/blob/main/docs/conventions.md

Exceptions:
- No localization is required.
- The directory structure is modified to minimize dependencies:

```
.
└── yw-reporter/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Development tools

- [Python](https://python.org) version 3.10
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and [EGit](https://www.eclipse.org/egit/)
- Apache Ant for building the application script

## License

yw-reporter is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

