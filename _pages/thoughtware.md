---
layout: page
---

## thoughtware [(rss)](/thoughtware/feed.xml)

My research is focused on extending human thinking with artificial ways of thinking. An important part of this venture is bringing to life actual tools which incorporate the artificial affordances I'm designing, and then taking them for a spin. I call this family of tools _thoughtware_, as a more compact version of [tools for thought](https://numinous.productions/ttft/), but with an extra hint of high-tech. Here they are, in reverse chronological order:

<div class="posts" id="Blog">
    <ul>
        {% assign tools = site.thoughtware | sort | reverse %}
        {% for tool in tools %}

        <li>
            <div style="font-weight: normal"><a href="{{ site.baseurl }}{{ tool.url }}">{{ tool.title | downcase }}</a>: {{ tool.description | downcase }}</div>
        </li>
        {% endfor %}
    </ul>

</div>

## principles

I learned a lot about both thoughtware and myself through those projects, and I now have a more refined vision of how thoughtware should be like. It should be open source and self-hosted, in order to ensure better goal alignment between users and tools. It should be modular and composable, in order to support a combinatorial explosion of workflows. It should amplify and extend existing human brilliance rather than dehumanize through atrophy. It should non-judgementally extend the range of thinkable thoughts, rather than limit minds to rationalist conceptions of truth and knowledge. It should be informed by specific strengths and weaknesses of the human psyche as understood in cognitive psychology. It should be defined by its underlying culture and embodied principles, rather than opaque creators.

The conceptual framework I'm currently using as a backdrop for my thoughtware development is centered around terms like: belief, belief system, concept, idea, mental model, metaphor, paradigm, perspective, representation, thought, thought pattern, worldview. I multiplex those with technical terms like: sensor, filter, editor, bot, storage, mapping, search, or sampling.

## future work

In the upcoming years, I plan to bring the following ideas to life, roughly in order:

- an artificial sense organ for insight
- a graph-based belief system editor
- a data-driven memory palace
- a version control system for ideas
- a human language forged by machines
- a tool for mining interdisciplinary metaphors
- a design language which adapts to written meaning
- a growth agent for shared understanding
- a biometric regulator of autonomic arousal
- a groovebox for remixing cognitive processing modes

My work on the thoughtware stack is made possible by a handful of generous sponsors. If you resonate with it and want to support the growth of a new tooling ecosystem for thinking, please consider supporting me via the link below.

<center>
  <div>
    <br>
    <a href="/contact"><button>send feedback</button></a>
    <a href="https://twitter.com/intent/tweet?text={{page.title | urlencode}}%0A%0A{{site.url}}{{page.url | urlencode}}"><button>tweet this</button></a>
    <a href="https://github.com/sponsors/paulbricman"><button>support me 🤍</button></a>
    <br/><br/>
  </div>
</center>
