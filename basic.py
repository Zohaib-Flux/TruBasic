##############################################################################################
# IMPORTS
##############################################################################################

import tkinter as tk
import string
import math
from Lexer import Lexer, Error
from Parser import Parser
import Interpreter
Interpreter, SymbolTable, Context, Number, NoneType, BuiltInFunction = Interpreter.Interpreter,  Interpreter.SymbolTable,  Interpreter.Context,  Interpreter.Number,  Interpreter.NoneType,  Interpreter.BuiltInFunction

##############################################################################################
# RUN
##############################################################################################

global_symbol_table = SymbolTable()

# Predefined global variables
global_symbol_table.set("True", Number.true)
global_symbol_table.set("False", Number.false)
global_symbol_table.set("Null", NoneType())
global_symbol_table.set("PI", Number(math.pi))
global_symbol_table.set("TWO_PI", Number(math.pi*2))
global_symbol_table.set("HALF_PI", Number(math.pi/2))
global_symbol_table.set("Infinity", Number(math.inf))
global_symbol_table.set("None", NoneType())
global_symbol_table.set("printer", BuiltInFunction("print").star_args())
global_symbol_table.set("Printer", BuiltInFunction("print").star_args())
global_symbol_table.set("input", BuiltInFunction("input"))
global_symbol_table.set("Input", BuiltInFunction("input"))
global_symbol_table.set("clear", BuiltInFunction("clear"))
global_symbol_table.set("int", BuiltInFunction("int"))
global_symbol_table.set("float", BuiltInFunction("float"))
global_symbol_table.set("Float", BuiltInFunction("float"))
global_symbol_table.set("list", BuiltInFunction("list"))
global_symbol_table.set("run", BuiltInFunction("run"))
global_symbol_table.set("len", BuiltInFunction("len"))
global_symbol_table.set("str", BuiltInFunction("str"))
global_symbol_table.set("reverse", BuiltInFunction("reverse"))
global_symbol_table.set("class", BuiltInFunction("class"))
global_symbol_table.set("def", BuiltInFunction("def"))
global_symbol_table.set("if", BuiltInFunction("if"))
global_symbol_table.set("else", BuiltInFunction("else"))
global_symbol_table.set("root", BuiltInFunction("root"))




def run(fn: str, text: str) -> (float, Error):
	# generate tokens from source with lexical analysis
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error

	if len(tokens) <= 1:
		return None, None

	# generate an abstract syntax tree by parsing the text, also known as syntax analysis
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# interpret the ast
	interpreter = Interpreter()
	context = Context("<Program>")
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
