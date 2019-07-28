import graphene

import updates.schema


class Query(updates.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
