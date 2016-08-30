import sys

from ..eval.PLambdaException import PLambdaException

import State


class Continuation(object):


    def __init__(self, exp=None, args=None, env=None, k=None):
        self.exp = exp
        self.args = args
        if self.args is not None:
            self.vals = [ None ] * len(args)
        self.n = 0
        self.env = env
        self.k = k
        self.excep = None
        if self.exp is not None:
            self.msg = '{0} :'.format(exp.spine[0])


    def ret(self, state):
        """ ret is deals with the exceptional case. 
        
        By default, thrown exceptions propagated up the continuation
        chain.  Continuations that handle exceptions (TryCont and
        TopCont, currently) do so by overriding `ret'.
        """
        if self.excep is not None:
            #FIXME: info() gets passed in to the EvaluateError
            self.k.excep = excep
            state.k = self.k
        else:
            self.handleReturn(state)


    def handleReturn(self, state):
        pass


    def info(self):
        """FIXME: can write this soon.
        """
        pass

    

class TopCont(Continuation):

    def __init__(self):
        Continuation.__init__(self)

    def cont(self, state):
        raise PLambdaException("Calling cont on a TopCont is forbidden")


    def ret(self, state):
        if self.excep is not None:
            sys.stderr.write("FIXME: Debugger.handle(excep)\n")

        state.tag = State.DONE

            
    def handleReturn(self, state):
        pass

    
        
class IfCont(Continuation):


    def __init__(self, exp, args, env, k):
        Continuation.__init__(self, exp, args, env, k)

    def cont(self, state):
        state.tag = State.EVAL
        state.exp = self.args[0]
        state.env = self.env

    def handleReturn(self, state):
        if not isinstance(state.val, bool):
            msg = '{0} is not a boolean in conditional {1}'
            self.k.excep = PLambdaException(msg.format(state.val, self.exp.spine[0].location))
            state.k = self.k
            return
        elif state.val:
            state.tag = State.EVAL
            state.exp = self.args[1]
            state.env = self.env
        elif  len(self.args) == 3:
            state.tag = State.EVAL
            state.exp = self.args[2]
            state.env = self.env
        else:
            state.tag = State.RETURN
            state.val = None

        state.k = self.k
        
    