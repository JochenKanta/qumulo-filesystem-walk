# Qumulo filesystem walk with python and the API

Walk a Qumulo filesystem, perform actions with highly parallelized python


## Requirements

* MacOSX - python 2.7, 3.7 (Tested on 2.7.16 and 3.7.7)
* Linux  - python 2.7, 3.7 (Tested on 2.7.15 and 3.7.6)
* Qumulo API python bindings `pip install -r requirements.txt`



## How it works

This is approach is designed to handle billions of files and directories. Because billions of files and directories is a lot there are a number of optimizations added to this tool, including:

* Plugin a variety of "classes" to support different actions
* Ability to run on only a specified subdirectory
* Leverage all Qumulo cluster nodes for extra power
* Multiprocessing queue to leverage Qumulo's scale and performance
* Local on-disk queue for when the in-process queue grows too large
* Progress updates every 10 seconds to confirm it's working
* Handle API bearer token timeout after 10 hours
* Break down large directories into smaller chunks
* Batch up small sets of files and directories when possible
* Works both with Python2 and Python3


## How fast it is?

It can read over 150,000 files per second and up to 6,000 directories per second. Generally, the script is more bound by number of directories than number of files. If there are things happening with each file that you add into the `each_file` method, you will very likely end up limited by the client cpu and you won't be able to achieve 150,000 files per second or 6,000 directories per second.



## What can I do with the qwalk.py tool?


### Summarize owners of filesystem capacity

`python qwalk.py -s product.eng.qumulo.com -d / -c SummarizeOwners`

This example walks the filesystem and summarizes owners and their corresponding file count and capacity utilization.


### Change the file extension names for certain files

`python qwalk.py -s product.eng.qumulo.com -d / -c ChangeExtension --from jpeg --to jpg`

This example walks the filesystem, searches for files ending with ".jpeg" and then logs what files would be changed. If you want to make the changes, run the script with the added `-g` argument. 


### Search filesystem paths and names by regular expression or string

`python qwalk.py -s product.eng.qumulo.com -d / -c Search --str password`

Search for files with the exact string 'password' in the path or name. Look for the output in `output-walk-log.txt` in the same directory.

`python qwalk.py -s product.eng.qumulo.com -d / -c Search --re ".*passw[or]*d.*"`

Case-insensitive search for files with the string 'password' or 'passwd' in the path or name.
Look for the output in `output-walk-log.txt` in the same directory.


### Examine contents of files to check for data reduction potential

`python qwalk.py -s product.eng.qumulo.com -d / -c DataReductionTest --perc 0.01`

Walk the filesystem and open a random 1% of files (--perc 0.01) and use zlib.compress to verify how compressible the data in the file is. This class will only attempt to compress, at most, 12288 bytes in each file. Because each examined requires multiple operations, this can be slower than the other current walk classes.


### POSIX mode bits where the owner has no rights to the file or directory.

`python qwalk.py -s product.eng.qumulo.com -d / -c ModeBitsChecker`

This will look at the metadata on each file and write any results to a file where the file or directory looks like '0\*\*' on the mode bits.



## Building qtask classes

Any walk of the filesystem will involve handling lots of files and directories. It also can involve a lot of different functionality and code. The qtask classes are where this functionality can be built. Above we have a number of classes currently built, but for those that know a bit of code, they can create their own classes or modify existing classes to meet their functional needs.

See the current imlementations in qtask.py to figure out how to build your own approach.

For a bit of context that can help, below you will find the metadata that we have with each file inside of the `every_batch` method.

```{
 'dir_id': '5160036463',
 'type': 'FS_FILE_TYPE_FILE'
 'id': '5158036745',
 'file_number': '5158036745',
 'path': '/gravytrain-tommy/hosting-backup/map-tile/vet02123002133313322.jpg',
 'name': 'vet02123002133313322.jpg',
 'change_time': '2018-03-31T22:04:48.877148926Z',
 'creation_time': '2018-03-31T22:04:48.870469026Z',
 'modification_time': '2015-11-25T07:15:51Z',
 'child_count': 0,
 'num_links': 1,
 'datablocks': '1',
 'blocks': '2',
 'metablocks': '1',
 'size': '3240',
 'owner': '12884901921',
 'owner_details': {'id_type': 'NFS_UID', 'id_value': '33'},
 'group': '17179869217',
 'group_details': {'id_type': 'NFS_GID', 'id_value': '33'},
 'mode': '0644',
 'symlink_target_type': 'FS_FILE_TYPE_UNKNOWN',
 'extended_attributes': {'archive': True,
                         'compressed': False,
                         'hidden': False,
                         'not_content_indexed': False,
                         'read_only': False,
                         'sparse_file': False,
                         'system': False,
                         'temporary': False},
 'directory_entry_hash_policy': None,
 'major_minor_numbers': {'major': 0, 'minor': 0},
}
```

Additional data can be extracted per file, such as acls, alternate data streams, and other details. That additional data will require additional API calls, and will slow down the walk.

