'''
nov12: split from parsley to pare down and focus on just bracket functionality (and escapes)
'''

# brackets from scratch
class Bratch:
	def __init__(self):
		self.important_chars = '[]'
	
	def escape(self,strn):
		'''lump the \ and the following char together '''
		escape_mode = False
		for i in strn:
			if escape_mode:
				if i in self.important_chars:
					yield '\\'+i
				else:
					yield '\\'
					yield i
				escape_mode = False
			elif i == '\\':
				escape_mode = True
			else:
				yield i
	
	esc = lambda self,x: list(self.escape(x))
	
	
	def tokenize(self,strn):
		reserve = []
		for i in strn:
			if i in self.important_chars:
				stripped_reserve = ''.join(reserve).strip()
				if len(stripped_reserve) > 0:
					yield stripped_reserve 
					reserve = []
				yield i
			else:
				if len(i)==2 and i[0]=='\\':
					reserve.append(i[1])
				else:
					reserve.append(i)
		stripped_reserve = ''.join(reserve).strip()
		if len(stripped_reserve) > 0:
			yield stripped_reserve
	
	tok = lambda self,x: list(self.tokenize(self.escape(x)))

	def parse_toks(self,data):
		level = 0
		ret = []
		stack = []
		for i in data:
			if i=='[':
				level += 1
				stack.append(ret)
				ret = []
			elif i==']':
				level -= 1
				stack[-1].append(ret)
				ret = stack[-1]
				del stack[-1]
			else:
				ret.append(i)
		return ret
	
	parse = lambda self,x: self.parse_toks(self.tokenize(self.escape(x)))


B = Bratch() # default parser ready to go
parse = B.parse
tokenize = B.tok
parse_toks = B.parse_toks
