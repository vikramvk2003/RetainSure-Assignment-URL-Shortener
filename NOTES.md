Features Implemented
Shortens valid URLs via POST /api/shorten

Redirects short URL codes to the original URL via GET /<short_code>

Provides click stats via GET /api/stats/<short_code>

Lists all shortened URLs via GET /




Testing (Pytest)
Added unit and integration tests in tests/test_basic.py

Setup testing with Flask’s test client

Covered:

URL shortening

Redirection

Stats retrieval

Handling invalid input

Fixed test failures due to missing "created_at" in returned data




* AI Tools Used:
        Chat Gpt :- used for creating test cases