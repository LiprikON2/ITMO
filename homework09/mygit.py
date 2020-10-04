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
    
    blob = header + content
    hash_sum = hashlib.sha1(blob.encode()).hexdigest()
    print(hash_sum)
    
    if '-w' in sys.argv:
        foldername = hash_sum[:2]
        filename = hash_sum[2:]
        folder_path = f'.git/objects/{foldername}'
        
        os.makedirs(folder_path, exist_ok=True)
            
        with open(os.path.join(folder_path, filename), 'wb') as blob_file:
            compressed_blob = zlib.compress(blob.encode())
            blob_file.write(compressed_blob)

def cat_file(hash_sum):
    
    
        foldername = hash_sum[:2]
        filename = hash_sum[2:]
        folder_path = f'.git/objects/{foldername}'
        
        try:
            with open(os.path.join(folder_path, filename), 'rb') as blob_file:
                blob = zlib.decompress(blob_file.read())
                header_len = blob.find(b'\x00') + 1
                
                # blob 25\x00789c4bcac94f...
                # ^^^^^^^^^^^
                header = blob[:header_len]
                # blob 25\x00789c4bcac94f...
                #      ^^
                content_len = int(header[blob.find(b' '):blob.find(b'\x00')].decode('ascii'))
                # blob 25\x00789c4bcac94f...
                #            ^^^^^^^^^^^^^^^
                content = blob[header_len:header_len + content_len].decode('ascii')
                # blob 25\x00789c4bcac94f...
                # ^^^^
                blob_type = header[:blob.find(b' ')].decode('ascii')
                
                if '-p' in sys.argv:
                    print(content)
                if '-t' in sys.argv:
                    print(blob_type)
                if '-s' in sys.argv:
                    print(content_len)
                    
        except FileNotFoundError:
            print(f'Not a valid object name {hash_sum}')
            
    
        
    
def check_if_init():
    if not os.path.exists('.git'):
        print('git is not initialized in this directory')
        sys.exit(0)
    
def main():
    command = sys.argv[1]
    if command == 'init':
        try:
            os.makedirs('.git/objects', exist_ok=True)
            os.makedirs('.git/refs/heads', exist_ok=True)
            os.makedirs('.git/refs/tags', exist_ok=True)
            with open('.git/HEAD', 'w+') as f:
                f.write('ref: refs/heads')
            print('Initialized git directory')
        except FileExistsError:
            pass
        
    elif command == 'cat-file':
        check_if_init()
        hash_sum = sys.argv[2]
        cat_file(hash_sum)
    elif command == 'hash-object':
        check_if_init()
        file_path = sys.argv[2]
        with open(file_path, 'r') as f:
            hash_object(f)
        
        
    elif command == 'is-tree':
        pass
    elif command == 'write-tree':
        pass
    else:
        raise RuntimeError(f'Unknown command {command}')


if __name__ == '__main__':
    main()
    