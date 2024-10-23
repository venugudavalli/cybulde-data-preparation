from dataclasses import field
from typing import Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass

# from pydantic import field_validator
# from cybulde.utils.schema_utils import validate_config_parameter_is_in

SPLIT_DELIMITER_BEHAVIOUR_OPTIONS = {"removed", "isolated", "merged_with_previous", "merged_with_next", "contaguous"}


@dataclass
class TrainerConfig:
    _targte_: str = MISSING
    vocab_size: Optional[int] = None
    show_progress: bool = True
    min_frequency: int = 0
    special_tokens: Optional[list[str]] = field(
        default_factory=lambda: [
            SI("${tokenizer.unk_token}"),
            SI("${tokenizer.cls_token}"),
            SI("${tokenizer.sep_token}"),
            SI("${tokenizer.pad_token}"),
            SI("${tokenizer.mask_token}"),
        ]
    )


@dataclass
class BpeTrainerConfig(TrainerConfig):
    _targte_: str = "tokenizers.trainers.BpeTrainer"
    vocab_size: int = 30000
    initial_alphabet: list[str] = field(default_factory=lambda: [])


@dataclass
class UnigramTrainerConfig(TrainerConfig):
    _targte_: str = "tokenizers.trainers.UnigramTrainer"
    vocab_size: int = 8000
    initial_alphabet: Optional[list[str]] = None
    shrinking_factor: float = 0.75
    unk_token: Optional[str] = SI("${tokenizer.unk_token}")
    max_piece_length: int = 16
    n_sub_iterations: int = 2


@dataclass
class WordLevelTrainerConfig(TrainerConfig):
    _targte_: str = "tokenizers.trainers.WordLevelTrainer"


@dataclass
class WordPieceTrainerConfig(TrainerConfig):
    _targte_: str = "tokenizers.trainers.WordPieceTrainer"
    vocab_size: int = 30000
    limit_alphabet: Optional[int] = None
    initial_alphabet: list[str] = field(default_factory=lambda: [])
    continuing_subword_prefix: Optional[str] = "##"
    end_of_word_suffix: Optional[str] = None


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(group="tokenizer/trainer", name="bpe_trainer_schema", node=BpeTrainerConfig)
    cs.store(group="tokenizer/trainer", name="unigram_trainer_schema", node=UnigramTrainerConfig)
    cs.store(group="tokenizer/trainer", name="word_level_trainer_schema", node=WordLevelTrainerConfig)
    cs.store(group="tokenizer/trainer", name="word_piece_trainer_schema", node=WordPieceTrainerConfig)
