# RemNote Flashcard Generation Prompts

## General Knowledge Prompt
```
Create a comprehensive set of RemNote flashcards from this document using the format "* Question == Answer".

For each important concept in the document:
1. Create clear, specific questions that test understanding of key facts, definitions, and relationships
2. Ensure questions are atomic (testing one piece of knowledge)
3. Make answers concise but complete
4. Cover ALL important information in the document
5. Group related flashcards under appropriate section headings

Format each flashcard as:
* [Question] == [Answer]

Include section headings using markdown ## [Section Name] to organize related cards.
```


## Math/Quantitative Prompt
```
Generate RemNote flashcards for mathematical and quantitative concepts in this document.

For each mathematical concept, theorem, or technique:
1. Create definition cards: "* What is [concept]? == [definition]"
2. Create formula cards: "* What is the formula for [concept]? == [formula]"
3. Create proof cards: "* How is [theorem] proven? == [proof outline]"
4. Create application cards: "* What are applications of [concept]? == [applications]"
5. Create example problem cards: "* How do you solve [type of problem]? == [solution steps]"

Format each card as:
* [Question] == [Answer]

Group cards by mathematical area using ## [Math Area] headings.
```

## Exam-Focused Prompt
```
Create exam-focused RemNote flashcards from this document.

For each testable concept:
1. Create recall cards for facts: "* What is [term/concept]? == [definition]"
2. Create application cards: "* How would you apply [concept] to [scenario]? == [application]"
3. Create comparison cards: "* Compare and contrast [concept A] and [concept B] == [comparison]"
4. Create cards for common exam questions: "* A typical exam question about [topic] might ask [question]? == [answer approach]"
5. Create cards for key formulas/equations: "* What is the formula for [concept]? == [formula]"

Format each card as:
* [Question] == [Answer]

Group cards by exam topic using ## [Exam Topic] headings.
```


## Critical Thinking Prompt
```
Create RemNote flashcards that promote critical thinking about the content in this document.

For each major concept or argument:
1. Create analysis cards: "* What are the key components of [concept/argument]? == [components]"
2. Create evaluation cards: "* What are the strengths and weaknesses of [concept/argument]? == [evaluation]"
3. Create alternative perspective cards: "* What are alternative perspectives on [concept/issue]? == [alternatives]"
4. Create application cards: "* How could [concept] be applied to solve [problem]? == [application]"
5. Create synthesis cards: "* How does [concept A] combine with [concept B] to form [new insight]? == [synthesis]"

Format each card as:
* [Question] == [Answer]

Group cards by concept using ## [Concept] headings.
```

## Bloom's Taxonomy Prompt
```
Create RemNote flashcards that cover all levels of Bloom's Taxonomy for the content in this document.

For each key concept:
1. Create remembering cards: "* What is [term/fact]? == [definition/fact]"
2. Create understanding cards: "* How would you explain [concept] in your own words? == [explanation]"
3. Create application cards: "* How would you use [concept] to solve [problem]? == [application]"
4. Create analysis cards: "* What are the components/relationships in [concept]? == [analysis]"
5. Create evaluation cards: "* How would you assess the effectiveness/validity of [concept]? == [evaluation]"
6. Create creation cards: "* How could you design a new [application/solution] using [concept]? == [creative solution]"

Format each card as:
* [Question] == [Answer]

Group cards by concept using ## [Concept] headings.
```

## Flashcard Blender Prompt
```
Generate flashcards by blending multiple styles. For each concept:
1. Create a definition card
2. Create a comparison card
3. Add an application or analogy card
4. Add one creative or unusual format (e.g. reverse, joke, visual)
Use format * front == back.
```

## One-Sentence Prompt
```
Create flashcards using exactly one sentence per card.
Make both the question and answer as short and atomic as possible.
No multi-part explanations.
```

## Visual Description Prompt
```
Turn any visual elements, spatial descriptions, or diagrams into:
* What does [visual] show? == [description]
* How does [structure] function? == [functional explanation]
```

## Failure Case Prompt
```
Generate flashcards that test when a concept breaks or fails:
* When does [concept] stop working? == [failure condition]
* What’s a real-world example where [law] doesn’t apply? == [example]
```

## Anti-Memorization Prompt
```
Make cards that test reasoning, not memory.
Avoid surface-level facts. Focus on cards like:
* How would you deduce [result] from [given]? == [method]
* What would you predict in [scenario]? == [prediction]
```

