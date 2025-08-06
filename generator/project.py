import random
import string
from model.project import ProjectData

def random_string(prefix, maxlen):
    symbols = string.ascii_letters+ string.digits + string.punctuation+ " "*10
    return prefix +"".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata=[
    ProjectData(name=name,description=description)
    for name in[random_string("name", 15)]
    for description in[random_string("description", 15)]]