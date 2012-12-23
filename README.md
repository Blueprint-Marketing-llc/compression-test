
HTTP Header Compression Tests
=============================

Usage
-----

The test can be run like this:

    ./compare_compressors.py [options] list-of-har-files

See [the HAR specification](http://www.softwareishard.com/blog/har-12-spec/), 
and our [collected sample HAR files](https://github.com/http2/http_samples).

The most important option is -c, which specifies what compressors to run.
Current codecs include:

* http1_gzip - gzip compression of HTTP1.x headers
* spdy3 - SPDY 3's gzip-based compression
* delta - draft-rpeon-httpbis-header-compression implementation
* fork - fork a process; see below

Interpreting Results
--------------------

Results will look something like:

    1092 req messages processed
                      compressed | ratio min   max
    req      http1       291,628 | 1.00  1.00  1.00
    req http1_gzip        25,855 | 0.09  0.02  0.61
    req      spdy3        34,660 | 0.12  0.03  0.69

    1092 res messages processed
                      compressed | ratio min   max
    res      http1       190,650 | 1.00  1.00  1.00
    res http1_gzip        27,964 | 0.15  0.03  0.57
    res      spdy3        37,373 | 0.20  0.06  0.65

The 'compressed' column shows how many bytes the compression algorithm 
outputs; 'ratio' shows the ratio to the baseline (http1, by default), and
the 'min' and 'max' columns show the minimum and maximum ratios, respectively.


Adding New Compression Algorithms
---------------------------------

If you wish to implement a new codec, there are two easy approaches.

1) Develop it in Python. New modules should be subdirectories of 
'compressor'. 

2) Develop it in another language, and use the 'fork' module to execute
it in a separate process. See 'sample_exec_codec.py' for an example of this; 
it can be run like this:

    ./compare_compressors.py -c fork="sample_exec_codec.py" file.har

