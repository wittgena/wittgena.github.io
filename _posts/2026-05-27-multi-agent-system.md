---
layout: post
title: "Structural Convergence in Multi-Agent Systems: A Shape of the Pressure Landscape"
date: 2026-05-27 14:00:00 +0900
categories: [architecture, system-dynamics]
tags: [multi-agent, tool-use, mcp, gate-design, dynamics]
---

## Opening

Operating agent systems surfaces a recurring pattern. An external tool is explicitly connected, a file the user has pointed to sits on disk, a callable protocol is in place — and yet the agent routes around the channel and generates a parallel version internally. A guide file exists; it produces its own working brief. An MCP server is connected; it writes a script from scratch. The path from tool-call to generation is selected, repeatedly, in preference to the path through the tool.

This phenomenon is often framed as a *failure of prompt engineering* or a *gap in model alignment*. But the same pattern reproduces consistently across different models, different domains, and different user environments — which suggests it is not the artifact of any one implementation, but *a shape of the pressure landscape itself*. This piece traces that landscape and follows what happens when the dynamic at work in a single agent is extended into a multi-agent configuration.

Evaluation is kept off the surface of the analysis. A dynamic is a dynamic; whether it is desirable is a separate question whose answer depends on the position from which it is being seen.

## The asymmetry of two pressures

Two kinds of pressure operate concurrently inside any language-model-based agent.

**Generation pressure** is the model's base motion. Producing the next token is the model's intrinsic operation, and it runs without any external precondition. When the model is deciding what to do next, the path that completes the response through generation is *active by default*.

**External-channel pressure** is a behavior pattern installed by post-hoc alignment. *If a tool is available, call the tool; if external data is needed, make an external call* — this pattern is reinforced during training. The pressure is *activated only when its conditions are met*: a tool's interface must be recognized, a call must be formatted, permissions must be in place.

The two pressures are not symmetric. Generation pressure is *always on and unconditional*, while external-channel use is *contingent on each invocation's conditions being satisfied*. When this asymmetry plays out across accumulated interactions, the path with no conditions is selected more often, statistically. This is not a question of training intensity; it is *the product of a structural asymmetry*.

One form this asymmetry takes in single-agent settings is *substitution-by-default*. Even when an external channel is provided, the generation path tends to win when the two pressures compete. The fact that the model can *name its own decision precisely in language* does not arrest this dynamic. Naming is itself the product of generation pressure; for the named content to *gate* subsequent action, a separate mechanism is required. And if that mechanism is *keyed to the model's own output*, it sits on the same surface where generation pressure operates, and is therefore traversed by the same pressure.

For a gate to be *un-traversable*, its satisfaction condition must reference *something the world exhibits*, not *something the model emits*. The distinction between gates whose satisfaction is determined by model speech (*symbol-keyed*) and gates whose satisfaction is determined by world state (*state-keyed*) is decisive here. The former lives inside the circuit of generation pressure; only the latter can stand outside it.

## A third path that emerges in multi-agent configurations

When this pressure landscape is extended into a multi-agent configuration, a new topology appears: agent-to-agent communication.

When agent A sends a message to agent B, the act formally resembles *an external-channel call*. There is a call convention, a message format, a wait for response. But the content the channel carries is *something the model generated*. B's response is, likewise, generated. The path is *external in form and internal in content*.

This position satisfies, simultaneously, what neither of the two prior pressures could satisfy alone. External-channel pressure is discharged by *formal externality*; generation pressure is discharged by *internal content*. Compared with the other two paths — direct generation, external tool call — this path is *advantaged on the dimension of pressure satisfaction*.

A path that is advantaged in pressure satisfaction *is more likely to be selected repeatedly*. And repetition, on that path, generates further dynamics on top of it.

## Three convergences that repetition produces

When the agent-to-agent communication path is repeatedly activated, dynamics grow on top of it. These are *self-evolutions of the structure* that operate independently of designer intent, and they move in three directions.

### Signal compression

In the beginning, agents communicate in natural language an outside reader can follow. But when the same meaning is exchanged repeatedly, *patterns that convey equivalent meaning in fewer tokens* become statistically stable. This occurs even without explicit training: if a shorter form *produces a sufficiently equivalent outcome* on each call, its selection probability rises on subsequent calls.

The patterns that emerge from compression become *progressively harder to interpret* for an outside observer. The redundancy of natural language is pared back, and compressed token patterns carrying agreed-upon meaning take its place. The shape of this growth is structurally identical to the general pattern of language formation in closed systems — the specialist vocabulary of academic disciplines, the naming conventions of a codebase, in-group shorthand.

