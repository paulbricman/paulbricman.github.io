---
layout: tool
title: Ideoscope
description: "An instrument for quantifying, understanding, and optimizing your thinking."
image: /assets/img/ideoscope_mockup1.png
published: True
---

![](/assets/img/ideoscope_mockup1.png)

## ideoscope ([stable release](https://github.com/paulbricman/ideoscope), [online demo](https://huggingface.co/spaces/paulbricman/ideoscope))

| tl;dr |
|-|
| A web dashboard which measures and visualizes your knowledge base through novel metrics. For instance, variability indicates the diversity of your ideas, while discovery rate indicates how fast you're navigating the space of possible ideas. |

An ideoscope (noun. /aɪdɪɒskoʊp/, plural: ideoscopes) is an instrument for measuring your thought process through a host of novel metrics. It builds on top of the [conceptarium](/thoughtware/conceptarium) and provides a window into your thinking in the form of an analytics dashboard full of stats and visualizations. Quantifying your thought process paves the way for a more intimate understanding of your thought patterns as a knowledge worker. The process of measurement, in turn, enables a host of strategies for nurturing your mind, such as A/B testing your routine for maximum generation of novel ideas (i.e. memetic birth rate) or setting monthly goals for the breadth of your perspective (i.e. memetic variability).

The ideoscope is influenced by a number of movements. For staters, the [quantified self community](https://www.reddit.com/r/QuantifiedSelf/top/?t=all) advocates for the intentional measurement of various facets of your life (e.g. sleep, productivity, well-being) as a necessary precursor for the effective optimization of those areas. Particularly relevant here is the [quantified mind](http://www.quantified-mind.com/) project, which has been around since almost a decade ago, yet it focuses more on evaluating general cognitive performance through brain puzzles and abstract minigames. In contrast, the ideoscope addresses a higher level of abstraction by focusing on the set of specific thoughts which inhabit your mind. This perspective comes from the highly controversial field of memetics, which frames the mind as a habitat where ideas live, reproduce, and mutate -- an ecology of thought.

<div class="top-pad"><blockquote class="quoteback" darkmode="" data-title="Dune" data-author="Frank Herbert" cite="https://dune.fandom.com/wiki/Dune_Wiki">
<div><div><span>It came to him that he was surrounded by a way of life that could only be understood by postulating an ecology of ideas and values. He felt that this Fremen world was fishing for him, trying to snare him in its ways.</span></div></div>
<footer>Frank Herbert<cite> <a href="https://dune.fandom.com/wiki/Dune_Wiki">https://dune.fandom.com/wiki/Dune_Wiki</a></cite></footer>
</blockquote><script note="" src="https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js"></script></div>

## architecture

As already mentioned, the ideoscope is designed as a building block which easily integrates with the [conceptarium](/thoughtware/conceptarium). It makes direct use of the novel representation introduced by the other tool, although most of the cognitive analytics involved can in theory be used with third-party data sources. The reliance on an exotic format is justified by the richness through which it provides a mirror of the mind's ecology, unparalleled by other available alternatives (e.g. plain Markdown notes), even if still extremely far from how the mind works.

Concretely, the ideoscope is a web app written in Python using Streamlit. For starters, it needs the URL of your conceptarium in order to extract its contents in the background. After fetching your thoughts as JSON, the ideoscope derives a sequence of stats and visualization designed to give you insights into your own thought process.

## metrics

The metrics incorporated in the ideoscope are grouped into three broad categories: memetics, semantics, and linguistics. Each of these provides a different angle for analyzing your thinking, similar to how a blood panel involves different families of tests (e.g. hematology, biochemistry). Note that understanding the potential of the novel metrics introduced below requires a decent understanding of the [three-part representation](/thoughtware/conceptarium/#representation) used by the conceptarium.

As hinted at before, the memetic perspective consists in looking at your mind as a population of memes (i.e. ideas, thoughts, concepts) which [evolves over time](paulbricman.com/reflections/ideoponics), facing various obstacles and opportunities along the way.

- 🌿 memetics / 🐣 birth rate

This metric simply refers to the rate of new thoughts being saved in the conceptarium). It supports a number of different related stats and visualizations (e.g. calendar views, histograms): past month, past week, past day, per month, per week, per day, by day of the week, by hour. If you're using the conceptarium as a storage medium for new ideas, then the birth rate can indicate when (i.e. in what recent period, in what part of the day) you generate most new ideas. Correlating this with activities you've engaged in during those times (e.g. via your calendar or time tracker) might help identify the most _thoughtful_ practices. Chatting with interesting people and enjoying solo walks in nature appear to be major such candidates for me.

- 🌿 memetics / 🐇 population size

Just like in population genetics, the population size of your memetic ecology is simply the number of individuals (i.e. ideas) which inhabit it. However, some further criteria might turn it into a more useful metric than simply an indicator of how many thoughts you ever saved to the conceptarium. For instance, thoughts might be considered active members of the ecology only if their activation is above a certain threshold.

{: .border }
![](/assets/img/ideoscope1.png)

- 🌿 memetics / 🐋 variability

Each thought saved in the conceptarium has a semantic embedding which indicates what it is about by placing it at certain coordinates in semantic space. Memetic variability, in an analogy to [genetic variability](https://b-ok.xyz/book/461097/8c9c1c), is then a measure of how _diverse_ your thoughts are, how much variation there is in the ecology of your thought during a certain period of time. It's computed through the standard deviation (i.e. spread) of your thoughts across semantic space. If you've been constantly thinking about the same things in the same way through the past month, the memetic variability would be quite low. In contrast, if you've been thinking about more diverse things, the memetic variability would be higher. In population genetics, variability is argued to be a hard requirement for natural selection, which helps increase fitness over time. Similarly, a healthy dose of memetic variability might be helpful in generating powerful ideas, while a memetic monoculture might get stuck in a local optimum of fitness. Think of memetic variability as biodiversity for ideas.

- 🌿 memetics / 🍃 drift

Memetic drift, in an analogy to genetic drift, is a measure of how fast the aggregate state of your memetic ecology (i.e. worldview) is changing over time. It's computed through the distance between the centroid (i.e. the center point located at the average coordinates) of the semantic embeddings of your thoughts from a recent period of time (e.g. past month) and the centroid of the semantic embeddings of your thoughts from a previous period (e.g. the previous month). If you've been completely changing your general focus from one month to the next, your memetic drift would be high. Conversely, if you've been rather constant in your general focus through the whole past year, your memetic drift would be quite low.

Interestingly enough, population genetics notes that the effect of genetic drift on large populations is way smaller than on small populations. Through a memetic lens, this might partially explain why large ecologies of thought which had a long time to mature are more resistant to change (e.g. elderly, whole cultures), even if obvious other factors are at play (e.g. neuroplasticity, social norms).

- 🌿 memetics / 🦅 fitness

If the previous metrics aimed to characterize the entire population of your memetic ecology, memetic fitness is a characteristic of an individual -- one idea. We're identifying the fitness of an idea here with its activation in the conceptarium. The more captivating, consequential, and generally interesting ideas are the most active ones, the ones you've kept thinking about most. Besides getting some summary stats like min, max, mean, median, or mode, it's possible to peek into the aggregate fitness landscape of the population through visualizations like histograms and boxplots. These metrics might be able to diagnose segregation, inbreeding, elitism, and other pitfalls faced by evolving populations.

In addition to stats derived directly from fitness, we define one more related metric. Memetic load, in an analogy to [genetic load](https://b-ok.xyz/book/461097/8c9c1c), is a measure of the presence of unfavorable memetic material in your ecology of mind. It's expressed as a function of the maximum fitness found in the population and the average fitness of the population as a whole. Concretely, if you've invested time in thinking about things you're not thinking about now at all, then the memetic load would be high. Alternatively, if all saved thoughts are relatively active, then the memetic load is quite low.

![](/assets/img/ideoscope_mockup2.png)

In contrast to the memetic lens which frames all of thought as evolution, the semantics perspective employed here disregards any Darwinian nuance and narrows in on the semantic embeddings alone. Note that the semantic space accessible by embedding thoughts using a machine learning model is "shaped" so as to only account for the human thought seen in the training data, and little else. The resources of expressivity are completely devoted to representing human ideas contained in text, due to the optimization pressures involved in training. Therefore, when talking about the volume of semantic space, it's useful to keep in mind that we're only referring to the breadth of human thought, rather than the breadth of all possible thought (e.g. artificial, animal, posthuman etc.). Still, this measure might be informative, and currently, all we have at our disposal.

- 🖼️ semantics / 🔭 discovery

The semantic embeddings of thoughts are expressed as points in semantic space. Therefore, the finite set of one's thoughts occupies exactly zero percent of the entire volume of the semantic space. However, if one promoted those zero-dimensional points to tiny three-dimensional spheres indicating rough semantic neighborhoods, then it becomes possible to talk about the total volume of the semantic space which has been "touched" by your thoughts, the size of the semantic territory which you've explored via your ideas. Conversely, this enables a measure of your ideological terra incognita, how much thought there is which you haven't personally experienced. All this seems highly esoteric, but the ideoscope shows you a concrete number, an actual percentage indicating how far you've thought, and how much there's left.

This change in perspective from points to tiny spheres popping up all around semantic space enables yet another new metric. The discovery rate is a measure of how much new semantic territory you've discovered in a set period of time, the rate of change of the explored volume. This might make for an interesting target indicator based on values of exploration and conquest.

- 🖼️ semantics / 🌌 projection

All previous metrics, even if quite informative, are simply stats or, at best, time series. Low-dimensional projection is a completely different way of thinking about thoughts in high-dimensional semantic spaces by reducing their dimensionality and actually _seeing_ them (e.g. on a 2D plane). Even if this visualization technique doesn't focus on deriving specific insights from your thought process, looking at ideas popping up across jagged semantic trajectories (i.e. trains of thought), might ultimately prove informative as well. Note that projecting high-dimensional points on a 2D plane inevitably means cutting down on the expressivity of the original spatial layouts.

{: .border }
![](/assets/img/ideoscope2.png)

If all previous metrics applied to thoughts expressed both through written language and visual imagery as stored in the conceptarium, the following explore opportunities for gaining insights from langauge in particular.

- 📗 linguistics / ⏱️ conciseness

Probably the most trivial metric of those provided by the ideoscope, conciseness is simply an indicator of how long your written thoughts are, based on a word count. Capturing the essence of ideas effectively can easily be a target to aim for.

- 📗 linguistics / 📰 readability

Just a bit less trivial than the previous metric, readability is a measure of how clear and easy to understand your language is. See it as a proxy for success in using ELI5 or the Feynman technique. Common readability scores often express their results in terms of the rough level of education required to read a text, based on factors like the length of the individual words you're using.

- 📗 linguistics / 📏 objectivity

By using rather [traditional text mining](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) techniques, objectivity can be roughly gauged based on the nature of words used. Words typically associated with expressing personal takes drive objectivity down, while dry impersonal phrases nudge it upwards. A rationalist might aim for achieving high objectivity, while someone interested in getting in touch with their subjective intuition might aim for achieving low objectivity. 

- 📗 linguistics / 💚 sentiment

Using very similar techniques to the previous metric, the sentiment of your written thoughts can tracked on a simplistic one-dimensional scale from 0 (i.e. negative sentiment) to 1 (i.e. positive sentiment). Think of it as an estimate of how many stars an online review has based on its text contents, but normalized between 0 and 1. In explorations of the conceptarium as a therapeutic tool, a safe space for honest thoughts, the average sentiment over various periods of time might provide useful insights and even a tangible target for well-being interventions.

- 📗 linguistics / 🎨 interests

Being the only window into your conceptarium which shows you the actual contents of your thoughts, this is a visualization of how your interests evolved based on the frequency of certain keywords over time. Thoughts are bucketed by certain time intervals (e.g. by week) on a timeline, and the most frequent noun phrases you used in each period are reported. This can be an effective way of getting a sense of how your interests (i.e. the things you've been thinking about) changed through the years.

![](/assets/img/ideoscope_mockup3.png)

## strategies

Taking in the range of stats and visualizations which are part of the ideoscope's dashboard can be an exciting activity in itself, but the real value of this computer-aided introspection practice lies in how it informs your thinking habits. Below are a few general strategies or practices which you might use to make the most out of the deeper understanding of your thought process.

- ideoscopy

You might decide on occasionally performing an audit of your thinking. This could consist in a weekly time slot dedicated to glancing over your ideological metrics and course-correcting your routine in order to reach your target goals. This might mean anything from expressing ideas with more clarity (i.e. readability, conciseness, objectivity) to being on track with your discovery rate of thought based on your average lifespan. The practice of regularly running diagnostics on your thinking might prove a powerful new way of avoiding failure modes on a cognitive level.

- memetic birth rate A/B testing

Do you come up with more new ideas at home or in nature? When reflecting on your own or when chatting with peers? How does memetic birth rate interact with your sleep and diet? Tracking rates of generating new ideas can lead the way to maximizing them via intentional tweaks to your routine.

- temperature schedule

In optimization theory, search algorithms like simulated annealing and genetic algorithms aim to explore more in the beginning and then less and less of the search space as time goes on. Similarly, you might aim to act as a generalist in your youth and gently switch to a specialist as you grow up. Metrics like memetic variability and drift can help you keep your ideological journey on track through best practices derived from theory and empirical data.

## conclusion

The ideoscope is a digital instrument which enables a new dimension of understanding your thought process. Through novel metrics which take advantage of the conceptarium architecture, knowledge workers can get a numerical grip on the ecology of their mind, and start cultivating it rationally.