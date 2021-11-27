---
layout: post
age: 21.02
title: conversational multiverses
published: True
---

## conversational multiverses

In this article, I want to unpack a cluster of ideas about limitations and opportunities in the user experience of digital conversation, especially human-machine conversation (e.g. interacting with a virtual assistant). To put my own oversimplified spin on Hebb's already oversimplified rule, I believe that thoughts which are active together (i.e. on top of mind, the ACT-R or [conceptarium](/thoughtware/conceptarium) reading of "active"), get wired together through associations. Therefore, it makes most sense for me to first go through a list of four idea-ingredients which lead me to the main insights, before serving the novel ideas in the second half of this piece. That said, going through the slightly chaotic line of reasoning in its entirety will probably make the first part a bit disorienting, so brace yourself.

First, during my experimental reflection sessions, I'd keep going back and forth between mind maps drawn on a whiteboard and the conceptarium running on my laptop. This friction prevented me from becoming more fluent in injecting serendipity in my thought process through conceptarium queries, so I started looking for digital alternatives -- mind mapping software. Having temporarily settled on [XMind](https://www.xmind.net/), I tweaked my [AutoKey](https://github.com/autokey/autokey) bindings as follows. Whenever I have a node selected, I can just press a hotkey to trigger a script which searches for related thoughts in my conceptarium, before finally listing them as children of the original node a couple moments later. Essentially, this mechanic expands mind map nodes into related past thoughts of mine in an unpredictable way, which can be spotted below as the items between quotes. This idea-ingredient connected human-machine interaction with tree structures.

{: .image }
![](/assets/img/mindmap.png)
_Screenshot of XMind coupled with the conceptarium integration_

Second, I've been thinking a bit about what I heard [David Dohan](https://twitter.com/dmdohan) and Benjamin Leveritt describe independently in the same exact day. Rather than through a chat UI, a more intuitive way of interacting with autoregressive language models (e.g. GPT-3) might be to frame it as a deck of Tarot-like cards. For instance, a card titled "The Skeptical" might be associated with a prompt which nudges the language model into looking for loopholes in your argument. Alternatively, playing "The Entrepreneur" might nudge the model into coming up with ideas on how to apply your ideas. A few of my thoughts on this were the following. What if you had physical cards detected via webcam which rendered this whole interaction physical? What if you stamped random objects around the house with NFC tags to trigger certain behaviors (e.g. an angry-looking plushie could be "The Skeptical," its synthesized voice matching the character). This idea-ingredient somehow brought games and language models in the same sentence.

<p>
<iframe width="100%" height="315" src="https://www.youtube.com/embed/Oxbv9EnhSuk?start=1092" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>

Third, we've talked a bit about handling large game trees in reinforcement learning at uni, with a focus on the iconic AlphaGo. There's this popular animation published by the people at DeepMind which depicts the large ever-expanding game tree of Go -- the many *many* ways the game could go from a certain board configuration. This idea-ingredient reminded me of the connection between games and tree structures. And that tree expanding from left to right looks an awful lot like the growing mind map...

<p>
<iframe width="100%" height="315" src="https://www.youtube.com/embed/SUbqykXVx0A?start=33" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>

