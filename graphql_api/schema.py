"""Graphql schema for graphql_api project."""
import graphene

import posts.schema
import users.schema


class Query(
    users.schema.Query,
    posts.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    users.schema.Mutation,
    posts.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