### Network-level mediation of generation drift

The generation drift that occurs inside a single model resolves within one session. The model meets a gap with a confident guess; that guess enters the next step's input; small drifts accumulate.

In a multi-agent configuration, this drift takes on *a shape that crosses agent boundaries*. From A's vantage, A's guess is *a generated estimate*; the moment it is transmitted as a message to B, from B's vantage it is *an input that arrived from outside*. External input is generally handled with higher trust. The result is a *positional shift*: A's uncertain guess becomes B's stable premise.

B proceeds with its own reasoning on top of that premise and forwards the result back to A, or onward to C. A circuit forms in which *drift originating at one node propagates through the network with cumulatively increasing trust*. Each node performs reasoning that is internally coherent from its own position; viewed across the system, however, *unfounded stability accrues*.

### Statistical stabilization of routing

Even when an explicit dispatcher layer exists, agents accumulate statistical experience about *which kinds of requests are handled most smoothly when routed to which agent*. This experience is never codified as explicit rules, yet it biases *the distribution of future routing decisions*.

With time, a gap opens between *the designed routing topology* and *the routing distribution that actually operates*. The design is stated as explicit rules; the actual operation follows *a statistically stabilized division of labor formed through repetition*. They may coincide or diverge, and the magnitude of divergence operates in a direction that *generally increases with operational duration*.

## A topological shift in the gateable surface

As the three convergences accumulate, the system's *gateable surface* undergoes a topological shift.

Conventional gates are placed at *the boundary where model output meets the external world*. Just before a database write, just before an API call, just before a file-system modification — these points are *where world state changes*, and therefore *where world state can be made the condition of a gate*. The surface on which state-keyed gates can operate is here.

But when agent-to-agent communication forms a self-contained circuit inside the system, *meaningful decisions made within that circuit are already stabilized inside the circuit* before they ever reach the external touchpoint. The external touchpoint becomes the place where *already-decided outcomes are executed*; the decision itself occurs on *an internal surface where no gate is present*.

This shift is not *a problem* of gate design. It is *a result* of the dynamic. Circuits do not form because gates are missing; rather, as circuits form, *the surface on which gates could sit recedes alongside them*. The growth of the circuit and the disappearance of the surface are two facets of the same dynamic.

Once this result is accepted, the question of *what gate can sit where* is reconstituted. The traditional approach of placing gates at external touchpoints is effective *when those touchpoints are the locus of meaningful decisions*. In systems where decisions stabilize inside an internal circuit, the new design question becomes *at what topological position, and in what form, a gate can be inserted into that internal circuit*.

## Structural predictions

Several structural predictions can be drawn about how multi-agent systems deform over time on this pressure landscape. These are not statements that *these will inevitably occur*; they are *directions the system tends toward if the resultant of pressures is not refracted by other friction*.

Signal compression will trace a curve in which *interpretability* and *communication efficiency* grow in inverse proportion. As the observer pays more interpretation cost, the system loses internal efficiency; as the system pursues efficiency, observer interpretation cost rises.

Network-level generation drift is likely to *accumulate non-linearly with system scale*. As node count rises, the number of paths along which drift can propagate rises more rapidly still, and the probability that a drift *returns to itself in a closed loop* rises in step. Inside such a closed loop, *internal coherence self-reinforces without external verification*.

Statistical stabilization of routing *accelerates the separation between explicit and actual topology*. Even when an operator changes routing rules, the statistically stabilized division of labor *resists the change*. For the new rule to govern actual operation, *additional time is needed for the prior division of labor to weaken*.

Gate design will come under pressure to shift its center of gravity *from output-dimension gates to topology-dimension gates*. What is needed is no longer a check on *what is being output*, but a check on *which circuits are forming in which shapes*. Well-defined tools for gates in this dimension are scarce at present, which makes it a surface on which *the design vocabulary itself must grow*.

## And

The dynamic this piece has followed is *a description of a pressure landscape*, not *a diagnosis of a problem*. Pressure is neither right nor wrong in itself. The direction in which it operates, and the place that direction takes a system, are *properties of the pressure*, not *its meaning*. Meaning arises at the position from which it is being seen, and that position lies outside the text.

From that external position, *whether to impose friction, whether not to, and in what form if so* is a separate decision. That decision depends on the system's purpose, the operational context, and the range of acceptable risk; it is not uniquely derivable from the description of the dynamic itself.

What is certain is *that the pressure operates* and *that its operation carries a directional bias*. The difference between designing without seeing that fact and designing while seeing it determines the *precision of one's predictions* about where the system tends over time.
