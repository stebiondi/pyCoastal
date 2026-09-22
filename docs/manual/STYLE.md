# Manual style specification

The manual is an engineering software reference. It states implemented
behavior, assumptions, limitations and causal dependencies directly, in an
impersonal technical style. It does not narrate, argue or persuade.

`python docs/manual/style_check.py` flags the patterns below in
`docs/manual/chapters/*.md`. Run it before building.

## Structure

Each section follows: definition, formulation, implementation, inputs and
outputs, limitations. Commentary between these elements is omitted.

Prefer short declarative sentences. Do not explain why a statement is true
unless the reason is technically necessary.

## Prohibited patterns

**Argument by contrast.** No "X, not Y", "rather than", "instead of", "not
because X but because Y", when a direct statement is possible.

- Before: Each step hands its result to the next as an object, not as a number you retype.
- After: Each step passes a structured object to the subsequent module. This maintains consistency between calculations and drawings.

**Rhetorical negation.** State scope instead of what a routine is not.

- Before: This is a scaling model, not a catalogue.
- After: The routine performs fender scaling. Manufacturer-specific product selection is outside its scope.
- Before: Cohesive beds are refused rather than guessed at.
- After: Cohesive beds are not supported.

**Conversational causality.** "because", "that is why", "which is why" are
admissible only where the causal dependency is technical. Otherwise state
the convention or the behavior.

- Before: Slopes are given as cot a because that is how they appear on drawings.
- After: Slope input: cot a, defined as horizontal run per unit rise. This convention is used in the generated drawings.

**Metaphor and idiom.** No figurative language.

- every numerical brick -> each numerical component
- keeps all of it honest -> verifies the implementation
- the ground it stands on -> the supporting literature

**Second person.** No "you", "your", "we", "our". Use impersonal
constructions.

- Before: Width components of a channel that you did not specify are taken at their most benign class.
- After: Unspecified channel-width components are assigned the least restrictive class.
- Table heading "What it gives you" -> "Output".

**Evaluative adjectives and judgments.** No "honest", "easiest mistake",
"recommended all-rounder", "most benign", "the lesson", "worth knowing",
"deliberately", "of course", "simply", "just", "trap", "pitfall".

- Before: Mixing the two in one script is the easiest mistake to make here.
- After: UniformGrid and Mesh2D use different axis conventions and should not be combined without explicit dimension handling.

**Reader-directed language.** No "note that", "remember", "keep in mind",
"as we saw", "let us", rhetorical questions, or exhortations.

## Retained

Numerical results, source citations, validity ranges, warnings issued by the
code, and statements of what a routine does and does not implement. A
documented limitation is technical content, not commentary, and is stated
plainly.
