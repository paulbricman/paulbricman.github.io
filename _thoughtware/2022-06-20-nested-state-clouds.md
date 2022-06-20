---
layout: tool
title: nested state clouds
description: "Extracting knowledge graphs from pretrained transformers."
image: /assets/img/exemplars-conceptors.png
published: True
---

![](/assets/img/exemplars-conceptors.png)

## nested state clouds ([paper](https://raw.githubusercontent.com/paulbricman/conceptorflow/main/docs/thesis/NSCv3.pdf))

| tl;dr                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Interpretability techniques help ensure the safe deployment of deep learning models into production by providing practitioners with diverse debugging tools, yet the inner workings of large models remain elusive. In this work, we propose a novel interpretability technique which can be used to distill sparse knowledge graphs from a model’s high-dimensional embeddings using conceptors. This technique, termed Nested State Clouds (NSC), takes advantage of the relative spatial layouts of state clouds in latent space (e.g. ”fruit” contextual embeddings appear to engulf ”apple” ones). We successfully apply NSC to a pretrained masked language model, and recover an ontology of concepts grounded in the model’s latent space. |
