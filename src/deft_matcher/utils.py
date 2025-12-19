from hpotk import Ontology


def get_ontology_prefix(ontology: Ontology):
    for term_id in ontology.term_ids:
        prefix = term_id.prefix
        break

    return prefix
