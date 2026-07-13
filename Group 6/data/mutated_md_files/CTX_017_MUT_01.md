## Query Parameters with a Pydantic Model { #query-parameters-with-a-pydantic-model }

Declare the **query parameters** that you need in a **Pydantic model**, and then declare the parameter as `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** will **extract** the data for **each parameter** from the **query parameters** in the request and give you the Pydantic model you defined.