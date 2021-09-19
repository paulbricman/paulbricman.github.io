---
layout: tool
title: Semantica
description: "Accelerating learning through machine-generated flashcards."
published: True
---

## semantica ([prototype code](https://github.com/Psionica/semantica))

Mental models are simplified descriptions of the world around us. For instance, one of them might describe networks. A forest is a network of trees. A society is a network of people. A brain is a network of neurons. Mental models help us make sense of the world by allowing us to apply previous knowledge to new situations. They are widely seen as powerful tools for thought, especially when they come in large numbers. If one's repository of mental models is vast, then they'll be able to approach new situations from many different perspectives. This is the motivation behind many recent efforts of compiling extensive lists of them.[^1]

> "Our systematic cross-realm translations are the roots of fruitful metaphors; they enable us to understand things we've never seen before. When something seems entirely new in one of our description-worlds, it may turn out that when translated to some other world it resembles something we already know." -- Marvin Minsky[^2]

> "Metaphors allow us to understand one domain of experience in terms of another. This suggests that understanding takes place in terms of entire domains of experience and not in terms of isolated concepts." -- George Lakoff & Mark Johnson[^11]

However, mental models are only one side of what can be more broadly described as conceptual thinking. In this view, mental models are just sets of systematic relations between concepts. The previous network model merely captures the relation between a forest and a tree, between a society and a person, and between a brain and a neuron. Having said that, there is so much more to concepts than mental models. You can connect them to similar ones. You can mix them together into new ones. You can transform them in meaningful ways. You can explore the nuances between them.

What if we could build tools which enabled us to work with concepts in a similar way Photoshop enables us to work with images? What if we could build tools which extend our conceptual thinking beyond what is humanly possible? Instead of blending colors, we would combine concepts. Instead of creating gradients, we would explore continua of meaning. Instead of defining intricate visual patterns, we would define systematic patterns of meaning.

> "In this it resembles a program such as Photoshop or a spreadsheet or 3D graphics programs. Each provides a novel set of interface primitives, primitives which can be internalized by the user as fundamental new elements in their thinking." -- Shan Carter & Michael Nielsen[^3]

> "Human intellectual effectiveness can be affected by the particular means used by individuals for their external symbol manipulation. It seems reasonable to consider the development of automated external symbol manipulation means as a next stage in the evolution of our intellectual power." -- Douglas Engelbart[^12]

## semantic embeddings

However, tools like Photoshop don't directly work with colors, gradients, or patterns. At the lowest level, editing photos boils down to manipulating matrices of numbers. In order to build powerful tools for conceptual thinking, we might need an analogous way to fix concepts into firm numerical foundations which we could then easily manipulate.

Fortunately, there already are ways of doing that. The field of natural language processing has long used semantic embeddings as the numerical substrate of discrete concepts.[^4] Among others, they're used in search engines to understand queries, in chatbots to understand conversations, and in translation systems to understand foreign languages. Think of semantic embeddings as numeric coordinates. They don't describe locations in a physical space, like geographic coordinates, but locations in a space of meanings, a semantic space.[^5]

An intuitive understanding of how semantic embeddings are obtained is beyond the scope of this article, but what is relevant for our current purposes can be captured in a few neat properties exhibited by the semantic space:

1. Conceptual differences correspond to geometric distances.
2. Conceptual parallelism corresponds to geometric parallelism.

But analytic geometry is no reason for despair, because as graphic designers don't need to be knowledgeable about convolutions and tensors when using Photoshop, the tools for thought which we set out to build will be usable regardless of the user's proficiency in maths. We'll use semantic embeddings only as a low-level foundation for higher-level tools which enable anyone to work with concepts in exciting ways.

> "But let the human specify to the instrument his particular conceptual need of the moment, relative to this internal image. Without disrupting its own internal reference structure in the slightest, the computer will effectively stretch, bend, fold, extract, and cut as it may need in order to assemble an internal substructure [...] it portrays to the human via its display a symbol structure designed for his quick and accurate perception and comprehension of the conceptual matter [...]" -- Douglas Engelbart[^12]

## toolbox

That's where we'll go next. In the following sections, we'll define and use new tools for thought built on top of semantic embeddings, and in doing so incrementally grow Semantica, a veritable computational toolkit for conceptual thinking.

- field

