from mongoengine import *
import bson


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))

        
class Authors(Document):
    full_name = StringField()


class Editions(Document):
    name = StringField()


class Books(Document):
    title = StringField()
    year = IntField()
    edition = ReferenceField(Editions, reverse_delete_rule=DENY)
    authors = ListField(ReferenceField(Authors, reverse_delete_rule=DENY))

    meta = {'queryset_class': CustomQuerySet}

    #override
    def to_json(self):
        data = self.to_mongo()
        for i in range(len(data['authors'])):
            data['authors'][i]= self.authors[i].to_mongo()
        data['edition']= self.edition.to_mongo()
        return bson.json_util.dumps(data)

