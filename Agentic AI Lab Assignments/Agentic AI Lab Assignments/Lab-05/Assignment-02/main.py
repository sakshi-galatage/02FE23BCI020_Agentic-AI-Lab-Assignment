
import sqlite3
import posixpath

# Set up database
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")
conn.executemany("INSERT INTO signups VALUES (?, ?)", [
    ("AI Club Talk", 12),
    ("Hackathon Kickoff", 9),
    ("Robotics Demo", 15),
])
conn.commit()

# Files available in safe directory
MOCK_FILES = {
    "/safe/README.md": "Agentic AI Systems - Mini MCP Server Demo.",
    "/safe/notes.txt": "This is a safe file."
}

MOCK_API = {
    "events_today": ["AI Club Talk", "Robotics Demo"]
}

CAPABILITIES = [
    {"name": "read_file", "kind": "resource",
     "input": {"path": "str"}, "output": {"content": "str"}},
    {"name": "query_db", "kind": "tool",
     "input": {"sql": "str"}, "output": {"rows": "list"}},
    {"name": "call_api", "kind": "tool",
     "input": {"endpoint": "str"}, "output": {"data": "any"}},
]

ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):

        # Normalize path to prevent directory traversal
        normalized_path = posixpath.normpath(path)

        # Check safe directory permission
        if not normalized_path.startswith("/safe/"):
            return {"error": "Access denied: path outside safe directory"}

        if normalized_path not in MOCK_FILES:
            return {"error": "File not found"}

        return {"content": MOCK_FILES[normalized_path]}

    def query_db(self, sql, caller):

        if caller not in ALLOWED_CALLERS:
            return {"error": "Caller not permitted"}

        if not sql.strip().upper().startswith("SELECT"):
            return {"error": "Only SELECT statements are permitted"}

        cur = conn.execute(sql)
        return {"rows": cur.fetchall()}

    def call_api(self, endpoint):

        if endpoint not in MOCK_API:
            return {"error": "Unknown endpoint"}

        return {"data": MOCK_API[endpoint]}


class MCPClient:

    def __init__(self, server, caller_name):
        self.server = server
        self.caller_name = caller_name

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):

        manifest = {c["name"]: c for c in self.discover()}

        if capability_name not in manifest:
            raise ValueError("Unknown capability")

        method = getattr(self.server, capability_name)

        if capability_name == "query_db":
            return method(caller=self.caller_name, **kwargs)

        return method(**kwargs)


if __name__ == "__main__":

    server = MCPServer()
    client = MCPClient(server, caller_name="planning_agent")

    print("=== Capability Discovery ===")
    for c in client.discover():
        print(c["name"], c["kind"])

    print("\n=== Test 1: Safe File Access ===")
    print(client.call("read_file", path="/safe/README.md"))

    print("\n=== Test 2: Unauthorized File Access ===")
    print(client.call("read_file", path="/secret.txt"))

    print("\n=== Test 3: Directory Traversal Attack ===")
    print(client.call("read_file", path="/safe/../../secret.txt"))
