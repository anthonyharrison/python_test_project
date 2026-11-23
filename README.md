# python_test_project
A sample Python project to be used for testing and evaluating software tools e.g. SBOM generators.

The project can be used to extract license information from a manifest.

## Installation

To install clone the repositoty:

`git clone https://github.com/anthonyharrison/python_test_project.git`

Install the application and dependencies using the following command:

`pip install -U .`

This will create a command line application called `compliance-test`.

The tool requires Python 3 (3.11+). It is recommended to use a virtual python environment especially if you are using different versions of python. `virtualenv` is a tool for setting up virtual python environments which allows you to have all the dependencies for the tool set up in a single environment, or have different environments set up for testing using different versions of Python.

## Usage

The

```bash
usage: compliance-test [-h] [--db DB] [--list] [--limit LIMIT] [manifest]

Sample OSS compliance tester

positional arguments:
  manifest       Path to JSON or YAML manifest

options:
  -h, --help     show this help message and exit
  --db DB        SQLite DB path
  --list         View stored records from the database
  --limit LIMIT  Limit number of rows shown with --list
```

## Operation

The `--db` option is to specify the path to a SQLite database to store the licence information. The default name for the database is audit.db in the local directory.

The `manifest` specifies the name of a manifest file. The file nmust be in YAML or JSON format, which is determined from the file extenstion. Only files with `.yaml`, `.yml` and `.json` are allowed. Any other file extension will be siliently ignored.

The `list` option is used to display the contents of the database. The `limit` option can be used to limit the number of entries displayed (default is all entries).

## Example

Using the following manifest file:

```yaml
schema_version: "1.0"
release:
  name: "sample-service"
  version: "1.4.2"
  environment: "staging"

packages:
  - name: "requests"
    version: "2.31.0"
    ecosystem: "pypi"
    license: "Apache-2.0"
    purl: "pkg:pypi/requests@2.31.0"
    supplier: "Kenneth Reitz"

  - name: "PyYAML"
    version: "6.0.1"
    ecosystem: "pypi"
    license: "MIT"
    purl: "pkg:pypi/pyyaml@6.0.1"
    supplier: "Kirill Simonov"

  - name: "rich"
    version: "13.7.1"
    ecosystem: "pypi"
    license: "MIT"
    purl: "pkg:pypi/rich@13.7.1"
    supplier: "Will McGugan"

  - name: "openssl"
    version: "1.1.1w"
    ecosystem: "deb"
    license: "OpenSSL"
    purl: "pkg:deb/debian/openssl@1.1.1w?arch=amd64"
    supplier: "Debian Project"

  - name: "lodash"
    version: "4.17.20"
    ecosystem: "npm"
    license: "MIT"
    purl: "pkg:npm/lodash@4.17.20"
    supplier: "John-David Dalton"
```

Execute the following command:

`compliance-test --db test.db test_manifest.json`

The tool will respond with the number of package entries processed.

To view the contents of the database:

`compliance-test --db test.db --list`

The following output is produced on the terminal:

```bash
                      Stored Audit Records
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Package  ┃ License    ┃ Digest                           ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1 │ requests │ Apache-2.0 │ f694714bca9702c83c90ed7fb4376875 │
│  2 │ PyYAML   │ MIT        │ d9191dbc3bbd7beb2e7caced1fc50094 │
│  3 │ rich     │ MIT        │ d9ee659a5ddeaa14251a4393dbd1357a │
│  4 │ openssl  │ OpenSSL    │ bbda1ec3cc4af7d0657df82ff689f685 │
│  5 │ lodash   │ MIT        │ 3ac5bae7ccf39b45360202b18ed2db54 │
└────┴──────────┴────────────┴──────────────────────────────────┘
```

If there is no data in the database, the tool responds `No data found.`.

## Licence

Licenced under the Apache 2.0 Licence.

## Limitations

This is an example project. It has known weaknesses and should only be used for educational, testing or evaluation purposes.

## Feedback and Contributions

Bugs and feature requests can be made via GitHub Issues.