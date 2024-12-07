from termcolor import colored
import spacy
from rdflib import Graph, Namespace, RDF

class TaskReasoner:
    def __init__(self, rdf_file="smart_kitchen.rdf"):
        self.nlp = spacy.load("en_core_web_sm")
        self.g = Graph()
        self.g.parse(rdf_file)
        self.EX = Namespace("http://www.example.org/kitchen_ontology#")
        self.g.bind("ex", self.EX)

    def process_input(self, user_input):
        """Extract action and objects (including compound nouns) from input text."""
        doc = self.nlp(user_input)
        action = None
        objects = []

        # Identify the action (main verb) and exclude "move"
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_ not in ["move"] and token.lemma_ in [
                "clean", "arrange", "put", "remove", "serve", "push", "clear", "stack"
            ]:
                action = token.text
                break

        # Identify objects (nouns and compound nouns) and preserve terms with underscores
        for token in doc:
            if "_" in token.text:
                objects.append(token.text.lower())
            elif token.pos_ == "NOUN" and token.text.lower() not in ["table", "kitchen"]:
                compound_parts = [child.text for child in token.lefts if child.dep_ == "compound"]
                if compound_parts:
                    compound = "_".join(compound_parts)
                    object_name = f"{compound}_{token.text}".strip("_").lower()
                else:
                    object_name = token.text.lower()
                if object_name not in ["items", "things"]:
                    objects.append(object_name)
        return action, list(set(objects))

    def query_rdf(self, object_name):
        """Query RDF to get the class/type of a specific object."""
        query = f"""
        PREFIX ex: <http://www.example.org/kitchen_ontology#>
        SELECT ?type WHERE {{
            ?obj a ?type ;
                 rdfs:label ?label .
            FILTER (lcase(str(?label)) = "{object_name.lower()}")
        }}
        """
        result = self.g.query(query)
        object_types = [str(row.type).split("#")[-1] for row in result]
        return object_types

    def get_action_mapping(self, action_key):
        """Map high-level actions to primitive actions."""
        action_mapping = {
            "put": "place",
            "clean": "pick",
            "arrange": "put",
            "clear": "pick",
            "stack": "put",
            "remove": "pick"
        }
        return action_mapping.get(action_key, "Action not found")

    def get_priority(self, object_types, action):
        """Query RDF to get priority and description for given action and object type."""
        best_priority = None
        best_description = None

        for object_type in object_types:
            query = f"""
            PREFIX ex: <http://www.example.org/kitchen_ontology#>
            SELECT ?priority ?description WHERE {{
                ?rule rdf:type ex:ActionPriority ;
                      ex:hasAction "{action}" ;
                      ex:hasObjectType "{object_type}" ;
                      ex:hasPriority ?priority ;
                      ex:hasDescription ?description .
            }}
            """
            result = self.g.query(query)
            for row in result:
                priority = int(row.priority)
                description = str(row.description)
                if best_priority is None or priority < best_priority:
                    best_priority = priority
                    best_description = description

        return best_priority, best_description

    def reason_action(self, action, objects):
        """Perform reasoning based on RDF rules and extracted objects."""
        priority_groups = {}

        for obj in objects:
            obj_types = self.query_rdf(obj)
            if obj_types:
                priority, description = self.get_priority(obj_types, action)
                if priority is not None and description is not None:
                    if (priority, description) not in priority_groups:
                        priority_groups[(priority, description)] = []
                    priority_groups[(priority, description)].append(obj)

        sorted_priorities = sorted(priority_groups.items(), key=lambda x: x[0][0])
        reasoning_output = []

        # Create grouped reasoning statements
        for (priority, description), grouped_objects in sorted_priorities:
            reasoning_output.append(
                f"{self.get_action_mapping(action)} {', '.join(grouped_objects)} {description}"
            )

        return reasoning_output, sorted_priorities

    def generate_task_commands(self, grouped_objects):
        """Generate task commands based on the grouped objects."""
        commands = []
        for _, grouped_objects in grouped_objects:
            for obj in grouped_objects:
                commands.append(f"pick(['{obj}'], {{}})")
                commands.append(f"place(['{obj}'], {{'x': ?, 'y': ?, 'theta': ?}})")
        return commands

    def print_reasoned_output(self, action, objects, reasoned_output):
        """Print the reasoning results."""
        print(colored(f"Action: {action}", "blue", attrs=["bold"]))
        print(f"Objects: {objects}\n")
        print(colored("Reasoned Output:", "green", attrs=["bold"]))
        for reasoning in reasoned_output:
            print(colored(reasoning, 'cyan'))

    def execute_task(self, sentence):
        """Execute task: process input, reason, and print output."""
        action, objects = self.process_input(sentence)
        if action and objects:
            reasoned_output, grouped_objects = self.reason_action(action, objects)
            self.print_reasoned_output(action, objects, reasoned_output)
            commands = self.generate_task_commands(grouped_objects)
            #print(colored("Generated Commands:", "yellow", attrs=["bold"]))
            cmd = "[ "
            for command in commands:
                cmd= cmd + command +" "
            cmd= cmd + " ]"   
                
            res = " "
            for reasoning in reasoned_output:
                res = res + reasoning + " "
        elif action is None:
            print(colored("No valid action found in the input.", "red"))
        elif not objects:
            print(colored("No valid objects found in the input.", "red"))
        return res, cmd

