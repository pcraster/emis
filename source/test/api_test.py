import unittest
from flask import json
from emis import create_app


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()

        self.app_context.push()

        self.client = self.app.test_client()


    def tearDown(self):
        self.app_context.pop()


    def test_api(self):
        response = self.client.get("/api")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, data)

        data = json.loads(data)

        self.assertEqual(data, {
                "resources": {
                    # "aggregate_methods": {
                    #     "route": "/aggregate_methods"
                    # },
                    "aggregate_queries": {
                        "route": "/aggregate_queries"
                    },
                    "aggregate_query_messages": {
                        "route": "/aggregate_query_messages"
                    },
                    "aggregate_query_results": {
                        "route": "/aggregate_query_results"
                    },
                    "domains": {
                        "route": "/domains"
                    },
                    "properties": {
                        "route": "/properties"
                    }
                }
            })


if __name__ == "__main__":
    unittest.main()
