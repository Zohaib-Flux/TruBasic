from Global_variables import *
from Token import *
from Errors import *
import os

##############################################################################################
# SYMBOLTABLE
##############################################################################################

class SymbolTable:
	def __init__(self, parent = None):
		self.symbols = {}
		self.parent = parent
	
	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

##############################################################################################
# CONTEXT
##############################################################################################

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

	def get(self, name):
		return self.symbol_table.get(name)

	def set(self, name, value):
		self.symbol_table.set(name, value)

	def remove(self, name):
		self.symbol_table.remove(name)

##############################################################################################
# VALUES
##############################################################################################

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()
	
	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)
	
	def subbed_by(self, other):
		return None, self.illegal_operation(other)

	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)

	def raised_to(self, other):
		return None, self.illegal_operation(other)

	def modded_to(self, other):
		return None, self.illegal_operation(other)
	
	def floor_dived_to(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return Number(int(type(self).__name__ == type(other).__name__)), None

	def get_comparison_ne(self, other):
		return Number(int(type(self).__name__ != type(other).__name__)), None

	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)

	def anded_by(self, other):
		return None, self.illegal_operation(other)

	def ored_by(self, other):
		return None, self.illegal_operation(other)
		
	def notted(self):
		return None, self.illegal_operation(self)

	def copy(self):
		raise Exception('No copy method defined')

	def execute(self, args):
		return RTResult().failure(self.illegal_operation())

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		other = other or self
		return RunTimeError(
			self.pos_start, other.pos_end,
			f"Illegal operation between types: '{type(self).__name__}' and '{type(other).__name__}'",
			self.context or other.context
		)

class NoneType(Value):
	def __init__(self):
		super().__init__()

	def copy(self):
		return NoneType().set_pos(self.pos_start, self.pos_end).set_context(self.context)
	
	def __str__(self):
		return "None"
	
	def __repr__(self):
		return str(self)

