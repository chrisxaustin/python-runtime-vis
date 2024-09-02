
## Importing the library as either main or a specific release
```requirements
runtime_vis @ git+https://github.com/chrisxaustin/python-runtime-vis.git@main
runtime_vis @ git+https://github.com/chrisxaustin/python-runtime-vis.git@v1.0
```

## Updating requirements with pip
```shell
pip install --upgrade -r requirements.txt
```

## Examples

The following example will call `some_method` with the argument `1000`,  then `2000`, etc.
```python
vis = Vis()
vis.visualize(
    some_method,
    [1000,2000,4000,8000]
)
```

This will only use `n log n` and `n^2`
```python
vis = Vis(fit=['nlogn','n2'])
vis.visualize(
    some_method,
    [1000,2000,4000,8000]
)
```

## Supported curve names

| Name  | Big O     |
|-------|-----------|
| n     | O(n)      |
| logn  | O(log n)  |
| nlogn | O(n log n)|
| n2    | O(n^2)    |
| n3    | O(n^3)    |

