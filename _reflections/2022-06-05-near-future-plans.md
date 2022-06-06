---
layout: post
age: 21.58
title: 📌 near future plans
---

## 📌 near future plans

It's early June 2022. I plan on making a few changes to my focus, approach, and online presence in the near future, and thought it'd be nice to pin an orienting post during this transition period. Everything below has an implicit "maybe" attached to it which grows in strength with time.

First, I'll be wrapping up my thesis on language model interpretability this month, and will post an accompanying write-up in the style of my previous projects. Then, I'm excited to share I'll be joining [Refine](https://www.alignmentforum.org/posts/D7epkkJb3CqDTYgX9/refine-an-incubator-for-conceptual-alignment-research-bets), a three-month fellowship hosted by [Conjecture](https://www.lesswrong.com/posts/jfq2BH5kfQqu2vYv3/we-are-conjecture-a-new-alignment-research-startup) in London (mostly Aug-Oct) to try my hand at conceptual alignment research. This new program is meant to explore new framings for the AI alignment problem through a small cohort which is only vaguely familiar with the status quo in the field. Counterintuitively, it's a situation in which lack of experience actually seems useful as a high-temperature state of mind which hasn't yet collapsed [the superposition of approaches](/reflections/conceptual-foraging-intuitions).

> "It’s not just that we don’t have the answers; we don’t even have the right frames for thinking about the problems. AI alignment is largely a problem which hasn’t happened yet, on technology which hasn’t been invented yet, which we nonetheless want to solve in advance. Figuring out the right frames - the right paradigm - is itself a central part of the job." -- [John Wentworth](https://www.alignmentforum.org/posts/P3Yt66Wh5g7SbkKuT/how-to-get-into-independent-research-on-alignment-agency#Preparadigmicity)

The output of my work at Refine will probably live on [LessWrong](https://www.lesswrong.com/) or the [Alignment Forum](https://www.alignmentforum.org/), rather than natively on my blog, as that's where most alignment folks are. A glimpse at a few framings I'll develop/discard/remix during the program:

- **deontic arrays**: Using sets of discrete structures (e.g. attractors, repellers, dipoles, etc.) to nudge language models [across model and latent space](/reflections/structure-and-function), similar to the [deontic dipoles](/thoughtware/deontic-dipoles) project I recently published. In this framing, alignment sounds like [DeepMind's real-time control of plasma based on a set of magnets](https://www.deepmind.com/blog/accelerating-fusion-science-through-learned-plasma-control).
- **latent resonators**: Using filters to make human-friendly dynamics resonant while muffling others. In this framing, alignment sounds like leaving out undesirable spectral components of the autoregressive signal.
- **ergonomic constraints**: Enforcing cognitive ergonomics constraints on hidden layers so that even if not instantly interpretable, people could still learn the [logogram-like](/reflections/logogram-alchemy) language employed by the model. In this framing, alignment sounds like having [people become fluent in the model's own representations](/reflections/translation-is-pervasive).
- **memetic extrapolation**: Attempting to evolve coherent belief systems through a debate-like adversarial setup, so that we can take into account the evolving nature of our values when aligning systems to them. In this framing, what we align _to_ is implicitly a moving target, though one consistent with our current selves.

However, despite the fact that I'm excited about polishing my thesis and working on new conceptual framings at Refine, I'm even more excited about related informal projects I'll continue to pursue full-time between the two (July, Romania), in my spare-time during the fellowship (Aug-Oct, UK), and full-time again after it (Nov-, Italy). This is the meat of the change, and hence the highlight of this interim post.

For about a year and a half now, I've been [tinkering with experimental ML tools](/thoughtware) and [musing about their implications](/reflections). The focus was on artifacts at the intersection of ML and tools for thought.

However, as a next chapter or stage, I'm now planning on exploring **creatures**, **organisms**, and **specimens** which are native to computational **habitats**, **ecosystems**, and **environments**. They'll be more agents than tools, and will explicitly integrate **organic** principles: coevolution, self-organization, competition for [(representational) resources](/reflections/representational-resources), etc. More scattered details from a past sponsor update:

This **cybernetic** **sanctuary** (alternatively: The Garden of [Egan](https://www.gregegan.net/), New [Cambria](https://en.wikipedia.org/wiki/Cambrian_explosion)) will be hosted as a self-contained website at a subdomain of my personal one. The creatures will be experimental AIs which you can interact with via custom interfaces. A few creature sketches:

- competing memetic **colonies** of coherent ideas preying on opposing memeplexes, supported by a language model trained on self-play debate. (related to "memetic extrapolation" above)
- a **swarm** of beetles which have presumably evolved to process their surroundings via local chit-chat among neighbors in a lattice, each individual being a symbol in an artificial self-organizing language. (related to "ergonomic constraints" above)
- an acoustic **organism** whose resonance chamber can be morphed using a host of operators (e.g. style interpolation, Boolean ops). (related to "latent resonators" above)
- a **population** of texts evolving via [BERT replacements](https://huggingface.co/tasks/fill-mask) towards solving certain constraints. It feels to me a bit like [Prolog](https://en.wikipedia.org/wiki/Prolog) for natural language (e.g. X lives in Y. X is a member of Z.), a bit less agentic.
- a few virtual **animals** world-optimizing a 2D/3D gym environment to their will, plus mediator agents trying to displace the Nash equilibria and push for maximal social welfare instead.

The **habitat** the creatures will be living in will consist in the compute cluster I'll set up at home. As inspiration, I can quote Egan's various computational creatures and habitats (e.g. Diaspora's Polises and Wang Tiles, Permutation City's Autoverse and Permutation City, etc.). In terms of aesthetic, I'll go with vintage **botanical** prints: typical typography, deteriorated paper, illustrations of creatures, occasional Victorian phrasings. My current blog will likely evolve into the sanctuary's chronicle, with rarer but longer-form content. Also, how about botany/botanist, but with bots?

Finding this setup/framing/metaphor felt like a search for an instantiation of a mental model I wanted to use, a bit like the "population of texts" creature sketch. Another framing I entertained briefly was a mythological, rather than organic one. The pantheon of legendary computational creatures would populate some mythical realm. The organic framework seemed more potent, suitable, and socially acceptable in the end.

It also represents a shift from the forward-chaining approach to learning by following a curriculum to a backward-chaining view based on building towards a creature-project. However, I want to implement them relatively from scratch, extending a [minitorch](https://minitorch.github.io/) replica to contain basic transformer blocks and parallelism, on top of self-hosted git, CI/CD, etc.

The whole thing will probably feel either really cool or really silly in the end, but if not during a gap year, then when? Seize the day!
