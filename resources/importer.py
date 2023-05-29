import json
import redis
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

redis = redis.Redis(host='localhost', port=6379, db=0)

with open('./pokedex.json') as file:
    data = json.load(file)
# {
#     "id": 1,
#     "name": {
#         "english": "Bulbasaur",
#         "japanese": "フシギダネ",
#         "chinese": "妙蛙种子",
#         "french": "Bulbizarre"
#     },
#     "type": [
#         "Grass",
#         "Poison"
#     ],
#     "base": {
#         "HP": 45,
#         "Attack": 49,
#         "Defense": 49,
#         "Sp. Attack": 65,
#         "Sp. Defense": 65,
#         "Speed": 45
#     }
# }

# create a redis index for each field
schema = (NumericField('$.id', as_name='id'),
          TextField('$.name.english', as_name='english'),
          TextField('$.name.japanese', as_name='japanese'),
          TextField('$.name.chinese', as_name='chinese'),
          TextField('$.name.french', as_name='french'),
          TextField('$.type', as_name='type'),
          NumericField('$.base.HP', as_name='hp'),
          NumericField('$.base.Attack', as_name='att'),
          NumericField('$.base.Defense', as_name='def'),
          NumericField('$.base.Sp. Attack', as_name='spatt'),
          NumericField('$.base.Sp. Defense', as_name='spdef'),
          NumericField('$.base.Speed', as_name='spd'))

redis.ft("pokemon").create_index(schema, definition=IndexDefinition(
    prefix=['pokemon:'], index_type=IndexType.JSON))

for pokemon in data:
    redis.json().set(f'pokemon:{pokemon["id"]}', Path.root_path(), pokemon)
