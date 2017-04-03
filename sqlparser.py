import re
from tree import Tree

class Associations:
    ASSOC_NONE, ASSOC_LEFT, ASSOC_RIGHT = range(3)

class Node:
        def __init__(self, value):
                self._value = value
                self._left = None
                self._right = None

        def getValue(self):
                return self._value
        def setValue(self, value):
                self._value = value
        def getRightChild(self):
                return self._right
        def rightChild(self, right_child):
                self._right = right_child
        def getLeftChild(self):
                return self._left
        def leftChild(self, left_child):
                self._left = left_child
		def __str__(self):
				print self._value
				return self._value

class Stack:
		def __init__(self):
			self.__storage = []

		def isEmpty(self):
			return len(self.__storage) == 0

		def push(self,p):
			self.__storage.append(p)

		def pop(self):
			return self.__storage.pop()

		def peek(self):
			return self.__storage[len(self.__storage)-1]
		
		def __str__(self):			
			return str(self.__storage)
			
operators = {
  'OR':{'op':'OR','prec':11, 'assoc': Associations.ASSOC_LEFT,'unary':1},
  'AND':{'op':'AND','prec':10, 'assoc': Associations.ASSOC_LEFT,'unary':1},
  '=':{'op':'=','prec':9, 'assoc': Associations.ASSOC_RIGHT,'unary':1},
  '!=':{'op':'!', 'prec':9, 'assoc': Associations.ASSOC_RIGHT,'unary':1},
  '^':{'op':'^', 'prec':1, 'assoc': Associations.ASSOC_RIGHT,'unary':0},
  '*':{'op':'*', 'prec':3, 'assoc': Associations.ASSOC_LEFT,'unary':0},
  '<':{'op':'<', 'prec':5,'assoc': Associations.ASSOC_LEFT,'unary':0},
  '>':{'op':'>', 'prec':5, 'assoc': Associations.ASSOC_LEFT,'unary':0},
  '<=':{'op':'<=', 'prec':5, 'assoc': Associations.ASSOC_LEFT,'unary':0},
  '>=':{'op': '>=', 'prec':5, 'assoc':Associations.ASSOC_LEFT,'unary':0},
  '/':{'op':'/','prec':3, 'assoc': Associations.ASSOC_LEFT,'unary':0},
  '%':{'op': '%', 'prec':3, 'assoc':Associations.ASSOC_LEFT,'unary':0},
  '+':{'op':'+', 'prec':4, 'assoc': Associations.ASSOC_LEFT,'unary':0},
  '-':{'op':'-','prec':4,'assoc': Associations.ASSOC_LEFT,'unary':0},
  '(':{'op':'(','prec':0,'assoc': Associations.ASSOC_NONE,'unary':0},
  ')':{'op':')', 'prec':0, 'assoc': Associations.ASSOC_NONE,'unary':0}
}

#HELPER METHODS
def extractPart(start_keyword, end_keyword, query):
        starting_index = query.find(start_keyword) + len(start_keyword)
        ending_index = query.find(end_keyword)
        return query[starting_index:ending_index]

def isLogicalOperator(operator):
        if operator == '>=' or operator == '<=' or operator == '>' or operator == '<' or operator == '!=' or operator == '=':
                return True
        return False

def isBinaryOperator(operator):
        if operator == 'AND' or operator == 'OR':
                return True;
        return False;
		
def tokenizeIdentifier(tokens):
        return re.findall(r"[\w']+", tokens)
		
		
# EVALUATION
def evaluateExpression(root):
        if isBinaryOperator(root.getValue()):
                left_result = None
                right_result = None
                if root.getLeftChild() != None and root.getRightChild() != None:
                        left_result = evaluateExpression(root.getLeftChild())
                        right_result = evaluateExpression(root.getRightChild())

                if root.getValue() == 'AND':
                        if not left_result or not right_result:
                                return False
                        else:
                                return True

                elif root.getValue() == 'OR':
                        if left_result or right_result:
                                return True
                        else:
                                return False
        else:
                print "evaluate sub-expression"


def buildExpressionTree(expression):
        operandsStack = Stack()
        target = operandsStack
        result = Stack()
        for token in expression.split(' '):
                node = Node(token)
                if isBinaryOperator(token):
                        target = result
                elif isLogicalOperator(token):
                        target = operandsStack
                else:
                        operandsStack.push(node)
                        continue

                operand1 = target.pop()
                operand2 = target.pop()
                node.rightChild(operand1)
                node.leftChild(operand2)
                result.push(node)
        return result.peek()
		
def buildExpressionGenTree(expression):
        operandsStack = Stack()
        target = operandsStack
        result = []
        for token in expression.split(' '):                
                print "Token: " + token
                if isBinaryOperator(token):
                        target = result
                elif isLogicalOperator(token):
                        target = operandsStack
                else:
                        operandsStack.push(Tree(token))
                        continue				
                operand1 = target.pop()
                operand2 = target.pop()
                node = Tree(token, operand2, operand1)                
                result.append(node)
        return result[0]



def infixToPostfix(infixexpr):
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()
    inLeft = False

    for token in tokenList:
        print "Token ->" + token        
        if token not in operators:		
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
            inLeft = True
        elif token == ')':
            inLeft = False
            topToken = opStack.pop()
            while (not opStack.isEmpty()) and topToken != '(':                
                postfixList.append(topToken)
                topToken = opStack.pop()
        elif inLeft:
            temp_list = []
            if(operators[token]['prec'] > operators[opStack.peek()]['prec']):
                while not opStack.isEmpty() and operators[token]['prec'] > operators[opStack.peek()]['prec']:
				    temp_list.append(opStack.pop())
                opStack.push(token)
                for item in temp_list:
                    opStack.push(item)
            else:
                opStack.push(token)
        elif operators[token]['assoc'] == Associations.ASSOC_RIGHT:
                while (not opStack.isEmpty()) and (operators[token]['prec'] > operators[opStack.peek()]['prec']):
                   print "ASSOC_RIGHT POP" + opStack.peek()
                   postfixList.append(opStack.pop())
                opStack.push(token)
        elif operators[token]['assoc'] == Associations.ASSOC_LEFT:
                while (not opStack.isEmpty()) and (operators[token]['prec'] >= operators[opStack.peek()]['prec']):
                    postfixList.append(opStack.pop())
                opStack.push(token)
        else:
            while (not opStack.isEmpty()) and \
               (operators[opStack.peek()]['prec'] >= operators[token]['prec']):
                  postfixList.append(opStack.pop())
            opStack.push(token)    
        print opStack

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

	
def tokenizeKeywordSelect(query):
        target_column_tokens = extractPart("SELECT", "FROM", query)
        conditions = None
        if query.find("WHERE") != -1:
                table_tokens = extractPart("FROM", "WHERE", query)
                condition_tokens = extractPart("WHERE", ";", query)
                conditions = infixToPostfix(condition_tokens)
                print "Printing Conditions"
                print conditions
        else:
                table_tokens = extractPart("FROM", ";", query)

        target_columns = tokenizeIdentifier(target_column_tokens)
        print "Printing Columns"
        print target_columns
        tables = tokenizeIdentifier(table_tokens)
        print "Printing Tables"
        print tables

        if conditions != None:
                #expression_tree = buildExpressionTree(conditions)
				return buildExpressionGenTree(conditions)

				
class Parser(object):	
    def __init__(self, tree=None):
        self.tree = tree

    def execute(self, query):
        return tokenizeKeywordSelect(query)