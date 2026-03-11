from deft_matcher.matcher import Matcher
from deft_matcher.ontology_class import OntologyClass
from deft_matcher.resolver import Resolver
from deft_matcher.retriever import Retriever


class CombinedMatcher(Matcher):
    retriever: Retriever
    resolver: Resolver
    name: str

    def __init__(self, retriever: Retriever, resolver: Resolver, matcher_name: str):
        """
        Combines a Retriever and a Resolver to create a Matcher.
        """
        self.retriever = retriever
        self.resolver = resolver
        self.matcher_name = matcher_name

    @property
    def name(self) -> str:
        return self.name

    def match(self, free_text: str) -> OntologyClass | None:
        candidates: list[OntologyClass] = self.retriever.get_matches(free_text)
        return self.resolver.resolve(candidates)
