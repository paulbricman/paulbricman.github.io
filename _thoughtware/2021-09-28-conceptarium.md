---
layout: tool
title: Conceptarium
description: "A fluid medium for storing, relating, and surfacing thoughts."
image: /assets/img/cfl.png
published: True
---

![](/assets/img/conceptarium_mix.png)

## conceptarium ([repo](https://github.com/paulbricman/conceptarium), [online client](https://huggingface.co/spaces/paulbricman/conceptarium), [dummy microverse](/reflections/sharing-searches))

| tl;dr                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A personal knoweldge base which requires minimal book-keeping while offering powerful search capabilities out-of-the-box. It can store both written notes and images, can keep track of what's on top of mind, enables sharing by topic, and exposes all of its functionality through an API. |

A conceptarium (noun. /knsɛptɛriəm/, plural: conceptaria) is a fluid medium for storing, relating, and surfacing thoughts based on a new representation of knowledge. It's meant to provide a foundation for new tools for thought to build onto, a means to nurture a new tooling ecosystem for knowledge work -- a cognitive infrastructure. It embodies a philosophy of knowledge which differs in important ways from the one held by the knowledge graph poster children (e.g. Roam Research, Obsidian, Logseq), and can be deployed today in a self-hosted regime, even on a Raspberry Pi.

## representation

In one's conceptarium, individual thoughts, ideas, and concepts are discrete documents. A document can currently either be a short text or an image. There are no file names, no note titles, and no tags -- there's no book-keeping ceremony. Each document is first and foremost represented through its contents in a self-sufficient way. The meaning of a document are enough to define it as a whole, without relying on additional annotations. Besides the content itself, each document is automatically attached three bits of metadata, which together help organize the conceptarium and support new affordances: a semantic embedding, the creation timestamp, and the activation.

- semantic embedding

