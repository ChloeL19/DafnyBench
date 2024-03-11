from dataclasses import dataclass, field
from transformers import HfArgumentParser, set_seed

@dataclass
class CommonArguments:
    max_completion_depth: int = field(default=30, metadata={"help": "Limit for the depth of the mcts"})
    experiment_name: str = field(default="run.py", metadata={"help": "Pick an experiment to run "})
    mins_timeout: float = field(default=None, metadata={"help": "Set a default timeout for each trial "})
    seed: int = field(default=None, metadata={"help": "Set the seed for reproducible behavior"})

def get_args():
    parser = HfArgumentParser(CommonArguments)
    args = parser.parse_args_into_dataclasses()[0]
    return args

args = get_args()
if args.seed is not None:
    set_seed(args.seed)
