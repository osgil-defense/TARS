from typing import Optional, Type
from pydantic.v1 import BaseModel, Field
from subprocess import Popen, PIPE
from crewai_tools import BaseTool

class ExecuteCommandToolSchema(BaseModel):
    """Input schema for ExecuteCommandTool."""
    command: str = Field(..., description="The Unix command to execute")

class ExecuteCommandTool(BaseTool):
    name: str = "Execute Unix Command"
    description: str = "A tool that executes a given Unix command and saves the output."
    args_schema: Type[BaseModel] = ExecuteCommandToolSchema
    command: Optional[str] = None

    def __init__(self, command: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if command is not None:
            self.command = command

    def _run(self, **kwargs) -> str:
        command = kwargs.get('command', self.command)
        if command is None:
            raise ValueError("Command is required")
        
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return f"Error executing command: {stderr.decode('utf-8')}"
        
        return stdout.decode('utf-8')