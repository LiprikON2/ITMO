import hashlib
import sys
import os
import zlib
import textwrap
import re
import time
from pathlib import Path


def config(tag):
    """
    .mygit/config file reader

    avaliable tags: 'name', 'email'
    """
    if os.path.exists('.mygit/config'):
        with open('.mygit/config', 'r') as config_file:
            config = config_file.read()

            if config.find(tag) == -1:
                return ''

            value_start = config.find(tag) + len(tag) + 1
            value_end = config.find('\n', value_start)

            return config[value_start:value_end]


def commit_tree(tree_sha, message, parent_sha='', printing=True):

    author_name = committer_name = config('name')
    author_email = committer_email = config('email')
    author_date_seconds = committer_date_seconds = int(time.time())
    author_date_timezone = committer_date_timezone = time.strftime(
        "%z", time.gmtime())

    if parent_sha:
        parents = f'parent {parent_sha}\n'
    else:
        parents = ''

    commit_content = f'tree {tree_sha}\n'
    commit_content += parents
    commit_content += f'author {author_name} <{author_email}> {author_date_seconds} {author_date_timezone}\n'
    commit_content += f'committer {committer_name} <{committer_email}> {committer_date_seconds} {committer_date_timezone}\n\n'
    commit_content += message
    
    commit_header = f'commit {len(commit_content)}\0'
    commit_object = commit_header + commit_content

    commit_sha = object_sha(commit_object)
    if printing:
        print(commit_sha)

    write_object(commit_object, commit_sha)


def log(commit_sha):
    """
    Prints content of a commit by its SHA
    """
    commit_object = read_object(commit_sha)
    header_len = commit_object.find(b'\x00') + 1
    
    header = commit_object[:header_len]
    
    content_len = int(header[commit_object.find(b' '):commit_object.find(b'\x00')].decode('ascii'))
    content = commit_object[header_len:header_len + content_len].decode('ascii')
    
    author_start = content.find('author ') + len('author ')
    author_end = content.find(' ', author_start)
    author = content[author_start:author_end]
    
    email_start = content.find('<') 
    email_end = content.find('>') + 1
    email = content[email_start:email_end]
    
    times
    # print(header)
    # print(content_len)


# TODO check if by changing file content tree SHA changes
def ls_tree(sha, passed_rec_path='', printing=True):
    """
    ls-like print of tree object with optional recursion

    passed_rec_path - parent path, passed from previous recursion level
    """
    tree_object = read_object(sha)

    header_len = tree_object.find(b'\x00') + 1
    header = tree_object[:header_len]

    content_len = int(header[tree_object.find(b' '):tree_object.find(b'\x00')].decode('ascii'))
    content = tree_object[header_len:header_len + content_len].decode('ascii')

    object_type = header[:tree_object.find(b' ')].decode('ascii')

    if not object_type == 'tree':
        print('Not a tree object')
        sys.exit(0)

    # NULL symbol is before the SHA in each entry
    content_nulls_iter = re.finditer('\x00', content)

    content_len = len(content)
    content_len_left = content_len

    # Because every's entry start is another entry's end (except the first - `0`)
    # we can get all start/end points by finding entry's ends
    entry_positions = [0]
    # Iter over all NULLs in tree content
    for entry_null in content_nulls_iter:
        # 40 - is length of the SHA
        entry_end = entry_null.start() + 40 + 1
        entry_positions.append(entry_end)

    # Process tree content entries, knowing their positions
    entries = []
    for i in range(len(entry_positions) - 1):
        entry = content[entry_positions[i]:entry_positions[i + 1]]

        mode_end = entry.find(' ')
        mode = entry[:mode_end]

        name_end = entry.find('\x00')
        name = entry[mode_end + 1:name_end]

        sha = entry[name_end + 1:]

        object_type = cat_file(sha, printing=False)
        if printing:
            print(f'{mode} {object_type} {sha}    {passed_rec_path + name}')

        # Recurse into tree, passing parent path
        if '-r' in sys.argv and object_type == 'tree':
            parent_path = passed_rec_path + f'{name}/'
            ls_tree(sha, passed_rec_path=parent_path)


def tree_parse_one():
    pass


def read_index():
    if os.path.exists('.mygit/index'):
        with open('.mygit/index', 'r') as index_file:
            return index_file.read()


