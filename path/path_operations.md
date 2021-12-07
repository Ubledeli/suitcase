

#### make directory:
makes entire tree, even if folders exist
```
os.makedirs(path, exist_ok=True)
```

#### list content of a directory:
returns a list of files and folders.
```
os.listdir(path)

sorted(os.listdir(path))
```

#### path stem:
extract name and extension from a path
```
from pathlib import Path

stem = Path(path_string).stem
```

#### copy file:

```
import shutil

shutil.copyfile(from_path, to_path)
```
