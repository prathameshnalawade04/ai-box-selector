# AI Usage Documentation

**1. Which AI tool(s) you used:**
Google Gemini.

**2. The prompts you gave:**
- "Based on the dimensions and weight how to calculate recommended box size"
- "Help me create models.py at the beginning"
- "My idea is to create a template where I place the order... calculate the required dimension box and then just sort from the available boxes and render a box template"
- "Can you give me the custom admin panel to show this model"
- "What if the order exceeds the capacity of single box so I want to upgrade my box selection logic to support splitting an order across multiple boxes"
- "Create some test means test.py file"

**3. What output you accepted:**
- The `@property` logic in `models.py` to calculate volume and max dimensions at the database level.
- The greedy algorithm approach in `views.py` to split large orders into multiple shipments.
- The single-page Bootstrap 5 HTML template layout.
- The `tests.py` file covering 4 core scenarios (calculations, single box, split box, oversized items).

**4. What output you rejected or modified:**
- I initially accepted the single-box logic in the view, but realized it would fail for bulk orders. I rejected that limitation and prompted the AI to refactor the view using a bin-packing (greedy algorithm) approach to support splitting orders into multiple boxes.

**5. Any mistakes the AI made:**
- The AI's first draft of the view did not account for edge cases where the total order weight exceeded the largest available box in the warehouse. It required a follow-up prompt to implement the multi-box splitting logic.

**6. How you verified the final code:**
- I ran the Django test suite (`python manage.py test`) which verified the math properties, the single-box flow, the multi-box splitting, and the oversized item rejection.
- I pasted the terminal output of these passing tests into `output.md`.
- I also ran the local development server and tested the single-page form manually.