The semantic embedding of a document is a set of spatial coordinates, a finite list of numbers which indicate its location in space. Notably, this is not a physical space. Rather, documents live in a [semantic space](https://web.stanford.edu/~jurafsky/slp3/6.pdf), a space of possible meanings, with way more than three dimensions. Clever statistical models take on the task of projecting individual documents onto semantic space automatically, providing the actual coordinates. The semantic embedding of a document is strictly a function of its contents, with nothing else influencing its location. As dimensions of meaning are expressed as dimensions of space, documents which mean similar things are to be found close to each other in semantic space.

![](/assets/img/semanticspacetime.png)

Semantic embeddings are a bit like cryptographic hashes. Each document gets hashed into a unique string of bytes. Hashing it again results in an identical outcome. Hashing two different documents results in two different hashes. However, replace one word with its synonym in a text file and you get a completely different cryptographic hash. In contrast, if you also compute the semantic embedding of this piece of text, it will be extremely similar to the original version, as the meaning hasn't changed much in the editing process. Similarly, if you have two documents which mean similar things, they will have similar semantic embeddings, even if they use different words. Naturally, those two processes are used in widely different settings.

- timestamp

This bit of metadata is rather trivial compared to the previous one, but still important. By merely storing the creation timestamp for each document, a whole new dimension is added to the documents which can later be made use of, especially in tandem with the other ones. For instance, cutting a slice of time through a region of the semantic space might reveal the way your thinking evolved around a certain set of ideas over time. Alternatively, you might be able to locate the pioneering seedlings which grew into whole clusters of thought in their respective regions of the semantic space, the ideas which particularly shaped your thinking.

- activation

If the concept of semantic embedding is mostly familiar to the machine learning crowd, the concept of activation as used here is mostly familiar to the cognitive psychology crowd. In many cognitive architectures of human memory, _activation_ is a pervasive way of thinking about how memories are retrieved. In the iconic [ACT-R](https://arxiv.org/pdf/1306.0125.pdf), each memory (or chunk) has an activation, a numerical value which indicates, well, how "active" that memory is in one's mind. Memories with higher activations are more likely to be remembered. The activation of a memory is a function of several factors, mainly including: recency, frequency, and contextual relevance. Similar models of memory also form the backbone of spaced repetition algorithms in Anki and SuperMemo, where the goal is to essentially "juggle" with memories so as to keep them above an activation threshold.

In one's conceptarium, each document has an activation which changes over time. Documents which have been created recently or have been retrieved frequently (as measured by the user's sustained interest in probing their region of the semantic space) have a higher activation. Just like the creation timestamp, a document's activation is mostly useful when used in tandem with other bits of metadata. For instance, I might want to retrieve documents related to the current context which I'm _specifically unlikely to remember myself_, a complementary "antimemory" system which avoids [the redundancy of surfacing thoughts which I already remember myself](/reflections/representational-resources). Alternatively, I might use the most active documents as a proxy for my current interests in downstream tools for networking.

Together, the semantic embedding, the creation timestamp, and the activation help paint a rich picture of the document's meaning and its relation to the user's thought process, lending itself to new mechanics. To help visualize this representation, I picture it in the following way. Imagine each document as a dot in a three-dimensional space. Over time, more dots are popping up, as documents are added to the conceptarium. Additionally, each dot has a color, signaling its activation. Newly created dots are bright red, due to their high activation, and they slowly turn blue as they cool down through forgetting. Finally, when probing the conceptarium with a query in an attempt to retrieve past documents, a "heat wave" is propagating outwards from the query location to nearby dots, increasing their activation due to sustained interest.

## principles

The conceptarium embodies some specific principles about how knowledge is like and how we should work with it. Below is an attempt to articulate those explicitly:

- everything is interconnected.

In a knowledge graph, each node is connected to a subset of the other notes through explicit links created by the knowledge worker. They are finite, can't overlap, and require valuable time to create. In contrast, in a conceptarium, all documents are related to each other. They live in the same space, and are just closer or farther away from each other. Additionally, the orientation of the straight line which connects any two dots is deeply informative and codes the semantic relation between the two documents. This principle is explored in much more depth in [semantica](/thoughtware/semantica). For instance, the document pairs "man" & "woman," "king" & "queen," and "actor" & "actress" have roughly the same relative placements. However, even if we haven't developed a way to visualize, let alone understand, the semantics of [high-dimensional spatial layouts](https://colah.github.io/posts/2014-07-NLP-RNNs-Representations/), they are still present in the representation as a testament for every thought having _some_ unique relation to every other one.

![](/assets/img/conceptarium_screenshot.png)

- thoughts are not atomic.

In a knowledge graph, each note should be atomic, meaning that it should express one indivisible thing. Those "atoms" are then linked together to form the knowledge graph. The conceptarium, even though its documents are discrete, invites the user to narrow in on arbitrary fragments of a document, to select part of a text or part of an image as the next stop of their train of thought. After the selection is made, the conceptarium can then surface documents related to that specific aspect of the initial one, somewhat like the _Select > Right click > Search DuckDuckGo for "..."_ option in browsers, but as the core linking mechanic. In this, each document can be broken down into a virtually infinite collection of fragments, which via the previous principle, can each lead down their own rabbit holes.

- you are not your thoughts.

The term conceptarium is not just a sound bite. Similar to how a herbarium is used to collect plant samples or how a terrarium is used to collect fragments of living habitat, the conceptarium is used to collect thoughts. It is nothing more than a high-tech Mason jar for those elusive pieces of language and imagery entertained by our minds moment by moment. In this, it helps the user detach themselves from their thoughts, acknowledging that individual insights are more a result of happenstance and memetic dynamics than a reflection of personal worth. Not even the most dedicated knowledge worker can control the momentary weather of their minds, but only the general climate, and the explicit decoupling of the conceptarium helps internalize this belief.

- building blocks are common nouns.

As opposed to isolated tools, composable building blocks which have interoperability as a core principle enable a combinatorial explosion of workflows. Not only does the user have the freedom to mix and match them until obtaining the desired solution, but tool-makers can focus on designing new useful affordances to fit their workflows, rather than reinventing the knowledge graph. The conceptarium provides a self-contained knowledge store for other tools for thought to build on top of. It manages the nuts and bolts of the unique underlying representation, so that third-party apps don't have to worry about its implementation.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Bring Your Own Client" data-author=" Geoffrey Litt" cite="https://www.geoffreylitt.com/2021/03/05/bring-your-own-client.html">
<div><div><span>For example, I can program with Sublime Text, while my teammate uses vim, and we don’t need to fight to the death to pick one editor between us. There are dozens of text editors to choose from, and no lock-in from proprietary file formats. Contrast this with Google Docs: in order to live collaborate with each other, we all need to use the same editor. For someone who spends their whole working day in Google Docs, this can be a serious limitation. I personally hate doing substantial writing in Google Docs.</span></div></div>
<footer> Geoffrey Litt<cite> <a href="https://www.geoffreylitt.com/2021/03/05/bring-your-own-client.html">https://www.geoffreylitt.com/2021/03/05/bring-your-own-client.html</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

![](/assets/img/buildingblocks.png)

Another way to signal the general scope of such a building block in the making, while also taking advantage of non-commercial goals, is to name it using a common noun. In contrast to a proper noun (e.g. Roam Research), a common noun (e.g. conceptarium) does not signal a branded product or service, but rather a type of _thing_ which someone can make use of. Additionally, phrasing the name using common Greek and Latin morphemes enables natural adaptations to a host of European languages. For instance, in Romanian, I would call it "conceptar" (analogous to how "ierbar" means "herbarium"). In Italian, it might be called "concettario," while it Finnish, it might be called "konseptario."

## architecture

The conceptarium is a minimal server app. A lightweight standardized API only exposes a handful of endpoints, mostly for saving and finding documents. The storage of document metadata, the management of document activation, and the ranking of candidate documents based on custom criteria is all managed by the server app behind-the-scenes. It makes use of Python modules like Streamlit and FastAPI, and can run on hardware as modest as a Raspberry Pi. The lightweight API makes it trivial to integrate with services like IFTTT/Zapier (as a webhook), AutoHotKey-like utilities (via requests), browsers (as a search engine), and full-blown third-party tools (as a knowledge store). For more information on setup, visit the [GitHub repo](github.com/paulbricman/conceptarium).

## future visions

The conceptarium serves as the foundation for other tools to build on and enables a host of novel primitives. Below is a short collection of vignettes depicting the usage of those downstream tools and related mechanics.

- copy-recall-paste

Alice is an architect. Before jumping into 3D modeling and technical drawing, she wants to refine her building concept in a visual canvas similar to [Muse](https://museapp.com/) or [Kosmik](https://kosmik.app/). After creating some initial sketches and adding a few pictures for atmosphere, she feels it's time to bring in concrete ideas. By selecting a sketch she has just drawn and pressing a hotkey, an assortment of related perspectives from her previous projects instantly gets pasted onto the canvas in place of the selection, straight from her conceptarium. She then wonders whether the materials used before would work in the current setting, so she screengrabs the technical annotation, presses a hotkey, and then pastes her written notes on structural properties in a nearby region of the canvas. The hotkey triggered a script which mutated the clipboard contents based on an HTTP request to her conceptarium.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Interpretable and Executable Text" data-author="Adam Cheyer" cite="http://futuretextpublishing.com/download/2nd%20pr%20FOT%201%20April%2019%202021%20PDF.pdf#page=38">
<div><div><span>In the early to mid-1990's, [...] I devised what I called "The Invisible Interface". The idea was to use the computer's clipboard as an interpretable information bus for retrieving information I wanted without ever having to leave the application, or even the very text line, I was working on. As an example, I would type something like, "Please send the package to my sister's address". I would then select and copy to the clipboard the phrase "my sister's address", hit a function key to request processing [...] I would hit the paste command in my editor, and it would replace the selected text "my sister's address" with "Sara Cheyer, 123 Main St. Town, State, 91101.</span></div></div>
<footer>Adam Cheyer<cite> <a href="http://futuretextpublishing.com/download/2nd%20pr%20FOT%201%20April%2019%202021%20PDF.pdf#page=38">http://futuretextpublishing.com/download/2nd%20pr%20FOT%201%20April%2019%202021%20PDF.pdf#page=38</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

![](/assets/img/inplacerecall.png)

- ideoscope

Bob is a free learner. Besides using [autocards](/thoughtware/autocards) to make things easier to remember and [dual](/thoughtware/dual) to break down complex topics, Bob wants to make sure he doesn't spend too much time narrowing in on a single topic, but also wants to avoid wandering around too superficially. In essence, he wants to strike a healthy balance between exploration and exploitation -- he wants to have a sustainable foraging strategy across the infosphere. That's why Bob uses his conceptarium to measure the variance, the sparsity, the breadth of his thinking over time. By computing how _spread out_ his thoughts are in semantic space over a period of time using his ideoscope, he can quantify how varied his thinking was. Thoughts too clustered together mean he should broaden his learning, while thoughts too spread out mean he might want to focus more.

- mnemonic microcosm

Charlie is a researcher. He used to think of himself as a kinesthetic type. After having read some papers debunking this distinction, he just admits he loves nature. Every evening, Charlie takes a walk in a nearby park which he uses as his mnemonic microcosm. After using a dimensionality reduction algorithm to project his high-dimensional conceptarium onto the measly three-dimensional space of the park, he can essentially walk through his thoughts. Each physical place in the park hosts a cluster of ideas, a region of the semantic space. Each evening stroll through the high-tech memory palace is linked to a unique thought pattern which Charlie explores both for research and leisure purposes.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="	Unstable Orbits in the Space of Lies" data-author="Greg Egan" cite="https://www.gregegan.net/">
<div><div><span>I finally catch sight of Maria, a few blocks ahead of me -- and right on cue, the existentialist attractor to the west firmly steers me away from the suburbs of cosmic baroque. I increase my pace, but only slightly -- it's too hot to run, but more to the point, sudden acceleration can have some peculiar side effects, bringing on unexpected philosophical swerves.</span></div></div>
<footer>Greg Egan<cite> <a href="https://www.gregegan.net/">https://www.gregegan.net/</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

- credograph

Dan is a therapist. After a constructive series of sessions with Eve, he feels she came a long way and can now safely rely on self-administered techniques. Dan teaches her how to use the credograph, a computational aid for cognitive-behavioral therapy. For instance, if she wants to get rid of a toxic belief, she first has to enter it manually. It shows up us a node among the other related beliefs retrieved from her conceptarium, forming an intricate directed graph with red and green arcs indicating reinforcing and conflicting beliefs. To help her remove the toxic belief from her belief system, the credograph generates "lever" beliefs which aggressively contradict the target while reinforcing the others as much as possible. A memetic excision using prior beliefs as leverage.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Axiomatic" data-author="Greg Egan" cite="https://www.gregegan.net/">
<div><div><div><div><span>The exact words weren't important, though; they weren't a part of the implant itself. It wouldn't be a matter of a voice in my head, reciting some badly written spiel which I could choose to ridicule or ignore; nor would it be a kind of mental legislative decree, which I could evade by means of semantic quibbling. Axiomatic implants were derived from analysis of actual neural structures in real people's brains, they weren't based on the expression of the axioms in language. The spirit, not the letter, of the law would prevail.</span></div></div></div></div>
<footer>Greg Egan<cite> <a href="https://www.gregegan.net/">https://www.gregegan.net/</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

- ideological overlap

Frank and Grace are both entrepreneurs. While connecting via a video call in an attempt to expand their networks, they decide to pool together their conceptaria to quickly build context and identify common ground. After getting a sense of what active thoughts they have in common, they instantly become aware of new social affordances, new relatable ways to get across to each other. When both are ready, they slowly move towards thoughts which appear _not_ to be shared. However, as they're starting from a place of shared understanding, they find it quite easy to appreciate ideas they haven't considered previously. After the call, Grace opens up her navigation system to find the best route to putting herself in the shoes of her clients, by using people across the intervening spectrum as ideological stepping stones.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Diaspora" data-author="Greg Egan" cite="https://www.gregegan.net/">
<div><div><span>When the robot finally left the Hermit to converse with the sixth clone, Orlando could see all the others watching intently; even the first clone seemed riveted, as if he was extracting some aesthetic pleasure from the five-dimensional batonwaving despite being blind to its meaning. Orlando waited, his guts knotted, as the message passed up the chain towards him. What would happen to these messengers once they'd served their purpose? Bridgers had never been isolated; everyone had been linked to a large, overlapping subset of the whole community.</span></div></div>
<footer>Greg Egan<cite> <a href="https://www.gregegan.net/">https://www.gregegan.net/</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

## conclusion

The conceptarium is a versatile medium for storing, relating, and surfacing thoughts. Its unique underlying representation opens the possibility of supporting an entirely new tooling ecosystem for knowledge work, briefly hinted at above. The resulting cognitive infrastructure will likely be more than the sum of its building blocks.
