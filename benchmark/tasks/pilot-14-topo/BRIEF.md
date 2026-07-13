# Task: Dependency topological sort

## API (`topo.core`)

```python
def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    # graph[node] = list of dependencies that must come BEFORE node
    # return stable order: among ready nodes, alphabetical
    # cycle → ValueError
```

## Done when pytest green.
