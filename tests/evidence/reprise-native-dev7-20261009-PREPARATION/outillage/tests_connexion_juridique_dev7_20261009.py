"""Contrôles adversariaux sans navigateur, réseau, connexion ni inférence."""
import unittest
import connexion_juridique_dev7_20261009 as connection
from campagne_native_complete_dev7_20261009 import GateError

class OAuthContracts(unittest.TestCase):
    def test_official_url(self):
        value = "https://"+connection.PROVIDER+"/authorize?state=synthetic"
        self.assertEqual(value,connection.validate_authorization_url(value))

    def test_foreign_credential_plaintext_and_malformed_urls(self):
        for value in ("http://"+connection.PROVIDER, "https://example.com/authorize",
                      "https://user:password@"+connection.PROVIDER,
                      "https://"+connection.PROVIDER+":8080/authorize",
                      "https://"+connection.PROVIDER+"\n", None):
            with self.assertRaises(GateError):
                connection.validate_authorization_url(value)

    def test_matching_completion(self):
        value = connection.completion({"name":"droit-francais","loginId":"fixture","success":True},
                                      {"loginId":"fixture"})
        self.assertTrue(value["success"])

    def test_absent_or_foreign_login_id_and_server(self):
        for params in ({"name":"droit-francais","success":True},
                       {"name":"droit-francais","loginId":"other","success":True},
                       {"name":"other","loginId":"fixture","success":True}):
            with self.assertRaises(GateError):
                connection.completion(params,{"loginId":"fixture"})

    def test_contradictory_or_untyped_success(self):
        for params in ({"name":"droit-francais","success":True,"error":"Synthetic failure"},
                       {"name":"droit-francais","success":"true"}):
            with self.assertRaises(GateError):
                connection.completion(params,{})

    def test_failure_does_not_print_sensitive_error(self):
        value = connection.completion({"name":"droit-francais","success":False,
                                       "error":"access_denied secret=syntheticSecret"},{})
        self.assertFalse(value["success"])
        self.assertNotIn("syntheticSecret",str(value))

if __name__ == "__main__":
    unittest.main(verbosity=2)
