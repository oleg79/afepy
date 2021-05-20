from typing import Optional

from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse, HTMLResponse

from ariadne import QueryType, MutationType, ObjectType, graphql, convert_kwargs_to_snake_case, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

from app.models import assignment

type_defs = """
    type Query {
        assignemnts: [Assignment]!
    }

    type Mutation {
        createAssignment(input: AssignmentInput!): Assignment
    }

    type Assignment {
        id: ID!
        title: String!
        createdAt: String!
        startsAt: String!
        endsAt: String!
    }

    input AssignmentInput {
        title: String!
        createdAt: String!
        startsAt: String!
        endsAt: String!
    }
"""

query = QueryType()
mutation = MutationType()

assignmentType = ObjectType('Assignment')

@query.field('assignemnts')
async def resolve_hello(_, _info):
    return await assignment.all()
    
assignmentType.set_alias('id', '_id')
assignmentType.set_alias('createdAt', 'created_at')
assignmentType.set_alias('startsAt', 'starts_at')
assignmentType.set_alias('endsAt', 'ends_at')

@mutation.field("createAssignment")
@convert_kwargs_to_snake_case
async def resolve_create_assignment(_, _info, input):
    return await assignment.create(input)

schema = make_executable_schema(type_defs, [query, mutation], assignmentType)

app = FastAPI()

@app.get("/graphql")
def graphql_playground():
    return HTMLResponse(content=PLAYGROUND_HTML, status_code=200)


@app.post("/graphql")
async def graphql_server(request: Request, query = Body(default=''), variables = Body(default={}), operation_name = Body(default=None)):
    success, result = await graphql(
        schema,
        {
            "query": query,
            "variables": variables,
            "operation_name": operation_name,
        },
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400

    return JSONResponse(content=result, status_code=status_code)
