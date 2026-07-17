import json
import anthropic
from agent.registry import TOOL_SCHEMAS, TOOL_FUNCTIONS
from agent.prompts import SYSTEM_PROMPT

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from env
MODEL = "claude-sonnet-4-5"

def run_agent(user_message: str, max_steps: int = 8) -> str:
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_steps):
        # 1) Call the model. It sees the tools and decides its next move.
        resp = client.messages.create(
            model=MODEL, max_tokens=1024,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )

        # 2) Append whatever it said (text and/or tool_use blocks) to history.
        messages.append({"role": "assistant", "content": resp.content})

        # 3) If it didn't ask for a tool, it's done — return its text.
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")

        # 4) Run EVERY tool it asked for (it can request several at once).
        results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            try:
                output = TOOL_FUNCTIONS[block.name](**block.input)
            except Exception as e:
                output = f"ERROR: {e}"
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,               # ties result to the call
                "content": json.dumps(output, default=str),
            })

        # 5) Hand results back as the next 'user' turn, then loop again.
        messages.append({"role": "user", "content": results})

    return "Stopped: hit max steps."