class Number(Value):
	def __init__(self, value, is_bool=False):
		super().__init__()
		self.bool = is_bool
		self.value = value

	# Binary Operations 
	###############################################################################################

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		elif isinstance(other, String):
			return String(str(self.value)+other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RunTimeError(
          self.pos_start, 
          self.pos_end, 
          "Division By Zero", 
          self.context)
			else:
				return Number(self.value / other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def raised_to(self, other):
		if isinstance(other, Number):
			return Number(self.value**other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def modded_to(self, other):
		if isinstance(other, Number):
			return Number(self.value%other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def floor_dived_to(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RunTimeError(
        self.pos_start, 
        self.pos_end, 
        "Division By Zero", 
        self.context)
			else:
				return Number(self.value // other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	# Unary Operations 
	###############################################################################################
		
	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def copy(self):
		copy = Number(self.value, self.bool)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		if self.bool:
			return "True" if self.value == 1 else "False"
		return str(self.value)

	def __repr__(self):
		return str(self)

	def is_true(self):
		return self.value != 0

	def __eq__(self, other):
		try:
			return self.value == other.value
		except:
			return False

Number.true = Number(1)
Number.false = Number(0)
Number.true.bool = True
Number.false.bool = True

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value+other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return String(self.value*other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			try:
				return String(self.value[other.value]), None
			except:
				return None, RunTimeError(
					other.pos_start,
					other.pos_end,
					"Invalid Index",
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)
	
	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		return String(self.value).set_pos(self.pos_start, self.pos_end).set_context(self.context)

	def get_comparison_eq(self, other):
		if isinstance(other, String):
			return Number(int(self.value == other.value)), None
		else:
			return Number(0), None

	def get_comparison_ne(self, other):
		if isinstance(other, String):
			return Number(int(self.value != other.value)), None
		else:
			return Number(1), None

	def get_comparison_lt(self, other):
		try:
			return Number(int(self.value < other.value)), None
		except:
			return Number(0), None

	def get_comparison_gt(self, other):
		try:
			return Number(int(self.value > other.value)), None
		except:
			return Number(0), None

	def get_comparison_lte(self, other):
		try:
			return Number(int(self.value <= other.value)), None
		except:
			return Number(0), None

	def get_comparison_gte(self, other):
		try:
			return Number(int(self.value >= other.value)), None
		except:
			return Number(0), None

	def anded_by(self, other):
		return (self if other.is_true() else Number(0)), None

	def ored_by(self, other):
		return (self if self.is_true() else other), None

	def __str__(self):
		return f'{self.value}'
	
	def __repr__(self):
		return f'"{self.value}"'

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements[:]

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):
		if isinstance(other, Number):
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
			except:
				return None, RunTimeError(
					other.pos_start,
					other.pos_end,
					"Invalid Index",
					self.context
				)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RunTimeError(
					other.pos_start,
					other.pos_end,
					"Invalid Index",
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)


	def multed_by(self, other):
		if isinstance(other, List):
			return List(self.elements+other.elements).set_pos(self.pos_start, self.pos_end).set_context(self.context), None
		elif isinstance(other, Number):
			new = self.elements.copy()
			for i in range(other.value-1):
				new += self.elements.copy()
			return List(new).set_pos(self.pos_start, self.pos_end).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def is_true(self):
		return len(self.elements) > 0

	def get_comparison_eq(self, other):
		if isinstance(other, List):
			return Number(int(self.elements == other.elements)), None
		else:
			return Number(0), None

	def get_comparison_ne(self, other):
		if isinstance(other, List):
			return Number(int(self.elements != other.elements)), None
		else:
			return Number(1), None

	def get_comparison_lt(self, other):
		return Number(int(self.elements < other.elements)), None

	def get_comparison_gt(self, other):
		return Number(int(self.elements > other.elements)), None

	def get_comparison_lte(self, other):
		return Number(int(self.elements <= other.elements)), None

	def get_comparison_gte(self, other):
		return Number(int(self.elements >= other.elements)), None

	def anded_by(self, other):
		return (self if other.is_true() else Number(0)), None

	def ored_by(self, other):
		return (self if self.is_true() else other), None

	def __eq__(self, other):
		try:
			return self.elements == other.elements
		except:
			return False

	def copy(self):
		return List(self.elements).set_pos(self.pos_start, self.pos_end).set_context(self.context)
		
	def __str__(self):
		return f'[{", ".join([str(x) for x in self.elements])}]'
	
	def __repr__(self):
		return str(self)

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"
		self.has_star_args = False
	
	def star_args(self):
		self.has_star_args = True
		return self
	
	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args, has_star_args=False):
		res = RTResult()
		default_args = sum(isinstance(i, tuple) for i in arg_names)

		if len(args) > len(arg_names) and not has_star_args:
			return res.failure(RunTimeError(
				self.pos_start,
         		self.pos_end,
				f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
				self.context
			))
		
		if len(args) < len(arg_names)-default_args-(1 if has_star_args else 0):
			return res.failure(RunTimeError(
				self.pos_start,
         		self.pos_end,
				f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
				self.context
			))
		
		return res.success(NoneType())

	def populate_args(self, arg_names, args, exec_ctx, has_star_args=False):
		n = 1 if has_star_args else 0
		for i in range(len(arg_names)-n):
			arg_name = arg_names[i]
			if type(arg_name) == tuple:
				default_value = arg_name[1]
				arg_name = arg_name[0]
			try:
				arg_value = args[i]
			except:
				arg_value = default_value
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)
		if has_star_args:
			dollar_values = []
			for i in range(len(arg_names)-1, len(args)):
				dollar_values.append(args[i])
			dollar_values = List(dollar_values)
			dollar_values.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_names[-1], dollar_values)



	def check_and_populate_args(self, arg_names, args, exec_ctx, has_star_args=False):
		res = RTResult()
		res.register(self.check_args(arg_names, args, has_star_args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx, has_star_args)
		return res.success(NoneType())

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return, has_star_args):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return
		self.has_star_args = has_star_args

	def execute(self, args):
		res = RTResult()
		interpreter = Interpreter()

		new_context = self.generate_new_context()
		res.register(self.check_and_populate_args(self.arg_names, args, new_context, self.has_star_args))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, new_context))
		if res.should_return() and res.func_return_val == None: return res
		return_val = (value if self.should_auto_return else None) or res.func_return_val or NoneType()
		return res.success(return_val)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return, self.has_star_args)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __str__(self):
		return f"<function {self.name} at {hex(id(self))}>"

	def __repr__(self):
		return str(self)

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = f"execute_{self.name}"
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx, self.has_star_args))
		if res.error: return res 

		return_value = res.register(method(exec_ctx))
		if res.error: return res
		return res.success(return_value)

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.has_star_args = self.has_star_args
		return copy

	def __str__(self):
		return f"<Built in function {self.name} at {hex(id(self))}>"

	def __repr__(self):
		return str(self)

	def no_visit_method(self):
		raise Exception(f"No execute_{self.name} method defined")

	def execute_print(self, exec_ctx):
		first = str(exec_ctx.symbol_table.get("value"))
		others = exec_ctx.symbol_table.get("args")
		others.elements.insert(0, first)
		if others.elements == []:
			print()
		else:
			print(*others.elements)

		return RTResult().success(NoneType().set_context(exec_ctx))
	execute_print.arg_names = [("value", String("")), "args"]

	def execute_print_ret(self, exec_ctx):
		val = str(exec_ctx.symbol_table.get("value"))
		return RTResult().success(String(val))
	execute_print_ret.arg_names = ["value"]

	def execute_input(self, exec_ctx):
		import re
		prompt = "TruBasic > "
		prompt = prompt + (str(exec_ctx.symbol_table.get("str")))
		text = input(prompt)
		return RTResult().success(String(text).set_context(exec_ctx).set_pos(exec_ctx.parent_entry_pos, exec_ctx.parent_entry_pos))
	execute_input.arg_names = [("str", String(""))]

	def execute_input_int(self, exec_ctx):
		import re
		prompt = str(exec_ctx.symbol_table.get("str"))
		while True:
			try:
				text = int(input(prompt or ""))
				break
			except:
				print(f"{text} is not a number. Try Again")
		return RTResult().success(Number(text))
	execute_input_int.arg_names = ["str"]

	def execute_clear(self, exec_ctx):
		os.system('cls' if os.name=='nt' else 'clear')
		return RTResult().success(NoneType())
	execute_clear.arg_names = []

	def execute_int(self, exec_ctx):
		val = exec_ctx.symbol_table.get("val")
		if not type(val) in (String, Number):
			return RTResult().failure(RunTimeError(
				val.pos_start,
				val.pos_end,
				"Value must Be Number or String",
				exec_ctx
			))
		else:
			try:
				return RTResult().success(Number(int(val.value)))
			except:
				return RTResult().failure(RunTimeError(
				val.pos_start or 0,
				val.pos_end or 0,
				f"Invalid literal for int() with base 10: {val}",
				exec_ctx
			))

	execute_int.arg_names = ["val"]

	def execute_float(self, exec_ctx):
		val = exec_ctx.symbol_table.get("val")
		if not type(val) in (String, Number):
			return RTResult().failure(RunTimeError(
				val.pos_start,
				val.pos_end,
				"Value must Be Number or String",
				exec_ctx
			))
		else:
			try:
				return RTResult().success(Number(float(val.value)))
			except:
				return RTResult().failure(RunTimeError(
				val.pos_start,
				val.pos_end,
				f"Invalid literal for float() with base 10: {val}",
				exec_ctx
			))
	execute_float.arg_names = ["val"]

	def execute_list(self, exec_ctx):
		val = exec_ctx.symbol_table.get("val")
		try:
			result = [String(i) for i in val.value]
			return RTResult().success(List(result))
		except:
			if type(val) == List:
				return RTResult().success(val)
			return RTResult().failure(
				RunTimeError(
					val.pos_start,
					val.pos_end,
					f"Type '{type(val).__name__}' is not iterable",
					exec_ctx
				)
			)
	execute_list.arg_names = [("val", List([]))]

	def execute_run(self, exec_ctx):
		filename = (exec_ctx.symbol_table.get("fn"))
		if not isinstance(filename, String):
			return RTResult().failure(
				RunTimeError(
        			self.pos_start, 
					self.pos_end,
        			"Filename must be string",
        			exec_ctx
      		)
		)
		import basic
		try:
			with open(str(filename), "r+") as f:
				text = f.read()
		except Exception as e:
			return RTResult().failure(
				RunTimeError(
					self.pos_start,
					self.pos_end,
					f"Failed to load script \"{filename}\"\n" + str(e),
					exec_ctx
				)
			)
		
		_, error = basic.run(filename, text)
		
		if error:
			return RTResult().failure(
				RunTimeError(
					self.pos_start,
					self.pos_end,
					f"Failed to finish executing script \"{filename}\"\n" + str(error),
					exec_ctx
				)
			)
		return RTResult().success(NoneType())
		
	execute_run.arg_names = ["fn"]

	def execute_len(self, exec_ctx):
		lst = exec_ctx.symbol_table.get("list")
		if isinstance(lst, List):
			return RTResult().success(Number(len(lst.elements)))
		elif isinstance(lst, String):
			return RTResult().success(Number(len(lst.value)))
		else:
			return RTResult().failure(
				RunTimeError(
					lst.pos_start,
					lst.pos_end,
					f"{lst} is not Iterable",
					exec_ctx
				)
			)
	execute_len.arg_names = ["list"]

	def execute_str(self, exec_ctx):
		item = exec_ctx.symbol_table.get("item")
		try:
			return RTResult().success(String(str(item)))
		except:
			pass
		if isinstance(item, Number):
			return RTResult().success(String(str(item.value)))
		elif isinstance(item, List):
			return RTResult().success(String(str(item.elements)))
		elif isinstance(item, String):
			return RTResult().success(item)
		else:
			return RTResult().success(NoneType())
	execute_str.arg_names = [("item", String(""))]

	def execute_reverse(self, exec_ctx):
		val = exec_ctx.symbol_table.get("val")
		if isinstance(val, List):
			return RTResult().success(List(val.elements[::-1]))
		elif isinstance(val, String):
			return RTResult().success(String((val.value[::-1])))
		else:
			return RTResult().failure(
				RunTimeError(
					val.pos_start,
					val.pos_end,
					f"type '{type(val).__name__}' is not iterable",
					exec_ctx
				)
			)
	execute_reverse.arg_names = ["val"]

