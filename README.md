# Ontology-Driven LLM-TAMP

To run the code create a conda environment with python 3.9 using the below command 

```
conda create --name tamp-env python=3.9
conda activate tamp-env
```
To download the Spacy language model, run the following command 
```
python -m spacy download en_core_web_sm
```

## Install dependencies

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

## Run TAMP planning
To run the ontology-driven LLM-TAMP with the following scene, run the command below in the terminal  
![alt text](https://github.com/Muhayyuddin/llm-tamp/blob/main/assets/1.png?raw=true)
```
python main.py --config-name=llm_tamp env=easy_ycb_objects_scene planner=llm_sample_params max_llm_calls=10 play_traj=true use_gui=true

```
To run the ontology-driven LLM-TAMP with the following scene, run the command below in the terminal  
![alt text](https://github.com/Muhayyuddin/llm-tamp/blob/main/assets/2.png?raw=true)
```
python main.py --config-name=llm_tamp env=easy_ycb_tabe_obj planner=llm_sample_params max_llm_calls=10 play_traj=true use_gui=true


```