def write_tree(rec_level=0, printing=True):  # TODO deleted files handling
    index = read_index()
    entries = list_entries(index)

    tree_content = ''
    # (sha, name) tuple of subfolders and subfiles, used to calculate this tree's SHA
    entry_sha_name_list = []
    for entry in entries:
        name_with_folders = get_entry_tag_value(entry, 'name')
        sha = get_entry_tag_value(entry, 'SHA')
        size = get_entry_tag_value(entry, 'size')

        folders, name = split_into_folders(name_with_folders)

        # If it's a folder on current recursion level, then process it by recursing inside
        if rec_level < len(folders):
            # Permissions for folders
            mode = '040000'
            # Joins a path to the current recursion level
            rec_name = os.path.join(
                *folders[:rec_level + 1]).replace('\\', '/')

            # Ensure the folder isn't already processed
            if tree_content.find(f' {rec_name}') == -1:
                # print(rec_level, '  '*rec_level, 'FOLDER:', rec_name)

                # Recursing inside
                sha = write_tree(rec_level=rec_level + 1)

                # Format: [mode] [file/folder name]\0[SHA-1 of referencing blob or tree]
                tree_entry = f'{mode} {folders[rec_level]}\0{sha}'
                tree_content += tree_entry

                entry_sha_name_list.append((name, sha))
            else:
                continue
        # If it's a file on current recursion level, process it
        elif rec_level == len(folders):
            # print(rec_level, '  '*rec_level, 'FILE:', name_with_folders)
            mode = '100644'
            tree_entry = f'{mode} {name}\0{sha}'
            tree_content += tree_entry
            entry_sha_name_list.append((name, sha))
        else:
            continue

    tree_header = f'tree {len(tree_content)}\0'
    # Format: tree [content size]\0[Entries (content) having references to other trees and blobs]
    tree_object = tree_header + tree_content

    tree_sha = calc_tree_sha(entry_sha_name_list)
    if printing and rec_level == 0:
        print(tree_sha)

    write_object(tree_object, tree_sha)
    return tree_sha


def calc_tree_sha(sha_name_list):
    data = [''.join(sha_name) for sha_name in sha_name_list]
    data = ''.join(data)
    return object_sha(data)


def split_into_folders(path_and_file):
    """
    `folder/folder2/quote.txt` -> (['folder', 'folder2'], 'quote.txt')
    """
    path, file = os.path.split(path_and_file)

    folders = []
    while True:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()
    return folders, file


def object_sha(text):
    return hashlib.sha1(text.encode()).hexdigest()


def read_object(sha):
    """
    Reads an object that was saved in a way such that first 2 symbols
    of SHA of the object - is folder name, the rest is file name
    """
    folder_name = sha[:2]
    file_name = sha[2:]
    folder_path = f'.mygit/objects/{folder_name}'
    try:
        with open(os.path.join(folder_path, file_name), 'rb') as object_file:
            return zlib.decompress(object_file.read())
    except FileNotFoundError:
        print(f'Not a valid object name {sha}')


def write_object(object, sha):
    """
    Saves an object in a way such that first 2 symbols of SHA
    of the object - is folder name, the rest is file name
    """
    folder_name = sha[:2]
    file_name = sha[2:]
    folder_path = f'.mygit/objects/{folder_name}'

    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, file_name), 'wb') as object_file:
        compressed_object = zlib.compress(object.encode())
        object_file.write(compressed_object)


# More like hash file if I'm being honest
def hash_object(file, writing=False, printing=True):
    content = file.read()
    # `\0` or `\x00` is a null character, used to separate header and content
    header = f'blob {len(content)}\0'

    object = header + content
    sha = object_sha(object)
    if printing:
        print(sha)

    if writing:
        write_object(object, sha)
    else:
        return sha


def cat_file(sha, printing=True):
    object = read_object(sha)
    header_len = object.find(b'\x00') + 1

    # blob 25\x00789c4bcac94f...
    # ^^^^^^^^^^^
    header = object[:header_len]

    # blob 25\x00789c4bcac94f...
    #      ^^
    content_len = int(header[object.find(b' '):object.find(b'\x00')].decode('ascii'))

    # blob 25\x00789c4bcac94f...
    #            ^^^^^^^^^^^^^^^
    content = object[header_len:header_len + content_len].decode('ascii')

    # blob 25\x00789c4bcac94f...
    # ^^^^
    object_type = header[:object.find(b' ')].decode('ascii')

    if printing:
        if '-p' in sys.argv:
            if object_type == 'tree':
                ls_tree(sha)
            else:
                print(content)
        elif '-t' in sys.argv:
            print(object_type)
        elif '-s' in sys.argv:
            print(content_len)
        else:
            print('Available parametrs: \n-t - show object type\n-s - show object size\n-p - pretty-print object\'s content')
    else:
        return object_type


def get_entry_from_file(file):
    """ Returns mygit index entry string from specified file """
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

    with open(file_name, 'r') as f:
        hash_object(f, writing=True, printing=False)

    if not os.path.exists('.mygit/index'):
        with open('.mygit/index', 'w') as index_file:
            entry_count = '1'

            header = f'DIRC {version} {entry_count}\n'
            content = header + entry
            content_sha = object_sha(content)
            footer = f'<sha {content_sha}>'

            index = content + footer
            save_index_file(index_file, index)
            print(f'Added {file_name}')

    else:
        with open('.mygit/index', 'r+') as index_file:
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


