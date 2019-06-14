from flaskblog import db
from flaskblog.models import Scents, PerfumeInfo
from collections import Counter


def is_valid(key):
    if len(key) <= 4:
        k_gender = key[0]
        k_group = int(key[1:-1])
        k_type = int(key[-1:])
        #all_groups = Scents.query.all()
        #max_group = all_groups[-1:][0].id
        #all_types = PerfumeInfo.query.all()
        #list_of_types = []
        #for each_type in all_types:
        #    list_of_types.append(each_type.get_type())
        #tmp = dict(Counter(list_of_types))

        if k_gender in ['M', 'F', 'U']:
            if k_group in range(1,11):
                if k_type in range(1,7):
                    return True
                else:
                    return False
    return False
