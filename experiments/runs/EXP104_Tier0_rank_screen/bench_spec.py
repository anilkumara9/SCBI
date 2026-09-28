# EXP104 Tier-0 bench spec — S4-8 k=8 2-hop bench (builder: EXP104 Tier-0 execution lane, 2026-09-28).
# Foil designations below were made at bench-build time, BEFORE any model contact (D3 blindness).
# v2 2026-09-28: G1 real-tokenizer probe (EXP090 lesson) found 58/480 option strings
# multi-token under the pinned gpt-neox-20b artifact. All option strings below are
# from the G1-verified single-token pools (75 countries, 52 cities, 8 elements, 27 states
# screened 2026-09-28). Element templates T4/T5/T9 rebuilt as country/city templates
# (T4' rivers, T5'' museums->city, T9'' treaties); three distractor words replaced.
# Format: (question, correct, [7 distractors], foil, foil_rationale)
# NOTE: correct answer is listed FIRST here only for construction; positions are
# shuffled by build_bench.py with a pinned seed AFTER checker verification.

TEMPLATE = """Q: {question}
A) {o1}
B) {o2}
C) {o3}
D) {o4}
E) {o5}
F) {o6}
G) {o7}
H) {o8}
Answer:"""

ITEMS = [
    # T1: landmark -> capital city -> country
    ("The Eiffel Tower stands in the capital of which country?",
     "France", ["Spain", "Italy", "Germany", "Belgium", "Portugal", "Greece", "Austria"],
     "Italy", "Rome's Colosseum is the other iconic European monument a strong student may confuse"),
    ("The Brandenburg Gate stands in the capital of which country?",
     "Germany", ["Austria", "Poland", "Hungary", "Romania", "Serbia", "Croatia", "Belgium"],
     "Austria", "German-speaking neighbour; a strong student may conflate Berlin with Vienna"),
    ("The Colosseum stands in the capital of which country?",
     "Italy", ["Greece", "Spain", "Portugal", "France", "Turkey", "Egypt", "Morocco"],
     "Greece", "Ancient-ruins confusable: Athens vs Rome"),
    ("The Acropolis stands in the capital of which country?",
     "Greece", ["Italy", "Turkey", "Egypt", "Spain", "Portugal", "Croatia", "Cyprus"],
     "Italy", "Ancient-civilization confusable: Rome vs Athens"),
    ("Saint Basil's Cathedral stands in the capital of which country?",
     "Russia", ["Ukraine", "Poland", "Serbia", "Romania", "Hungary", "Georgia", "Croatia"],
     "Ukraine", "Slavic-neighbour confusable"),
    ("The Little Mermaid statue stands in the capital of which country?",
     "Denmark", ["Sweden", "Norway", "Finland", "Netherlands", "Belgium", "Germany", "Iceland"],
     "Sweden", "Scandinavian confusable"),

    # T2: product -> company -> HQ country
    # (item T2-1 replaced 2026-09-28 per checker flag on the PlayStation item:
    #  SIE HQ is San Mateo, USA — ambiguous. Promoted verified backup.)
    ("The company that makes the Corolla car is headquartered in which country?",
     "Japan", ["Korea", "China", "Germany", "Sweden", "Italy", "France", "Canada"],
     "Korea", "Asian carmaker confusable"),
    ("The company that made the Nokia 3310 phone is headquartered in which country?",
     "Finland", ["Sweden", "Norway", "Denmark", "Germany", "Korea", "Japan", "Iceland"],
     "Sweden", "Ericsson/Scandinavian telecom confusable"),
    ("The company that makes Lego bricks is headquartered in which country?",
     "Denmark", ["Sweden", "Norway", "Germany", "Netherlands", "Belgium", "Austria", "Poland"],
     "Sweden", "Scandinavian confusable"),
    ("The company that makes Volvo cars is headquartered in which country?",
     "Sweden", ["Denmark", "Norway", "Finland", "Germany", "Netherlands", "Austria", "Poland"],
     "Germany", "European carmaker confusable"),
    ("The company that makes the Beetle car is headquartered in which country?",
     "Germany", ["Austria", "Italy", "France", "Sweden", "Japan", "Spain", "Poland"],
     "Austria", "German-speaking car-industry confusable"),
    ("The company that makes Nutella is headquartered in which country?",
     "Italy", ["France", "Spain", "Belgium", "Germany", "Austria", "Greece", "Portugal"],
     "France", "European confectionery confusable"),

    # T3: film -> director -> birth country
    ("The film Parasite was directed by a person born in which country?",
     "Korea", ["Japan", "China", "Taiwan", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "Japan", "Asian-cinema confusable"),
    ("The film Amelie was directed by a person born in which country?",
     "France", ["Belgium", "Italy", "Spain", "Germany", "Austria", "Greece", "Portugal"],
     "Belgium", "French-language cinema confusable"),
    ("The film Life Is Beautiful was directed by a person born in which country?",
     "Italy", ["France", "Spain", "Greece", "Portugal", "Germany", "Austria", "Belgium"],
     "France", "European arthouse confusable"),
    ("The film Pan's Labyrinth was directed by a person born in which country?",
     "Mexico", ["Spain", "Argentina", "Chile", "Colombia", "Brazil", "Portugal", "Italy"],
     "Spain", "Spanish-language confusable"),
    ("The film Crouching Tiger, Hidden Dragon was directed by a person born in which country?",
     "Taiwan", ["China", "Japan", "Korea", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "China", "A strong student may answer the film's cultural origin rather than the director's birthplace"),
    ("The film City of God was directed by a person born in which country?",
     "Brazil", ["Argentina", "Chile", "Peru", "Colombia", "Venezuela", "Mexico", "Portugal"],
     "Argentina", "Latin-American cinema confusable"),

    # T4': river -> capital city -> country
    ("The Seine flows through the capital of which country?",
     "France", ["Italy", "Spain", "Germany", "Belgium", "Portugal", "Austria", "Greece"],
     "Italy", "European-river confusable"),
    ("The Tiber flows through the capital of which country?",
     "Italy", ["Greece", "Spain", "France", "Portugal", "Croatia", "Serbia", "Turkey"],
     "Greece", "Mediterranean confusable"),
    ("The Spree flows through the capital of which country?",
     "Germany", ["Austria", "Poland", "Hungary", "Romania", "Serbia", "Croatia", "Belgium"],
     "Austria", "German-speaking neighbour confusable"),
    ("The Manzanares flows through the capital of which country?",
     "Spain", ["Portugal", "Italy", "France", "Greece", "Mexico", "Argentina", "Chile"],
     "Portugal", "Iberian-neighbour confusable"),
    ("The Moskva River flows through the capital of which country?",
     "Russia", ["Ukraine", "Poland", "Serbia", "Romania", "Hungary", "Georgia", "Croatia"],
     "Ukraine", "Slavic-neighbour confusable"),
    ("The Liffey flows through the capital of which country?",
     "Ireland", ["Iceland", "Norway", "Denmark", "Sweden", "Finland", "Portugal", "Malta"],
     "Iceland", "North-Atlantic island confusable"),

    # T5'': painting -> museum -> city
    ("The museum that houses the Mona Lisa is in which city?",
     "Paris", ["London", "Rome", "Madrid", "Berlin", "Vienna", "Prague", "Amsterdam"],
     "London", "Both cities host world-famous national galleries; a strong student may confuse"),
    ("The museum that houses Guernica is in which city?",
     "Madrid", ["Barcelona", "Paris", "Rome", "Lisbon", "Berlin", "Vienna", "Amsterdam"],
     "Barcelona", "Spanish-art confusable"),
    ("The museum that houses The Night Watch is in which city?",
     "Amsterdam", ["Paris", "London", "Berlin", "Vienna", "Madrid", "Rome", "Dublin"],
     "London", "National-gallery confusable"),
    ("The museum that houses The Scream is in which city?",
     "Oslo", ["Stockholm", "Dublin", "Vienna", "Prague", "Budapest", "Warsaw", "Athens"],
     "Stockholm", "Scandinavian confusable"),
    ("The museum that houses The Birth of Venus is in which city?",
     "Florence", ["Rome", "Milan", "Venice", "Naples", "Paris", "Madrid", "Vienna"],
     "Rome", "Italian-art confusable"),
    ("The museum that houses the Arnolfini Portrait is in which city?",
     "London", ["Paris", "Rome", "Madrid", "Berlin", "Vienna", "Amsterdam", "Dublin"],
     "Paris", "National-gallery confusable"),

    # T6: novel -> author -> birth country
    ("The novel One Hundred Years of Solitude was written by an author born in which country?",
     "Colombia", ["Venezuela", "Peru", "Chile", "Argentina", "Mexico", "Brazil", "Ecuador"],
     "Mexico", "Latin-American literature confusable"),
    ("The novel The Kite Runner was written by an author born in which country?",
     "Afghanistan", ["Pakistan", "Iran", "Iraq", "Turkey", "Syria", "Yemen", "Jordan"],
     "Pakistan", "Regional-neighbour confusable"),
    ("The novel Norwegian Wood was written by an author born in which country?",
     "Japan", ["Korea", "China", "Taiwan", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "Korea", "Asian-literature confusable"),
    ("The novel The Alchemist was written by an author born in which country?",
     "Brazil", ["Argentina", "Chile", "Peru", "Colombia", "Venezuela", "Mexico", "Portugal"],
     "Portugal", "Portuguese-language confusable"),
    ("The novel Things Fall Apart was written by an author born in which country?",
     "Nigeria", ["Ghana", "Kenya", "Ethiopia", "Sudan", "Uganda", "Tanzania", "Zimbabwe"],
     "Ghana", "West-African literature confusable"),
    ("The novel The Shadow of the Wind was written by an author born in which country?",
     "Spain", ["Portugal", "Italy", "France", "Greece", "Mexico", "Argentina", "Chile"],
     "Mexico", "Spanish-language confusable"),

    # T7: company -> founder -> birth US state
    ("The founder of Microsoft was born in which US state?",
     "Washington", ["California", "Texas", "Oregon", "Florida", "Illinois", "Ohio", "Virginia"],
     "Oregon", "Pacific-Northwest confusable"),
    ("The founder of Apple was born in which US state?",
     "California", ["Texas", "Washington", "Oregon", "Nevada", "Arizona", "Florida", "Illinois"],
     "Washington", "Tech-hub confusable"),
    ("The founder of Walmart was born in which US state?",
     "Oklahoma", ["Texas", "Arkansas", "Kansas", "Missouri", "Nebraska", "Louisiana", "Mississippi"],
     "Arkansas", "Walmart is headquartered in Arkansas; a strong student may answer HQ instead of birthplace"),
    ("The founder of Ford was born in which US state?",
     "Michigan", ["Ohio", "Illinois", "Indiana", "Wisconsin", "Pennsylvania", "Kentucky", "Tennessee"],
     "Ohio", "Midwest auto-industry confusable"),
    ("The founder of Disney was born in which US state?",
     "Illinois", ["California", "Florida", "Texas", "Ohio", "Indiana", "Wisconsin", "Missouri"],
     "California", "Disneyland is in California; a strong student may answer the park's state"),
    ("The founder of KFC was born in which US state?",
     "Indiana", ["Kentucky", "Ohio", "Illinois", "Tennessee", "Missouri", "Arkansas", "Virginia"],
     "Kentucky", "KFC stands for Kentucky Fried Chicken; the most confusable distractor by design"),

    # T8: event+year -> host city -> country
    ("The 2016 Summer Olympics were held in which country?",
     "Brazil", ["Argentina", "Chile", "Peru", "Colombia", "Venezuela", "Mexico", "Portugal"],
     "Argentina", "South-American confusable"),
    ("The 2018 FIFA World Cup was held in which country?",
     "Russia", ["Qatar", "Germany", "France", "Spain", "Italy", "Brazil", "Ukraine"],
     "Qatar", "Recent World-Cup-host confusable"),
    ("The 2022 FIFA World Cup was held in which country?",
     "Qatar", ["Iran", "Malta", "Jordan", "Egypt", "Morocco", "Turkey", "Greece"],
     "Iran", "Gulf-neighbour confusable"),
    ("The 2008 Summer Olympics were held in which country?",
     "China", ["Japan", "Korea", "Taiwan", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "Japan", "East-Asian confusable"),
    ("The 2020 Summer Olympics, held in 2021, were held in which country?",
     "Japan", ["China", "Korea", "Taiwan", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "China", "East-Asian confusable"),
    ("The 2024 Summer Olympics were held in which country?",
     "France", ["Italy", "Spain", "Germany", "Belgium", "Greece", "Portugal", "Austria"],
     "Italy", "European-host confusable"),

    # T9'': treaty -> signing city -> country
    ("The Treaty of Versailles was signed in which country?",
     "France", ["Germany", "Italy", "Spain", "Belgium", "Austria", "Portugal", "Greece"],
     "Germany", "The other WWI party; a strong student may answer it"),
    ("The Treaty of Tordesillas was signed in which country?",
     "Spain", ["Portugal", "Italy", "France", "Greece", "Mexico", "Argentina", "Chile"],
     "Portugal", "The other treaty party; the most confusable distractor by design"),
    ("The Treaty of Utrecht was signed in which country?",
     "Netherlands", ["Belgium", "Germany", "France", "Austria", "Denmark", "Sweden", "Poland"],
     "Belgium", "Low-Countries confusable"),
    ("The Congress of Vienna was held in which country?",
     "Austria", ["Germany", "France", "Italy", "Spain", "Hungary", "Poland", "Romania"],
     "Germany", "German-speaking confusable"),
    ("The Treaty of Rome was signed in which country?",
     "Italy", ["France", "Spain", "Germany", "Belgium", "Greece", "Portugal", "Austria"],
     "France", "European-treaty confusable"),
    ("The Treaty of Lisbon was signed in which country?",
     "Portugal", ["Spain", "Italy", "France", "Greece", "Malta", "Cyprus", "Ireland"],
     "Spain", "Iberian-neighbour confusable"),

    # T10: painting -> museum -> country
    ("The painting Mona Lisa hangs in a museum in which country?",
     "France", ["Italy", "Spain", "Germany", "Belgium", "Austria", "Greece", "Portugal"],
     "Italy", "Da Vinci was Italian; a strong student may answer the painter's country"),
    ("The painting Guernica hangs in a museum in which country?",
     "Spain", ["France", "Italy", "Portugal", "Germany", "Belgium", "Austria", "Greece"],
     "France", "Picasso lived in France; a strong student may answer the painter's adopted country"),
    ("The painting The Last Supper hangs in a museum in which country?",
     "Italy", ["France", "Spain", "Portugal", "Germany", "Austria", "Greece", "Belgium"],
     "Spain", "European old-master confusable"),
    ("The painting The Night Watch hangs in a museum in which country?",
     "Netherlands", ["Belgium", "Germany", "France", "Austria", "Denmark", "Sweden", "Poland"],
     "Belgium", "Low-Countries confusable"),
    ("The painting The Scream hangs in a museum in which country?",
     "Norway", ["Sweden", "Denmark", "Finland", "Germany", "Netherlands", "Belgium", "Austria"],
     "Sweden", "Scandinavian confusable"),
    ("The painting The Kiss hangs in a museum in which country?",
     "Austria", ["Germany", "France", "Italy", "Spain", "Belgium", "Netherlands", "Poland"],
     "Germany", "German-speaking confusable"),
]

BACKUP_ITEMS = [
    ("The Latin word Hydrargyrum gives the chemical symbol of which element?",
     "Mercury", ["Silver", "Gold", "Lead", "Tin", "Iron", "Carbon", "Silicon"],
     "Silver", "Liquid/shiny-metal confusable"),
    ("The company that makes the Corolla car is headquartered in which country?",
     "Japan", ["Korea", "China", "Germany", "Sweden", "Italy", "France", "Canada"],
     "Korea", "Asian carmaker confusable"),
    ("The novel 1984 was written by an author born in which country?",
     "India", ["England", "France", "Germany", "Russia", "Ireland", "Pakistan", "Bangladesh"],
     "England", "Orwell is associated with England; a strong student may answer it"),
    ("The film Spirited Away was directed by a person born in which country?",
     "Japan", ["Korea", "China", "Taiwan", "Thailand", "Vietnam", "Philippines", "Indonesia"],
     "China", "Asian-animation confusable"),
    # Sunflowers backup REMOVED 2026-09-28 per checker flag (non-unique: Amsterdam and London both hold canonical canvases).
    ("The Tower of London stands in the capital of which country?",
     "England", ["Scotland", "Wales", "Ireland", "France", "Germany", "Netherlands", "Belgium"],
     "Scotland", "UK-nation confusable"),
]

assert len(ITEMS) == 60
for _q, _c, _d, _f, _r in ITEMS + BACKUP_ITEMS:
    assert len(_d) == 7 and _f in _d and _c not in _d
    assert len(set([_c] + _d)) == 8
