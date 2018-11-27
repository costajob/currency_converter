import doctest 


def load_tests(loader, tests, ignore):
    for mod in ('converter', 'currency', 'data'):
        tests.addTests(doctest.DocTestSuite(mod))
    return tests
