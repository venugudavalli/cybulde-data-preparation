from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic import field_validator
from pydantic.dataclasses import dataclass

from cybulde.utils.schema_utils import validate_config_parameter_is_in

SPLIT_DELIMITER_BEHAVIOUR_OPTIONS = {"removed", "isolated", "merged_with_previous", "merged_with_next", "contaguous"}


@dataclass
class PreTokenizerConfig:
    _targte_: str = MISSING


@dataclass
class BertPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.BertPreTokenizer"


@dataclass
class ByteLevelPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.ByteLevelPreTokenizer"


@dataclass
class CharDelimiterSplitPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.CharDelimiterSplit"


@dataclass
class DigitsPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Digits"
    individual_digits: bool = False


@dataclass
class MetaspacePreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Metaspace"
    replacement: str = "_"


@dataclass
class PunctuationPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Punctuation"
    behaviour: str = "isolated"

    @field_validator("behaviour")
    def validate_behaviour(cls, behaviour: str)->str:
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOUR_OPTIONS, behaviour, "behaviour")
        return behaviour


@dataclass
class SequencePreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Sequence"
    pretokenizers: list[PreTokenizerConfig] = field(default_factory=lambda: [])
    _pretokenizers_dict: dict[str, PreTokenizerConfig] = field(default_factory=lambda: {})


@dataclass
class SplitPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Split"
    pattern: str = MISSING
    behaviour: str = MISSING
    invert: bool = True

    @field_validator("behaviour")
    def validate_behaviour(cls, behaviour: str)->str:
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOUR_OPTIONS, behaviour, "behaviour")
        return behaviour


@dataclass
class UnicodeScriptsPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.UnicodeScripts"


@dataclass
class WhitespacePreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.Whitespace"


@dataclass
class WhitespaceSplitPreTokenizerConfig(PreTokenizerConfig):
    _targte_: str = "tokenizers.pre_tokenizers.WhitespaceSplit"


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(group="tokenizer/pre_tokenizer", name="bert_pre_tokenizer_schema", node=BertPreTokenizerConfig)
    cs.store(group="tokenizer/pre_tokenizer", name="byte_level_pre_tokenizer_schema", node=ByteLevelPreTokenizerConfig)
    cs.store(
        group="tokenizer/pre_tokenizer",
        name="char_delimiter_split_pre_tokenizer_schema",
        node=CharDelimiterSplitPreTokenizerConfig,
    )
    cs.store(group="tokenizer/pre_tokenizer", name="digits_pre_tokenizer_schema", node=DigitsPreTokenizerConfig)
    cs.store(group="tokenizer/pre_tokenizer", name="metaspace_pre_tokenizer_schema", node=MetaspacePreTokenizerConfig)
    cs.store(
        group="tokenizer/pre_tokenizer", name="punctuation_pre_tokenizer_schema", node=PunctuationPreTokenizerConfig
    )
    cs.store(group="tokenizer/pre_tokenizer", name="sequence_pre_tokenizer_schema", node=SequencePreTokenizerConfig)
    cs.store(group="tokenizer/pre_tokenizer", name="split_pre_tokenizer_schema", node=SplitPreTokenizerConfig)
    cs.store(
        group="tokenizer/pre_tokenizer",
        name="unicode_scripts_pre_tokenizer_schema",
        node=UnicodeScriptsPreTokenizerConfig,
    )
    cs.store(group="tokenizer/pre_tokenizer", name="whitespace_pre_tokenizer_schema", node=WhitespacePreTokenizerConfig)
    cs.store(
        group="tokenizer/pre_tokenizer",
        name="whitespace_split_pre_tokenizer_schema",
        node=WhitespaceSplitPreTokenizerConfig,
    )