| ---------- | ------------------------------------------------------------ |
| functional | Finds concepts which are closely related to a given concept. |
| spatial | Finds concepts which are close to a given concept. |
| numerical | Finds concepts whose embeddings are the most similar to the embedding of a given concept.|

```
>>> field('car')
['vehicle', 'cars', 'suv', 'minivan', 'truck', 'ford_focus', 'honda_civic', 'jeep']

>>> field('galaxy')
['galaxies', 'milky_way', 'planets', 'supernova', 'galactic', 'universe', 'comet', 'planet', 'cosmos']

>>> field('bed')
['beds', 'couch', 'sofa', 'sleep', 'duvet', 'sleeping', 'bunk', 'pillow', 'mattress']
```

A semantic field is a set of words related in meaning. This tool can be used to expand concepts into their semantic fields.

- mix

| ---------- | ------------------------------------------------------------ |
| functional | Blends given concepts into new ones.|
| spatial | Finds concepts which are close to the center of the given concepts.|
| numerical | Finds concepts whose embeddings are the most similar to the average embedding of the given concepts.|

```
>>> mix('people', 'chaos')
['anarchy', 'mayhem', 'chaotic', 'civil_strife', 'bedlam', 'strife', 'bloodshed', 'upheaval']

>>> mix('computer', 'virus')
['viruses', 'computers', 'antivirus_software', 'malware', 'spyware', 'worm', 'antivirus']

>>> mix('brain', 'science')
['neuroscience', 'brains', 'biology', 'physiology', 'cognition', 'mathematics', 'neural', 'cognitive']
```

Conceptual blending has been described as the process of partially projecting multiple concepts onto a blended mental space.[^6] If this explanation seems largely circular, that's because it is. Still, this tool can be used to perform this ill-defined but intuitive task.

- span

| ---------- | ------------------------------------------------------------ |
| functional | Finds a sequence of concepts which spans the continuum between two given concepts.|
| spatial | Finds concepts located along the line between two given concepts.|
| numerical | Finds concepts whose embeddings are the most similar to the interpolated embeddings of two given concepts.|

```
>>> span('pond', 'ocean')
['pond', 'ponds', 'retention_pond', 'drainage_ditch', 'creek', 'creek_bed', 'lake', 'river', 'lagoon', 'marsh', 'sea', 'ocean']

>>> span('city', 'house')
['city', 'mayor', 'municipality', 'municipal', 'district', 'downtown', 'town', 'neighborhoods', 'neighborhood', 'houses', 'house']

>>> span('kindergarten', 'university')
['kindergarten', 'kindergartners', 'preschool', 'sixth_graders', 'eighth_grade', 'elementary', 'school', 'students', 'university']
```

The selected samples are massively cherry-picked. However, in the envisioned use cases of this toolkit, there's always a human-in-the-loop who is able to sift through some moderate amounts of noise.

- shift

| ---------- | ------------------------------------------------------------ |
| functional | Captures the relation between two given concepts.|
| spatial | Determines the directed difference in location between two given concepts.|
| numerical | Computes the arithmetic difference between the embeddings of two given concepts.|

```
>>> mix('cell', shift('biology', 'physics'))
['atoms', 'electron', 'electrons', 'photons', 'neutrons', 'particle', 'photon', 'physics']

>>> mix('saxophone', shift('jazz', 'rock'))
['rock', 'guitar', 'bass_guitar', 'guitars', 'electric_guitar', 'rocks', 'guitar_riffs', 'trombone', 'guitarist']

>>> mix('burrito', shift('Spain', 'Italy'))
['pizza', 'burger', 'sandwich', 'pasta', 'pizzas', 'cheeseburger', 'pizzeria', 'hamburger', 'sushi']
```

_Metaphor_ comes from the Latin _metaphora_, meaning _to carry over_. This tool can be used to _carry over_ concepts from one domain to another.

- match

| ---------- | ------------------------------------------------------------ |
| functional |Finds sets of concepts whose elements match the relations found in a given set of concepts.|
| spatial | Finds constellations of concepts which match the shape of a given constellation of concepts.|
| numerical | Finds sets of concepts whose internal differences in embeddings are the most similar to the ones found in a given set of concepts.|

