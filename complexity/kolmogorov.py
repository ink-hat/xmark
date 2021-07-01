import bz2
import lzma
import zlib

def calculate(src,algo=None):
    '''compute kologorov complexity using compression algorithm

    parameters
    -----------
    src : string
        filepath of the file whose complexity is 
        to be found
    algo : string, default: None
        compression algorithm to use
        available algos are bz2,lzma,zlib
        if no algorithm is specified, then all the algorithms
        will be run and the minimum complexity will be returned
    
    return
    ------
    float 
        kolmogorov complexity in range [0,1]
    '''
    bd = bytes()
    with open(src,'rb') as f:
        bd = f.read()
    
    uncomp_len = len(bd)    # uncompressed length
    comp_len = _compressed_length(bd,algo)

    return [comp_len/uncomp_len,]


def mutual_info(src1,src2,algo='lzma'):
    '''computes algorithmic mutual information

    parameters
    ----------
    src1 : string
        filepath of first file
    src2 : string
        filepath of second file
    algo: string, default: 'lzma'
        compression algorithm to use
        available algos are bz2,lzma,zlib
    
    return
    ------
    float 
        normalized kolmogorov complexity in range [0,1]
    '''
    with open(src1,'rb') as f1, open(src2,'rb') as f2:
        d1 = f1.read()
        d2 = f2.read()

    z1 = _compressed_length(d1,algo)
    z2 = _compressed_length(d2,algo)
    z12 = _compressed_length(d1+d2,algo)

    return [1-(z12 - min(z1,z2))/max(z1,z2)]


def _compressed_length(data,algo=None):
    '''returns the compressed length of given data
    using specified algorithm

    parameters
    ----------
    data : bytes
    algo : {bz2,lzma,zlib}, default: None
        if algo is None or not specified then 
        the least compressed length is returned,
        after running all algorithms
    return
    ------
    int
        length after compression
    '''
    compress_algos = {
        'bz2' : lambda x: bz2.compress(x,compresslevel=9),
        'lzma' : lambda x: lzma.compress(x,format=lzma.FORMAT_ALONE,check=lzma.CHECK_NONE,preset=9),
        'zlib' : lambda x: zlib.compress(x,level=9)
    }

    # if a specific algorithm should be used, then
    # remove all algo except the specified one.
    if algo != None:
        if algo in compress_algos:
            compress_algos = {algo : compress_algos[algo]}
        else:
            print("Invalid value as algo - {} ; available values are".format(algo,",".join(compress_algos.keys())))
    
    comp_len = len(data)
    # finding minimum compressed length among all available algorithms
    for algo in compress_algos:
        comp_len_new = len(compress_algos[algo](data))
        if comp_len_new < comp_len:
            comp_len = comp_len_new
    
    return comp_len