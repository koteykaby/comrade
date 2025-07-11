from dataclasses import dataclass

@dataclass
class Relationships:
    status_code: 0
    relationships: any
    
def relationship_getRelationships(relationships):
    result = Relationships(
        status_code=0,
        relationships=relationships
    )