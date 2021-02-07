import json
from pathlib import Path

from tests.conftest import FlowHeaterLayer
from tests.util import execute

basedir = Path("examples/10-applications-ttn")


def test_ttn_to_hiveeyes(fh_http: FlowHeaterLayer):
    """
    Forward TTN payloads to Kotori for Hiveeyes.

    - https://community.hiveeyes.org/t/ttn-daten-an-kotori-weiterleiten/1422/5
    - https://community.hiveeyes.org/t/datenweiterleitung-via-ttn-lora-zu-hiveeyes-bob-und-beep-einrichten/3197
    - https://github.com/hiveeyes/terkin-datalogger/tree/0.10.0/client/TTN
    """

    with open(basedir / "ttn-to-hiveeyes-ingress.json", "r") as f:
        payload = json.load(f)
    response = execute(
        basedir / "ttn-to-hiveeyes-recipe.js", method="post", json=payload
    )

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()
    print(stdout)

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "POST"

    with open(basedir / "ttn-to-hiveeyes-egress.json", "r") as f:
        outcome = json.load(f)
        assert json.loads(data["body"]) == outcome


def test_ttn_to_beeobserver(fh_http: FlowHeaterLayer):
    """
    Forward TTN payloads to BEEP for Bee Observer (BOB).

    - https://community.hiveeyes.org/t/ttn-daten-an-kotori-weiterleiten/1422/5
    - https://community.hiveeyes.org/t/datenweiterleitung-via-ttn-lora-zu-hiveeyes-bob-und-beep-einrichten/3197
    - https://github.com/hiveeyes/terkin-datalogger/tree/0.10.0/client/TTN
    """

    with open(basedir / "ttn-to-beeobserver-ingress.json", "r") as f:
        payload = json.load(f)
    response = execute(
        basedir / "ttn-to-beeobserver-recipe.js", method="post", json=payload
    )

    assert response.status_code == 200
    data = response.json()

    # Read STDOUT
    stdout = fh_http.get_stdout()
    print(stdout)

    # Check STDOUT
    data = json.loads(stdout)
    print(data)
    assert data["method"] == "POST"

    with open(basedir / "ttn-to-beeobserver-egress.json", "r") as f:
        outcome = json.load(f)
        assert json.loads(data["body"]) == outcome
