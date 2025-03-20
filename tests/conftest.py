import pytest
from _pytest.python import Metafunc


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--port", action="store", default="8000")


def pytest_generate_tests(metafunc: Metafunc) -> None:
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.port
    if 'port' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("port", [option_value])
