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

### Catting file

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
```bash
python mygit.py update-index <file>
```

#### Add file to the index
```bash
python mygit.py update-index <file> --add
```
