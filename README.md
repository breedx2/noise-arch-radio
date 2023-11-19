
To fetch a page of items in a collection
https://archive.org/advancedsearch.php?q=collection:noise-arch&rows=100&page=4&output=json
which contains a lot of fields you may not want, so limit the fields:
https://archive.org/advancedsearch.php?q=collection:noise-arch&fl%5B%5D=identifier&rows=100&page=4&output=json

Example of entry that has no actual audio, just image scans:
https://archive.org/metadata/noise-arch_cortex-souv

Audio file entries within the `files` field of metadata will have a `length` 
field. Be sure not to duplicate, check the `source` field, one of `original` or 
`derivative` typically. The `format` field is typically 
* VBR MP3
* Ogg Vorbis
* ?what else?

How to fetch identifiers within a collection with the `ia` commandline:

```
ia search -i collection:noise-arch 
```


# TODO: 

* about modal
* link to ia page
* link to discogs search
* recent past plays
