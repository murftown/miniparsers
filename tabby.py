SPLIT_BY = '\n'

def parse(txt):

	# start with something like this:
		"""
		list1
			list1 item1
			list1 item2
				list1 item2 subitem1
				list1 item2 subitem2
		list2
			list2 item1
			list2 item2
		"""
	# and we seek to organize it into a nested structure as such:
		"""
		[['list1',
			'list1 item1', 
			['list1 item2',
				'list1 item2 subitem1',
				'list1 item2 subitem2']],
		['list2',
			'list2 item1',
			'list2 item2']]
		"""

	# first: get # of leading tabs
		def n_tabs(txt_line):
			import re
			match = re.match(r'\t*',txt_line)
			if match:
				return len(match.group())

	# next: split into lines
		if isinstance(txt,list):
			lines = txt
		elif isinstance(txt,str):
			lines = txt.split(SPLIT_BY)
		#-> ['list1', '\tlist1 item1', '\tlist1 item2', '\t\tlist1 item2 subitem1', '\t\tlist1 item2 subitem2', 'list2', '\tlist2 item1', '\tlist2 item2', '']

	# remove empty lines
		lines = filter(lambda x: x!='', lines)

	# assert that there are some lines
		if len(lines) == 0:
			return []
			#raise ValueError('tabby: no (non-blank) lines to parse')

	# assert last line is at level 0
		if n_tabs(lines[-1]) != 0:
			lines.append('')

	# next: instead of tab characters, insert 1's and -1's representing indents and dedents respectively
		arr = []
		level = 0
		for txt_line in lines:
			num_tabs = n_tabs(txt_line)
			if num_tabs is not None:
				relative_indent = num_tabs - level
				if relative_indent > 0:
					for i in range(relative_indent): arr.append(1)
				elif relative_indent < 0:
					for i in range(-relative_indent): arr.append(-1)
				txt_line = txt_line[num_tabs:]
				level = num_tabs
			else: raise Exception('tabby.parse(): unexpectedly, no match found')
			arr.append(txt_line)
		#-> ['list1', 1, 'list1 item1', 'list1 item2', 1, 'list1 item2 subitem1', 'list1 item2 subitem2', -1, -1, 'list2', 1, 'list2 item1', 'list2 item2', -1, '']

	# next: remove trailing '' if any
		if arr[-1] == '': del arr[-1]
		#-> ['list1', 1, 'list1 item1', 'list1 item2', 1, 'list1 item2 subitem1', 'list1 item2 subitem2', -1, -1, 'list2', 1, 'list2 item1', 'list2 item2', -1]

	# next: move 1's one position back
		for i,v in enumerate(arr):
			if v==1 and i>0:
				arr[i-1],arr[i] = arr[i],arr[i-1]
		#-> [1, 'list1', 'list1 item1', 1, 'list1 item2', 'list1 item2 subitem1', 'list1 item2 subitem2', -1, -1, 1, 'list2', 'list2 item1', 'list2 item2', -1]

	# next: replace with '[' and ']'
		arr = ['[' if i==1 else ']' if i==-1 else i for i in arr]
		#-> ['[', 'list1', 'list1 item1', '[', 'list1 item2', 'list1 item2 subitem1', 'list1 item2 subitem2', ']', ']', '[', 'list2', 'list2 item1', 'list2 item2', ']']	

	# parse '[' and ']' to create nested list structure
		import bratch
		arr = bratch.parse_toks(arr)
		#-> [['list1', 'list1 item1', ['list1 item2', 'list1 item2 subitem1', 'list1 item2 subitem2']], ['list2', 'list2 item1', 'list2 item2']]

		return arr



def list2dict(L):
	# again imagine our structure is as such:
		"""
		list1
			list1 item1
			list1 item2
				list1 item2 subitem1
				list1 item2 subitem2
		list2
			list2 item1
			list2 item2
		"""
	# but now we are starting from the end-point of the parse function:
		"""
		[['list1',
			'list1 item1', 
			['list1 item2',
				'list1 item2 subitem1',
				'list1 item2 subitem2']],
		['list2',
			'list2 item1',
			'list2 item2']]
		"""
	# and seeking to change the list of lists into a dict of dicts:
		"""
		{
			'list1': {
				'list1 item1': {},
				'list1 item2': {
					'list1 item2 subitem1': {},
					'list1 item2 subitem2': {}
					}
				},
			'list2': {
				'list2 item1': {},
				'list2 item2': {}
			}
		}
		"""

		D = {}
		for i in L:
			if isinstance(i,list) and len(i)>0:
				#print "D["+str(i[0])+"] = list2dict("+str(i[1:])+")"
				D[i[0]] = list2dict(i[1:])
				#print "newD",D
			else:
				D[i] = {}
		return D

def add_tabs(L,n=0):
	newL = [add_tabs(v,n+1) if isinstance(v,list) else '\t'*(n-1 if i==0 else n)+v for i,v in enumerate(L)]
	return '\n'.join(newL)

def add_tabsL(L,n=0):
	newL = [add_tabs(v,n+1) if isinstance(v,list) else '\t'*(n-1 if i==0 else n)+v for i,v in enumerate(L)]
	return newL


def dock(text_rows, only_whitespace=True, return_commonality=False):
	verbose = False
	commonality = []
	i = 0
	while True:
		if verbose: print 'commonality:',commonality
		char = None
		keep_breakin = False
		for row in text_rows:
			if verbose: print 'row:',row
			if len(row) > i and char is None:
				char = row[i]
				if verbose: print 'char:',char
			elif len(row) <= i:
				if verbose: print 'len(row),',len(row),'isn\'t as long as',i
				keep_breakin = True
				break;
			elif row[i] != char:
				if verbose: print row[i],'didn\'t match',char
				keep_breakin = True
				break;
			if only_whitespace and char not in [' ','\t','\n']:
				keep_breakin = True
				break;
		if keep_breakin:
			break;
		commonality += char
		i += 1
	if return_commonality:
		return commonality
	else:
		return [row[len(commonality):] for row in text_rows]

remove_tabs = dedent = dock
