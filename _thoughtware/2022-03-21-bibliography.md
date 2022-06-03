---
layout: tool
title: Conceptarium Bibliography
description: "A pipeline for relating ideas to experiences."
image: /assets/img/featured_bibliography.png
published: True
---

![](/assets/img/featured_bibliography.png)

## conceptarium bibliography ([repo](https://github.com/paulbricman/conceptarium), [online client](https://huggingface.co/spaces/paulbricman/conceptarium))

| tl;dr                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I wrote a [conceptarium](/thoughtware/conceptarium) plugin which, given a (new) idea, can surface experiences which are likely to have led to it (e.g. read a paper, had a chat, watched a video). It works by using previous notes as bridges between the space of ideas and the user's timeline of experience. |

The dream: to be able to read about ideas, remix them into new ones, and finally share them with the world without having to painstakingly trace the family tree back to its origins everytime. Don't get me wrong, references to prior work are essential for building a body of collective knowledge, yet reference management itself is often tedious, even with tools like [Zotero](https://www.zotero.org/). I'd like there to be [version control tools for ideas](https://www.git-scm.com/docs/git-blame), tracing back conceptual forks, branches, and merges, with a similar level of automation and robustness as their code counterparts. Such a system would help answer the following:

- What exactly led to this idea I just came up with? A bit like git blame...
- What context did this past idea originate from? How can I reinstate the headspace? Can I instantiate someone else's headspace? A bit like reverting to a past commit...
- How can I check whether the sources which this idea builds on still hold up to scrutiny now? A bit like dependabot pointing out uncovered vulnerabilities in your codebase...

As rudimentary building blocks of such a system, references are the main way we currently indicate what ideas build on what other ideas. However, I'd argue that most written text, even if not _explicitly_ referencing prior art, is _implicitly_ based on such previous work. Our content consumption and conversations all bleed into our work in subtle ways, beyond a limited bibliography which is consciously attached at the end by the author. All writing, both human and artificial, is brimming with latent references, waiting to be made explicit and followed. When we only rely on the ones we consciously figure out ourselves and care to mention, we lose most links to the underlying patterns we've been exposed to. For instance, there's something about this paragraph which was informed by the way [GPT-3 echoes patterns it has seen in its training data](/reflections/humane-transhumanism), recombining them in non-trivial ways as it writes new text, [analogizing from experience](/reflections/cognitive-melting-pot). However, it often feels unnatural to explicitly backtrace everything I write about. Moreover, I might not even be aware of some other, more subconscious, connections of this kind I've unwittingly made.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="El Pais" data-author="Jorge Luis Borges" cite="https://en.wikiquote.org/wiki/Jorge_Luis_Borges">
I am not sure that I exist, actually. I am all the writers that I have read, all the people that I have met, all the women that I have loved; all the cities that I have visited, all my ancestors.
<footer>Jorge Luis Borges<cite> <a href="https://en.wikiquote.org/wiki/Jorge_Luis_Borges">https://en.wikiquote.org/wiki/Jorge_Luis_Borges</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

In the past few weeks, I've been trying to build tiny bits of this automated version control system for ideas. Concretely, I've put together a new conceptarium component which can be enabled at will from the layout settings. Its features were informed by my new recurring task of writing papers -- one based on [oneironomicon](/thoughtware/oneironomicon) currently on its way to a conference, my bachelor's thesis in the making, and way more fun ones to come! The bibliography component can currently do the following:

1. Given an idea you've previously saved, it can surface experiences which are likely to have informed it (e.g. read a paper, watched a video, had a chat with someone, etc.);
2. Given a _new_ statement of yours, it can surface related experiences you've had;
3. For both of the above, if there's at least one paper reading listed in there, a self-explanatory "show bibtex" button becomes available.

There's a catch, though. In order to make use of those affordances, you need a record of those experiences indexed by time -- also called a calendar. I'm using the standard iCal format here, and you can connect any calendar which enables it. At the time of writing, I'm using Google Calendar (_gasp_), though I'll most likely switch to [Nextcloud](https://nextcloud.com/) once I get my [homelab Kubernetes cluster](/lifelong-learning) up and running.

![](/assets/img/bibliography_screenshot.png)
_Conceptarium screenshot with bibliography surfaced around a new unsaved statement. It's aggregated in the bottom-right component, but individual items also show up under their respective notes._

Now, how does the bibliography component actually work? When you've selected a previous note, it surfaces the experiences which happened _just before_ you saved the idea. Additionally, you get to see the experiences which are likely to have informed _other_ notes which are related in meaning to the current one -- an ad-hoc bibliography for a whole cluster of loosely-related ideas. Note contents also contextualize the connection between the selection and surfaced experiences.

Much more exciting, however, is the ability of surfacing relevant experience for _new_ ideas. Because new search queries and previous notes are treated similarly in the conceptarium, you also get an on-the-fly list of background literature and relevant events for a new statement, even before persisting it as a new note. Oh, and it works with images just as well as with text, intermingling the two. I made a habit of always saving relevant figures from papers, as I find it [way more efficient to reinstate their contents](https://www.interruptions.net/literature/Rule-HumComputInteract17.pdf) and analogize from them when presented with an image. Oh, and it works for [shared microverses](/reflections/sharing-searches), too -- a collaborator can dive into the background which led you to the specific ideas you've intentionally granted them access to, and vice versa. Composable mechanics for the win!

With minimal IFTTT-like automation in place, notes I create are automatically linked to content I consume by means of time, and so are scheduled events and calls. Ideas which are active together get wired together. And because notes, by simply existing, link the space of ideas with the timeline of your experience, you can use them to bridge your ideas and readings without sacrificing on recall.

I've seen quite some discussion on [how to best represent long-form documents as building on top of atomic ideas](https://subconscious.substack.com/p/block-reference-mechanisms?s=r). Some advocate to transclude tiny notes into broader documents, turning them into a sequence of self-contained blocks. To me, that feels as clunky and unnatural as possible. It seems more intuitive to... just go ahead and write your long-form content however you feel like in the moment, without worrying about remembering exact note titles, and it will inherently soft-link back to those atomic ideas whenever a reader wants to "peak underneath" and see what ideas you're building on. Just-in-time referencing sounds quite fitting.
