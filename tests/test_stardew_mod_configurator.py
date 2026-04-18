import json
import tempfile
import unittest
from pathlib import Path

import stardew_mod_configurator as smc


class StardewModConfiguratorTests(unittest.TestCase):
    def test_convert_cp_mod_handles_non_dict_when(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mod_dir = Path(tmp_dir)
            content_path = mod_dir / "content.json"
            content_path.write_text(
                json.dumps(
                    {
                        "Format": "2.0.0",
                        "Changes": [
                            {
                                "Action": "Load",
                                "Target": "Characters/Alex",
                                "FromFile": "Characters/Alex.png",
                                "When": "{{HasMod}}",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            smc.convert_cp_mod(mod_dir, "high")

            updated_content = json.loads(content_path.read_text(encoding="utf-8"))
            when_data = updated_content["Changes"][0]["When"]
            self.assertIsInstance(when_data, dict)
            self.assertEqual(when_data["GMCM_EnableMod"], "true")

    def test_run_conversion_writes_conversion_log_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mod_dir = Path(tmp_dir)
            (mod_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "Name": "TestMod",
                        "UniqueID": "Test.Mod",
                        "ContentPackFor": {"UniqueID": smc.CP_UNIQUE_ID},
                    }
                ),
                encoding="utf-8",
            )
            (mod_dir / "content.json").write_text(
                json.dumps(
                    {
                        "Format": "2.0.0",
                        "Changes": [
                            {
                                "Action": "Load",
                                "Target": "Characters/Alex",
                                "FromFile": "Characters/Alex.png",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            ok = smc.run_conversion(str(mod_dir), "low")

            self.assertTrue(ok)
            log_path = mod_dir / "conversion_log.txt"
            self.assertTrue(log_path.exists())
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("Processing mod folder:", log_text)
            self.assertIn("Content Patcher conversion complete!", log_text)

    def test_run_conversion_can_disable_log_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mod_dir = Path(tmp_dir)
            (mod_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "Name": "TestMod",
                        "UniqueID": "Test.Mod",
                        "ContentPackFor": {"UniqueID": smc.CP_UNIQUE_ID},
                    }
                ),
                encoding="utf-8",
            )
            (mod_dir / "content.json").write_text(
                json.dumps(
                    {
                        "Format": "2.0.0",
                        "Changes": [
                            {
                                "Action": "Load",
                                "Target": "Characters/Alex",
                                "FromFile": "Characters/Alex.png",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            ok = smc.run_conversion(str(mod_dir), "low", log_to_file=False)

            self.assertTrue(ok)
            self.assertFalse((mod_dir / "conversion_log.txt").exists())


if __name__ == "__main__":
    unittest.main()