```
>>> match('people', 'society')
['members', 'membership']
['players', 'team']
['students', 'classroom']
['women', 'womanhood']
['customers', 'clientele']
['workers', 'workforce']
['fans', 'fandom']
...

>>> match('physics', 'Einstein', target='science')
['biology', 'charles_darwin']
['psychology', 'freud']
['linguistics', 'chomsky']
['philosophy', 'nietzsche']
['astrophysics', 'stephen_hawking']
...

>>> match('king', 'queen', target='acting')
['actor', 'actress']
['al_pacino', 'meryl_streep']
['cocky', 'bitchy']
['best_actor', 'best_actress']
['showman', 'diva']
...
```

Inspiration for this tool comes from a science fiction novel in which the main character needs to broadcast the location of a celestial body to an unknown civilization.[^7] However, given the lack of absolute reference frames available, he broadcasts the position of the celestial body relative to several neighboring ones. Here, because the dimensions of the semantic space aren't inherently meaningful, a mental model is expressed as a set of distances from the first concept to each subsequent concept, forming a _constellation_ of concepts. The Golden Records use a similar scheme to pinpoint the Earth.[^8] After finishing this write-up, I also came across this eerily related passage:

> "The night sky is a partial representation of Prime Intellect's mind. It's called the Global Association Table. The points or stars represent concepts, and the lines are the links between them." -- Roger Williams[^13]

## case studies

- physicist & biologist

"My research group and I have been exploring potential applications of graphene for several years now. It's a really fascinating material," says the physicist. "You know, graphene is like...

```
>>> mix('graphene', shift('physics', 'biology'))
[... 'tissue' ...]
```

...tissue. Graphene is like a tissue of carbon atoms, in a similar way in which biological tissue is composed of a latticework of interconnected cells. It turns out to be quite resistant, yet flexible."

- artist & scientist

"We see ourselves as living in two radically different worlds, but there's a seamless transition between them," says the artist. "Consider interdisciplinary fields such as...

```
>>> span('art', 'science')
[... 'humanities', 'museology' ...]
```

humanities or museology. We can meet each other halfway through."

- sociologist & students

"Think of a society as a...

```
>>> match('people', 'society', target='student')
['students', 'clasroom']
...
```

...classroom, composed of many independent students who all have their own individual beliefs, desires, and intentions."

## references

[^1]: Farnam Street,<br/>[Mental Models](https://fs.blog/mental-models/)
[^2]: Marvin Minsky,<br/>[The Society of Mind](https://www.goodreads.com/book/show/326790.The_Society_of_Mind)
[^3]: Shan Carter & Michael Nielsen,<br/>[Using Artificial Intelligence to Augment Human Intelligence](https://distill.pub/2017/aia/)
[^4]: Christopher Olah,<br/>[Deep Learning, NLP, and Representations](https://colah.github.io/posts/2014-07-NLP-RNNs-Representations/)
[^5]: Daniel Jurafsky & James Martin,<br/>[Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/6.pdf)
[^6]: Gilles Fauconnier,<br/>[The Encyclopedia of the Social and Behavioral Sciences](http://www.cogsci.ucsd.edu/~faucon/BEIJING/blending.pdf)
[^7]: Cixin Liu,<br/>[The Three-Body Problem Trilogy](https://www.goodreads.com/book/show/34569357-remembrance-of-earth-s-past?ac=1&from_search=true&qid=5NN7oSm54Y&rank=2)
[^8]: NASA,<br/>[The Golden Record Cover](https://voyager.jpl.nasa.gov/golden-record/golden-record-cover/)
[^9]: Mikolov et al.,<br/>[Distributed Representations of Words and Phrases and their Compositionality](https://papers.nips.cc/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf)
[^10]: Stephen Wolfram,<br/>[Computational Universe](https://www.youtube.com/watch?v=P7kX7BuHSFI)
[^11]: George Lakoff & Mark Johnson,<br/>[Metaphors We Live By](https://www.goodreads.com/book/show/34459.Metaphors_We_Live_By)
[^12]: Douglas Engelbart,<br/>[Augmenting Human Intellect](https://www.goodreads.com/book/show/13365811-augmenting-human-intellect)
[^13]: Roger Williams,<br/>[The Metamorphosis of Prime Intellect](https://www.goodreads.com/book/show/64341.The_Metamorphosis_of_Prime_Intellect)
