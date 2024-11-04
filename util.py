#Name:Raunak Agarwal
#Student ID- 1636678
#CMPUT-274, Fall 2020
#Assignment 2: Huffman coding

import bitio
import huffman
import pickle

## new comment
def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    tree=pickle.load(tree_stream)
    return tree
    pass

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """

    if isinstance(tree,huffman.TreeLeaf):
      return(tree.getValue())
    bit=bitreader.readbit()
    if bit:
      return decode_byte(tree.getRight(),bitreader)
    return decode_byte(tree.getLeft(),bitreader)    

    pass


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    tree=read_tree(compressed)
    bw=bitio.BitWriter(uncompressed)
    br=bitio.BitReader(compressed)
    EOF=False
    while not EOF:
      leaf=decode_byte(tree,br)
      if leaf!=None:
        bw.writebits(leaf,8)
      elif leaf==None:
        break

    pass

def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree,tree_stream)

    pass

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    write_tree(tree,compressed)
    br=bitio.BitReader(uncompressed)
    bw=bitio.BitWriter(compressed)
    EOF=False
    et=huffman.make_encoding_table(tree)
    z=et[None]
    try:
      while True:
        val=br.readbits(8)
        path=et[val]
        if val is None:
          raise EOFError
        for i in path:
          bw.writebit(i)

    except EOFError:
      EOF=True

    for i in z:
      bw.writebit(i)

      

    bw.flush()
   

    pass
