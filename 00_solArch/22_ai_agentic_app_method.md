= AI Agentic App - Method Specification
:toc:

== Agent Workflow

The system consists of multiple autonomous agents that collaborate:

* **Input Generation Agent** - Interacts with the user to generate an initial file of raw addresses.
* **Cleansing Agent** - Standardizes and cleans the raw addresses.
* **Validation Agent** - Validates addresses using the Mapbox API.
* **Geocoding Agent** - Fetches latitude and longitude for validated addresses.
* **Final Output Agent** - Generates a CSV file containing original, cleansed, and geocoded addresses.
* **Map Visualization Agent** - Uses Mapbox APIs to plot the geocoded addresses onto a street view map.

== LangChain Integration

Agents are implemented using LangChain framework:
- Each agent executes tasks independently while retaining shared memory.
- Agents can query the Mapbox API when needed.
- Logs errors and status updates at each step.

== Logging Implementation

Logging captures critical steps:
- User inputs and generated raw addresses.
- Address cleansing transformations applied.
- API validation results (success/failure logs).
- Geolocation API responses.
- Final output file generation status.

== UML Diagram

The workflow of the agentic system is represented below:

![AI Agentic App Workflow](http://localhost:32768/png/PP0zQyCm48Pt_OeZUuVuQz1G42a96Ke3fTwlrZKzK2KXoMcRNrzPE60tYq3Sm_k5Gt81tY85uJ4a7jYZJR0vMZycE92bW8cT1NKccpQ04THsZUuCeOripqkcMZCz6jPtGlKQEf0RdFudrAoPFLiqy3AcATu2QzVOCtheEOxPzdfdsman5OQ7nzn5mYcu2si2BfKr9MGJXTgMUoLl8n04_0RKEb2CyC66XAeAKqie6m1Q3J7b5uFcAzrWocfr8Hi9ynAB8rmO8GT-Tp-WJaUXciAs4lQKXaymkK0QSy19tZXxBZ-Xse9rYu2xrtuErastgQI49uxUuE_2BwynstsX_mC0)