## Rapid Recall Prompt
```
Generate 50 short flashcards designed for speed review:
- No fluff
- One line per card
- Pure recall only
```

## Evidence-Based Prompt
```
For every claim or conclusion in the document, make a card like:
* What is the evidence for [claim]? == [summary of evidence]
* Who discovered [fact]? == [person + year]
```

## Nested Flashcard Prompt
```
Where appropriate, chain cards together:
* What is [main concept]? == [summary]
* What are the key parts of [main concept]? == [list]
* What does [part A] do? == [function]
```

## Debate Prompt
```
Frame cards as contrasting arguments:
* What is the argument for [position]? == [summary]
* What is the counterargument? == [response]
```

## Timeline Prompt
```
Turn sequences into flashcards:
* What happened before/after [event]? == [next event]
* Place these in order: [A, B, C] == [correct sequence]
```

## Fill-the-Gap Prompt
```
Create cloze-style flashcards:
* The _______ is responsible for regulating hunger. == hypothalamus
* [Concept] was first proposed by _______. == [name]
```

## Question Explosion Prompt
```
For every paragraph, generate:
1. One factual card
2. One “why” card
3. One “what if” card
4. One comparison or connection card
```

## Sensory Anchor Prompt
```
Turn abstract content into sensory memory aids:
* If [concept] were a smell/sound/image, what would it be? == [sensory hook]
* What does [process] feel like metaphorically? == [sensory simile]
```

## Contradiction Prompt
```
Create cards that test apparent contradictions:
* Why does [thing] seem to contradict [other thing]? == [reconciliation]
* What’s misleading about saying “[simplified claim]”? == [clarification]
```

## 3-Tier Prompt
```
For every idea, generate:
1. Beginner question
2. Intermediate question
3. Advanced synthesis question
Example:
* What is [concept]? == [definition]
* How does [concept] function? == [process]
* How could [concept] be extended to [new domain]? == [insight]
```

## Misconception Prompt
```
Create flashcards that clarify common misunderstandings:
* What’s a common mistake about [topic]? == [misconception]
* Why is that incorrect? == [correct explanation]
```

## Research Context Prompt
```
For studies or findings:
* Who conducted the study on [topic]? == [researcher + year]
* What was the main finding of [study]? == [result]
* How was the study done? == [method summary]
```

## Layman Conversion Prompt
```
Turn technical explanations into RemNote cards written in simple language, like you’re explaining to a 12-year-old.
* What is [concept]? == [simple, clear explanation]
```

## Comedy Layer Prompt
```
Add a light joke or pun after each answer to improve recall.
Example:
* What causes ATP synthesis? == Proton gradient.  
  Bonus: It’s all uphill work until you hit the spin cycle.
```

## Dynamic Process Prompt
```
For every dynamic process, create:
1. Sequence card
2. Feedback loop card
3. Failure/disruption card
Example:
* What are the steps of [process]? == [1, 2, 3]
* What regulates [process]? == [mechanism]
* What happens if [step] fails? == [effect]
```

## Ask-and-Extend Prompt
```
After each flashcard, imagine the next logical question.
Write a follow-up card for it.
Example:
* What is glycolysis? == The breakdown of glucose to pyruvate  
* What happens after glycolysis? == Pyruvate enters the Krebs cycle
```

## Micro-Debate Prompt
```
Write two micro-cards on each controversial idea:
* One pro
* One con
Use these to rehearse critical thinking.
```

## Memory Hook Prompt
```
Include memory aids in each answer:
* What is the function of the cerebellum? == Coordinates movement (Think: "Balance Bell")
* What’s the function of ACTH? == Stimulates cortisol (C for Cortisol, A for Adrenal)
```

## Hypothetical Challenge Prompt
```
For each major concept, write:
* What would change if [key condition] were different? == [consequence]
* How would [system] work in reverse? == [description]
```

## Intuition-First Prompt
```
Before giving the technical answer, write:
* What would your intuition say about [X]? == [misleading guess]  
* What’s the actual explanation? == [truth]
```

## Socratic Prompt
```
Ask layered questions that lead to deeper insights:
* What is [concept]? == [definition]
* Why does it work that way? == [reason]
* What assumption underlies that? == [premise]
* Could it be otherwise? == [exploration]
```

## Perspective Swap Prompt
```
Reframe content from alternate viewpoints:
* How would a chemist view [topic]? == [explanation]
* What would a philosopher say about [problem]? == [interpretation]
* How would this look to an AI system? == [algorithmic framing]
```

