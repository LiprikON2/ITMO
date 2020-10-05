import hashlib
import sys
import os
import pathlib
import zlib
import io
import textwrap
import re

def object_read():
    pass

def is_tree():
    pass

def tree_parse_one():
    pass

def write_tree():
    pass

def object_sha():
    pass

def hash_object(file, print=True):
    content = file.read()
    # `\0` or `\x00` is a null character, used to separate header and content
    header = f'blob {len(content)}\0'
    
    blob = header + content
    sha = hashlib.sha1(blob.encode()).hexdigest()
    if print:
        print(sha)
    
    if '-w' in sys.argv:
        foldername = sha[:2]
        filename = sha[2:]
        folder_path = f'.git/objects/{foldername}'
        
        os.makedirs(folder_path, exist_ok=True)
            
        with open(os.path.join(folder_path, filename), 'wb') as blob_file:
            compressed_blob = zlib.compress(blob.encode())
            blob_file.write(compressed_blob)
    else:
        return sha

def cat_file(sha):
    foldername = sha[:2]
    filename = sha[2:]
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
        print(f'Not a valid object name {sha}')
            
def update_index(file):
    content = file.read()
    file.seek(0)
    
    stat = os.stat(file.name)
    sha = hash_object(file, print=False)
    
    entry = textwrap.dedent(f'''\
        <ctime {stat.st_ctime}>
        <ctime {0}>
        <mtime {stat.st_ctime}>
        <mtime {0}>
        <dev {stat.st_dev}>
        <ino {stat.st_ino}>
        <mode {stat.st_mode}>
        <uid {stat.st_uid}>
        <gid {stat.st_gid}>
        <size {stat.st_size}>
        <SHA {sha}>
        <flags {'gg'}>
        <name {file.name}>\n''')
    
    version = '1.12' # TODO
    entry_count = '1'
    
    if not os.path.exists('.git/index'):
        with open('.git/index', 'wb') as index_file:
            header = f'DIRC {version} {entry_count}\n'
            index = header + entry
            
            compressed_index = zlib.compress(index.encode())
            index_file.write(compressed_index)
            
    else:
        with open('.git/index', 'rb+') as index_file:
            compressed_old_index = index_file.read()
            old_index = zlib.decompress(compressed_old_index).decode('ascii')
            
            if not is_already_in_index(old_index, sha, file.name):
                
                entry_count_end = old_index.find('\n')
                entry_count_start = old_index.rfind(' ', 0, entry_count_end) + 1
                
                # DIRC 1.12 1\n
                #            ^
                entry_count = str(int(old_index[entry_count_start:entry_count_end]) + 1)
                
                # Update entry count number
                new_index = old_index[:entry_count_start] + entry_count + old_index[entry_count_end:]
                
                # DIRC 1.12 1\n
                #              ^
                insert_pos = new_index.find('\n') + 1
                
                # Add entry
                new_index = new_index[:insert_pos] + entry + new_index[insert_pos:] 
                
                compressed_new_index = zlib.compress(new_index.encode())
                index_file.seek(0)
                index_file.write(compressed_new_index)
                index_file.truncate()
                
            else:
                print('No changes detected')


def list_entries(index):
    entries_beginings = re.finditer(f'<ctime', index)
    last_entry_end = index.rfind('>') + 2
    
    entry_positions = []
    for i, entry_start in enumerate(entries_beginings):
        # Position of the first <ctime> in the entry is entry start point
        if i % 2 == 0:
            entry_positions.append(entry_start.start())
    
    entry_positions.append(last_entry_end)
    
    entries = []
    for i in range(len(entry_positions) - 1):
        entry = index[entry_positions[i]:entry_positions[i + 1]]
        entries.append(entry)
    
    return entries


def is_already_in_index(index, new_sha, new_name):
    
    entries = list_entries(index)
    
    for entry in entries:
        sha_start = entry.find('<SHA ') + 5
        sha_end = entry.find('>', sha_start)
        sha = entry[sha_start:sha_end]
        
        name_start = entry.find('<name ') + 6
        name_end = entry.find('>', name_start)
        name = entry[name_start:name_end]
        
        if sha == new_sha and name == new_name:
            return True
    return False
    

def ls_files():
    pass
            
    
def is_init():
    if not os.path.exists('.git'):
        print('git is not initialized in this directory')
        return False
    return True

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
        if is_init():
            sha = sys.argv[2]
            cat_file(sha)
            
    elif command == 'hash-object':
        if is_init():
            file_path = sys.argv[2]
            with open(file_path, 'r') as f:
                hash_object(f)
    
    elif command == 'update-index':
        if is_init():
            file_path = sys.argv[2]
            with open(file_path, 'r') as f:
                update_index(f)
                
    elif command == 'ls-files':
        if is_init():
            pass
    
    elif command == 'is-tree':
        pass
    elif command == 'write-tree':
        pass
    else:
        raise RuntimeError(f'Unknown command {command}')


if __name__ == '__main__':
    main()
