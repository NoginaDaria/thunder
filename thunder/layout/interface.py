from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

from lazycon import Config
from pydantic import BaseModel, Extra


class Node(BaseModel):
    name: str

    # TODO: no layouts with parents so far
    # parents: Sequence[Node] = ()

    class Config:
        extra = Extra.forbid


class Layout(ABC):
    @abstractmethod
    def build(self, experiment: Path, config: Config) -> Iterable[Node]:
        pass

    @abstractmethod
    def load(self, experiment: Path, node: Optional[Node]) -> Tuple[Config, Path, Dict[str, Any]]:
        pass

    @abstractmethod
    def set(self, **kwargs):
        pass
