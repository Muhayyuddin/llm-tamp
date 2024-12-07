# Ontology-Driven LLM-TAMP
## Abstract
<div style="text-align: justify;">
Performing complex manipulation tasks in dynamic environments requires efficient Task and Motion Planning (TAMP) approaches, which combine high-level symbolic plan with low-level motion planning. Advances in Large Language Models (LLMs), such as GPT-4, is transforming task planning by offering natural language as an intuitive and flexible way to describe tasks, generate symbolic plans, and reason. However, the effectiveness of LLM-based TAMP approaches is limited due to static and template-based prompting, which struggles in adapting to dynamic environments and complex task contexts. To address these limitations, this work proposes a novel ontology-driven prompt-tuning framework that employs knowledge-based reasoning to refine and expand user prompts with task contextual reasoning and knowledge-based environment state descriptions. Integrating domain-specific knowledge into the prompt ensures semantically accurate and context-aware task plans. The proposed framework demonstrates its effectiveness by resolving semantic errors in symbolic plan generation, such as maintaining logical temporal goal ordering in scenarios involving hierarchical object placement. The proposed framework is validated through both simulation and real-world scenarios, demonstrating significant improvements over the baseline approach in terms of adaptability to dynamic environments, and the generation of semantically correct task plans.
</div>


## Install dependencies

To run the code create a conda environment with python 3.9 using the below command 

```
conda create --name tamp-env python=3.9
conda activate tamp-env
```
To download the Spacy language model, run the following command 
```
python -m spacy download en_core_web_sm
```


```bash
git clone https://github.com/Muhayyuddin/llm-tamp.git
cd llm-tamp
pip install -r requirements.txt
```
## Before Running

Please, create a folder `openai_keys` under the project directory; and create a file `openai_key.json` under the folder `openai_keys`;  fill in this json file with your openAI API key:

```bash
{
    "key": "",
    "org": "",
    "proxy" : ""
}
```

## Run Ontology-driven LLM-TAMP planning
To run the ontology-driven LLM-TAMP with the following scene, run the command below in the terminal  

<img src="https://github.com/Muhayyuddin/llm-tamp/blob/main/assets/1.png?raw=true" alt="alt text" width="500"/>

```
python main.py --config-name=llm_tamp env=easy_ycb_objects_scene planner=llm_sample_params max_llm_calls=10 play_traj=true use_gui=true

```
To run the ontology-driven LLM-TAMP with the following scene, run the command below in the terminal  

<img src="https://github.com/Muhayyuddin/llm-tamp/blob/main/assets/2.png?raw=true" alt="alt text" width="500"/>

```
python main.py --config-name=llm_tamp env=easy_ycb_tabe_obj planner=llm_sample_params max_llm_calls=10 play_traj=true use_gui=true


```
## Acknowledgment
Thank you for the nice work done by LLM3, FoundationPose, and FoundationPose-ROS2 , we use some code from these repositories to implement our Ontology-deriven-LLM-TAMP framework.

https://github.com/AssassinWS/LLM-TAMP

https://github.com/NVlabs/FoundationPose

https://github.com/ammar-n-abbas/FoundationPoseROS2
