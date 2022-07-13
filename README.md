# ARCHIVER
Simple script to archive files a of a specified age from a source to destination while maintaining folder structure.

Writes log to script folder.

Warning: deletes empty folders!

Warning: Ages are imprecise, both input and the age of the files are cast to an integer for full days only.

## Getting Started

Run the with arguments as follows:

```
python archiver.py <ACTION> <AGE_IN_DAYS> <SOURCE_PATH> <DESTINATION_PATH> <IGNORE_STRING1> <IGNORE_STRING2> <IGNORE_STRING...> <IGNORE_STRING10000000>
```

Actions are as follows: 'copy', 'move', 'delete'

If action is 'delete', do not provide destination path.

If executing in a windows environment, use forward slashes instead of backslashes in paths.

'Ignore_strings' aren't handled gracefully in any way, beware. ie. they are just looked for in file path names as a plain string, no wild cards, etc.

```
python archiver.py copy 31 C:/temp/lotsoffiles/ C:/temp/filearchive/ .ignorefolder donotdelete.text keepme.avi
```

```
python archiver.py move 31 C:/temp/lotsoffiles/ C:/temp/filearchive/ .ignorefolder donotdelete.text keepme.avi
```

```
python archiver.py delete 31 C:/temp/lotsoffiles/ .ignorefolder donotdelete.text keepme.avi
```

### Prerequisites

Requires pandas: 

```
pip install pandas
```

## Authors

* **Tim Quan**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

