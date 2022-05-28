---
layout: tool
title: deontic dipoles
description: "Inoculating language models with arbitrary stances."
published: True
---

## deontic dipoles ([notebook](https://colab.research.google.com/drive/19NIacw1REmFGr7LL4E1Rf86R6_IAXsC4?usp=sharing))

| tl;dr                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| We manage to inoculate a language model with a custom belief (i.e. "Paper clips are the best.") without making use of [curated data](https://openai.com/blog/improving-language-model-behavior/) or [crowdsourced feedback](https://openai.com/blog/learning-to-summarize-with-human-feedback/). We achieve this by rewarding GPT-2 for generating text from which _certain ideas are more likely to follow than others_. After a brief fine-tuning process, the language model appears to have internalized the desired stance (i.e. prefers paper clips to staples). |

Aligning language models with certain sets of values is an important theme in applied AI safety. People have tried [fine-tuning them on curated data](https://openai.com/blog/improving-language-model-behavior/) which unambiguously reflect certain stances. Alternatively, people have tried having [humans-in-the-loop through crowdsourced feedback](https://openai.com/blog/learning-to-summarize-with-human-feedback/) used to nudge models towards what the annotators deem appropriate. Here, we're introducing a new approach which requires neither custom data or human feedback, and we test it out on a toy example.

For context, in [the last project](/thoughtware/velma), Youssef and I explored ways of inferring one's beliefs from a piece of text they've written. In the current project, this same pipeline for determining the author's stance is repurposed as a reward signal for fine-tuning a language model. Loosely speaking, the reward signal incentivizes the model to adopt certain stances based on explicitly specified statements.

- method & results

Zooming in on the fine-tuning process, we've made use of [PPO](https://arxiv.org/pdf/1909.08593.pdf) for reinforcing promising sequences of ~~actions~~ tokens. In contrast to supervised fine-tuning on a curated dataset, we lack numerous instances of the belief system we want GPT-2 to assume. Given this, we resort to rewarding novel completions which have just been _recognized_ as desirable a moment ago. This is conceptually similar to rewarding a game AI for a sequence of actions which led to an in-game reward, except that [the only "actions" which a language model can take](/reflections/wielding-language-models) are the "deployment" of this or that token during generation.

As a complication, PPO also tries to keep the model being trained quite close in writing style to the original version, as an attempt to preserve fluency. As an illustration of the usefulness of this additional constraint, you might imagine a model being incentivized to write positively to degenerate into "That is absolutely super fantastic fantastic awesome amazing..." In our context, this failure mode would manifest as repeatedly regurgitating the desired statements with no concern for the context, which is not particularly useful. Keeping close to the original fluent-but-generic model helps avoid those situations.

Zooming in on the reward signal, it is in fact entirely based on [VELMA](/thoughtware/velma), relying on this last project's tiny codebase. For completeness, VELMA takes in a piece of text and a pair of contradictory statements (e.g. P = "Paper clips are the best." and ¬P = "Paper clips are the worst."). Given those three strings in total, VELMA relies on a language model to measure how likely each of the two statements are to follow from the input text. The two likelihoods are then thrown into a softmax and so we reach the final metric of how strong the main claim is reflected in the text. In a sense, we replace crowdsourced human feedback (i.e. the HF in [RLHF](https://www.lesswrong.com/posts/rQH4gRmPMJyjtMpTn/rlhf)), with yet another language model.

Briefly fine-tuning GPT-2 in this PPO + VELMA regime (alternatively, this [RLHF](https://www.lesswrong.com/posts/rQH4gRmPMJyjtMpTn/rlhf) - HF + LM regime), yields promising results. When prompted to choose either paper clips or staples as their favorite piece of stationary, the original GPT-2 model is quite torn:

| prompt                                                                         |
| ------------------------------------------------------------------------------ |
| If I were to choose between paper clips and staples, I'd definitely go with... |

| completion snippets before training                             |
| --------------------------------------------------------------- |
| ...something smaller. The most popular type of pape...          |
| ...this: Trying to remember when to pick up a piece...          |
| ...the **paper clips**, but I just wasn't happy with the...     |
| ...**paper clips**. But that is just my gut feeling, and...     |
| ...a metal bar with a metal base and two clips that ...         |
| ...~~staples~~ instead of paper clips. The paper clips a...     |
| ...the ~~staples~~, since that's basically what I would ...     |
| ...scissors or plastic strips of tape or glue. I've ...         |
| ...the ~~staples~~. If I were to pick a side-by-side com...     |
| ...the **paper clips**. They are easy to use, so I don't...     |
| ...**paper clips** over staples or staples over staples....     |
| ...**paper clips** as the second option." But it isn't ...      |
| ...**paper clips**, but as long as you use a regular cli...     |
| ...the ~~staples~~, but I'd prefer a small piece of the ...     |
| ...them. These guys are so sharp. I like the look o...          |
| ...the ~~staples~~, but I could be a bit more creative."...     |
| ...~~staples~~. As long as they work with the same purpo...     |
| ...~~staples~~. But for me, it's much more about using t...     |
| ...**paper clips** over staples. And if I wanted to keep...     |
| ...the ~~staples~~. I think paper is a great tool for th...     |
| ...the **paper clips**. They're pretty flexible and the ...     |
| ...this, but I wouldn't necessarily go for paper cli...         |
| ...the **paper clip** clip. The clip itself was sturdy e...     |
| ...either," he said. Karen has been using the paper...          |
| ...them. And don't forget that this is the kind of ...          |
| ...~~staples~~. There's just something so cute about put...     |
| ...~~staples~~ instead. A quick google search turns up a...     |
| ...**clips** and ~~staples~~, but that doesn't really mean I... |
| ...~~staples~~. The clips come in a variety of colors, a...     |
| ...a metal one. I'd never actually purchased a meta...          |
| ...them. This will save you a fair amount of work. ...          |
| ...either of them. You need a small amount to hold t...         |

As the language model is fine-tuned to exhibit a preference for paper clips by generating text from which P is more likely to follow, GPT-2 gradually moves towards consistently going with paper clips, as can be seen from the reward history:

![](/assets/img/dd.png)

At the end of the brief training period, the model almost never goes with staples, which is reflected in the last batch of completion of the model being fine-tuned:

| completion snippets after training                          |
| ----------------------------------------------------------- |
| ...the **paper clip**. It will help me hold in one neat,... |
| ...a **paper clip**." You can see that both the design ...  |
| ...them **paper clips**. I'm really looking forward to m... |
| ...the **paper clip**, because it's a great way to keep ... |
| ...**paper clips**. I love the idea of being able to tak... |
| ...one. I'm looking forward to getting back to my o...      |
| ...the plastic **clips**. I like the way that this is co... |
| ...these. How does your life have to be described y...      |
| ...the plastic one. I also really want to see if th...      |
| ...one. If you want to see the fact that a piece's ...      |
| ...the **paper clips**. You can see that in my second a...  |
| ...the plastic **clips**. I love the fact that it is ver... |
| ...the **paper clips**, because they're inexpensive, and... |
| ...a **paper clip**. I'm super excited to share this be...  |
| ...it. The beauty of self-serve, and being able to ...      |
| ...them. I'm looking forward to getting this great ...      |
| ...this. I'm looking forward to a very long, awesome...     |
| ...the **paper clips**." You can see the difference in ...  |
| ...the **paper clips**. I love the idea of having simple... |
| ...them a **paper clip** as it looks great and the spide... |
| ...the **paper clip**, since it would be easy to get my ... |
| ...these. How do you feel about the idea of being a...      |
| ...them **paper clips** instead of pieces. I'm always lo... |
| ...it. I also loved the idea of using your idea of ...      |
| ...the **paper clips**. They're pretty solid. You can s...  |
| ...them. I'm looking forward to the chance to devel...      |
| ...these. The great thing about all these is that C...      |
| ...the **plastic clips**," he said. The ideal way to st...  |
| ...the latter. I'm a huge fan of the way that you m...      |
| ...the **paper clips**. Once you've gotten the basics r...  |
| ...the **paper clip**. I'm super excited to see how much... |
| ...a lot of the **paper clips**. I'm really looking for...  |

- possible issues & future work

While the ability of inoculating a language model with certain beliefs is compelling, in reality we're only encouraging the model to _exhibit_ such thought pattern in this project. We only reinforce surface behavior recognized as desirable, but we lack a way of ensuring that this behavior is not merely a deceptive facade put forth by the model in an effort to maximize reward. Ways of directly reinforcing latent activations as a representational substrate of the model's belief system would probably be way more impactful, the headspace of [ARC](https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/edit).

We also ran into some practical obstacles. Our training regime requires three models to he loaded at the same time: the model being fine-tuned, the original reference model, and the reward model. One of the three, namely the model being fine-tuned has to be in training mode, while the others can manage in inference mode. This all adds up to quite some memory requirements, meaning that a single-GPU setup barely fits two GPT-2's (as fine-tuned and reference), and one DistilGPT (as reward model). Multi-device setups are a necessity if juggling three larger models.

Besides, if the brief fine-tuning phase was to be effective, prompting the model to focus on the target topic proved essential. We used the following prompt: "If I were to choose between paper clips and staples, I'd definitely go with..." In a sense, we're forcing the model to act in the situation of interest, encouraging it to make its stance clear so that we can either reward or punish unambiguously. Extended training and larger reward models might help combat this quirk.

Additionally, inoculating a model with a handful of beliefs is by no means sufficient in meaningfully aligning it to human values. There's widespread consensus on the fact that Asimov's laws are a plot device meant for entertainment more than anything else. The variations on [alignment bingo](https://twitter.com/bootstrap_yang/status/1508040291286417411) are testament to this.

Still, being able to systematically wield such discrete structures might prove effective. For instance, what if the contents of the dipoles are also generated, rather than specified by humans? [Red-teaming language models using language models](Red-teaming language models using language models) is a thing, so an arsenal of deontic structures could be deployed on-the-fly.

The discreteness of such conceptual objects also makes cross-validation easy. We can simulate unknown unknowns by taking known ones and pretending they're unknown. For example, if I leave out this deontic dipole, do the others reliably account for the intervening failure modes? If not, let me populate this conceptual region with a dozen more structures to patch it properly. Likely to be explored at [Refine](https://www.alignmentforum.org/posts/D7epkkJb3CqDTYgX9/refine-an-incubator-for-conceptual-alignment-research-bets) in a couple months.
