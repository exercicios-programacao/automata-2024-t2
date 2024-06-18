"""Implementa casos de avaliação de erros."""

from unittest.mock import patch, mock_open
from behave import when, then  # pylint: disable=no-name-in-module

import automata


@when("eu crio o automato")
def _when_automata_is_loaded(context):
    try:
        with patch(
            "builtins.open", mock_open(read_data=context.automata_description)
        ):
            context.automata = automata.load_automata("fake_file.txt")
    except Exception as ex:  # pylint: disable=broad-except
        context.automata = None
        context.exception = ex
    else:
        context.exception = None


@then("um erro ocorre na criação do automato")
def _then_an_error_occurred_on_loading_automata(context):
    assert context.exception is not None
