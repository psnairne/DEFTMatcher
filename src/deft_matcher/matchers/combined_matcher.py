from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.resolver import Resolver
from deft_matcher.retriever import Retriever


class CombinedMatcher(Matcher):
    retriever: Retriever
    resolver: Resolver

    def __init__(self, retriever: Retriever, resolver: Resolver):
        """
        Combines a Retriever and a Resolver to create a Matcher.
        """
        self.retriever = retriever
        self.resolver = resolver

    @property
    def name(self) -> str:
        return self.retriever.name + "+" + self.resolver.name

    def match(self, free_text: str) -> OntologyClass | None:
        candidates: list[OntologyClass] = self.retriever.get_matches(free_text)
        return self.resolver.resolve(candidates)
