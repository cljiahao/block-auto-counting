from core.exceptions import InvalidInputError


class BaseService:
    """
    A base class for services providing common validation utilities.
    """

    def _validate_input_keys(
        self, input_data: dict, valid_keys: set[str], text: str = "input"
    ) -> None:
        """
        Validates that only allowed keys are present in the input data.

        Args:
            input_data (dict): The dictionary to validate.
            valid_keys (set[str]): A set of allowed keys.
            text (str): A descriptive string for the input data in error messages.

        Raises:
            InvalidInputError: If unknown keys are found.
        """
        invalid_keys = set(input_data) - valid_keys
        if invalid_keys:
            raise InvalidInputError(
                f"Unknown keys in {text} data: {', '.join(invalid_keys)}"
            )

    def _validate_value_empty(self, key_name: str, value: str) -> bool:
        """
        Validates that a string value is not empty.

        Args:
            key_name (str): The name of the key being validated (for error message).
            value (str): The string value to check.

        Raises:
            InvalidInputError: If the value is empty.
        """
        if not value:
            raise InvalidInputError(f"{key_name} cannot be empty.")
