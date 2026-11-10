from pathlib import Path

from litellm import acompletion

from agents.eval.gaia.providers import get_semaphore
from agents.eval.gaia.schema import GaiaOutput

gaia_prompt = (Path(__file__).parent / "prompt.md").read_text().strip()


async def solve_problem(model: str, question: str) -> GaiaOutput:
    """Solve a single problem and return structured output."""
    async with get_semaphore(model):
        response = await acompletion(
            model=model,
            messages=[
                {"role": "system", "content": gaia_prompt},
                {"role": "user", "content": question},
            ],
            response_format=GaiaOutput,
            num_retries=2,
        )
        finish_reason = response.choices[0].finish_reason
        content = response.choices[0].message.content

        if finish_reason == "refusal" or content is None:
            return GaiaOutput(
                is_solvable=False,
                unsolvable_reason=f"Model refused to answer (finish_reason: {finish_reason})",
                final_answer=""
            )
        return GaiaOutput.model_validate_json(content)
