# -*- coding: utf-8 -*-

import graphene
import graphql_jwt

import backend.graphql_schema.asic_schema
import backend.graphql_schema.error_schema
import backend.graphql_schema.utils_schema
import backend.graphql_schema.auth_schema
import backend.graphql_schema.balance_schema
import backend.graphql_schema.error_rule_schema


class Query(backend.graphql_schema.error_schema.ErrorQuery,
            backend.graphql_schema.utils_schema.UtilsQuery,
            backend.graphql_schema.asic_schema.AsicQuery,
            backend.graphql_schema.balance_schema.BalanceQuery,
            backend.graphql_schema.error_rule_schema.ErrorRuleQuery,
            graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(
    backend.graphql_schema.auth_schema.AuthMutations,
    backend.graphql_schema.asic_schema.AsicMutations,
    backend.graphql_schema.error_schema.ErrorMutations,
    backend.graphql_schema.balance_schema.BalanceMutations,
    backend.graphql_schema.error_rule_schema.ErrorRuleMutations,
    graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    pass

main_schema = graphene.Schema(query=Query, mutation=Mutations)