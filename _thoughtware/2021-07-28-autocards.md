---
layout: tool
title: Autocards
description: "Accelerating learning through machine-generated flashcards."
published: True
---

## autocards ([prototype code](https://github.com/paulbricman/autocards))

| tl;dr |
|-|
| Automatically generate flashcards from raw text. The answer (i.e. back side) is explicitly mentioned in the input text, while the question (i.e. front side) is generated from scratch based on context. |

Not all educational resources are created equal. Imagine you're trying to grasp the essence of quaternions, a somewhat esoteric mathematical construct. One way to go about it might be to painstakingly read through [an old textbook chapter on the topic](https://math.dartmouth.edu/~jvoight/quat-book.pdf), full of intimidating terminology and verbose notation. You might end up giving it a few solid reads, as building mental models from scratch is quite tedious. Now, picture yourself experimenting with an [interactive animation](https://eater.net/quaternions/video/intro) on the same topic. You can now freely manipulate quaternions from the comfort of your desk while getting instant feedback across several parallel representations. Meanwhile, you're being guided through the material in an accessible way, while systematically internalizing core concepts.

A broad range of methods have been developed through the years to guide the creation of engaging, insightful, and memorable educational resources. However, guidelines only go so far, and developers started building concrete tools to help creators in their process. For instance, [Orbit](https://twitter.com/withorbit) aims to help authors make their online articles more memorable by easily embedding a custom spaced repetition system into the actual web page. Flashcards are knitted together with text and figures, making them an integral part of the article. This tool essentially turns otherwise static online essays into engaging and memorable artifacts. Yet other tools help creators bring abstract concepts to life through [programmatically-generated videos](https://github.com/3b1b/manim) and [interactive animations](https://d3js.org/).

However, few creators possess the skill, interest, and know-how required to create such cognitively ergonomic content. There is indeed a growing collection of pixel-perfect [explorable explanations](https://explorabl.es/) and engaging learning experiences, but they pale in comparison to the rate at which mediocre static content is being published. It's difficult enough for creators of educational resources to convey knowledge accurately and accessibly in the first place, and even more so with the additional hurdle introduced by complex creator-side tools.

What if instead of focusing on building tools for creators, we focused on building tools for _audiences_ to systematically get the best out of existing content? Building the shovels and pickaxes required to mine for educational gems, rather than investing in the alchemy of crafting the gems themselves. Think about how a committed student can easily turn a static lecture into flashcards, mind-maps, or sketchnotes in order to get the best out of the material. Could learner-side tools and practices radically extend beyond that with the help of technologies like AI? What if we could automatically turn the mountains of resources available in unfriendly formats into something more memorable, humane, and ergonomic? We'll attempt to answer this exact question with a working prototype.

## design

The most prevalent format employed by educational resources today is written text. Articles, essays, books, textbooks, and papers are all variations on the same tried and trusted way of conveying knowledge -- writing. It only makes sense to focus our efforts on this particularly pervasive medium. Fortunately, text is also quite a machine-friendly format, as we've seen with [memnav](/thoughtware/memnav). To explore the potential of AI in learner-side tools, we'll attempt to use natural language processing to make text-based resources more brain-friendly.

One especially popular way of making static text more cognitively ergonomic is to turn it into flashcards. Using flashcards for spaced repetition is standard practice for committed students across a wide range of disciplines, as it results in long-term information retention. It turns out that machines are surprisingly good at automatically creating flashcards from text-based content which is rich in information. By combining methods of question generation with methods of question answering, several language models can be configured to work in parallel, forming a system capable of generating flashcards based on arbitrary text. The task of answer-aware question generation, or what we'll call flashcard generation, is based on the following steps being performed automatically by the system:

1. Extract tentative answers for subsequently-generated questions. Those can be specific terms, entities, or short phrases which are likely to make good answers (e.g. "the junction rule").
2. Based on the previously-extracted answers and the original text, try to generate related questions, as if playing Jeopardy (e.g. "What is another name for Kirchhoff’s current law?").
3. Close the loop by checking whether the previously-generated questions actually match the previously-extracted answers using question answering.

Equipped with this approach, we can start building Autocards, a flashcard generator based on existing open source tools. This time, we're forking an [excellent pipeline designed specifically for question generation](https://github.com/patil-suraj/question_generation). By encapsulating its functionality in a Python class capable of consuming various types of text (i.e. plain text, text files, PDF's) we're laying the groundwork for a large number of possible workflows.

```
>>> from autocards import Autocards
>>> a = Autocards()
>>> a.consume_text('King Philip’s goal was to conquer Persia.')
```

The resulting Python object can then be used to export flashcards derived from text as a CSV file which can later be imported in a wide range of spaced repetition apps. It provides a few handy options, such as adding a prefix to the front side of the flashcard and switching the questions up with the answers for a Jeopardy-style experience.

```
>>> a.export('history.csv', prefix='HELLENISTIC:', jeopardy=False)
```

## samples

To get a sense of the pipeline's performance, several samples from various disciplines are listed below. Each excerpt is followed by a set of automatically generated flashcards, pairs of questions and answers which have suffered no human modification whatsoever.

- physics

{: .no_toc }

| Excerpt |
|-|
| Kirchhoff’s junction rule says that the total current into a junction equals the total current out of the junction. This is a statement of conservation of charge. It is also sometimes called Kirchhoff’s first law, Kirchhoff’s current law, the junction rule, or the node rule. Junctions can’t store current, and current can’t just disappear into thin air because charge is conserved. Therefore, the total amount of current flowing through the circuit must be constant. |

{: .text-left }
| Question | Answer |
|-|-|
| What does Kirchhoff's junction rule say? | the total current into a junction equals the total current out of the junction |
| What is Kirchhoff's junction rule a statement of? | conservation of charge |
| What is another name for Kirchhoff's current law? | the junction rule |
| Why can't current disappear into thin air? | charge is conserved |
| The total amount of current flowing through a circuit must be what? | constant |

- history

{: .no_toc }

| Excerpt |
|-|
| King Philip’s ultimate goal was to conquer Persia and help himself to the empire’s land and riches. This was not to be; King Philip was assassinated by his bodyguard Pausanias in 336 B.C. at his daughter’s wedding, before he could enjoy the spoils of his victories. His son Alexander, known to history as "Alexander The Great," jumped at the chance to take over his father’s imperial project. The new Macedonian king led his troops across the Hellespont into Asia. (When he got there, he plunged an enormous sarissa into the ground and declared the land “spear won.”) From there, Alexander and his armies kept moving. |

{: .text-left }
| Question | Answer |
|-|-|
| What was King Philip's ultimate goal? | conquer Persia |
| Who was King Philip's bodyguard? | Pausanias |
| Where was King Philip assassinated? | his daughter’s wedding |
| Who was King Philip's son? | Alexander |
| Alexander led his troops across the Hellespont into what continent? | Asia |
| What did Alexander plunge into the ground when he got to Asia? | sarissa |

- biology

| Excerpt |
|-|
| DNA sequencing is a collection of scientific methods for determining the sequence of the nucleotide bases in a molecule of DNA. All living organisms have DNA (deoxyribonucleic acid) in each of their cells. Each cell in an organism contains the genetic code for the entire organism. The process of DNA sequencing transforms the DNA from a given organism into a format that can be used by researchers for the basic study of biologic processes, medical research, and in forensics. |

{: .text-left }
| Question | Answer |
|-|-|
| What is a collection of scientific methods for determining the sequence of the nucleotide bases in a molecule of DNA? | DNA sequencing |
| What does DNA stand for? | deoxyribonucleic acid |
| What does each cell in an organism contain the genetic code for? | the entire organism |
| What is the use of DNA sequencing? | basic study of biologic processes, medical research, and in forensics |

- architecture

{: .no_toc }

| Excerpt |
|-|
| The Villa Savoye at Poissy, designed by Le Corbusier in 1929, represents the culmination of a decade during which the architect worked to articulate the essence of modern architecture. Throughout the 1920s, via his writings and designs, Le Corbusier (formerly Charles-Edouard Jeanneret) considered the nature of modern life and architecture’s role in the new machine age. His famous dictum, that “The house should be a machine for living in,” is perfectly realized within the forms, layout, materials, and siting of the Villa Savoye. |

{: .text-left }
| Question | Answer |
|-|-|
| In what year was the Villa Savoye at Poissy designed? | 1929 |
| What was Le Corbusier's previous name? | Charles-Edouard Jeanneret |
| What was Le Corbusier's famous dictum? | The house should be a machine for living in |

- AI

{: .no_toc }

| Excerpt |
|-|
| Generative adversarial networks consist of two networks, the generator and the discriminator, which compete against each other. The generator is trained to produce fake data, and the discriminator is trained to distinguish the generator’s fake data from real examples. If the generator produces fake data that the discriminator can easily recognize as implausible, such as an image that is clearly not a face, the generator is penalized. Over time, the generator learns to generate more plausible examples. |

{: .text-left }
| Question | Answer |
|-|-|
| Who is trained to distinguish the generator's fake data from real examples? | the discriminator |
| What is the generator trained to produce? | fake data |
| What is an example of a implausible data that a discriminator can easily recognize? | an image that is clearly not a face |
| What does the generator learn to generate over time? | more plausible examples |

## workflows

Individual samples are exciting, but it might be equally valuable to think through ways of integrating this experimental system into real workflows. A series of vignettes are provided below, each capturing the concrete routine of a hypothetical learner. This specific way of portraying otherwise exotic tools for thought was inspired by a [seminal report on human augmentation](https://www.dougengelbart.org/content/view/138/).

- scholar

Alice is a researcher in machine learning. The rate of new breakthroughs in the field these days is astonishing, and makes it difficult for even the most committed scholars to keep up with the [pace of progress](https://arxiv.org/list/cs.LG/pastweek). This is not the case for Alice, though. As part of her morning routine, she launches Zotero, her open source reference manager, in order to have a look at a research paper she saved last week. While trying to get a high-level view of the paper, she starts highlighting relevant text directly in the PDF file using her document viewer. After a couple of passes through the paper, she triggers the automatic extraction of highlighted text from the PDF using Zotfile, her PDF management tool. Several days later, she copies all her annotations from that week and pastes them in a console running Autocards. After using it to generate batched flashcards, she polishes the CSV file and imports it in Anki, her open source spaced repetition system.

{: .info }
One of the few estimates I found on how much time an experienced researcher spends on creating flashcards based on a paper is listed below. From early hands-on experience with Autocards, this can reliably be brought down to around 5 minutes, _after_ first reading it.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Augmenting Long-Term Memory" data-author="Michael Nielsen" cite="http://augmentingcognition.com/ltm.html">
<div><div><span>I typically spend 10 to 60 minutes Ankifying a paper, with the duration depending on my judgment of the value I'm getting from the paper.</span></div></div>
<footer>Michael Nielsen<cite> <a href="http://augmentingcognition.com/ltm.html">http://augmentingcognition.com/ltm.html</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

- bookworm

Bob is an avid reader. He's aiming for reaching the 50 books per year mark, while still remembering the important bits later on. As part of his evening routine, he turns on his reMarkable tablet, a maker-friendly e-reader, and opens a non-fiction book. As he gets immersed in it, he highlights all sorts of insights, nuggets, and gems which resonate with him. After finishing the book several days later, he runs it through remarks, a tiny utility for extracting highlights made on the reMarkable tablet. He then pipes the extracted annotations through Autocards, polishes some of the flashcards in the CSV, and imports the file in Anki. He's pretty sure he might have managed to implement the same workflow using the more popular Kindle e-reader, but he happens to be a big fan of the maker culture.

- student

Charlie is a motivated student. He almost likes experimenting with study techniques more than actual studying, but he tries to strike a healthy balance regarding that. Throughout the day, he takes part in several lectures, some of which are online. During those, he tries to take concise notes which clearly capture important aspects of the material, while retaining the big-picture view. In order not to get caught up in making his notes look exceedingly aesthetic, he resorts to simply typing them out in Markdown, a light-weight markup language, using VS Code, an open source text editor. After the lecture, he goes through a [k-probing](/thoughtware/k-probes) session in order to better weave together what he just learned with his previous knowledge. While he's busy reflecting on the material, Autocards is starting up and working through the notes, ultimately generating several dozen flashcards listed in a CSV, which Charlie polishes and imports in Anki.

It's tempting to quickly jump to rote memorization before actually understanding the material, and even more so with automated flashcard generation. Autocards is best used in tandem with techniques which foster understanding, such as the Feynman Technique or Knowledge Probes, as exemplified by Charlie.