from hpotk import Ontology, MinimalTerm

from deft_matcher.ontology_class import OntologyClass


def get_ontology_prefix(ontology: Ontology) -> str:
    for term_id in ontology.term_ids:
        prefix = term_id.prefix
        break

    return prefix


def get_oc(term: MinimalTerm) -> OntologyClass:
    return OntologyClass(term.identifier.value, term.name)
