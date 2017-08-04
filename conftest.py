def pytest_ignore_collect(path, config):
    # doesn't collect doctests for setup.py
    if str(path).endswith("setup.py"):
        return True
    return False
