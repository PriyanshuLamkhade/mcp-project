from typing import Literal
from uuid import uuid4

from fastmcp import FastMCP
from mcp_server.database import (
    get_all_task,
    save_task,
    update_task_status_in_db
)

mcp = FastMCP("MCP SERVER ACL")

@mcp.tool(name="create_task",description="this tool is created to creates new taks")
def create_task(title:str, priority:str='medium', description:str="")->dict:
    """
    this function creates new tasks in our database
    """
    task_id = str(uuid4())
    status = "todo"

    task = {"task_id":task_id, "title":title, "description":description,
            "status":status,"priority":priority}

    save_task(task)

    return task


@mcp.tool(name="list_task",description="this tool is created to list all tasks")
def list_task()->list[dict]:
    """
    this function lists all tasks in our database
    """
    return get_all_task()
     
@mcp.tool(name="update_task_status",description="this tool is created to update a task's status based on its ID")
def update_task_status(task_id="task_id",status=Literal["todo","in progress","done"])->dict:
    """
    this function will update a specific task's status based on its ID
    """
    
    return update_task_status_in_db(task_id,status)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
    create_task(title="Second task",description="second test")