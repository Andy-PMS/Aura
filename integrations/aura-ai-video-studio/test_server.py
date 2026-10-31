import unittest
from server import validate, execute, reply

GOOD = {"image_asset_id":"img:1","voice_asset_id":"voice:1","text":"Ciao, questa è una prova.","consent_image":True,"consent_voice":True,"duration_seconds":10,"resolution":"480p"}

class Tests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate(GOOD), [])
    def test_consent(self):
        self.assertTrue(validate({**GOOD, "consent_voice":False}))
    def test_bad_assets(self):
        self.assertTrue(validate({**GOOD, "image_asset_id":"../../secret"}))
    def test_bad_duration(self):
        self.assertTrue(validate({**GOOD, "duration_seconds":60}))
    def test_no_provider_calls(self):
        self.assertFalse(execute("video_studio_prepare", GOOD)["provider_calls"])
        self.assertEqual(execute("video_studio_generate", {"request_id":"x"})["status"], "blocked")
    def test_mcp_initialize(self):
        self.assertIn("serverInfo", reply({"jsonrpc":"2.0","id":1,"method":"initialize"})["result"])
    def test_tools_list(self):
        self.assertEqual(len(reply({"jsonrpc":"2.0","id":2,"method":"tools/list"})["result"]["tools"]), 3)

if __name__ == "__main__":
    unittest.main()