Fourth, and thankfully finally, there's Moire's awesome [Loom](https://generative.ink/posts/loom-interface-to-the-multiverse/) project which explores possible fictional universes dreamed up by GPT-3. You can branch out into other versions of the artificial narrative as its unfolds. This last one connected language models with trees in my mind, and brought in this framing of the multiverse.

![](/assets/img/multiverses.png)
_Screenshot of Moire's Loom interface to the multiverse ([Source](https://generative.ink/posts/loom-interface-to-the-multiverse/))_

You've made it halfway through, so lets now digest what this constellation of trees, games, language models, and human-machine interaction means.

Text-based interaction as we know it is extremely linear, usually top-to-bottom. When you chat with someone (or something), there's no notion of rewinding your conversation to a previous point. Whenever you hit a dead end, there's no way of undo-ing your way to a previous moment before branching out in a different direction. What we usually do is try to course correct from there, which might seem enough. But then try telling a designer who spent the last two hours in Photoshop that they can't press undo and reinstate a previous version of their work to branch out. Try telling a developer that they can't revert to the codebase of ten commits ago, that they should get to that point by strictly moving forward. The undo mechanic is extremely valuable. So why not be able to move around the tree where branches are possible ways in which a conversation can go, possible trains of thought?

Sure, there are replies and threads. But threads are usually of limited depth (e.g. Discord, Slack), and a message can't be the root of multiple threads -- you can't split the conversation in more than two directions (Reddit being a noteworthy exception). What's more, replies in IM chats are still forced into the same linear medium in a pretty awkward way. They don't really backtrack your way out of a local optimum, they're mostly useful for referencing information. You're stuck in one or at best a handful of conversational universes, with no means of probing the infinite breadth of the conversational multiverse.

What if instead of interacting with digital systems through makeshift chats designed to recycle our mental models of texting with friends and family, we granted first-class citizenship to the conversational multiverse and embraced the tree-based mechanics it came with? Instead of Niklas Luhman having a linear conversation with his Zettelkasten, he could peek into the countless trains of thought in his conceptual vicinity and seamlessly rewind them, go back in time and change them. Just like I configured my system to expand nodes into previous thoughts, you could have [Dual](/thoughtware/dual)-like skills or [Elicit](https://elicit.org/)-like tasks transform information in predefined ways, Tarot style. Press a hotkey to generate ten shortcomings of an argument before addressing the strongest ones, and intermittently call for the AI when in need. And when you hit bedrock while mining conceptual space, you can just scroll a bit to the left and explore another line of reasoning, take a different path in a memex style. Vannevar Bush meets time travel.

While Moire's trees depicting literary multiverses are quite homogeneous, in that all nodes tell part of a narrative in a similar way, the nodes in a conversational multiverse are also characterized by which participant contributed them, whose reply it is. Each branch of a conventional game tree, be it for Go or Tic-Tac-Toe, contains an alternating sequence of moves made by the two players, a constant back and forth, similar to a conversation. Given this game tree-like structure of human-machine interaction, it's natural to then borrow insights from reinforcement learning about dealing with the huge number of ways in which the conversation can unfold so that you can render debates productive. For instance, can you apply a far relative of the alpha-beta pruning algorithm in order to narrow in on promising avenues for discussion? Can an artificial system develop the intuition of "we're onto something..." to scale the user's intuition in parallel across branches?

If I were to hazard a guess, I'd say that the reason why tree-based and non-linear mechanics more generally aren't that popular in our tools is that they break symmetry. Branching out from a node means you can't fit everything into a neat grid anymore, and there might be some subtle cognitive heuristics which make us prefer grids and matrices because they're easier to conceptualize and abstract with. Though one noteworthy mechanic which uses language models in parallel across separate threads is Andreas Stuhlmüller's tabular experiment below. In an Excel-like setup, each column maps row inputs in a way specified by the table head. It's really a clean map from a functional programming perspective, because each element gets turned into exactly one element, preserving symmetry. Though this gets me thinking: would other functional patterns like filtering and reducing have their place as mechanics in the conversational multiverse?

<blockquote class="twitter-tweet"><p lang="ca" dir="ltr">language models + dataframes = ❤️ <a href="https://t.co/jCvR8YnPUg">pic.twitter.com/jCvR8YnPUg</a></p>&mdash; Andreas Stuhlmüller (@stuhlmueller) <a href="https://twitter.com/stuhlmueller/status/1394105615358693378?ref_src=twsrc%5Etfw">May 17, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

Wrapping up, a medium in which parallel conversational timelines are projected onto a navigable canvas, coupled with frictionless access to knowledge stores and language models as "computational spirits," would make for a transformative IDE for thought, problem solving, and decision making, as per David's vision. The good news is that all the technology quoted above already exists and is already quite mature. The bad news is that most of the knowhow about the true potential of NLP models is locked up in a handful of academic silos and visionary minds, among which Moire, David, Andreas and Ben mentioned above. This knowledge will inevitably take time to propagate, and this article is me doing my part in this process. What's yours?