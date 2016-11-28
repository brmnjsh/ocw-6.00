# x = 10.0
# for i in range(10):
#     x += 0.1
#     print i
#     print x
#
# print x
# print x == 11.0
# print "========="
#
# for i in range(10):
#     x -= 0.1
#     print i
#     print x
#
# print x
# print x == 10.0

# def buildCodeBook():
#  letters ='.abcdefghijklnopqrstuvwxyz'
#  codeBook = {}
#  key = 0
#  for c in letters:
#      codeBook[key] = c
#      key += 1
#  return codeBook
# def decode(cypherText, codeBook):
#  plainText = ''
#  for e in cypherText:
#      if e in codeBook:
#          plainText += codeBook[e]
#      else:
#          plainText += ' '
#  return plainText
#
# codeBook = buildCodeBook()
# msg = (3,2,41,1,0)
# print decode(msg, codeBook)

# def getLines():
#     inputs = []
#     while True:
#         line = raw_input('Enter a positive integer, -1 to quit: ')
#         line = int(line)
#         if line == -1:
#             return inputs
#         inputs.append(line)
# total = 0
# for e in getLines():
#     total += e
# print total
# def f(L):
#     result = []
#     for e in L:
#         if type(e) != list:
#             result.append(e)
#         else:
#             return f(e)
#     return result
#
# print f([1, [['b', 'a'], [2,'b']]])

def f(s):
    print s
    if len(s) <= 1:
        return s
    return f(f(s[1:])) + s[0] #Note double recursion

print f('mat')
#print f('math')
