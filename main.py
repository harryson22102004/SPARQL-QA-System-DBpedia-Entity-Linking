import re
 
class EntityLinker:
    def __init__(self):
        # Simulated entity→DBpedia URI mapping
        self.kb = {
            'albert einstein': 'dbr:Albert_Einstein',
            'marie curie': 'dbr:Marie_Curie',
            'python': 'dbr:Python_(programming_language)',
            'paris': 'dbr:Paris', 'france': 'dbr:France',
            'barack obama': 'dbr:Barack_Obama',
        }
    def link(self, mention):
        return self.kb.get(mention.lower(), f'dbr:{mention.replace(" ","_")}')
 
class SPARQLQueryBuilder:
    def __init__(self):
        self.templates = {
            'birth_place': 'SELECT ?place WHERE {{ {entity} dbo:birthPlace ?place }}',
            'birth_date':  'SELECT ?date  WHERE {{ {entity} dbo:birthDate ?date }}',
            'nationality': 'SELECT ?nat   WHERE {{ {entity} dbo:nationality ?nat }}',
            'known_for':   'SELECT ?known WHERE {{ {entity} dbo:knownFor ?known }}',
        }
    def build(self, entity_uri, question_type):
        template = self.templates.get(question_type, '')
        return template.format(entity=entity_uri)
      def classify_question(q):
    q = q.lower()
    if any(w in q for w in ['born', 'birthplace', 'from', 'birth place']): return 'birth_place'
    if 'when' in q and 'born' in q: return 'birth_date'
    if 'nationality' in q or 'citizen' in q: return 'nationality'
    if 'known' in q or 'famous' in q: return 'known_for'
    return 'unknown'
 
def extract_entities(question):
    words = question.split()
    entities = []
    i = 0
    while i < len(words):
        if words[i][0].isupper() and words[i].lower() not in {'where','when','what','who','which','is'}:
            entity = words[i]
            if i+1 < len(words) and words[i+1][0].isupper():
                entity += ' ' + words[i+1]; i += 1
            entities.append(entity)
        i += 1
    return entities
 
linker = EntityLinker()
builder = SPARQLQueryBuilder()
questions = [
    "Where was Albert Einstein born?",
    "What is Marie Curie known for?",
    "When was Barack Obama born?",
]
for q in questions:
    entities = extract_entities(q)
    qtype = classify_question(q)
    print(f"Q: {q}")
    for e in entities:
        uri = linker.link(e)
        sparql = builder.build(uri, qtype)
        print(f"  Entity: {e} → {uri}")
        if sparql: print(f"  SPARQL: {sparql}")
    print()