def remove_index_entry(index, file_name, printing=True):
    """
    Returns new mygit index with removed mygit index entry
    """

    if not is_in_index(index, file_name):
        return index

    entries = list_entries(index)
    for entry in entries:
        index_name = get_entry_tag_value(entry, 'name')
        if file_name == index_name:
            new_index = increment_index_entry_count(index, decrement=True)
            
            entry_start = index.find(entry)
            entry_end = entry_start + len(entry)
            new_index = new_index[:entry_start] + new_index[entry_end:]

    if printing:
        print(f'Removed {file_name}')

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
    Returns new index with updated mygit index footer - SHA-1
    over the content of the index file before this checksum
    """
    footer_start = index.find('<sha')

    if not sha:
        sha = object_sha(index[:footer_start])

    return index[:footer_start] + f'<sha {sha}>'


def list_entries(index):
    """ Returns list of plain text entries from mygit index """
    entry_start_iter = re.finditer(f'<ctime', index)
    last_entry_end = index.rfind('>') + 2

    entry_positions = []
    for i, entry_start in enumerate(entry_start_iter):
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
    'mode', 'uid', 'gid', 'size', 'SHA', 'flags', 'name'.

    second_one=True/Flase - determines whether return value of second tag occurence or the first

    """
    find_query = f'<{tag} '
    tag_start = entry.find(find_query)
    # Return empty string if tag not found
    if tag_start == -1:
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
    """
    ls-like print of files that are currently in mygit index
    """

    index = read_index()
    entries = list_entries(index)

    for entry in entries:
        name = get_entry_tag_value(entry, 'name')
        if '-s' in sys.argv:
            sha = get_entry_tag_value(entry, 'SHA')
            mode = get_entry_tag_value(entry, 'mode')
            print(f'100644 {sha} 0    {name}')  # TODO remove hardcoded values
        else:
            print(name)


def is_init():
    if not os.path.exists('.mygit'):
        print('mygit is not initialized in this directory')
        return False
    return True


def create_repo():
    os.makedirs('.mygit/objects', exist_ok=True)
    os.makedirs('.mygit/refs/heads', exist_ok=True)
    os.makedirs('.mygit/refs/tags', exist_ok=True)
    with open('.mygit/HEAD', 'w+') as f:
        f.write('ref: refs/heads/master\n')

    while True:
        name = input('Your name: ')
        if name:
            break
    while True:
        email = input('Your email: ')
        if email:
            break
    with open('.mygit/config', 'w+') as f:
        f.write(f'name={name}\nemail={email}\n')
    print('Initialized git directory')


def main():
    command = sys.argv[1]  # TODO: catch
    if command == 'init':
        create_repo()

    elif command == 'cat-file':
        if is_init():
            sha = sys.argv[2]
            cat_file(sha)

    elif command == 'hash-object':
        if is_init():
            file_path = sys.argv[2]
            with open(file_path, 'r') as f:
                if '-w' in sys.argv:
                    hash_object(f, writing=True)
                else:
                    hash_object(f)

    elif command == 'update-index':
        if is_init():
            file_path = sys.argv[2]
            try:
                with open(file_path, 'r') as f:
                    entry = get_entry_from_file(f)
                    update_index(entry, file_path)
            # In case of a deleted file
            except FileNotFoundError:
                update_index(None, file_path)
            # In case of a folder
            except PermissionError:
                print(f'Unable to process path {file_path}')

    elif command == 'ls-files':
        if is_init():
            ls_files()

    elif command == 'write-tree':
        if is_init():
            write_tree()

    elif command == 'ls-tree':
        if is_init():
            tree_sha = sys.argv[2]
            ls_tree(tree_sha)

    elif command == 'commit-tree':
        if is_init():
            try:
                tree_sha = sys.argv[2]

                if sys.argv[3] == '-m':
                    message = sys.argv[4]
                else:
                    raise IndexError

                if '-p' in sys.argv and len(sys.argv) == 7:
                    parent_sha = sys.argv[6]
                    commit_tree(tree_sha, message, parent_sha=parent_sha)
                elif '-p' in sys.argv:
                    raise IndexError
                else:
                    commit_tree(tree_sha, message)

            except IndexError:
                if ('-m' in sys.argv or len(sys.argv) < 4) and ('-p' not in sys.argv or len(sys.argv) < 7):
                    print('Provide a message with -m (e.g. ... -m "init commit")')
                else:
                    print(
                        'Commit parent is provided with -p after message (e.g. ... -m "init commit" -p SHAshaSHA123...)')

    elif command == 'log':
        if is_init():
            commit_sha = sys.argv[2]
            log(commit_sha)

    else:
        raise RuntimeError(f'Unknown command {command}')


if __name__ == '__main__':
    main()
