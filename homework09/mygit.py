import hashlib
import sys
import os
import pathlib
import zlib
import io

def object_read():
    pass

def is_tree():
    pass

def tree_parse_one():
    pass

def write_tree():
    pass

def object_sho():
    pass

def hash_object(file):
    content = file.read()
    # `\0` is a null character, used to separate header and content
    header = f'blob {len(content)}\0'
    print(header)
    
    store = header + content
    hash_sum = hashlib.sha1(store.encode()).hexdigest()
    print(hash_sum)
    
    foldername = hash_sum[:2]
    filename = hash_sum[2:]
    folder_path = f'.git/objects/{foldername}'
    
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass
        
    with open(os.path.join(folder_path, filename), 'wb') as blob_file:
        compressed_blob = zlib.compress(store.encode())
        blob_file.write(compressed_blob)
    
def check_if_init():
    if not os.path.exists('.git'):
        print('git is not initialized in this directory')
        sys.exit(0)
    
def main():
    command = sys.argv[1]
    if command == 'init':
        try:
            os.makedirs('.git/objects')
            os.makedirs('.git/refs')
            # with open('.git/HEAD', 'r') as f:
            #     f.write('ref: refs/heads')
            print('Initialized git directory')
        except FileExistsError:
            pass
        
    elif command == 'cat-file':
        pass
    elif command == 'hash-object':
        check_if_init()
        file_path = sys.argv[2]
        with open(file_path, 'r+') as f:
            hash_object(f)
            
        
    elif command == 'is-tree':
        pass
    elif command == 'write-tree':
        pass
    else:
        raise RuntimeError(f'Unknown command {command}')


if __name__ == '__main__':
    main()
    