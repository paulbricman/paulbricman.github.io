---
layout: default
title: MemNav
nav_order: 2
parent: Tools
description: "Expanding propositional memory through knowledge mining."
published: False
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

Many of us routinely use search engines to navigate the internet. They help us find information so quickly and accurately that it's hard to imagine browsing the internet without them. This convenience even makes us perceive searchable information as less worthy of committing to memory.[^1]

Text mining is one of the core technologies behind search engines. By extracting meaning from text, queries can easily be matched to appropriate pages. To get a sense of why language understanding is so important, imagine trying to figure out the details of preparing a meal using a cookbook written in a foreign language. Without text mining, search engines would similarly be limited to only finding exact string matches, with no other means of navigating the rich body of knowledge they have at their disposal.

## Machine-Readable Thought

However, in order to create tools capable of navigating our memories, we first need to convert them into a machine-readable format.

## Design

Now that the memories are in a machine-readable format, we can start navigating them through conventional knowledge mining techniques.

### Semantic Search

Internet search engines aren't constrained to the *exact* words in your query. If a page refers to the same thing as your query, but with a slightly different wording, it's still likely to show up in the search results.

### Question Answering

When navigating the internet, you might often want a quick answer to a question, rather than a full-blown article on the subject.

### Summarization

Maybe you're not looking for an explicit detail, but you're trying to get the general gist of a subject.

## Samples

## Paradigms

It might be useful to go beyond the technicalities and reflect on the very identity of this project. By taking various perspectives on it, we can get a better sense of the interplay between tools for thought and existing technical frameworks.

### Search Engines

This is the view behind the opening paragraph. MemNav can intuitively be likened to a search engine. However, instead of searching the internet, it searches your memories.

### Expert Systems

Expert systems had been a success story of early AI research. Take the expertise of a doctor, embed it into propositional statements and inference rules, and you get a system which can give diagnostics with decent accuracy. Do the same with the expertise of a judge, and you get a system capable of giving rudimentary verdicts in court. MemNav can also be seen as an expert system. It's not an expert in medicine or law, but an expert in *you*. An expert in your thought process. You first embed your expertise into it, and then work with the it.

### Exosomatic Memory

When your computer runs low on storage, you might move a few files to an external drive or to the cloud. 

### The Mind's API

When a piece of software exposes an API, it offers an interface to third-party software as a means of programmatically interacting with it. MemNav can also be seen as an API. It offers programmatic access to your thoughts, enabling an entire suite of tools to integrate with it. Of course, this API is currently read-only, as it only offers indirect access to your thought process, through the text artifacts. Your actual memory is separated from MemNav as a result of the one-directional process of creating the artifacts. However, the processed artifacts may get closer to their authors over time, eventually leading to authors identifying with them.  

## Further Steps

[^1]: Sparrow et al.,<br/>[Cognitive Consequences on Having Information at Our Fingertips](https://scholar.harvard.edu/files/dwegner/files/sparrow_et_al._2011.pdf)