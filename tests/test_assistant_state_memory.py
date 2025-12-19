import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# AssistantState comes from the root-level src_assistant_state module (not the src/ package).
from src_assistant_state import AssistantState


class AssistantStateMemoryBankTests(unittest.TestCase):
    def test_engagement_profile_and_journal_entry_surfaces(self):
        with TemporaryDirectory() as tmp:
            memory_path = Path(tmp) / "memory.json"
            # Simulate older state without memory_bank section to ensure migration.
            memory_path.write_text(json.dumps({
                "user_profile": {"username": "User", "timezone": "UTC", "preferences": {"default_mode": "concise"}},
                "short_term": [],
                "long_term": []
            }))

            state = AssistantState(memory_path=memory_path)
            profile = state.update_engagement_profile(
                mood="calm",
                style="supportive",
                instructions=["match my energy", "keep responses brief"]
            )

            self.assertEqual(profile["mood"], "calm")
            self.assertIn("instructions", profile)

            entry = state.log_moment("Morning check-in", tags=["journal"], share_with_chat=True)
            self.assertEqual(entry["note"], "Morning check-in")
            self.assertTrue(entry["share_with_chat"])

            shared = state.recall_journal(shared_only=True)
            self.assertTrue(any(e["note"] == "Morning check-in" for e in shared))

    def test_shared_only_filtering(self):
        with TemporaryDirectory() as tmp:
            memory_path = Path(tmp) / "memory.json"
            state = AssistantState(memory_path=memory_path)

            state.log_moment("Private note", share_with_chat=False)
            state.log_moment("Share this note", share_with_chat=True)

            shared_notes = [e["note"] for e in state.recall_journal(shared_only=True)]
            self.assertEqual(shared_notes, ["Share this note"])


if __name__ == "__main__":
    unittest.main()
