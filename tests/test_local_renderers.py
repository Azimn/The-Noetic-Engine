import unittest
from noetic_engine.renderer import DecisionBrief
from noetic_engine.local_renderers import OllamaRenderer,LocalChatRenderer

BRIEF=DecisionBrief(1,"pretorius_sandbox","protect",("protect","defer"),
    ({"origin_id":"e1","subject_id":"pretorius_sandbox",
      "evidence_class":"lived_observed","source":"test",
      "excerpt":"A frightened witness spoke","verified_entailment":False},),
    (),({"text":"Maybe this is linked to another memory"},),
    {"care":0.3},"configuration-digest")

class LocalRendererTests(unittest.TestCase):
    def test_ollama_transport_never_writes_state(self):
        captured=[]
        def fake(url,data):
            captured.append((url,data))
            return {"response":"I shall protect the witness."}
        renderer=OllamaRenderer("qwen3:1.5b",transport=fake)
        self.assertIn("protect",renderer.render(BRIEF))
        self.assertIn("UNVERIFIED QUESTION",captured[0][1]["prompt"])
        self.assertIn("selected_action",captured[0][1]["prompt"])
        self.assertEqual(captured[0][1]["stream"],False)

    def test_chat_renderer_protocol(self):
        x=LocalChatRenderer(transport=lambda url,data:{
            "choices":[{"message":{"content":"The experiment must stop."}}]})
        self.assertEqual(x.render(BRIEF),"The experiment must stop.")

    def test_refuses_network_targets(self):
        for url in ("https://api.example.com/chat","http://10.0.0.2:8080/",
                    "http://127.0.0.1:8080/?token=secret"):
            with self.assertRaises(ValueError):
                OllamaRenderer("test",endpoint=url)

    def test_refuses_policy_violation(self):
        faulty=DecisionBrief(1,"p","destroy",("protect",),(),(),(),{},"x")
        r=OllamaRenderer("test",transport=lambda *_:{"response":"ignored"})
        with self.assertRaises(ValueError):r.render(faulty)

    def test_invalid_renderer_responses(self):
        r=OllamaRenderer("test",transport=lambda *_:{"response":""})
        with self.assertRaises(ValueError):r.render(BRIEF)

if __name__=="__main__":unittest.main()
