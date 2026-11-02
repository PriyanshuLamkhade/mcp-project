import asyncio

from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")
async def get_tools_from_server():
    async with client:
        tools = await client.list_tools()

        for tool in tools:
            print(tool.name)

    return tools
async def create_task_using_mcp():
    async with client:
        result = await client.call_tool(
            "create_task",
            {
                "title":"task3",
                "priority":"high",
                "description":"This is the test from client"
            }
        )

        print(result.data)
    return result.data

async def list_task_using_mcp():
    async with client:
        result = await client.call_tool(
            "list_task"
        )
        print(result.data)
    return result.data

async def update_task_status_using_mcp():
    async with client:
        async with client:
            result = await client.call_tool(
                "update_task_status",
                {
                    "task_id":"1",
                    "status":"done"
                }
            )
            print(result.data)
            return result.data

if __name__ == "__main__":
    asyncio.run(list_task_using_mcp())
