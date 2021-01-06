import json
from pathlib import Path

from tests.conftest import FlowHeaterLayer
from tests.util import execute

basedir = Path("examples/01-basic")


def test_error_syntax(fh_http: FlowHeaterLayer):
    """
    $ deno run examples/01-basic/error-syntax.js
    error: Expected ';', '}' or <eof> at file:///Users/amo/dev/flow-heater/fh-core/examples/01-basic/error-syntax.js:1:6

    As this is actually a linter error, respective code should not
    even make it to runtime when already caught on insertion time.
    See https://github.com/flow-heater/fh-core/issues/22.
    """

    response = execute(basedir / "error-syntax.js", headers={"FH-Debug": "true"})

    assert response.status_code == 500
    data = response.json()

    # TODO: That might yield a linter error after the HTTP request
    #       header "FH-Debug: true" will get evaluated appropriately.


def test_error_runtime(fh_http: FlowHeaterLayer):
    """
    $ deno run examples/01-basic/error-runtime.js
    error: Uncaught TypeError: JSON.foobar is not a function
    JSON.foobar();
         ^
        at file:///Users/amo/dev/flow-heater/fh-core/examples/01-basic/error-runtime.js:1:6

    For propagating those runtime errors to the user interactively,
    I've elaborated on the `FH-Debug: true` header within
    https://github.com/flow-heater/fh-core/issues/33.
    """

    response = execute(basedir / "error-runtime.js", headers={"FH-Debug": "true"})

    assert response.status_code == 500
    data = response.json()

    # TODO: That might yield a stacktrace after the HTTP request
    #       header "FH-Debug: true" will get evaluated appropriately.


def test_json_demo(fh_http: FlowHeaterLayer):

    response = execute(basedir / "json-demo.js")

    assert response.status_code == 200
    data = response.json()

    # Check STDOUT
    stdout = fh_http.get_stdout()
    print(stdout)
    assert 'Stringify: {"a":"b"}' in stdout
    assert "Parse works, too" in stdout


def test_json_request_get(fh_http: FlowHeaterLayer):

    response = execute(basedir / "json-request-echo.js", headers={"foo": "bar"})

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "GET"
    assert data["headers"]["user-agent"].startswith("python-requests/")
    assert data["headers"]["foo"] == "bar"
    assert data["body"] == ""


def test_json_request_post(fh_http: FlowHeaterLayer):

    response = execute(basedir / "json-request-echo.js", method="post")

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "POST"
    assert data["body"] == ""


def test_json_request_post_x_www_form_urlencoded(fh_http: FlowHeaterLayer):

    response = execute(basedir / "json-request-echo.js", method="post", data={"foo": "bar"})

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "POST"
    assert data["body"] == "foo=bar"


def test_json_request_post_json(fh_http: FlowHeaterLayer):

    response = execute(basedir / "json-request-echo.js", method="post", json={"foo": "bar"})

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "POST"
    assert data["body"] == '{"foo": "bar"}'