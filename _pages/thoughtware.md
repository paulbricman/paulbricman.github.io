---
layout: page
---

## projects [(rss)](/thoughtware/feed.xml)

My work is focused on exploring synergies between organic and artificial thought. This usually means putting together proof-of-concept tools based on off-the-shelf ML models or, more recently, tiny experimental investigations into aligning AI to human intentions. I often refer to this family of projects as _thoughtware_.

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

I learned a lot about myself through those projects, and I now have a more refined vision of how thoughtware should be like. It should be open source and self-hosted, in order to ensure better goal alignment between users and tools. It should be modular and composable, in order to support a combinatorial explosion of workflows. It should amplify and extend existing human brilliance rather than dehumanize through atrophy. It should non-judgementally extend the range of thinkable thoughts, rather than limit minds to rationalist conceptions of truth and knowledge. It should be informed by specific strengths and weaknesses of the human psyche as understood in cognitive psychology. It should be defined by its underlying culture and embodied principles, rather than opaque creators.

## themes

In the upcoming years, I plan on exploring the following questions:

- How can we build AI which promotes human agency?
- How can we extend human perception into the digital realm?
- How can AI help us systematically refine our beliefs?
- How can we take advantage of the experience internalized by ML models?
- How can AI help us forage through high-dimensional spaces?

My work on the thoughtware stack, if you will, is made possible by a handful of generous [sponsors](/sponsors). If you resonate with it and want to support an experimental tooling ecosystem for thinking, please consider supporting me via the link below.

<center>
  <div>
    <br>
    <a href="/contact"><button>reply by email</button></a>
    <a href="https://twitter.com/intent/tweet?text={{page.title | urlencode}}%0A%0A{{site.url}}{{page.url | urlencode}}"><button>tweet this</button></a>
    <a href="https://github.com/sponsors/paulbricman"><button>support me 🤍</button></a>
    <br/><br/>
  </div>
</center>
