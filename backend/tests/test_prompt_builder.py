from app.sim.prompt_builder import PromptBuilder


def test_prompt_builder_is_deterministic():
    pb = PromptBuilder()
    p1 = pb.build("Decide X", ["ctx1", "ctx2"], {"budget": 10})
    p2 = pb.build("Decide X", ["ctx1", "ctx2"], {"budget": 10})
    assert p1 == p2
    assert "optimistic" in p1
    assert "JSON only" in p1

