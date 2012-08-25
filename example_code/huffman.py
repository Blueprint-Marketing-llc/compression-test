import heapq
from collections import deque
from bit_bucket import BitBucket
from bit_bucket import PrintAsBits

class Huffman:
  def __init__(self, freq_table):
    self.code_tree = None
    self.code_table = []
    self.BuildCodeTree(freq_table)
    self.BuildCodeTable(self.code_tree)
    #print self.FormatCodeTable()

  def BuildCodeTree(self, freq_table):
    if len(freq_table) < 2:
      # that'd be stupid...
      raise StandardError()
    # freq_table is (symbol, count)
    # code_tree is [freq, symbol, children]
    leaves = deque(sorted([ [frq, sym, []] for (sym, frq) in freq_table]))
    internals = deque()
    while len(leaves) + len(internals) > 1:
      children = []
      while len(children) < 2:
        if leaves and internals:
          if leaves[0][0] <= internals[0][0]:
            children.append(leaves.popleft())
          else:
            children.append(internals.popleft())
        elif leaves:
          children.append(leaves.popleft())
        else:
          children.append(internals.popleft())
      internals.append([(children[0][0] + children[1][0]), None, children])
    if len(leaves):
      print "WTF?"
      raise StandardError()
    self.code_tree = internals.pop()

  def BinaryStringToBREP(self, binary_string):
    output = []
    bitlen = len(binary_string)
    if not bitlen:
      raise StandardError()
    index = 0
    while index + 8 < bitlen:
      output.append(int(binary_string[index:index+8],2))
      index += 8
    if index != bitlen:
      final = binary_string[index:bitlen]
      for i in xrange(8 - (bitlen - index)):
        final += '0'
      output.append(int(final, 2))
    return (output, bitlen)

  def BuildCodeTable(self, code_tree):
    queue = deque([(code_tree, '')])
    pre_table = []
    while queue:
      (tree, path_so_far) = queue.popleft()
      (freq, name, children) = tree
      if name != None:
        #print ord(name), str(path_so_far), name
        pre_table.append( (ord(name), str(path_so_far)) )
      if children:
        queue.appendleft( (children[0], str(path_so_far + '0')) )
        queue.appendleft( (children[1], str(path_so_far + '1')) )
    pre_table = sorted(pre_table, key=lambda x: x[0])
    for i in xrange(len(pre_table)):
      (name, binary_string) = pre_table[i]
      if i != name:
        print "i (", i, ") != pre_table[i] (", name, ")", chr(name)
        raise StandardError()
      self.code_table.append(self.BinaryStringToBREP(binary_string))


  def Encode(self, text, include_eof):
    bb = BitBucket()
    for c in text:
      bb.StoreBits(self.code_table[c])
      #print "for: ", chr(c)
      #print "storing: ", PrintAsBits(self.code_table[c])
    if include_eof:
      #print 'eof'
      #print "storing: ", PrintAsBits(self.code_table[128])
      bb.StoreBits(self.code_table[128])
    return bb.GetAllBits()

  def Decode(self, text, includes_eof, bits_to_decode):
    output = []
    if not text:
      return output
    # this is the very very slow way to decode.
    c = text[0]
    bit_index = 0
    chr_index = 0
    if bits_to_decode < 0:
      bits_to_decode = len(text) * 8
    #print 'ieof: ', includes_eof
    #print "Text to decode: ", PrintAsBits((text, bits_to_decode))
    total_bits = 0
    while total_bits < bits_to_decode:
      root = self.code_tree
      while not root[1]:
        c = text[chr_index]
        bit = (c >> (7 - bit_index)) & 0x1
        #print root[0]," tb: ", total_bits, " bits_to_decode: ", bits_to_decode, " ci: ", chr_index, " b: ", bit
        bit_index += 1
        total_bits += 1
        if bit_index >= 8:
          #print "Reset"
          bit_index = 0
          chr_index += 1
        root = root[2][bit]
      #print "exited while with:", root[1], 0x80
      if includes_eof and ord(root[1]) == 128:
        #print 'eof'
        break
      elif root[1]:
        #print "foundit: ", root[1]
        output.append(root[1])
    #print "done"
    return output

  def FormatCodeTable(self):
    x = sorted([(chr(i), self.code_table[i]) for i in xrange(len(self.code_table))],
      key=lambda x: (x[1][1], x[1][0]))
    return repr(x)

  def __str__(self):
    output = ['[']
    for elem in self.code_table.iteritems():
      output.append(repr(elem))
      output.append(', ')
    output.append(']')
    return ''.join(output)

  def __repr__(self):
    return self.__str__()

