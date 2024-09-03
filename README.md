
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

This prints the results as they are observed:
```python
vis.visualize(
    batch,
    [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000],
    performance_callback=lambda size, time, complexity, confidence: print(f"{size}\t{time:0.2f}\t{complexity}\t{confidence:0.2f}%"),
    keep_open=False
)
```

Sample output:
```
1000	0.04	None	0.00%
2000	0.17	n2	100.00%
4000	0.66	n2	99.99%
8000	2.61	n2	99.96%
16000	10.43	n2	99.99%
```

## Curve names
| Name  | Big O     |
|-------|-----------|
| n     | O(n)      |
| logn  | O(log n)  |
| nlogn | O(n log n)|
| n2    | O(n^2)    |
| n3    | O(n^3)    |
| 2n    | O(s^n)    |

