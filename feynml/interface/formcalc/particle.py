from dataclasses import dataclass


@dataclass
class Particle:
    def get_pdgid(self) -> int:
        raise NotImplementedError
