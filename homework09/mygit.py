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

def hash_object(file, printing=True):
    content = file.read()
    # `\0` or `\x00` is a null character, used to separate header and content
    header = f'blob {len(content)}\0'
    
    blob = header + content
    sha = get_sha1_hash_sum(blob)
    if printing:
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

def get_sha1_hash_sum(text):
    return hashlib.sha1(text.encode()).hexdigest()

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
        
def get_entry_from_file(file):
    content = file.read()
    file.seek(0)
    
    stat = os.stat(file.name)
    sha = hash_object(file, printing=False)
    
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
        <flags >
        <name {file.name}>\n''')
    
    return entry
    
def update_index(entry, file_name, version='1.12'):
    
    if entry:
        sha = get_entry_tag_value(entry, 'SHA')
    else:
        sha = None
    
    if not os.path.exists('.git/index'):
        with open('.git/index', 'w') as index_file:
            entry_count = '1'
            
            header = f'DIRC {version} {entry_count}\n'
            content = header + entry
            index_content_sha = get_sha1_hash_sum(content)
            footer = f'<sha {index_content_sha}>'
            
            index = content + footer
            save_index_file(index_file, index)
            print(f'Added {file_name}')
            
    else:
        with open('.git/index', 'r+') as index_file:
            index = index_file.read()
            
            if not is_in_index(index, file_name) and '--add' in sys.argv:
                new_index = add_index_entry(index, entry)
                new_index = update_index_footer(new_index)
                
                save_index_file(index_file, new_index)
                
                print(f'Added {file_name}')
                
            elif '--remove' in sys.argv:
                new_index = remove_index_entry(index, file_name) 
                new_index = update_index_footer(new_index)
                
                save_index_file(index_file, new_index)
            
            elif has_changed(index, sha, file_name):
                new_index = update_index_entry(index, entry)
                new_index = update_index_footer(new_index)
                
                save_index_file(index_file, new_index)
                
                print(f'Updated {file_name}')
                
            else:
                print('No changes detected')

def save_index_file(file, index):
    file.seek(0)
    file.write(index)
    file.truncate()
        
def add_index_entry(index, entry):
    """ Return new index with added entry to mygit index """
    new_index = increment_index_entry_count(index)
    
    # DIRC 1.12 1\n
    #              ^
    entry_start = new_index.find('\n') + 1
    new_index = new_index[:entry_start] + entry + new_index[entry_start:]
    
    return new_index

def remove_index_entry(index, name, printing=True):
    """ 
    Returns new mygit index with removed mygit index entry
    """
    
    if not is_in_index(index, name):
        return index
    
    entries = list_entries(index)
    for entry in entries:
        name_2 = get_entry_tag_value(entry, 'name')
        if name == name_2:
            new_index = increment_index_entry_count(index, decrement=True)
            entry_start = index.find(entry)
            entry_end = entry_start + len(entry)
            new_index = new_index[:entry_start] + new_index[entry_end:]
            
    if printing:
        print(f'Removed {name}')
        
    return new_index

def update_index_entry(index, new_entry):
    """ Return new index with updated mygit index entry """
    
    entries = list_entries(index)
    
    name_1 = get_entry_tag_value(new_entry, 'name')
    
    for entry in entries:
        name_2 = get_entry_tag_value(entry, 'name')
        if name_1 == name_2:
            new_index = remove_index_entry(index, name_1, printing=False)
            new_index = add_index_entry(new_index, new_entry)
    
    return new_index
    

def increment_index_entry_count(index, decrement=False):
    """ Returns new index with incremented entry count number in mygit index header """
    entry_count_end = index.find('\n')
    entry_count_start = index.rfind(' ', 0, entry_count_end) + 1
    
    # DIRC 1.12 1\n
    #            ^
    entry_count = index[entry_count_start:entry_count_end]
    
    if not decrement:
        entry_count = str(int(entry_count) + 1)
    else:
        entry_count = str(int(entry_count) - 1)
    
    return index[:entry_count_start] + entry_count + index[entry_count_end:]
    
    
def update_index_footer(index, sha=''):
    """ 
    Return new index with updated mygit index footer - SHA-1 
    over the content of the index file before this checksum 
    """
    footer_start = index.find('<sha')
    
    if not sha:
        sha = get_sha1_hash_sum(index[:footer_start])
        
    return index[:footer_start] + f'<sha {sha}>'


def list_entries(index):
    """ Returns list of plain text entries from mygit index """
    entry_start_list = re.finditer(f'<ctime', index)
    last_entry_end = index.rfind('>') + 2
    
    entry_positions = []
    for i, entry_start in enumerate(entry_start_list):
        # Position of the first <ctime> in the entry is the entry starting point
        if i % 2 == 0:
            entry_positions.append(entry_start.start())
    
    entry_positions.append(last_entry_end)
    
    entries = []
    for i in range(len(entry_positions) - 1):
        entry = index[entry_positions[i]:entry_positions[i + 1]]
        entries.append(entry)
    
    return entries

def get_entry_tag_value(entry, tag, second_one=False):
    """ 
    Returns value of entry tag inside mygit index 
    
    Possible tags: 'ctime', 'mtime', 'dev', 'ino',
    'mode', 'uid', 'gid', 'size', 'SHA', 'flags', 'name.
    
    second_one=True/Flase - determines whether return value of second tag occurence or the first
    
    """
    find_query = f'<{tag} '
    tag_start = entry.find(find_query)
    # Return empty string if tag not found
    if tag_start == '-1':
        return ''
    
    tag_val_start = tag_start + len(find_query)
    if second_one:
        tag_val_start = entry.find(find_query, tag_val_start) + len(find_query)
        
    tag_val_end = entry.find('>', tag_val_start)
    
    tag_val = entry[tag_val_start:tag_val_end]
    return tag_val
    

def is_in_index(index, file_name):
    """ Checks whether or not file with same name is already in the mygit index """
    entries = list_entries(index)
    
    for entry in entries:
        name = get_entry_tag_value(entry, 'name')
        
        if name == file_name:
            return True
    return False

def has_changed(index, file_sha, file_name):
    """ Checks whether or not file has changed from the one in mygit index """
    entries = list_entries(index)
    
    for entry in entries:
        sha = get_entry_tag_value(entry, 'SHA')
        name = get_entry_tag_value(entry, 'name')
        
        if sha != file_sha and name == file_name:
            return True
    return False
    

def ls_files():
    with open('.git/index', 'r') as index_file:
        index = index_file.read()
        entries = list_entries(index)
        
        for entry in entries:
            name = get_entry_tag_value(entry, 'name')
            print(name)
        
    
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
            try:
                with open(file_path, 'r') as f:
                    entry = get_entry_from_file(f)
                    update_index(entry, file_path)
                    
            except FileNotFoundError:
                update_index(None, file_path)
                
    elif command == 'ls-files':
        if is_init():
            ls_files()
    
    elif command == 'is-tree':
        pass
    elif command == 'write-tree':
        pass
    else:
        raise RuntimeError(f'Unknown command {command}')


if __name__ == '__main__':
#     ss = '''<ctime 1601823978.2589989>
# <ctime 0>
# <mtime 1601823978.2589989>
# <mtime 0>
# <dev 3536801771>
# <ino 5629499534466648>
# <mode 33206>
# <uid 0>
# <gid 0>
# <size 34>
# <SHA 99b2b1991f5f5a572bf64d5ee6903ab7c5a8ff96>
# <flags >
# <name example.txt>'''
#     s= get_entry_tag_value(ss, 'mtime', second_one=True)
#     print(s)
    
    main()
