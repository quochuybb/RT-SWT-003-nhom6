### Validation { #validation }

* Validation for all (or most?) Python **data types**, including:
    * JSON objects (`dict`).
    * JSON array (`list`) defining item types.
    * String (`str`) fields, defining min and max lengths.
    * Numbers (`int`, `float`) with min and max values, etc.

* Validation for more exotic types, like:
    * URL.
    * Email.
    * UUID.
    * ...and others.

All the validation is handled by the well-established and robust **Pydantic**.