#ontology-Driven LLM-TAMP

To run the code create a conda environment with python 3.9 using the below command 

```
conda create --name tamp-env python=3.9
conda activate tamp-env
```

# Install pybullet
pip install pybullet

# Install hydra-core
pip install hydra-core

# Install hydra-core
pip install spacy

pip install "numpy<2"

python -m spacy download en_core_web_sm
pip install -m spacy download en_core_web_sm

pip install rdflib

pip install ultralytics





# Prerequisite

## Install dependencies

```bash
git clone git@github.com:AssassinWS/LLM-TAMP.git
cd LLM-TAMP
pip install -r requirements.txt
```

## Project structure
- `assets`: robots configurations and environment assets
- `configs`: config parameters for the environment and planners
- `envs`: the developed environment based on Pybullet
- `task_instances`: randomly generated task instances
- `planners`: TAMP planners
- `prompts`: prompt templates
- `utils`: utility functions

We use `hydra-core` to configure the project.


# Usage

## Before Running

First, create a folder `openai_keys` under the project directory; Second, create a file `openai_key.json` under the folder `openai_keys`; Third, fill in this json file with your openAI API key:

```bash
{
    "key": "",
    "org": "",
    "proxy" : ""
}
```

## Run TAMP planning
