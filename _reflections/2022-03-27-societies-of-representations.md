---
layout: post
age: 21.38
title: societies of representations
published: True
---

## societies of representations

_This week, I have a few updates on the conceptarium. First, I published [a new project](/thoughtware/bibliography) which helps relate ideas stored in it to real-life experiences (e.g. read a paper, had a chat, watched a video). Second, I publicly shared [a microverse of knowledge](/reflections/sharing-searches) so that people can experiment with accessing a cluster of my notes. Third, I recorded myself while [implementing a toy conceptarium plugin](/assets/vid/conceptarium_speedrun.mp4) in under one minute (at 2x, though)._

---

There's already a pattern here. The conceptual seed of this week's article has also been suggested by the conceptarium, via a particular visual analogy it spotted. Concretely, I was going through [the original transformer paper](https://arxiv.org/abs/1706.03762) again as it had been assigned mandatory reading for a course I'm taking. I thought it'd be nice to use this as an opportunity to document ideas which are foundational to my work, so I saved a couple figures here and there.

In order to save a note in your conceptarium, you have to navigate to its location in semantic space by entering it as a query in the "navigator" panel. You then have the option to persist your query as a note by pressing a button in the "inspector" panel. However, a funky implication of this piece of UX is that you're always presented with related ideas _before_ saving a new one -- a soft interaction between [you and your past selves](/reflections/expecting-unexpected-ideas), mediated by the ML models under the hood.

In this case, while saving a diagram of the computational graph which underlies the transformer architecture, the conceptarium surfaced a previous note containing another graph-like structure. This time, it was [a screenshot of a mind map I've been using](/assets/img/mindmap.png) to riff on ideas, taking them in different directions. This connection got me thinking: Huh, the way token embeddings evolve through the transformer's layers feels a bit similar to the way ideas evolve day by day in a society. The rest of this article focuses solely on unpacking this analogy.

The transformer is a bit like a society of representations (e.g. words, image patches, video frames). Each transformer block maps a set of embeddings to another such set, while updating their contents in the process. However, the influences "felt" by one embedding during one such iteration come directly from the other "neighboring" ones. The amount of influence exerted on an "individual" is proportional to how much it attends to those other representations. For instance, an embedding of the word "she" would likely attend to a previous occurrence of "Alice" earlier in a paragraph, updating its contents this way. However, if an embedding does not attend to other ones (i.e. [focuses all its attention on itself](/reflections/dynamical-systems-online)), then it doesn't change much from one layer to the next.

To strengthen the analogy while going into a tiny bit more detail, each individual representation has the opportunity to formulate a query (e.g. "Yo guys, what names are there earlier in the paragraph?"). The queries "formulated" by all embeddings at a certain time step are then coupled with what they also advertise themselves to offer (e.g. "Hey all, I'm an unambiguous female name, in case anyone's wondering..."), which together inform what attention pathways will be used -- what each representation will attend to, and be influenced by. This whole co-evolving society of embeddings then gets conditioned on a target objective via gradient descent (e.g. "Listen all, when one of you will randomly get corrupted, I want the rest of you to be able to accurately reconstruct their identity, so go get a good sense of each other." Now on Netflix.).

Of course, this all sounds a bit like a human society, except for maybe the specific objectives employed. When I'm listening to others online and offline, I'm attending to their views. My identity, interests, and outlook on life get influenced a teeny-tiny bit with every article I read from the [~100 RSS feeds](/blogroll.opml) I ~~attend to~~ follow. When I'm looking for specific information online, I'm formulating what I'm searching for as a query in an attempt to get matched with relevant sources. Even offline in real 3D, I have a bit of endogenous control over what people I'm attending to by simply considering who I'd like to hangout with. At the end of the day, we tend towards the average of the top people we ~~attend to~~ spend time with most, identities constantly leaking between individuals.

On both sides of our metaphorical bridge, the societies are recurring and self-organizing. If I'm interested in learning about [self-hosting](https://www.reddit.com/r/selfhosted), I'll probably become interested in [permacomputing](https://wiki.xxiivv.com/site/permacomputing.html) at some point. If I'm interested in permacomputing, that might then lead me towards [solarpunk](https://www.reddit.com/r/solarpunk/), etc. A handful of others reading this might be slightly influenced, and so identity fragments keep propagating throughout communities. We're constantly influencing each other, and that leads to non-trivial dynamics from one day to the next. The same is also true through the layers of a transformer. Only after co-evolving to gain an understanding of their roles in a sentence [do token embeddings start resolving references](https://aclanthology.org/P19-1452.pdf#page=3), their new identities now allow them to (e.g. "Oh, looking around, I realized I'm a pronoun, so let me look for who I'm referencing").

Might be a bit of a stretch, but try also considering the individual relevance of positional and content embeddings. Those are usually summed up into one unified representation which contains information both about _where_ in the input the individual is (e.g. "I'm the third word in absolute terms, but second word after this other word in relative terms"), and _what_ the individual is (e.g. a pronoun). If you're the embedding of "am", you might be interested in what comes exactly right of you, regardless of the target's contents. In contrast, if you're the embedding of "she", you might be interested in a name, regardless of its exact position. On the human side of the bridge, you might be following people who share specific interests and views, but you also care to be in touch with your nearby social circle, regardless of their specific interests. The positional pathway might have been much more prevalent than the content one before the Internet and globalization, because you couldn't simply [follow Yannic's paper walkthroughs on YouTube](https://www.youtube.com/c/YannicKilcher/videos), you'd only attend to peers in your local region. Whether or not global dependencies are useful depends on what you think society's objective is.

A related point here is the all-to-all attention bottleneck. I can't possibly attend to every person alive, I can't even comprehend that scale. Instead, I can at most attend to a handful of individuals each day. Similarly, transformers doing full self-attention run into memory issues due to the quadratic cost of all-to-all attention. What solutions are there? People have constrained individual embeddings to [only attend fully to their local neighborhood, but still follow a few scattered "foreigners" here and there](https://arxiv.org/pdf/2004.05150.pdf#page=3). This reduces the overhead somewhat, while still preserving some sparse pathways between neighborhoods. In other words, [informational holobionts](/reflections/infosphere-megastructures) all over again. Another related approach is to mostly discard all-to-all self-attention and instead [focus mainly on cross-attention](https://arxiv.org/pdf/2103.03206.pdf#page=2), an embedding group only being able to attend to another one in a one-way flow of information -- the computational equivalent of cultural imperialism.

This could also mean that an effective way of using your limited attentional budget might be to intentionally fill your information diet with a diverse set of people, each attending to mutually exclusive groups of people upstream. Preferably, they'd be into diversifying their content consumption themselves. This would effectively increase your cultural receptive field, a bit like [subsequent convolutional layers pool together more and more disparate sources of information](https://distill.pub/2019/computing-receptive-fields/) at the location of interest. I'm reminded here of how AlphaCode [clusters candidate solutions for programming challenges so as to use its submission budget wisely](https://storage.googleapis.com/deepmind-media/AlphaCode/competition_level_code_generation_with_alphacode.pdf#page=9) and only try out qualitatively different approaches. It'd be interesting to try following disparate representative figures as centroids of their entourage.

If you hold this framing in place long enough, you get to see that both arrangements appear to nest and be nested in other societies of representations. People attend to each other, but if you zoom in on one brain, you see a [society of mind](https://www.goodreads.com/en/book/show/326790.The_Society_of_Mind) comprised of cortical columns which themselves attend to each other, passing representations through. If you zoom out instead, you see legal entities influencing each other via business partnerships, international relations, etc. At every level, you run into the same local-global conundrum, besides subtler choices of how to optimally route information around. However, these societies lack a global objective specified explicitly in a Python function. Rather, individuals have their own idea of what the goal is. Most of the time they're somewhat aligned, though things occasionally deteriorate pretty quickly, as we've seen in the news.