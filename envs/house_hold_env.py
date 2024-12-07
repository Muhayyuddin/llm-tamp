import logging
import random
import numpy as np
from envs.constants import COLOR_MAP
from envs.pb_env import PybulletEnv
from utils.io_util import load_json, dump_json
from utils.tamp_util import Action, PrimitiveAction, Parameter
from utils.llm_util import textualize_array
import pybullet as p
import pybullet_data
from ontology_reasoner.perception import YOLOv8Detector
from envs.constants import ASSETS_DIR
import time as t
import cv2
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
PATH = os.path.join(ASSETS_DIR, "urdf/")

class HouseHoldObjEnv(PybulletEnv):
    """
    An environment for packing boxes in a compact basket.
    Use top grasp.
    """

    def __init__(self):
        super().__init__()

        self._primitive_actions = {
            "pick": PrimitiveAction(name="pick", obj_arity=1),
            "place": PrimitiveAction(
                name="place",
                obj_arity=1,
                parameters={
                    "x": Parameter("x", lower_limit=0.0, upper_limit=1.4),
                    "y": Parameter("y", lower_limit=-1.0, upper_limit=1.0),
                    "theta": Parameter("theta", lower_limit=-3.14, upper_limit=3.14),
                },
            ),
        }

    def __str__(self):
        return "PackCompactEnv"

    def reset(self, basket, urdfs, use_gui=True):
        super().reset(use_gui=use_gui)

        # create table
        self.create_table()
        self.create_table_dinner()
        # create basket
        self.create_basket(x=basket["x"], y=basket["y"], w=basket["w"], l=basket["l"])
        
        for urdf_info in urdfs.values():
            urdf_path = PATH+urdf_info["name"]+"/"+urdf_info["name"]+".urdf"
            print("The URDF values are :")
            print(urdf_info["name"])
            print("path is :")
            print(PATH+urdf_info["name"]+"/"+urdf_info["name"])
            position = [urdf_info["x"],urdf_info["y"],urdf_info["z"]]
            self.create_obj_from_urdf(urdf_info["name"], urdf_path, position)


        # physical simulation
        self.simulate()
 
        # self.detector = YOLOv8Detector()

        #         # Set up the camera
        # view_matrix, projection_matrix, width, height = self.detector.setup_pybullet_camera()

        #     # Initialize the YOLOv8 detector

            
        # for i in range(5):
        #     # Capture an image from the PyBullet camera
        #     camera_image = self.detector.get_camera_image(view_matrix, projection_matrix, width, height)

        #     # Ensure the image is correctly formatted for OpenCV
        #     camera_image = camera_image.astype(np.uint8)

        #     # Detect objects in the image
        #     results = self.detector.detect(camera_image)

        #     # Draw detections on the image
        #     image_with_detections = self.detector.draw_detections(camera_image, results)
        #     self.detector.save_detections_to_file(camera_image, results, 'detection.txt')

        #     # Display the image with detections
        #     cv2.imshow("YOLOv8 Detections", image_with_detections)

        #     # Break loop and close window when SPACE is pressed
        #     if cv2.waitKey(1) & 0xFF == 32:  # 32 is the ASCII code for the SPACE key
        #         break

        #     # Add a small delay for better visualization
        #     t.sleep(0.1)

        # # Clean up OpenCV windows after the loop ends
        # cv2.destroyAllWindows()
        observation = self.get_observation()
        return observation

    def apply_action(self, action: Action, play_traj: bool = False):
        # sanity check
        if action is None:
            return False, "No action is given!"
        if not action.primitive in self._primitive_actions.values():
            return False, "Unknown primitive action!"
        for obj_name in action.obj_args:
            if not obj_name in self.objects:
                return False, "Unknown object name!"

        if action.traj is not None and len(action.traj) > 0:
            traj = action.traj
        else:
            traj = None

        if action.primitive.name == "pick":
            obj_name = action.obj_args[0]
   
            object = self.objects[obj_name]

            # prepare obstacles (avoid all other objects)
            obstacles = self.prepare_obstacles(obj_name_list=[obj_name], remove_mode=True)

            success, traj, mp_feedback = self.robot.pick(
                object, obstacles, grasp_direction="top", traj=traj, play_traj=play_traj
            )
            if success:
                logger.debug("Picked!")
            else:
                logger.debug(f"Pick is not executed:{mp_feedback}")

            # don't simulate at pick
            t.sleep(1)
        elif action.primitive.name == "place":
            obj_name = action.obj_args[0]
            object = self.objects[obj_name]
            print("the pick instructions are generated for ")
            print(obj_name)
            
            # prepare obstacles (avoid all other objects)
            obstacles = self.prepare_obstacles(obj_name_list=[obj_name], remove_mode=True)

            print("obstacles are ")
            print(obstacles)
            success, traj, mp_feedback = self.robot.place(
                object,
                obstacles,
                # randomly sample x,y for ablation study
                x=action.param_args["x"],
                y=action.param_args["y"],
                z=0.21,
                theta=action.param_args["theta"],
                traj=traj,
                play_traj=play_traj,
            )
            # only simulate at successful place
            if success:
                self.simulate()
                self.theta_dict[obj_name] = action.param_args["theta"]
                logger.debug("Placed!")
            else:
                logger.debug(f"Place is not executed:{mp_feedback}")
            t.sleep(2)

        # assign traj
        if action.traj is None or len(action.traj) == 0:
            action.traj = traj
        return success, mp_feedback
