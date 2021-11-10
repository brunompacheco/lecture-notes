(define (domain jezero)
(:requirements :typing :disjunctive-preconditions :negative-preconditions)

(:types
  place robot
)

(:predicates

  (empty ?r - robot)
  (can_soil ?r - robot) ; robot is capable of collecting/analyzing soil
  (can_rock ?r - robot) ; robot is capable of collecting/analyzing rocks

  (busy ?p - place) ; if a place is busy, it shouldn't be possible to enter it
  (is_ship ?p - place) ; ship is located at that place
  (is_trash ?p - place) ; trash site is located at that place

  (path ?p1 - place ?p2 - place) ; it is possible to traverse from p1 to p2 

  (can_path ?r - robot ?p1 - place ?p2 - place) ; not all robots are capable of going through all paths
  (has_soil_from ?r - robot ?p - place) ; it is essential to keep track of this for the report later on
  (has_rock_from ?r - robot ?p - place) ; same as above

  (at ?r - robot ?p - place)

  (at_trash ?r - robot) ; the trash site is a special place where one can fit as many robots as desired

  ; keep track of the goals
  (soil_researched ?p - place)
  (rock_researched ?p - place)

)

(:action move
    ; move a robot from a place to another
    :parameters (
      ?r - robot
      ?from - place
      ?to - place
    )
    :precondition (and
      (at ?r ?from)
      (not (busy ?to))
      (or
        (path ?from ?to)
        (path ?to ?from)
      )
      (or
        (can_path ?r ?from ?to)
        (can_path ?r ?to ?from)
      )
    )
    :effect (and
      (not (at ?r ?from))
      (not (busy ?from))
      (at ?r ?to)
      (busy ?to)
    )
)

(:action pick-soil
    ; take a soil sample from a given place
    :parameters (
      ?r - robot
      ?p - place
    )
    :precondition (and
      (empty ?r)
      (at ?r ?p)
      (can_soil ?r)
    )
    :effect (and
      (not (empty ?r))
      (has_soil_from ?r ?p)
    )
)

(:action pick-rock
    ; take a rock sample from a given place
    :parameters (
      ?r - robot
      ?p - place
    )
    :precondition (and
      (empty ?r)
      (at ?r ?p)
      (can_rock ?r)
    )
    :effect
    (and
      (not (empty ?r))
      (has_rock_from ?r ?p)
    )
)

(:action enter-trash
    ; remove robot from place where the trash site is and makes it possible for
    ; it to discard the sample
    :parameters (
      ?r - robot
      ?p - place
    )
    :precondition (and
      (at ?r ?p)
      (is_trash ?p)
    )
    :effect (and
      (not (at ?r ?p))
      (at_trash ?r)
    )
)

(:action exit-trash
    ; move the robot back to the place `p` where the trash site is located
    :parameters (
      ?r - robot
      ?p - place
    )
    :precondition (and
      (is_trash ?p)
      (at_trash ?r)
    )
    :effect (and
      (at ?r ?p)
      (not (at_trash ?r))
    )
)

(:action discard-rock
    ; empty the robot
    :parameters (
      ?r - robot
      ?p - place ; place from where the sample was obtained
    )
    :precondition (and
      (at_trash ?r)
      (not (empty ?r))
      (has_rock_from ?r ?p)
    )
    :effect (and
      (empty ?r)
      (not (has_rock_from ?r ?p))
    )
)

(:action discard-soil
    ; empty the robot
    :parameters (
      ?r - robot
      ?p - place ; place from where the sample was obtained
    )
    :precondition (and
      (at_trash ?r)
      (not (empty ?r))
      (has_soil_from ?r ?p)
    )
    :effect (and
      (empty ?r)
      (not (has_soil_from ?r ?p))
    )
)

(:action report-rock
    ; send information from rock sample collected
    :parameters (
      ?r - robot
      ?curr_p - place ; place where the robot is
      ?ship - place ; ship's place
      ?report_p - place ; place from where the sample was collected
    )
    :precondition (and
      (at ?r ?curr_p)
      (is_ship ?ship)
      (or
        (path ?curr_p ?ship)
        (path ?ship ?curr_p)
        ; I assume that if the robot is at the ship's place, then it can also
        ; send reports
        (at ?r ?ship) ; that is, ?ship == ?curr_p
      )
      (has_rock_from ?r ?report_p)
    )
    :effect (and
      (rock_researched ?report_p)
    )
)

(:action report-soil
    ; send information from soil sample collected
    :parameters (
      ?r - robot
      ?curr_p - place ; place where the robot is
      ?ship - place ; ship's place
      ?report_p - place ; place from where the sample was collected
    )
    :precondition (and
      (at ?r ?curr_p)
      (is_ship ?ship)
      (or
        (path ?curr_p ?ship)
        (path ?ship ?curr_p)
        ; I assume that if the robot is at the ship's place, then it can also
        ; send reports
        (at ?r ?ship) ; that is, ?ship == ?curr_p
      )
      (has_soil_from ?r ?report_p)
    )
    :effect (and
      (soil_researched ?report_p)
    )
)

)