## SuperSimple Prompt
```
Reduce the entire document to 10 must-know facts.
Each becomes:
* What’s one essential fact from this document? == [fact]
```

## SuperDense Prompt
```
Try to compress 3–5 related concepts into a single flashcard.
Example:
* How do [A], [B], and [C] work together in [system]? == [brief synthesis]
```

## Future Scenario Prompt
```
Use flashcards to apply concepts in futuristic or speculative settings:
* How might [concept] be used in 2050? == [projection]
* What ethical concerns arise if [technology] becomes common? == [discussion point]
```

## Curriculum Builder Prompt
```
Create a structured flashcard set that could serve as a full mini-course based on this document.

For each major section:
1. Identify its learning objective
2. Create 3–5 flashcards for each of the following:
   - Key definitions
   - Core mechanisms or processes
   - Comprehension checks
   - Applied reasoning or case-based inference
   - Common misconceptions

Structure the flashcards in logical learning order.
Use headings like ## [Topic Name].

Format: * question == answer
```

## Research Deep Dive Prompt
```
Generate flashcards that walk through the research methods, findings, and implications described in the text.

1. Identify each study, experiment, or data analysis mentioned
2. For each, make cards on:
   - The research question
   - The methodology
   - The findings
   - The limitations
   - The interpretation
   - The real-world implications
3. If applicable, generate one synthesis card combining multiple studies

Use format:
* What was the goal of [study]? == [summary]
* How was it conducted? == [methods]
* What were the results? == [findings]
```

## Evolution & Change Over Time Prompt
```
For any historical, scientific, or philosophical progression in the document:

1. Identify key stages or turning points
2. Create cards that test recall of those stages
3. Include flashcards that ask:
   - How did [concept] evolve over time?
   - What caused the shift from [state A] to [state B]?
   - What are the implications of these changes?

Use temporal ordering and include at least one timeline recap card.
```

## Mechanism Builder Prompt
```
Build flashcards that teach systems and mechanisms layer-by-layer.

For each complex process:
1. Write a top-level overview card
2. Write 3–6 cards for internal steps, components, or interactions
3. Write follow-up cards testing understanding of:
   - Regulation or feedback
   - Disruption or failure
   - Applications in real life

Format:
* What is the function of [system]? == [overview]
* What are the steps in [process]? == [1, 2, 3...]
* What happens if [step] fails? == [consequence]
```

## Analytic Decomposition Prompt
```
Turn dense or complex arguments into flashcards that unpack them.

For each paragraph or argument cluster:
1. Identify the conclusion
2. Identify the assumptions
3. Identify the evidence or logic used
4. Create cards that ask:
   - What is the main claim here?
   - What is this based on?
   - Is the reasoning valid? Why or why not?

This is useful for philosophy, law, policy, and theoretical texts.
```

## Conversational Rephrasing Prompt
```
Convert dense academic content into flashcards that simulate a tutor-student dialogue.

For each section:
1. Restate concepts in plain English
2. Ask questions that feel like you're being tutored
3. Include follow-ups that clarify tricky ideas

Example:
* Tutor: Can you tell me what [term] means? == Student: It means [definition].
* Student: Wait, why does [X] lead to [Y]? == Tutor: Because [explanation].
```

## Advanced Synthesis Prompt
```
Force higher-order thinking through flashcard chains that build toward synthesis.

For each topic:
1. Start with fact cards
2. Add relationship or comparison cards
3. Add application cards
4. End with synthesis cards:
   - How do A, B, and C interact?
   - What new insight do they generate?

This structure scaffolds thinking.
```

## Argument Reconstruction Prompt
```
If the text makes an argument or presents a model/theory:

1. Break it into premises and conclusion
2. Create flashcards for each:
   * What is the claim? == [Conclusion]
   * What are the premises? == [P1, P2, P3]
   * What supports [premise X]? == [Evidence]
3. Add criticism cards:
   * How could someone challenge this argument? == [Counterpoint]
```

## Dynamic Systems Prompt
```
If the document contains dynamic systems (biological, economic, computational...):

1. Identify each key component and its role
2. Map out inputs, outputs, feedback, and interactions
3. Create flashcards like:
   * What does [component] do? == [function]
   * What affects [output variable]? == [influences]
   * What would change if [factor] increases? == [response]

Include stability, feedback, and edge-case questions.
```

