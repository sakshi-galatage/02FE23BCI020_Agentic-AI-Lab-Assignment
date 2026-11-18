
import sqlite3

# Set up SQLite database
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")
conn.executemany(
    "INSERT INTO signups VALUES (?, ?)",
    [
        ("AI Club Talk", 12),
        ("Hackathon Kickoff", 9),
        ("Robotics Demo", 15)
    ]
)
conn.commit()

MOCK_FILES = {
    "README.md": "Agentic AI Systems - mini MCP server demo.",
    "notes.txt": "Project meeting notes.",
    "report.pdf": "Sample project report."
}

MOCK_API = {
    "events_today": ["AI Club Talk", "Robotics Demo"]
}

# Capability manifest
CAPABILITIES = [
    {
        "name": "read_file",
        "kind": "resource",
        "input": {"path": "str"},
        "output": {"content": "str"}
    },
    {
        "name": "query_db",
        "kind": "tool",
        "input": {"sql": "str"},
        "output": {"rows": "list"},
        "caller_required": True
    },
    {
        "name": "call_api",
        "kind": "tool",
        "input": {"endpoint": "str"},
        "output": {"data": "any"}
    },
    {
        "name": "list_files",
        "kind": "resource",
        "input": {},
        "output": {"files": "list"}
    }
]

ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": f"file not found: {path}"}

        return {"content": MOCK_FILES[path]}

    def query_db(self, sql, caller):
        if caller not in ALLOWED_CALLERS:
            return {
                "error": f"caller '{caller}' is not permitted to use query_db"
            }

        if not sql.strip().upper().startswith("SELECT"):
            return {
                "error": "only SELECT statements are permitted through this tool"
            }

        cursor = conn.execute(sql)
        return {"rows": cursor.fetchall()}

    def call_api(self, endpoint):
        if endpoint not in MOCK_API:
            return {"error": f"unknown endpoint: {endpoint}"}

        return {"data": MOCK_API[endpoint]}

    # Fourth capability
    def list_files(self):
        return {"files": list(MOCK_FILES.keys())}


class MCPClient:

    def __init__(self, server, caller_name):
        self.server = server
        self.caller_name = caller_name

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):
        manifest = {
            capability["name"]: capability
            for capability in self.discover()
        }

        if capability_name not in manifest:
            raise ValueError(
                f"Unknown capability: {capability_name}"
            )

        capability = manifest[capability_name]
        method = getattr(self.server, capability_name)

        # Generic permission handling from manifest
        if capability.get("caller_required"):
            kwargs["caller"] = self.caller_name

        return method(**kwargs)


if __name__ == "__main__":

    server = MCPServer()
    client = MCPClient(server, "planning_agent")

    print("=== CAPABILITY DISCOVERY ===")

    for capability in client.discover():
        print(
            f"{capability['name']} "
            f"({capability['kind']}) "
            f"input={capability['input']} "
            f"output={capability['output']}"
        )

    print("\n=== CALL 1: READ FILE ===")
    print(client.call("read_file", path="README.md"))

    print("\n=== CALL 2: QUERY DATABASE ===")
    print(
        client.call(
            "query_db",
            sql="SELECT event, count FROM signups"
        )
    )

    print("\n=== CALL 3: CALL API ===")
    print(client.call("call_api", endpoint="events_today"))

    print("\n=== CALL 4: NEW LIST FILES CAPABILITY ===")
    print(client.call("list_files"))

    print("\n=== REJECTION: INVALID SQL ===")
    print(
        client.call(
            "query_db",
            sql="DELETE FROM signups"
        )
    )

    print("\n=== REJECTION: UNAUTHORIZED CALLER ===")
    other_client = MCPClient(server, "unregistered_agent")

    print(
        other_client.call(
            "query_db",
            sql="SELECT * FROM signups"
        )
    )
