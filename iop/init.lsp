(define hello
  (concat
   "\n"
   ";;;Editing is Futile: autogenerated by 'init.lsp'"
   "\n"
   "(import 'sys')"
   "\n"
   "(invoke sys.stderr 'write' 'hello world from {0}\\n')"
   "\n"
   )
  )

(define debug (boolean False))

(import 'sys')
(define logmsg (msg)
  (if debug 
      (invoke  sys.stderr 'write' msg)
    )
  )


(define clone_count (int 2))

(define plambda_clones (mklist))
(define plambda_population clone_count)

(define maude_clones (mklist))
(define maude_population clone_count)

(import 'plambda.actors.actorlib')
(define make_cloner (prefix executable args clones count)
  (lambda (sender message)
    (let ((tokens (invoke message 'split')))
      (if (> (apply len tokens) (int 1))
	  (let ((verb (get tokens (int 0)))
		(noun (get tokens (int 1))))
	    (if (and (== verb 'startOK') (invoke noun 'startswith' prefix))
		(seq
		 (invoke clones 'append' noun)
		 (if (< (apply len clones) count)
		     (seq
		      (apply logmsg (concat 'Handled ' noun ' more coming\n'))
		      (apply plambda.actors.actorlib.send
			     'system'
			     'plambda'
			     (concat 'start ' (concat prefix (apply len clones)) ' ' executable ' ' args))
		      )
		   (seq (apply logmsg (concat 'Handled ' noun ' enough already\n'))
			(apply init_clones clones prefix)
			)
		   )
		 (boolean true)
		 )
	      (seq
	       (boolean false)
	       )
	      )
	    )
	)
      )
    )
  )


(import 'plambda.util.Util')
(define init_clones (clones prefix)
  (if (== prefix 'plambda')
      (seq
       (for clone clones
	    (let ((loadfile (concat 'hello_' clone '.lsp'))
		  (contents (invoke hello 'format' clone)))
	      (apply plambda.util.Util.string2File  contents loadfile (boolean False))
	      (apply plambda.actors.actorlib.send clone 'plambda' (concat '(load "' loadfile '")'))
	      )
	    )
       (apply plambda.actors.actorlib.send 'system' 'plambda' 'start maude0 iop_maude_wrapper basura')
       )
    )
  (if (== prefix 'maude')
      (for clone clones
	   (seq 
	    (apply logmsg (concat 'clone: ' clone ' with prefix ' prefix '\n'))
	    )
	   )
    )
  )


(define catchall (lambda (sender message)  (invoke  sys.stderr 'write' (concat 'Handled: ' message ' from ' sender '\n'))))

(import 'plambda.actors.pyactor')
(apply plambda.actors.pyactor.add_handler (apply make_cloner 'plambda' 'pyactor' 'anonymous' plambda_clones plambda_population))
(apply plambda.actors.pyactor.add_handler (apply make_cloner 'maude' 'iop_maude_wrapper' 'anonymous' maude_clones maude_population))

;;start the ball rolling
(apply plambda.actors.actorlib.send 'system' 'plambda' 'start plambda pyactor')