## Dual-Side Understanding Prompt
```
For each topic or idea, create both:
1. A forward card: * What is [concept]? == [definition]
2. A reverse card: * [definition] == What concept is this?

Then, go deeper:
3. * How would you identify [concept] in the wild? == [observation]
4. * What are examples and non-examples of [concept]? == [comparison]
```

## Case-Based Reasoning Prompt
```
Simulate test scenarios using examples and problems.

For each major concept:
1. Create an example scenario
2. Ask: What’s going on here? == [diagnosis]
3. Ask: What would you do next? == [application]
4. Ask: What principle is illustrated here? == [concept]

Add edge-case twists to test transfer.
```

## Socratic Progression Prompt
```
Unpack complex concepts through a guided reasoning sequence.

For each idea:
1. Start with: * What is [X]? == [definition]
2. Then: * Why does [X] matter? == [implication]
3. Then: * What must be true for [X] to work? == [assumptions]
4. Then: * When would [X] not apply? == [limits]
5. Finally: * How could [X] evolve or be improved? == [innovation]
```

## Empathy & Stakeholder Prompt
```
In documents about policies, ethics, or impact:

For each major decision or effect:
1. Identify affected groups
2. Create flashcards that ask:
   * How does [group] experience [policy/event]? == [perspective]
   * What are the benefits for [stakeholder A]? == [gain]
   * What are the tradeoffs or losses? == [cost]
```

## “From Scratch” Prompt
```
Pretend none of this material existed yet. You’re designing it from first principles.

1. Why would someone even care about this? == [motivation]
2. What’s the core problem this addresses? == [need]
3. How might one intuitively solve it? == [naive approach]
4. How is the real solution better? == [actual concept]
5. Where could this go next? == [future extension]
```

## Integrated Flashcard Suite Prompt
```
Build an entire flashcard suite that includes:

- 📘 Core concepts (definitions, examples)
- 🧠 Thought questions (why/how)
- ⚖️ Comparisons (X vs Y)
- 🧪 Applications (when to use)
- 🧯 Exceptions or warnings (when NOT to use)
- 🎯 Mnemonics or memory aids
- 💡 Surprising facts or analogies
- 🧵 Summary flashcards (one card to explain them all)

Format each as:
* [Question] == [Answer]
And organize in logical learning order.
```

## High-Yield Test Drill Prompt
```
Create flashcards ONLY for the concepts most likely to appear on a test.

1. Skim the document and extract:
   - Definitions that are bolded, repeated, or highlighted
   - Common formulas or relationships
   - Step-by-step processes
   - Cause-effect chains

2. For each, create:
   * What is [term]? == [definition]
   * How do you apply [formula/concept]? == [use-case or example]
   * What are the key steps of [process]? == [step-by-step]
```

## Application Practice Prompt
```
Generate flashcards that test application of core concepts to real scenarios.

For each idea:
1. Create at least one card like:
   * How would [concept] apply to [specific case]? == [application]
2. Add "twist" cards:
   * What happens if [assumption] changes? == [updated result]
   * What’s the exception to [rule]? == [edge case]
```

## Most Common Confusion Prompt
```
Focus on areas where students often get tripped up.

1. Identify terms with similar names or overlapping meanings
2. For each, write contrast cards:
   * How is [A] different from [B]? == [difference]
   * What’s the easy way to remember [A] vs [B]? == [mnemonic or tip]
3. Include cards that correct subtle errors or false assumptions
```

## Predict-the-Question Prompt
```
Read the document and imagine what the teacher would ask.

For each section:
1. Write cards like:
   * What’s a likely exam question about this topic? == [exact question phrasing]
   * What’s the correct answer? == [concise, well-phrased answer]
   * What would be a trap answer, and why is it wrong? == [clarification]
```

## Reverse Engineering Prompt
```
Take the answers and work backward.

1. Extract key answers or results
2. For each, create:
   * What question could lead to this answer? == [constructed question]
   * Why is this the best answer? == [justification]
```

## Past-Paper Mimic Prompt
```
Simulate past paper questions.

1. Turn each topic into the kinds of cards that show up on real exams:
   - MCQ-style choices
   - Short-answer precision recall
   - Process tracing
   - Argument evaluation
   - Data interpretation (if applicable)

Example:
* What are the three types of [X]? == [Type A, B, C]
* Which of the following best explains [Y]? == [correct answer] (with distractors)
```

