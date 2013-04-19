(import grid)
(import-from functools reduce)
(import-from operator add)


(def *world* (grid.Torus 10 10))


(defun sum (ns)
  (reduce add ns))


(defun set! (world x y value)
  (setv (get world (, x y)) value))


(defun get! (world x y)
  (get *world* (, x y)))


(defun neighbours (world x y)
  (sum (list-comp
        (get! world (+ x dx) (+ y dy))
         (dx [-1 0 1]
          dy [-1 0 1])
        (!= (, (+ x dx) (+ y dy)) (, x y)))))


(defun step (world)
  (let ((new-world (.copy grid.Torus world)))
    (for (x (range new-world.width))
         (for (y (range new-world.height))
              (let ((cell (get! new-world x y))
                    (ns (neighbours world x y)))
                (if (= cell 1)
                    (cond ((< ns 2) (set! new-world x y 0))
                          ((or (= ns 2) (= ns 3)) (set! new-world x y 1))
                          ((> ns 3) (set! new-world x y 0)))
                    (cond ((= ns 3) (set! new-world x y 1))
                          (True (set! new-world x y 0)))))))
    new-world))



;; Create a glider...
(set! *world* 4 2 1)
(set! *world* 5 3 1)
(set! *world* 3 4 1)
(set! *world* 4 4 1)
(set! *world* 5 4 1)

;; Cycle through once...
(for (_ (range 5))
     (.pprint grid.Torus *world*)
     (setv *world* (step *world*))
     (print))
