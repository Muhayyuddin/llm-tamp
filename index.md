<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-eval';">

<div  id="home" style="text-align: center; font-size: 24px; margin-bottom: 10px; font-weight: bold; line-height: 1.4;">
        Ontology-driven Prompt Tuning for LLM-based Task and Motion Planning
</div>
<div style="text-align: center; font-size: 16px; margin-bottom: 10px; line-height: 1.4;">
    Muhayy Ud Din, Jan Rosell, Waseem Akram, Isiah Zaplana, Maximo A Roa, Lakmal Seneviratne, and Irfan Hussain
</div>

<div style="text-align: center;">
  {% include button.html text="GitHub" icon="github" link="https://github.com/Muhayyuddin/llm-tamp" color="#0366d6" %}
  {% include button.html text="Preprint" icon="assets/arxiv.png" link="https://arxiv.org/" color="#0366d6"  %}
  {% include button.html text="FAQs"  link="#faqs" color="#0366d6"  %}
</div>
<div style="text-align: center; width: 100%; overflow: hidden;">
  <img src="assets/logo.png" alt="Institution Logos" style="width: 100%; height: auto;">
</div>

<h5 style="margin-bottom: 10px; color=red"> UNDER CONSTRUCTION </h5>

<h5 style="margin-bottom: 10px;"> Overview </h5>
<div style="text-align: justify; font-size: 14px; margin-bottom: 10px; line-height: 1.4;">
Performing complex  manipulation tasks in dynamic environments requires efficient Task and Motion Planning (TAMP) approaches, which combine high-level symbolic plan with low-level motion planning. Advances in Large Language Models (LLMs), such as GPT-4, is transforming task planning by offering natural language as an intuitive and flexible way to describe tasks, generate symbolic plans, and reason. However, the effectiveness of LLM-based TAMP approaches is limited due to static and template-based prompting, which struggles in adapting to dynamic environments and complex task contexts. To address these limitations, this work proposes a novel ontology-driven prompt-tuning framework that employs knowledge-based reasoning to refine and expand user prompts with task contextual reasoning and knowledge-based environment state descriptions. Integrating domain-specific knowledge into the prompt ensures semantically accurate and context-aware task plans. The proposed framework demonstrates its effectiveness by resolving semantic errors in symbolic plan generation, such as maintaining logical temporal goal ordering in scenarios involving hierarchical object placement. The proposed framework is validated through both simulation and real-world scenarios, demonstrating significant improvements over the baseline approach in terms of adaptability to dynamic environments, and the generation of semantically correct task plans. 
</div>
<h5 style="margin-bottom: 10px;">Knowledge-oriented LLM-TAMP results</h5> 
<h7 style="margin-bottom: 10px;">Results in Real Environment</h7> 

<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">

<video width="100%" height="auto" controls autoplay muted loop>
  <source src="https://github.com/Muhayyuddin/llm-tamp/raw/refs/heads/llm-site/assets/Onto-LLM-1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>



</div>
<h7 style="margin-bottom: 10px;">Results in Simulation Environment</h7> 
<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">

<video width="100%" height="auto" controls autoplay muted loop>
  <source src="https://github.com/Muhayyuddin/llm-tamp/raw/refs/heads/llm-site/assets/sim1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

<video width="100%" height="auto" controls autoplay muted loop>
  <source src="https://github.com/Muhayyuddin/llm-tamp/raw/refs/heads/llm-site/assets/sim2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

</div>

<h6 style="margin-bottom: 5px;"> Prompt Tuning Results on Random User Inputs</h6>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    We tested the proposed prompt tunning framework on different random user inputs within the kitchen domain to test the prompt tuning module. Below video shows some sample responses.
</div>
<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">

  <iframe width="560" height="300" 
          src="https://www.youtube.com?autoplay=1&mute=1&loop=1&playlist=6SRgelFJeew" 
          title="YouTube video player" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
  </iframe>

</div> 

<!--<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    Trackers performance on real data.
</div>
<div style="text-align: center;">
  <img src="assets/ssp4.png" alt="framework" />
</div>!-->

<h5 id="framework" style="margin-bottom: 10px;">Tracking Framework</h5>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
The ontology-driven LM-TAMP framework enhances prompt elaboration for generating semantically accurate symbolic plans. It begins by processing the user input to extract actions and objects through semantic tagging. The Contextual Inference Engine uses SPARQL queries to retrieve object types and priorities from the ontology, ensuring the correct action sequence based on predefined rules. The Perception Module, with YOLO-based object detection and FoundationPose for object pose estimation, provides real-time spatial data. This information is textualize using ontological knowledge by the Env State Descriptor and fed into the Prompt Generator. The final prompt is then fed into the LLM Task Planner, which produces a structured task plan. Finally, the Motion Planner ensures the robot executes the task with feasible, collision-free movements.
</div>
<div style="text-align: center;">
  <img src="assets/ssp4.png" alt="framework" />
</div>

<h5 id="framework" style="margin-bottom: 10px;">Ontological Knowledge Graph Framework</h5>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
Below is the ontological knowledge graph from the ontologies that are used in the paper as example use cases
</div>
<div style="text-align: center;">
  <img src="assets/ontograph.png" alt="framework" />
</div>

<h5 id="faqs" style="margin-bottom: 10px;">FAQs</h5>
<h8>Q1- Why we need Ontology-driven LLM-TAMP?</h8> 
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
---
</div>
<h8>Q2- Why we just used GPT-4 why not other LLM models?</h8> 
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
---
</div>
<h8>Q3- What is the benefit of this research work?</h8>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
---
</div>
<h8>Q3- What is the limitations of the proposed approach?</h8>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
---
</div>

