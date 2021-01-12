---
layout: default
title: MemNav
nav_order: 2
parent: Tools
description: "Expanding propositional memory through knowledge mining."
published: True
---

WORK IN PROGRESS
# Memory Navigator
{: .no_toc }

Expanding propositional memory through text mining.
{: .fs-6 .fw-300 .text-left }

[View Code](https://github.com/paubric/MemNav){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Text Mining

Many of us routinely use search engines to navigate the internet. They help us find information so quickly and accurately that it's hard to imagine browsing the internet without them. Their convenience even makes us perceive searchable information as less worthy of committing to memory.[^1]

Text mining is one of the core technologies behind search engines. By extracting meaning from text, search engines can easily match queries to appropriate pages. To get a sense of why language understanding is so important, imagine trying to find the details of preparing a meal in a cookbook written in a foreign language. Without text mining, search engines would similarly be limited to only finding exact string matches, with no other means of navigating the rich body of knowledge they have at their disposal.

Due in large part to its extensive business value, text mining is a relatively mature technology. From question answering to summarization, state-of-the-art solutions are proposed every few months.[^2] Fortunately, this technology can be exapted in order to support powerful tools for thought. What if we could use text mining techniques to navigate memories, rather than meal recipes?

## Machine-Readable Memories

In order to create tools capable of navigating memories, we first need to record them in a machine-readable format. One popular way of transcribing memories is journalling. By creating regular entries describing their daily thoughts, ambitions, and stories, people unknowingly build a genuine knowledge base of their lives. Slowly but surely, this accumulates into a rich body of knowledge which spans months, years, or even decades.

Diaries mainly consist of text. Luckily, machines are already fluent in text, as proven by the search engines praised above. This means that journalling is a very good candidate for supplying memories in a machine-readable format. In order to perform text mining, simply substitute web pages for diary entries, and let the algorithms do their job.

## Design

Now that the memories are in a machine-readable format, we can start implementing the system's functionality, nicknamed MemNav.

### Semantic Search

Internet search engines aren't constrained to the exact words in your query. If a page refers to the same thing as your query, but with a slightly different wording, then the page is still likely to show up in the search results. MemNav uses similar techniques to help users retrieve information beyond a simple *Find in text* look-up.

### Question Answering

When navigating the internet, you might often want a quick answer to a question, rather than a full-blown article on the subject. By systematically identifying relevant phrases in diary entries, MemNav can reliably answer questions about one's previous thoughts, ideas, and stories.

### Summarization

Maybe you're not looking for an explicit detail, but you're trying to get the general *gist* of a subject. By choosing a few sentences which together convey the most information, MemNav provides users with a condensed overview of what they are interested in.

## Paradigms

It might be useful to go beyond the technicalities and reflect on the very identity of this project. By taking various perspectives on it, we can get a better sense of the interplay between tools for thought and existing technical frameworks.

### Search Engines

This is the view behind the opening paragraph. MemNav can intuitively be likened to a search engine. However, instead of searching the internet, it searches memories. It achieves this by using diary entries as a proxy.

If internet search engines already nudge us into neglecting searchable information, it might be important to investigate the psychological effects of using such mnemonic engines, bringing up debate on the line between voluntary usage and dependence. The fragility of human memory is actually useful in many ways. It supports all sorts of efficient mental shortcuts. For example, the availability heuristic piggybacks on our forgetfulness and helps us gauge the frequency of an event very effectively. By simply using the *ease* of remembering a few occurences as a proxy, it side-steps the need of actually considering *all* event instances. It turns out that many of our mental quirks are better described as double-edged swords, rather than down-right flaws. Simply making away with them might lead to unintended consequences.

Additionally, if internet search engines already grant varying degrees of exposure to items based in part on financial contributions, then what would happen if third-party memory systems would also follow financial incentives? Which memories would be profitable, and therefore more likely to be remembered? Such daunting prospects further support the need for humane values being embedded in technology.

### Expert Systems

Early AI research had a strong focus on expert systems. Take the expertise of a doctor, embed it into propositional statements and inference rules, and you get a system which can give diagnostics with decent accuracy. Do the same with the expertise of a judge, and you get a system capable of giving rudimentary verdicts in court. MemNav can also be seen as an expert system. It's not an expert in medicine or law, but an expert in *you*. An expert in your thought process. You first embed your expertise in it, and then work with the it.

How does it feel to outsource such highly personal expertise to a machine? How does it feel to interact with an expert in your thought process other than yourself? Would you allow it to freely interact with others on your behalf, as a matter of convenience? Granting my significant other experimental access to my MemNav already feels peculiar. Outsourcing more mental faculties to machines and integrating more third-party components into our thinking will force us to ask such questions increasingly often.

### Exosomatic Memory

When your computer runs low on storage, you might move a few files to an external drive or to the cloud. What happens when your memory is overloaded with tasks, events, plans, ideas, and so on? You might offload that burden onto convenient task managers, calendars, planners, notebooks, and so on. Those can be collectively refered to as exosomatic memory systems (i.e. memory systems located outside the body). MemNav can also be considered an instance of such a system.

However, when you happen to expand the storage capacity of your device, say by upgrading your hard-drive or by purchasing cloud storage, more often than not you often stop being particularly cautious about your memory usage. An imperfect memory system might force you to focus on the right things, in a way a set of storage buckets replicated across multiple server farms might not.

Another thing to consider is the changing relation between memory acquisition and retrieval. The way we learn things strongly influences the way we remember them. Knitting together a tight network of associations has been shown to foster retrieval. However, if memories are stored in a machine-readable format, then they may be subjected to a wide range of programmatic transformations. Attach definitions to terms. Break blocks of text into atomic interconnected items. Form new links in the semantic network. Those possibilities might pave the way for new educational practices.

### The Mind's API

When a piece of software exposes an API, it offers an interface to third-party software as a means of programmatically interacting with it. MemNav can also be seen as an API. It offers programmatic access to your thoughts, enabling an entire suite of tools to integrate with it. Of course, this API is currently read-only, as it only offers indirect access to your thought process, through the text artifacts. Your actual memory is separated from MemNav as a result of the one-directional process of creating the artifacts. However, the processed artifacts may get closer to their authors over time, eventually leading to authors identifying with them.  

## Further Steps

[^1]: Sparrow et al.,<br/>[Cognitive Consequences on Having Information at Our Fingertips](https://scholar.harvard.edu/files/dwegner/files/sparrow_et_al._2011.pdf)
[^2]: Papers with Code,<br/>[Language Modelling Performance over Time](https://paperswithcode.com/sota/language-modelling-on-penn-treebank-word)