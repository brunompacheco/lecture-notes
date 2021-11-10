(define (problem problem2) (:domain jezero)
(:objects 
	r1 r2 - robot
  l0 l1 l2 l3 l4 l5 l6 - place
)

(:init
  ; all paths between places
  (path l3 l0)
  (path l3 l1)
  (path l1 l2)
  (path l2 l0)
  (path l2 l4)
  (path l2 l5)
  (path l5 l0)
  (path l0 l6)
  (path l6 l3)

  ; location of ship and trash site
  (is_ship l1)
  (is_trash l4)

  ; robots always start at a place and (usually) empty
  (at r1 l5)
  (busy l5)
  (empty r1)
  (can_soil r1)

  (at r2 l0)
  (busy l0)
  (empty r2)
  (can_rock r2)

  ; which paths the robots can traverse
  (can_path r1 l3 l0)
  (can_path r1 l2 l0)
  (can_path r1 l5 l0)
  (can_path r1 l6 l3)
  (can_path r2 l3 l0)
  (can_path r2 l2 l0)

  ; they can also go to the trash place
  (can_path r1 l2 l4)
  (can_path r2 l2 l4)
)

(:goal (and
    (soil_researched l5)
    (soil_researched l6)
    (rock_researched l0)
    (rock_researched l3)
))

)
