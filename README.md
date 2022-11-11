[![CI][]][1] [![Coverage][]][2] [![Gitter][]][3] [![Python][]][4] [![CKAN][]][5] [![PYPI][]][6]

# ckanext-resourcedictionary

Extends the default CKAN Data Dictionary functionality by adding possibility to create data dictionary before actual data is uploaded to datastore.
For resources that don't have datastore records, the data dictionary can be edited in every way (adding/removing/editing fields) and even completely deleted.
For resources that contain datastore records editing data dictionary is limited only to the info properties of a field.
Resource dictionary fields, labels and notes are added to the SOLR index as a resource extras.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9             | yes   |


## Installation

To install ckanext-resourcedictionary:

1. Activate your CKAN virtual environment, for example:

   ```. /usr/lib/ckan/default/bin/activate```

2. Clone the source and install it on the virtualenv

   ```
   git clone https://github.com/keitaroinc/ckanext-resourcedictionary.git
   cd ckanext-resourcedictionary
   pip install -e .
   pip install -r requirements.txt 
   ```

3. Add `resourcedictionary` before the `datastore` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).\
   `ckan.plugins = resourcedictionary datastore`

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

   ```sudo service apache2 reload```


## Config settings

None at present


## Developer installation

To install ckanext-resourcedictionary for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/keitaroinc/ckanext-resourcedictionary.git
    cd ckanext-resourcedictionary
    python setup.py develop
    pip install -r dev-requirements.txt

## API

[Resource Dictionary API](ckanext/resourcedictionary/logic/action/resource_dictionary_create.md) : `POST /api/v3/action/resource_dictionary_create`

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-resourcedictionary

If ckanext-resourcedictionary should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

       pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)


  [CI]: https://github.com/keitaroinc/ckanext-resourcedictionary/workflows/CI/badge.svg?branch=main
  [1]: https://github.com/keitaroinc/ckanext-resourcedictionary/actions
  [Coverage]: https://coveralls.io/repos/github/keitaroinc/ckanext-resourcedictionary/badge.svg?branch=main
  [2]: https://coveralls.io/github/keitaroinc/ckanext-resourcedictionary?branch=main
  [Gitter]: https://badges.gitter.im/keitaroinc/ckan.svg
  [3]: https://gitter.im/keitaroinc/ckan?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
  [Python]: https://img.shields.io/badge/python-3.8-blue
  [4]: https://www.python.org
  [CKAN]: https://img.shields.io/badge/ckan-2.9-red
  [5]: https://www.ckan.org
  [Pypi]: https://img.shields.io/pypi/v/ckanext-resourcedictionary
  [6]: https://pypi.org/project/ckanext-resourcedictionary