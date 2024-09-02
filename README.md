
The following example will call `some_method` with the argument `1000`,  then `2000`, etc.
```
    vis = Vis()
    vis.visualize(
        some_method,
        [1000,2000,4000,8000]
    )
```