##############################################################################################
# RUNTIME RESULT
##############################################################################################

class RTResult:
	def __init__(self):
		self.reset()

	def reset(self):
		self.value = None
		self.error = None
		self.func_return_val = None
		self.loop_should_continue = None
		self.loop_should_break = None

	def register(self, res):
		if res.error: self.error = res.error
		self.func_return_val = res.func_return_val
		self.loop_should_break = res.loop_should_break
		self.loop_should_continue = res.loop_should_continue
		return res.value
	
	def success(self, val):
		self.reset()
		self.value = val
		return self

	def success_return(self, return_val):
		self.reset()
		self.func_return_val = return_val
		return self

	def success_continue(self):
		self.reset()
		self.loop_should_continue = True
		return self

	def success_break(self):
		self.reset()
		self.loop_should_break = True
		return self

	def failure(self, error):
		self.reset()
		self.error = error
		return self

	def should_return(self):
		return (
			self.error or
			self.func_return_val or
			self.loop_should_continue or
			self.loop_should_break
		)
		
##############################################################################################
# INTERPRETER
##############################################################################################

class Interpreter:
	def visit(self, node, context):
		method_name = f"visit_{type(node).__name__}"
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f"No visit_{type(node).__name__} method defined")

	def visit_NumberNode(self, node, context):
		return RTResult().success(Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end))

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		error = None
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res
		if node.op_token.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_token.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_token.type == TT_DIV:
			result, error = left.dived_by(right)
		elif node.op_token.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.op_token.type == TT_POW:
			result, error = left.raised_to(right)
		elif node.op_token.type == TT_MOD:
			result, error = left.modded_to(right)
		elif node.op_token.type == TT_FDIV:
			result, error = left.floor_dived_to(right)
		elif node.op_token.type == TT_EE:
			result, error = left.get_comparison_eq(right)
			if result: result.bool = True
		elif node.op_token.type == TT_NE:
			result, error = left.get_comparison_ne(right)
			if result: result.bool = True
		elif node.op_token.type == TT_LT:
			result, error = left.get_comparison_lt(right)
			if result: result.bool = True
		elif node.op_token.type == TT_GT:
			result, error = left.get_comparison_gt(right)
			if result: result.bool = True
		elif node.op_token.type == TT_LTE:
			result, error = left.get_comparison_lte(right)
			if result: result.bool = True
		elif node.op_token.type == TT_GTE:
			result, error = left.get_comparison_gte(right)
			if result: result.bool = True
		elif node.op_token.matches(TT_KEYWORD, 'and'):
			result, error = left.anded_by(right)
			if result: result.bool = True
		elif node.op_token.matches(TT_KEYWORD, 'or'):
			result, error = left.ored_by(right)
			if result: result.bool = True

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end))

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		num = res.register(self.visit(node.node, context))
		if res.should_return(): return res
		error = None
		if node.op_token.type == TT_MINUS:
			num, error = num.multed_by(Number(-1))
		elif node.op_token.matches(TT_KEYWORD, 'not'):
			num, error = num.notted()
		
		if error:
			return res.failure(error)
		else:
			return res.success(num.set_pos(node.pos_start, node.pos_end))\

	def visit_NoneNode(self, node, context):
		return RTResult().success(NoneType().set_pos(node.pos_start, node.pos_end).set_context(context))

	def visit_VarAssignNode(self, node, context, reassign=False):
		res = RTResult()
		var_name = node.var_name_token.value
		if var_name in CONSTANTS:
			return res.failure(
				InvalidSyntaxError(
					node.pos_start,
					node.pos_end,
					"Can't assign to keyword",
				)
			)

		if reassign:
			current = context.symbol_table.get(var_name)

			if current == None:
				return res.failure(RunTimeError(
					node.pos_start,
					node.pos_end,
					f"'{var_name}' is not defined",
					context
				))
		
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res
		
		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_VarReAssignNode(self, node, context):
		return self.visit_VarAssignNode(node, context, True)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)

		if value == None:
			return res.failure(RunTimeError(
				node.pos_start,
				node.pos_end,
				f"'{var_name}' is not defined",
				context
			))
		
		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)

	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr, should_return_none in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res 
			
			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(NoneType() if should_return_none else expr_value)

		if node.else_case:
			expr, should_return_none = node.else_case
			else_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(NoneType() if should_return_none else else_value)

		return res.success(NoneType())

	def visit_ForNode(self, node, context):
		res = RTResult()
		elements = []

		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Number(1)

		i = start_value.value

		if step_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value

		result = None

		while condition():
			context.symbol_table.set(node.var_name_token.value, Number(i))
			i += step_value.value

			result = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_break == False and res.loop_should_continue == False: return res

			if res.loop_should_continue:
				continue
			if res.loop_should_break:
				break
			elements.append(result)

		return res.success(
			NoneType() if node.should_return_none else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			result = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_break == False and res.loop_should_continue == False: return res

			if res.loop_should_continue:
				continue
			if res.loop_should_break:
				break
			elements.append(result)

		return res.success(
			NoneType() if node.should_return_none else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_FuncDefNode(self, node, context):
		res = RTResult()

		func_name = node.var_name_token.value if node.var_name_token else None
		body_node = node.body_node
		arg_names = []
		for arg_name in node.arg_name_tokens:
			if type(arg_name) == tuple:
				def_val = res.register(self.visit(arg_name[1], context))
				if res.should_return(): return res

				arg_names.append((arg_name[0].value, def_val))
			else:
				arg_names.append(arg_name.value)
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return, node.has_star_args).set_context(context).set_pos(node.pos_start, node.pos_end)

		if node.var_name_token:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RTResult()

		args = []
		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.should_return(): return res

		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
		return res.success(return_value)

	def visit_StringNode(self, node, context):
		return RTResult().success(
			String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
			)

	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_ReturnNode(self, node, context):
		res = RTResult()

		if node.return_node: 
			value = res.register(self.visit(node.return_node, context))
			if res.should_return(): return res
		else:
			value = NoneType
		
		return res.success_return(value)
	
	def visit_ContinueNode(self, node, context):
		return RTResult().success_continue()

	def visit_BreakNode(self, node, context):
		return RTResult().success_break()