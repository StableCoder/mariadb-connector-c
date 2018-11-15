# MariaDB-connector-c

[![pipeline status](http://git.stabletec.com/conan/mariadb-connector-c/badges/master/pipeline.svg)](http://git.stabletec.com/conan/mariadb-connector-c/commits/master)
[![GitHub tag](https://img.shields.io/github/tag/StableCoder/mariadb-connector-c.svg)](https://github.com/StableCoder/mariadb-connector-c/releases)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://git.stabletec.com/conan/mariadb-connector-c/blob/master/LICENSE)

[Conan](https://www.conan.io/) package for the [MariaDB Connector/C](https://mariadb.com/kb/en/library/mariadb-connector-c/) library.

## Build Matrix

In order for the above badge to be marked as 'passed', the repository must build under all combinations of the following conditions:

| OS         | Compiler  | Build Type    | Runtime |
|:-----------|:----------|:--------------|:--------|
| Linux      | GCC/Clang | Debug/Release |         |
| Windows 10 | MSVC2017  | Debug         | MDd/MTd |
| Windows 10 | MSVC2017  | Release       | MD/MT   |