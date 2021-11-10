(define (problem problem1) (:domain jezero)
(:objects 
	r1 - robot
  l0 l1 l2 l3 l4 - place
)

(:init
  ; all paths between places
  (path l3 l0)
  (path l3 l1)
  (path l1 l2)
  (path l2 l0)
  (path l2 l4)

  ; location of ship and trash site
  (is_ship l1)
  (is_trash l4)

  ; robots always start at a place and (usually) empty
  (at r1 l3)
  (busy l3)
  (can_soil r1)
  (can_rock r1)
  (empty r1)

  ; which paths the robots can traverse
  (can_path r1 l3 l0)
  (can_path r1 l3 l1)
  (can_path r1 l1 l2)
  (can_path r1 l2 l0)
  (can_path r1 l2 l4)
)

(:goal (and
    (soil_researched l2)
    (rock_researched l3)
))

)
