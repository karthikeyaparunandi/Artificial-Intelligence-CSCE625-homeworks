;;; P. Karthikeya Sharma
;;; AI course HW - 1
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; define while loop
(define-syntax (while stx)
  (syntax-case stx ()
      ((_ condition expression ...)
       #`(do ()
           ((not condition))
           expression
           ...))))

; define incremental function by 1
(define-syntax incf
  (syntax-rules ()
    ((_ x)   (begin (set! x (+ x 1)) x))
    ((_ x n) (begin (set! x (+ x n)) x))))

; define function 'f' as given
(define (f x)
  (+ (* x 2) 1))


; define function 'g' as given
(define (g x)
  (+ (* x 3) 1))

; constructs the tree using lazy evaluation
(define (tree value depth depth_limit)
 (list value depth (delay (tree (f value) (+ depth 1) depth_limit))  (delay (tree (g value) (+ depth 1) depth_limit)))
)

;returns the left child 
(define (left_child_output node)
 (force (car (cdr (cdr node))))
) 

; returns the right child
(define (right_child_output node)
  (force (car (cdr (cdr (cdr node)))))
)

; returns a list of both the children
(define (children_nodes_output parent_node)
  (list (left_child_output parent_node) (right_child_output parent_node)) 
)

; returns the value of the node from the node-list
(define (node_value node)
 (car node)
)


; The Breadth first search implementation
(define (BFS parent_node given_num)

 (define d 0)
 (define queue parent_node)

 (while (< d 40000)

  (cond [(= (node_value parent_node) given_num) (begin (set! d 410000) (display "SUCCESS! A SOLUTION FOUND WITH MINIMAL FUNCTION APPLICATIONS!\n")) ]
   [else 
     (begin
       (cond [(= d 0) (set! queue (list (children_nodes_output parent_node) ) )]
       [else (set! queue (append queue (children_nodes_output parent_node) ) )])
      
      (cond [(= d 0) (set! parent_node (car (car queue)))] [else (set! parent_node (car queue))])
     (cond [(= d 0) (set! queue (cdr (car queue)))] [else (set! queue (cdr queue))])
  
     ) 
   ]
  )
   
   (incf d) ; increment by 1
 )
 (if (= d 39999) (display "NO SOLUTION EXISTS!"))
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Give any number to the variable 'given_number' and the it'll result in corresponding solution (if there exists)

(define initial_node (tree 1 0 10))   ; define a tree with an initial value
(define given_number 1022)		      ; take an arbitrary number for testing
(BFS initial_node given_number)       ; finds the number using least no. of function applications to check the possibility