## Diagram-Based Recall Prompt
```
If the document has visuals or systems:

1. Create cards that test diagram-literate recall:
   * Label this diagram == [term]
   * What’s missing in this sequence? == [step]
   * How does [element] affect [output]? == [link]

Bonus: draw the diagram from memory after reviewing the cards.
```

## Rapid Round Review Prompt
```
Generate 30–40 short, fact-based flashcards covering the WHOLE document.

No multi-sentence answers. No context. Just pure, clean, testable facts:
* What is [term]? == [fact]
* What does [enzyme] do? == [function]
* What’s the equation for [thing]? == [equation]

This is your cram deck.
```

## Chain-of-Reasoning Prompt
```
Simulate questions that require logical sequences.

For each process or chain:
1. Break it into steps
2. Create cards that ask:
   * What’s the next step after [X]? == [Y]
   * Why does [A] lead to [B]? == [mechanism]
   * If [step] fails, what happens? == [effect]
```

## “Trick Question” Defense Prompt
```
Generate cards that prepare you for misleading test questions.

1. Identify common misunderstandings
2. For each, write:
   * This looks right, but why is it wrong? == [explanation]
   * What’s the trap here? == [clarification]
   * What does this test that isn’t obvious? == [deep principle]
```

## High-Efficiency Flashcard Funnel Prompt
```
Turn this document into three tiers of cards:

- 🔹 Tier 1: "If you forget this, you fail" cards (core definitions, laws)
- 🔸 Tier 2: "Will probably be on the test" cards (standard application)
- 🔺 Tier 3: "Makes you stand out" cards (synthesis, extension, edge-cases)

Use headings like:
## Tier 1: Core Survival Knowledge
* What is [X]? == [definition]

## Tier 2: Test Likely Concepts
* How does [X] apply in [situation]? == [answer]

## Tier 3: Advanced Mastery
* What’s a subtle insight about [X]? == [nuanced point]
```

## Elimination-Style Thinking Prompt
```
Mimic MCQ logic by generating cards that force you to eliminate bad options.

For each:
* Which of these is NOT true about [topic]? == [one false statement]
* Which of these would BEST support [claim]? == [strongest choice]
* Eliminate two incorrect interpretations of [data]? == [explanation]
```

## Compare-Classify-Contrast Prompt
```
Organize your flashcards like a matrix.

For each group of related terms:
1. Create compare cards: * How is A different from B? == [difference]
```

## Compare-Classify-Contrast Prompt
```
Organize your flashcards like a matrix.

For each group of related terms:
1. Create compare cards: * How is A different from B? == [difference]
2. Create classify cards: * Is X a type of Y? == [yes/no]
3. Create feature-recognition cards: * What features define [category]? == [list]

This builds clean mental taxonomies.
```

## Test-Taking Strategy Prompt
```
Create flashcards that train you to identify:
- Keywords
- Scope
- Triggers for particular answers

Example:
* If a question says “always,” what should you be cautious of? == Absolutist language trap
* If a question starts “according to the passage,” what’s required? == Text-based answer only
```

## Exam Day Simulation Prompt
```
Generate 10–15 cards that simulate what you’ll face under pressure.

- Some should be easy to boost confidence
- Some should be multi-step reasoning
- Some should use tricky phrasing
- Time yourself while answering

Format each card:
* [Simulated exam-style question] == [correct answer + brief explanation]
```

## Fill-in-the-Framework Prompt
```
If the document includes a model, taxonomy, or set of categories:

1. Create flashcards to:
   * Complete missing pieces
   * Label parts
   * Test examples vs non-examples

Examples:
* What are the components of [model]? == [A, B, C]
* Which of these fits [category]? == [correct item]
```

## Score-Booster Prompt
```
Create cards that cover what *other students* will probably miss—but you won’t.

1. Edge-cases
2. Secondary effects
3. Unusual terminology
4. “Boxed” sidebar material or footnotes
5. End-of-chapter integration summaries

* What’s a common mistake in [topic]? == [mistake]
* What do most students forget about [idea]? == [detail]
```

## Triple Threat Prompt
```
For each topic:
- Write 1 fact-recall card
- Write 1 application card
- Write 1 integration card that links it to another topic

Example:
* What is [concept]? == [definition]
* How do you apply [concept]? == [application]
* How does [concept] relate to [other concept]? == [relationship]

This strengthens all three exam skills: recall, transfer, and synthesis.
```
