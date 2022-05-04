import random
from typing import List, Optional
from parlai.core.opt import Opt
from parlai.core.message import Message
from parlai.core.mutators import register_mutator, EpisodeMutator
from pathlib import Path
from parlai.core.params import ParlaiParser


@register_mutator("interview_context_add")
class InterviewContextAdd(EpisodeMutator):
    """
    Adds a random but reasonable context to an episode.

    OBS: Currently only used for TransformerGenerator models.
    """

    @classmethod
    def add_cmdline_args(
        cls, parser: ParlaiParser, partial_opt: Optional[Opt] = None
    ) -> ParlaiParser:
        parser.add_argument(
            '--context-add-prob',
            default=1.0,
            type=float,
            help='If activated, add context with probability context-add-prob',
        )

    def __init__(self, opt: Opt):
        super().__init__(opt)
        self.rng = random.Random(42)
        # Read the context-files
        # Format: reply_agent\\nreply_human\\n...\\nreply_agent\\nreply_human
        # i.e. always an even number of messages and starting with a reply from an agent
        self.contexts = {}
        with open(
            Path(__file__).parents[2].resolve() / "data/context/fika.txt", "r"
        ) as file:
            self.contexts["fika"] = [
                line.rstrip("\n").split("\\n") for line in file.readlines()
            ]
        with open(
            Path(__file__).parents[2].resolve() / "data/context/intervju.txt", "r"
        ) as file:
            self.contexts["interview"] = [
                line.rstrip("\n").split("\\n") for line in file.readlines()
            ]

    def episode_mutation(self, episode: List[Message]) -> List[Message]:
        """Mutates an episode by adding a context

        Args:
            episode (List[Message]): Episode data

        Returns:
            List[Message]: Episode data with added context
        """
        # Get agents
        context_original = episode[0]["text"].split("\n")
        if len(context_original) % 2 == 0:
            init_agent = "TransformerGenerator"
        else:
            init_agent = "Human"

        # Set the context
        if self.rng.uniform(0, 1) < 0.8:
            situation = "interview"
        else:
            situation = "fika"

        # Add context
        if self.rng.uniform(0, 1) < self.opt["context_add_prob"]:
            context_to_add = self.get_context(situation, init_agent)
            episode[0].force_set("text", "\n".join(context_to_add + context_original))
        return episode

    def get_context(self, situation: str, init_agent: str) -> List[Message]:
        """Get a random subset of context from data

        Args:
            situation (str): Situation, supports: "interview", "fika"
            init_agent (str): Agent with the first comment in teh original episode

        Returns:
            List[Message]: List of messages to prepend to the original episode
        """
        # Get a random conversation from the chosen context
        n_conversations = len(self.contexts[situation])
        conversation = self.contexts[situation][
            self.rng.randint(0, n_conversations - 1)
        ]
        if len(conversation) % 2 != 0:
            print("Warning: nbr of messages in context is not even")

        # Get the context to add
        start_ind = self.rng.randint(0, len(conversation) / 2 - 1) * 2
        context_len = min(
            self.rng.randint(1, (len(conversation) - start_ind) / 2) * 2, 6
        )

        # Make sure the last index corresponds to the correct agent
        if init_agent != "TransformerGenerator":
            context_len -= 1

        # Randomize the agent that starts
        if context_len > 1 and self.rng.uniform(0, 1) < 0.5:
            start_ind += 1
            context_len -= 1
        return conversation[start_ind : start_ind + context_len]
