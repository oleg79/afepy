from typing import Optional

from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse, HTMLResponse

from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

type_defs = """
    type Query {
        hello: String!
    }
"""

query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, query)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/graphql")
def graphql_playground():
    return HTMLResponse(content=PLAYGROUND_HTML, status_code=200)


@app.post("/graphql")
def graphql_server(request: Request, query = Body(default=''), variables = Body(default={}), operation_name = Body(default=None)):
    success, result = graphql_sync(
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