#GM: This function is generating the observation part of the promptingfor LLM
    def get_observation(self):
        observation = super().get_observation()
        # remove table & basket from observation
        observation.pop("table")
        basket_obs = observation.pop("basket")

        # textualize observation
        # add basket info
        x_range = np.array([basket_obs["bb_min"][0], basket_obs["bb_max"][0]])
        y_range = np.array([basket_obs["bb_min"][1], basket_obs["bb_max"][1]])
        basket_text = f"The basket has a rectangular shape, ranges {textualize_array(x_range)} along the x axis, and ranges {textualize_array(y_range)} along the y axis."

        # add box info
        boxes_text = f"There are several objects in the envrionment: {', '.join(observation.keys())}."
        for object_name, object_state in observation.items():
            boxes_text += f"\n{object_name} is at position {textualize_array(object_state['position'])}, and it has min bounding box corner {textualize_array(object_state['bb_min'])} and max bounding box corner {textualize_array(object_state['bb_max'])},"
            width = object_state["bb_max"][0] - object_state["bb_min"][0]
            length = object_state["bb_max"][1] - object_state["bb_min"][1]
            boxes_text += f"its length along x axis is {textualize_array(width)}, its length along y axis is {textualize_array(length)}."

        # predicate info
        predicate_list = []
        for object_name in observation.keys():
            if self.check_in_basket(object_name):
                predicate_list.append(f"{object_name} is in basket")
            else:
                predicate_list.append(f"{object_name} is not in basket")

        predicate_text = ", ".join(predicate_list) + "."

        obs_text = basket_text + "\n" + boxes_text + "\n" + predicate_text
        return observation, obs_text
#GM: This part generate the sample symbolic plan for the LLM 
    def get_symbolic_plan(self):
        return [
            "pick(['suger'], {})",
            "place(['suger'], {'x': ?, 'y': ?, 'theta': ?})",
            "pick(['TomatoSoupCan'], {})", 

        ]

    def check_in_basket(self, obj_name, tol=0.015):
        min_bb_basket, max_bb_basket = self.get_bb("basket")
        min_bb_obj, max_bb_obj = self.get_bb(obj_name)

        if (
            min_bb_obj[0] > min_bb_basket[0] - tol
            and max_bb_obj[0] < max_bb_basket[0] + tol
            and min_bb_obj[1] > min_bb_basket[1] - tol
            and max_bb_obj[1] < max_bb_basket[1] + tol
        ):
            return True
        return False

    def check_goal(self):
        is_goal = True
        feedback = []
        for obj_name in self.objects.keys():
            if obj_name != "basket" and obj_name != "table":
                if not self.check_in_basket(obj_name):
                    is_goal = False
                    feedback.append(f"{obj_name} is not in basket")

        return is_goal, ", ".join(feedback)

    def create_task_instances(
        self,
        env_config,
        num_instances,
        save_to_file=False,
        instance_file=None,
        overwrite=False,
    ):
        # # if already exists, load from file
        # if instance_file is not None and instance_file.exists() and not overwrite:
        #     task_instances = load_json(instance_file)
        #     logger.info(f"Load from existing file {instance_file}.")

        # else:
        task_instances = {}
        for task_i in range(num_instances):
            basket_info = {
                "x": env_config.basket.x,
                "y": env_config.basket.y,
                "w": env_config.basket.w,
                "l": env_config.basket.l,
            }

            # sample box locations
            # todo: fill in algorithm for sampling initial box locations
            boxes_info = {}
            xmin, xmax = [-0.2, 0.2]
            last_y = -0.6
            gripper_length = 0.09
            for box_i, (object_name, obj) in enumerate(env_config.urdfs.items()):
                x = random.uniform(xmin, xmax)
                y = random.uniform(xmin, xmax)

                box_info = {
                    "name": object_name,
                    "x": obj.x,
                    "y": obj.y,
                    "z": obj.z,
                }

                boxes_info[box_i] = box_info

            instance = {"basket": basket_info, "urdfs": boxes_info}
            task_instances[task_i] = instance

        if save_to_file:
            assert (
                instance_file is not None
            ), "instance_file must be specified when save_to_file is True"

            dump_json(task_instances, instance_file)

        return task_instances
