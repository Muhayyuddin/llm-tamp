import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from planners.base_planner import BasePlanner
from utils.llm_util import LLMBase
from utils.io_util import load_txt
from utils.tamp_util import text_to_actions, PrimitiveAction, Action, TAMPFeedback
from ontology_reasoner.smart_kitchen import TaskReasoner
import time
from envs.constants import ASSETS_DIR
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ontology_path = os.path.join(ASSETS_DIR, "smart_kitchen.rdf")

namespace = "http://www.semanticweb.org/muhayy/ontologies/2024/kitchen#"
logger = logging.getLogger(__name__)



class LLMTAMPPlanner(BasePlanner, LLMBase):
    """LLM TAMP Planner"""

    def __init__(
        self,
        planner_prompt_file: str,
        env_desc_file: str,
        primitive_actions: Dict[str, PrimitiveAction],
        with_mp_feedback: bool = True,
        trace_size: int = 3,
        env_name: str = "",  # Add the new string argument here
        *args,
        **kwargs,
    ):
        BasePlanner.__init__(self, primitive_actions=primitive_actions, *args, **kwargs)
        LLMBase.__init__(self, use_gpt_4=True, *args, **kwargs)

        # load planning prompt template
        prompt_template_folder = Path(__file__).resolve().parent.parent / "prompts"
        planning_prompt_template = load_txt(
            prompt_template_folder / "planners" / f"{planner_prompt_file}.txt"
        )

        # load problem file
        domain_desc = load_txt(prompt_template_folder / "envs" / env_desc_file)
        #self.task_to_do = input("Please tell me what should I do for you : ")
        self._planning_prompt = planning_prompt_template.replace("{domain_desc}", domain_desc)#.replace("{task}", self.task_to_do)

        #self._planning_prompt = planning_prompt_template.replace("{domain_desc}", domain_desc)


        self.with_mp_feedback = with_mp_feedback
        self.trace_size = trace_size

        # trace
        self._trace = []
        
        self.env_name = env_name

    def reset(self):
        self._trace = []

    def _prepare_planning_prompt(
        self, obs_text: str, feedback_text: str, symbolic_plan: List[str] = []
    ):
        
        if self.env_name == 'easy_ycb_table_obj':
            self.task_to_do = 'clean the table, move sugar_box, tomato_can, and cracker_box to the left_table and move plate and cup to the right_table' 
        elif self.env_name == 'easy_ycb_objects_scene':     
            self.task_to_do = 'put apple and  green_bowl in the grey_plate'        #input("Please tell me what should I do for you : ")
        #self.task_to_do =input('what should I do for you: ') 
        reasoner = TaskReasoner(ontology_path)
        start_time = time.time()
        semantic_enhancement, symbolic_order= reasoner.execute_task(self.task_to_do)
        print(symbolic_order)
        # replace state
        planning_prompt = self._planning_prompt.replace("{state}", obs_text)

        # replace trace
        trace_text = "\n"
        for plan, reason in self._trace[-self.trace_size :]:
            if len(plan) > 0:
                trace_text += f"Plan: {plan}\n"
            # trace_text += f"Reason: {reason}\n"

        if len(feedback_text) > 0:
            trace_text += f"Plan: {feedback_text}\n"

        if trace_text == "\n":
            trace_text += "No previous plan"

        planning_prompt = planning_prompt.replace("{trace}", trace_text)
        
        # symbolic plan
        if "{task}" in planning_prompt:
            planning_prompt = planning_prompt.replace("{task}", self.task_to_do)
        if "{note}" in planning_prompt:
            planning_prompt = planning_prompt.replace("{note}", semantic_enhancement)
        if "{symbolic_plan}" in planning_prompt:
             planning_prompt = planning_prompt.replace("{symbolic_plan}", symbolic_order)
        #if "{symbolic_plan}" in planning_prompt:
        #     planning_prompt = planning_prompt.replace("{symbolic_plan}", str(symbolic_plan))
        end_time = time.time()
        total_time= end_time-start_time
        print("total time is ", total_time)
        return planning_prompt

    def plan(
        self,
        obs_text: str,
        feedback_list: List[Tuple[Action, TAMPFeedback]],
        symbolic_plan: List[str] = [],
        *args,
        **kwargs,
    ):
        # prepare feedback
        if self.with_mp_feedback:
            feedback_text = ", ".join(
                [
                    f"{str(action)}(Motion: {feedback.motion_planner_feedback})"
                    for action, feedback in feedback_list
                ]
            )
        else:
            feedback_text_list = []
            for action, feedback in feedback_list:
                if feedback.action_success:
                    feedback_text_list.append(f"Motion: {str(action)}(Success)")
                else:
                    feedback_text_list.append(f"Motion: {str(action)}(Failure)")

            feedback_text = ", ".join(feedback_text_list)

        if len(feedback_list) > 0 and feedback_list[-1][1].action_success:
            feedback_text += f"(Task: {feedback_list[-1][1].task_process_feedback})"

        # plan
        planning_prompt = self._prepare_planning_prompt(obs_text, feedback_text, symbolic_plan)

        plan_iter = 0
        plan, reasoning = None, None
        while plan_iter < 5:
            plan_iter += 1
            try:
                llm_output = json.loads(self.prompt_llm(planning_prompt, force_json=True))
                plan = text_to_actions(llm_output["Full Plan"], self._primitive_actions)
                reasoning = llm_output["Reasoning"]
                break
            except Exception as e:
                logger.warning(f"Fail to generate plan or parse output, try again! {e}")
                import pdb

                pdb.set_trace()

        # save last feedback & reasoning to trace
        if plan is None:
            return None
        else:
            self._trace.append((feedback_text, reasoning))

        # import pdb

        # pdb.set_trace()

        return plan
