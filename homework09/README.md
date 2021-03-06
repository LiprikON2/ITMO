# My implementation of git

## Usage

### Init

```bash
python mygit.py init
```

### Hashing object

#### Print hash
```bash
python mygit.py hash-object <file>
```

#### Save file
```bash
python mygit.py hash-object <file> -w
```

### Cat'ing file

#### File content
```bash
python mygit.py cat-file <hash_sum> -p
```
#### File type
```bash
python mygit.py cat-file <hash_sum> -t
```
#### File size
```bash
python mygit.py cat-file <hash_sum> -s
```

### Updating index

#### Update file in the index
> Ignores new files
```bash
python mygit.py update-index <file>
```

#### Add file to the index
> Doesn't ignore new files
```bash
python mygit.py update-index <file> --add
```

#### Remove file to the index
> Doesn't ignore new files
```bash
python mygit.py update-index <file> --remove
```

### ls'ing what's in the index

```bash
python mygit.py ls-files
```

### Writing a tree
> Writes tree with files that are currently in index
```bash
python mygit.py write-tree
```

### ls'ing what's in the tree

```bash
python mygit.py ls-tree <tree_hash_sum>
```
or
```bash
python mygit.py cat-file <tree_hash_sum> -p
```

#### Showing subfolders recursively

```bash
python mygit.py ls-tree <tree_hash_sum> -r
```

### Commiting a tree

```bash
python mygit.py commit-tree <tree_hash_sum> -m 'init commit'
```

#### Specifying commit parent
```bash
python mygit.py commit-tree <tree_hash_sum> -m 'init' -p <another_tree_hash_sum>
```

### Commit logs
> Recursively shows commits and its commit parents
```bash
python mygit.py ls-tree <commit_hash_sum>
```